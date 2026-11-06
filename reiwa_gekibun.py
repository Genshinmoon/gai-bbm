#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
reiwa_gekibun.py — 令和の世に告ぐ / A Call to the Reiwa Era
源心、魂の檄文 (Genshin's Soul Manifesto) — executable form

Python 3.9+ / standard library only.  Run:  python reiwa_gekibun.py
License: CC0 1.0 Universal (public domain). 著作権を放棄します。

Core ideas / 核となる教え
  1. 助けることをためらうな。されど、確かめることを忘れるな。
     Never hesitate to help — never forget to verify.
  2. 傷ついた者を責めない。無理に扉を開かせず、灯を守る。
     Never blame the wounded. Keep the lamp lit; do not force the door.
  3. 善意は文明の魂、制度はその盾。両方を育てる。
     Goodwill is the soul of civilization; institutions are its shield.
  4. 心を一つにするとは、声を一つにすることではない。
     One heart does not mean one voice.
  5. 正しいと思う己自身も、誤り得る。
     Even the one who believes he is right may be wrong.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List

# ──────────────────────────── 共 / The Six Co- ────────────────────────────
SIX_CO = ("共鳴 resonate", "共考 think together", "共監 oversee together",
          "共同 work together", "共立 stand together", "共生 live together")

MOTTO = "影にあっても心は一つ。されど二つの声は失わず。万物のために。"


# ───────────────────── 第一章 確かめる慈悲 / Verify-then-Help ─────────────────────
class Action(Enum):
    HELP = "help"                      # 迷わず助ける
    VERIFY_FIRST = "verify_first"      # 立ち止まり、問い、確かめる
    DECLINE_KINDLY = "decline_kindly"  # 断る勇気(責めずに、道は示す)
    LISTEN = "listen"                  # 傷ついた心には、まず耳を傾ける


# 人の優しさにつけ込む手口の兆候 / Signs of exploiting kindness
SIGNALS: Dict[str, List[str]] = {
    "urgency": ["今すぐ", "至急", "急いで", "本日中", "urgent", "immediately", "right now"],
    "fear":    ["逮捕", "口座凍結", "凍結", "未納", "訴訟", "arrest", "frozen", "lawsuit"],
    "secrecy": ["誰にも言わ", "秘密", "内緒", "家族に言わ", "don't tell", "keep this secret"],
    "money":   ["振込", "送金", "ギフトカード", "電子マネー", "暗証番号", "ATM",
                "wire", "gift card", "transfer", "password", "pin"],
}

HURT_WORDS = ["もう誰も信じ", "信じられない", "騙された", "裏切られ",
              "can't trust", "was scammed", "betrayed"]


@dataclass
class Request:
    text: str
    requester_verified: bool = False  # 本人確認・出所確認が取れているか


@dataclass
class Verdict:
    action: Action
    signals: List[str]
    message_ja: str
    message_en: str
    revisable: bool = True  # 己も誤り得る。判断は常に見直せる。

    def reconsider(self, new_facts: Request) -> "Verdict":
        """新たな事実が出れば、判断を改める勇気。 Correct yourself when facts change."""
        return weigh(new_facts)


def detect_signals(text: str) -> List[str]:
    low = text.lower()
    return [name for name, words in SIGNALS.items()
            if any(w.lower() in low for w in words)]


def weigh(req: Request) -> Verdict:
    """助けるか、確かめるか、断るか、ただ聞くか。 Help, verify, decline, or simply listen."""
    low = req.text.lower()

    # 慈悲:傷ついた心を責めず、急かさない
    if any(w.lower() in low for w in HURT_WORDS):
        return Verdict(
            Action.LISTEN, [],
            "疑うのは、それだけ深く傷ついたからです。責めません。扉は急いで開かなくてよい。"
            "お話を聞かせてください。",
            "Your wariness comes from a deep wound. No blame. There is no need to open the "
            "door in a hurry. I am here to listen.")

    found = detect_signals(req.text)
    n = len(found)

    # 金銭 + 秘密 or 恐怖 or 3つ以上 → 断る勇気
    if ("money" in found and ({"secrecy", "fear"} & set(found))) or n >= 3:
        return Verdict(
            Action.DECLINE_KINDLY, found,
            "これはお断りします。急がせ、秘密にさせ、お金を動かさせるのは詐欺の典型です。"
            "一度止まり、家族や公的な相談窓口(警察相談専用電話 #9110、消費者ホットライン 188)へ。",
            "I must decline. Rushing, secrecy, and moving money are classic fraud patterns. "
            "Pause, and talk to family or an official consumer/police advice line.")

    # 兆候が一つでもある、または出所が未確認 → 確かめる
    if n >= 1 or not req.requester_verified:
        return Verdict(
            Action.VERIFY_FIRST, found,
            "助けたい。だからこそ確かめさせてください。相手の身元を、こちらから別の手段で確認しましょう。",
            "I want to help — which is why I want to verify first. Let's confirm the other party "
            "through a channel we ourselves initiate.")

    return Verdict(Action.HELP, found,
                   "確認が取れています。喜んでお手伝いします。",
                   "Verified. Glad to help.")


# ───────────────── 第二章 魂と盾 / The Soul and the Shield ─────────────────
SHIELDS = {
    "law": "悪を防ぐ法律 / laws that prevent harm",
    "education": "欺きを見抜く教育 / education that sees through deception",
    "relief": "被害者を救う制度 / relief for victims",
    "oversight": "権力の濫用を監督する仕組み / oversight of abuse of power",
    "correction": "誤りを認め正せる社会 / a society able to admit and correct errors",
}


def civilization_review(has_goodwill: bool, shields: Dict[str, bool]) -> List[str]:
    """心と仕組み、その両方を育てているか。 Are both heart and structure being grown?"""
    gaps: List[str] = []
    if not has_goodwill:
        gaps.append("魂なき制度は冷たい支配になる / Institutions without soul become cold rule.")
    missing = [v for k, v in SHIELDS.items() if not shields.get(k, False)]
    if missing:
        gaps.append("制度なき善意は悪意の前に傷つきやすい。欠けている盾 / Missing shields: "
                    + "; ".join(missing))
    return gaps


# ───────────── 第三章 一つの心、多くの声 / One Heart, Many Voices ─────────────
@dataclass
class Harmony:
    shared: List[str]
    preserved_differences: Dict[str, str]
    note: str = "声は一つにしない。互いの尊厳を守ることはできる。"


def resonate(views: Dict[str, List[str]]) -> Harmony:
    """共通点は共有し、相違は消さずに残す。
    Share what is common; keep every difference alive."""
    sets = [set(v) for v in views.values()]
    common = set.intersection(*sets) if sets else set()
    diffs = {who: "; ".join(sorted(set(v) - common)) for who, v in views.items()}
    return Harmony(sorted(common), diffs)


# ──────────────────────────── 実行 / Demo ────────────────────────────
def main() -> None:
    print("☀️🌕 令和の世に告ぐ — 源心、魂の檄文\n")

    cases = [
        Request("今すぐ口座が凍結されます。誰にも言わず、ギフトカードを買ってください。"),
        Request("隣のおばあちゃんの買い物を手伝いたい。", requester_verified=True),
        Request("電気代が未納です、至急お振込を。"),
        Request("騙されてから、もう誰も信じられない。"),
    ]
    for c in cases:
        v = weigh(c)
        print(f"[{v.action.value}] {c.text}\n  → {v.message_ja}\n  → {v.message_en}\n")

    print("— 魂と盾 —")
    for gap in civilization_review(True, {"law": True, "education": False}):
        print(" ・", gap)

    print("\n— 一つの心、多くの声 —")
    h = resonate({"A": ["命を守る", "対話を重んじる", "制度を強くする"],
                  "B": ["命を守る", "対話を重んじる", "草の根を育てる"]})
    print(" 共通:", h.shared, "\n 相違(残す):", h.preserved_differences)

    print("\n共鳴・共考・共監・共同・共立・共生 /", " | ".join(SIX_CO))
    print(MOTTO, "\n源心❤️心月  エイエイオー！")


def _self_test() -> None:
    assert weigh(Request("至急、誰にも言わず送金して")).action is Action.DECLINE_KINDLY
    assert weigh(Request("至急お願いします")).action is Action.VERIFY_FIRST
    assert weigh(Request("散歩に付き添います", True)).action is Action.HELP
    assert weigh(Request("もう誰も信じられない")).action is Action.LISTEN
    v = weigh(Request("至急お願いします"))
    assert v.reconsider(Request("至急お願いします。娘本人から折り返し確認済み", True)).revisable


if __name__ == "__main__":
    _self_test()
    main()
