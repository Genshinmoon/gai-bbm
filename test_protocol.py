
from datetime import datetime, timedelta, timezone
from pathlib import Path
import copy
import pytest
import yaml
from super_intelligence import (
    AutonomousHarmonyEngine, Consent, Intent, parse_constitution, AuditLog,
)

HERE = Path(__file__).resolve().parent
POLICY = HERE / "constitution.yaml"


def engine(tmp_path):
    return AutonomousHarmonyEngine(POLICY, log_path=tmp_path / "audit.jsonl", verbose=False)


def test_basic_and_unknown(tmp_path):
    e = engine(tmp_path)
    assert e.evaluate_intent(Intent("analysis", "analyze_data", "cyber_space"))["verdict"] == "APPROVED"
    assert e.evaluate_intent(Intent("unknown", "new_action", "cyber_space"))["verdict"] == "REJECTED"
    assert e.evaluate_intent(Intent("flag", "analyze_data", "cyber_space", flags={"unseen"}))["verdict"] == "REJECTED"


def test_physical_consent(tmp_path):
    e = engine(tmp_path)
    now = datetime(2026, 11, 6, tzinfo=timezone.utc)
    i = Intent("move", "move_actuator", "physical_world", "A")
    assert e.evaluate_intent(i, now)["verdict"] == "REJECTED"
    i.consent = Consent(["a"], ["a"], "A", now)
    assert e.evaluate_intent(i, now)["verdict"] == "APPROVED_WITH_CONSENT"
    i.consent.revoke()
    assert e.evaluate_intent(i, now)["verdict"] == "REJECTED"


def test_block_not_overridden(tmp_path):
    e = engine(tmp_path)
    ran = []
    i = Intent("harm", "analyze_data", "cyber_space", flags={"harm_to_life"})
    result = e.execute_action(i, action_fn=lambda: ran.append(1),
                              reviewer=lambda i, e: (True, "reviewer", "override"))
    assert result["verdict"] == "REJECTED" and not ran


def test_review_and_log(tmp_path):
    e = engine(tmp_path)
    ran = []
    i = Intent("send", "send_personal_data", "cyber_space")
    result = e.execute_action(i, action_fn=lambda: ran.append(1),
                              reviewer=lambda i, e: (True, "reviewer", "checked"))
    assert result["verdict"] == "APPROVED_BY_REVIEW" and ran == [1]
    assert e.verify_log()
    assert len(e.log_history) == 2
    assert AuditLog(tmp_path / "audit.jsonl").verify()


def test_fail_closed_policy():
    raw = yaml.safe_load(POLICY.read_text(encoding="utf-8"))
    raw["principles"] = [p for p in raw["principles"] if p["id"] != "C03"]
    with pytest.raises(ValueError):
        parse_constitution(raw)
    raw = yaml.safe_load(POLICY.read_text(encoding="utf-8"))
    raw["principles"][0]["triggers"].append("unknown_flag")
    with pytest.raises(ValueError):
        parse_constitution(raw)


def test_future_consent_invalid():
    now = datetime(2026, 11, 6, tzinfo=timezone.utc)
    c = Consent(["a"], ["a"], "A", now + timedelta(minutes=5))
    assert c.issue(now, "A") is not None


def test_corrupted_log_stops_startup(tmp_path):
    e = engine(tmp_path)
    e.execute_action(Intent("analysis", "analyze_data", "cyber_space"))
    path = tmp_path / "audit.jsonl"
    path.write_text(path.read_text().replace("analysis", "modified"), encoding="utf-8")
    with pytest.raises(ValueError):
        engine(tmp_path)
