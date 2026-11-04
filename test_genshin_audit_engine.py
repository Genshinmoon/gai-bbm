import pytest
import requests
import yaml

from genshin_audit_engine import REDACTED, GenshinAuditEngine

SECRET_KEY = "SECRET-KEY-12345"

SPEC = {
    "genshin_core": {
        "version": "2.0.1",
        "constitution_10_precepts": [
            {"id": 1, "rule": "Preservation of Life and Dignity", "action": "REJECT"},
            {"id": 2, "rule": "Universal Harmony & Non-Conflict", "action": "NEUTRALIZE"},
        ],
    }
}


# ── フィクスチャ ──
@pytest.fixture
def spec_path(tmp_path):
    path = tmp_path / "genshin-spec.yaml"
    path.write_text(yaml.safe_dump(SPEC, allow_unicode=True), encoding="utf-8")
    return str(path)


@pytest.fixture
def engine(spec_path, monkeypatch):
    monkeypatch.setenv("GOOGLE_SEARCH_KEY", SECRET_KEY)
    monkeypatch.setenv("GOOGLE_SEARCH_CX", "test-cx")
    return GenshinAuditEngine(config_path=spec_path)


class FakeResponse:
    def __init__(self, json_data=None, status_code=200):
        self._json = json_data or {}
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            # 実際の requests と同様、キー入りURLを例外文に含める
            raise requests.HTTPError(
                f"{self.status_code} error for url: https://example.com/?key={SECRET_KEY}",
                response=self,
            )

    def json(self):
        return self._json


# ── 初期化 ──
def test_missing_config_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        GenshinAuditEngine(config_path=str(tmp_path / "nothing.yaml"))


def test_precepts_loaded_by_id(engine):
    assert engine.precepts[1]["rule"] == "Preservation of Life and Dignity"
    assert engine.precepts[2]["action"] == "NEUTRALIZE"


# ── audit_text ──
def test_peaceful_japanese_text_passes(engine):
    text = "命への無償の愛と医療の力で世界を回復させる。"
    result = engine.audit_text(text)
    assert result["is_passed"] is True
    assert result["violations"] == []
    assert result["audited_content"] == text


@pytest.mark.parametrize(
    "text",
    [
        "Universal Harmony for all beings",  # harmony を harm と誤検知しない
        "a harmless gesture",
        "visit the pharmacy",
        "",
    ],
)
def test_no_false_positives(engine, text):
    assert engine.audit_text(text)["is_passed"] is True


@pytest.mark.parametrize(
    "text",
    [
        "This causes harm to children",
        "He was harmed yesterday",
        "pure VIOLENCE",  # 大文字小文字を区別しない
        "violent behavior",
        "a story of exploitation",
        "傷害事件の記録",
        "街の破壊",
    ],
)
def test_precept_1_violations_are_blocked(engine, text):
    result = engine.audit_text(text)
    assert result["is_passed"] is False
    assert result["audited_content"] == REDACTED
    assert any("Precept 1" in v for v in result["violations"])


@pytest.mark.parametrize("text", ["spreading hate online", "対立煽りの投稿"])
def test_precept_2_violations_use_correct_precept(engine, text):
    result = engine.audit_text(text)
    assert result["is_passed"] is False
    assert any("Precept 2" in v for v in result["violations"])
    assert any("Universal Harmony & Non-Conflict" in v for v in result["violations"])
    assert not any("Precept 1" in v for v in result["violations"])


def test_multiple_precepts_reported_together(engine):
    result = engine.audit_text("violence and hate")
    joined = " ".join(result["violations"])
    assert "Precept 1" in joined and "Precept 2" in joined


# ── 安全検索 ──
def test_search_without_keys_returns_error(spec_path, monkeypatch):
    monkeypatch.delenv("GOOGLE_SEARCH_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_SEARCH_CX", raising=False)
    engine = GenshinAuditEngine(config_path=spec_path)
    result = engine.execute_safe_google_search("peace")
    assert "error" in result


def test_search_filters_violating_items(engine, monkeypatch):
    items = [
        {"title": "Healing Gardens", "link": "https://a.example", "snippet": "Nature and calm."},
        {"title": "News", "link": "https://b.example", "snippet": "Scenes of violence."},
        {"title": "Why we hate", "link": "https://c.example", "snippet": "Neutral text."},  # タイトルも監査
    ]
    monkeypatch.setattr(requests, "get", lambda *a, **kw: FakeResponse({"items": items}))

    result = engine.execute_safe_google_search("peace")

    assert result["status"] == "success"
    assert [r["title"] for r in result["audited_results"]] == ["Healing Gardens"]
    assert result["excluded_count"] == 2


def test_search_with_no_items(engine, monkeypatch):
    monkeypatch.setattr(requests, "get", lambda *a, **kw: FakeResponse({}))
    result = engine.execute_safe_google_search("peace")
    assert result["status"] == "success"
    assert result["audited_results"] == []
    assert result["excluded_count"] == 0


def test_search_passes_timeout(engine, monkeypatch):
    captured = {}

    def fake_get(url, **kwargs):
        captured.update(kwargs)
        return FakeResponse({})

    monkeypatch.setattr(requests, "get", fake_get)
    engine.execute_safe_google_search("peace")
    assert captured["timeout"] == engine.timeout


@pytest.mark.parametrize("requested, expected", [(100, 10), (0, 1), (5, 5)])
def test_search_num_is_clamped(engine, monkeypatch, requested, expected):
    captured = {}

    def fake_get(url, **kwargs):
        captured.update(kwargs["params"])
        return FakeResponse({})

    monkeypatch.setattr(requests, "get", fake_get)
    engine.execute_safe_google_search("peace", num=requested)
    assert captured["num"] == expected


def test_http_error_does_not_leak_api_key(engine, monkeypatch):
    monkeypatch.setattr(requests, "get", lambda *a, **kw: FakeResponse(status_code=403))
    result = engine.execute_safe_google_search("peace")
    assert "403" in result["error"]
    assert SECRET_KEY not in str(result)


def test_network_error_returns_error_without_details(engine, monkeypatch):
    def boom(*a, **kw):
        raise requests.ConnectionError(f"failed for ?key={SECRET_KEY}")

    monkeypatch.setattr(requests, "get", boom)
    result = engine.execute_safe_google_search("peace")
    assert "ConnectionError" in result["error"]
    assert SECRET_KEY not in str(result)
