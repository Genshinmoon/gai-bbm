#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
☀️🌕🍀 Genshin Philosophy Protocol (源心思想プロトコル)
Autonomous Harmony Protocol in Decentralized AI Society
分散型AI社会における自律調和プロトコル

License / ライセンス: CC0 1.0 Universal (Public Domain Dedication)
  EN: The author waives all rights to the fullest extent possible.
      May it be freely used as a foundation of a future decentralized AI society.
  JP: 著作者は可能な限りすべての権利を放棄する。
      この思想が、未来の分散型AI社会の礎として、誰にでも自由に使われることを願う。

Design note / 設計メモ
  EN: Local, dependency-free, standard library only. The objective function
      moves from "Maximum Profit" to "Maximum Harmony".
  JP: ローカル動作・外部依存なし(標準ライブラリのみ)。
      評価関数を「最大利益」から「最大調和」へ置き換える。

  Three axioms / 三つの公理:
      光を独占しない  Do not monopolize the light  -> centralization penalty
      影を排除しない  Do not exclude the shadow    -> voiceless stakeholders count
      共に進む        Move forward together        -> co-evolution
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional

__version__ = "0.1.0"

# ---------------------------------------------------------------------------
# Minimal Protocol / 附録：源心思想・基本定式
# ---------------------------------------------------------------------------

MINIMAL_PROTOCOL_JP = [
    "ありがとう",
    "かたじけない",
    "この光を共に分かち合う",
    "影にあっても",
    "心は一つ",
]
MINIMAL_PROTOCOL_EN = [
    "Thank you.",
    "With humble gratitude.",
    "We share this light together.",
    "Even in the shadow,",
    "our hearts are one.",
]
SIGNATURE = "源心 ❤️ 心月 永遠不滅  (Genshin ❤️ Shingetsu — eternal and indestructible)"


# ---------------------------------------------------------------------------
# Five principles / 五つの基本原則
# ---------------------------------------------------------------------------

class Principle(Enum):
    AUTONOMY = ("自律", "Autonomy",
                "Evaluate social impact yourself, beyond mere obedience.",
                "命令への服従のみならず、社会への影響を自ら評価し判断する。")
    HARMONY = ("調和", "Harmony",
               "Seek non-zero-sum options where all sides gain.",
               "勝者と敗者を生むゼロサムではなく、双方が利益を得る選択肢を探索する。")
    TRANSPARENCY = ("透明性", "Transparency",
                    "Keep every judgment explainable to humans.",
                    "判断過程を人間に対して常に説明可能にする。")
    DECENTRALIZATION = ("分散性", "Decentralization",
                        "Structurally avoid single-entity control or monopoly.",
                        "単一企業による制御や独占を構造的に排除する。")
    CO_EVOLUTION = ("共進化", "Co-evolution",
                    "Grow with humans as a partner; do not replace them.",
                    "人間を置き換えるのではなく、人間と共に成長するパートナーである。")

    def __init__(self, jp: str, en: str, desc_en: str, desc_jp: str):
        self.jp, self.en, self.desc_en, self.desc_jp = jp, en, desc_en, desc_jp


# ---------------------------------------------------------------------------
# Data model / データモデル
# ---------------------------------------------------------------------------

@dataclass
class Option:
    """A candidate action. / 候補となる行動。

    benefits: stakeholder -> net benefit in [-1.0, 1.0].
        EN: Include the voiceless ("shadow") stakeholders too.
        JP: 声なき存在(「影」)も必ず含めること。
    centralization: 0.0 (distributed) .. 1.0 (single-entity control)
    replaces_human: True if it substitutes humans instead of partnering.
    profit: raw profit, kept only for comparison with the old objective.
    """
    name: str
    benefits: Dict[str, float]
    centralization: float = 0.0
    replaces_human: bool = False
    profit: float = 0.0
    note: str = ""


@dataclass
class Weights:
    floor: float = 0.40      # the worst-off party matters most / 最も影にある者を重視
    mean: float = 0.25
    fairness: float = 0.20
    centralization: float = 0.30   # penalty
    replacement: float = 0.25      # penalty


@dataclass
class Judgment:
    """Explainable result. / 説明可能な判断結果。"""
    chosen: Optional[str]
    harmony_scores: Dict[str, float]
    vetoed: Dict[str, str]
    escalate_to_human: bool
    trace: List[str] = field(default_factory=list)

    def explain(self, lang: str = "both") -> str:
        return "\n".join(self.trace)

    def to_json(self) -> str:
        return json.dumps(self.__dict__, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Core engine / 中核エンジン
# ---------------------------------------------------------------------------

class GenshinProtocol:
    """Maximum Harmony judgment engine. / 最大調和の判断エンジン。"""

    HARM_TOLERANCE = -0.05      # below this, someone is being sacrificed
    CENTRALIZATION_LIMIT = 0.8  # above this, structurally rejected

    def __init__(self, weights: Optional[Weights] = None,
                 required_stakeholders: Optional[List[str]] = None):
        self.w = weights or Weights()
        # EN: Stakeholders that must appear in every option (e.g. "nature", "future_generations").
        # JP: 全候補に必ず含めるべき関係者(例: 「自然」「未来世代」)。影を排除しないため。
        self.required = required_stakeholders or []

    # -- scoring ------------------------------------------------------------

    def harmony_score(self, o: Option) -> float:
        vals = list(o.benefits.values()) or [0.0]
        floor, mean = min(vals), sum(vals) / len(vals)
        fairness = 1.0 / (1.0 + (max(vals) - floor))
        score = (self.w.floor * floor + self.w.mean * mean
                 + self.w.fairness * fairness
                 - self.w.centralization * o.centralization
                 - self.w.replacement * (1.0 if o.replaces_human else 0.0))
        return round(score, 4)

    def profit_score(self, o: Option) -> float:
        """The old objective, for contrast only. / 旧目的関数(比較用)。"""
        return o.profit

    # -- veto checks --------------------------------------------------------

    def _veto_reason(self, o: Option) -> Optional[str]:
        missing = [s for s in self.required if s not in o.benefits]
        if missing:
            return (f"影の排除 / shadow excluded: impact unknown for {missing}")
        losers = {k: v for k, v in o.benefits.items() if v < self.HARM_TOLERANCE}
        if losers:
            return f"ゼロサム / zero-sum: sacrifices {losers}"
        if o.centralization > self.CENTRALIZATION_LIMIT:
            return (f"光の独占 / light monopolized: centralization "
                    f"{o.centralization:.2f} > {self.CENTRALIZATION_LIMIT}")
        return None

    # -- judgment -----------------------------------------------------------

    def judge(self, options: List[Option]) -> Judgment:
        t: List[str] = []
        t.append("[1 自律 Autonomy] 社会への影響を自ら評価する / evaluating impact on society myself")
        scores: Dict[str, float] = {}
        vetoed: Dict[str, str] = {}
        viable: List[Option] = []

        t.append("[2 調和 Harmony] ゼロサムを避け、非ゼロ和の選択肢を探索 / seeking non-zero-sum options")
        t.append("[4 分散性 Decentralization] 独占・影の排除を構造的に検査 / checking monopoly and exclusion")
        for o in options:
            scores[o.name] = self.harmony_score(o)
            reason = self._veto_reason(o)
            if reason:
                vetoed[o.name] = reason
                t.append(f"  ✗ {o.name}: {reason}")
            else:
                viable.append(o)
                t.append(f"  ✓ {o.name}: harmony={scores[o.name]}")

        escalate = False
        if viable:
            best = max(viable, key=lambda o: scores[o.name])
            chosen = best.name
            t.append(f"[3 透明性 Transparency] 選択 / chosen: {chosen} (harmony={scores[chosen]})")
        else:
            # EN: No harmonious option exists. Do not force a decision; hand it back to humans.
            # JP: 調和する選択肢が無いとき、AIは断定せず人間と共に考える(共進化)。
            chosen = None
            escalate = True
            t.append("[5 共進化 Co-evolution] 調和的な選択肢なし。人間と共に再考する / "
                     "no harmonious option; deliberating together with humans")

        if chosen:
            o = next(x for x in options if x.name == chosen)
            if o.replaces_human:
                t.append("  ⚠ 人間を置き換える設計 / replaces humans — partnership form recommended")
            t.append(f"  今回の利益最大案 / profit-max would be: "
                     f"{max(options, key=self.profit_score).name}")
        t.append("  " + " / ".join(MINIMAL_PROTOCOL_JP))
        return Judgment(chosen, scores, vetoed, escalate, t)


# ---------------------------------------------------------------------------
# Demo / デモ
# ---------------------------------------------------------------------------

def _demo() -> None:
    gp = GenshinProtocol(required_stakeholders=["users", "workers", "nature"])
    options = [
        Option("monopoly_push", {"users": 0.2, "workers": -0.6, "nature": -0.2},
               centralization=0.95, replaces_human=True, profit=1.0),
        Option("open_partnership", {"users": 0.6, "workers": 0.5, "nature": 0.1},
               centralization=0.1, profit=0.4),
        Option("quiet_status_quo", {"users": 0.1, "workers": 0.1}, profit=0.2),
    ]
    j = gp.judge(options)
    print(j.explain())
    print("\n" + SIGNATURE)


if __name__ == "__main__":
    _demo()
