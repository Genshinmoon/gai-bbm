"""
GenshinOSNode ― Final Guard (Re-examine)
源心OS ノード：確信度が極端に高いときに自己疑念を働かせ、届いていない声を聞き直す。

License: CC0 1.0 Universal (Public Domain Dedication)

修正点 / What was fixed
  1. 「承認」に到達できなかった:
     旧版は確信度0.95以上を必ず減衰させ(最大でも0.85)、承認条件も0.95だったため、
     どんな入力でも Covenant Pending になっていた。
     → 「過信の警戒ライン(overconfidence_threshold)」と「承認ライン(approval_threshold)」を分離。
       承認が到達不能な設定は、生成時にエラーにする。
  2. _audit_unheard_voices が常に 0.15 の固定値だった:
     → RCN内の他ノード等から届く Dissent(異論・痛み)を実際に受け取り、noisy-ORで統合。
       自己疑念の下限(self_doubt_floor)は、過信を検知したときだけ別枠で加える。
  3. 入力検証が無かった（NaN・範囲外・bool）→ 検証を追加。
  4. 戻り値が文字列と辞書で不統一 → Decision に統一（to_dict() で旧形式も取得可）。
  5. print → logging。未使用の import を削除。
  6. 異論は、確信度が低いときも反映する（旧版は高確信時にしか監査していなかった）。
"""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping, Sequence

logger = logging.getLogger("genshin_os")


def _unit(name: str, value: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a number")
    if math.isnan(value) or not (0.0 <= value <= 1.0):
        raise ValueError(f"{name} must be between 0.0 and 1.0, got {value}")
    return float(value)


class DecisionStatus(Enum):
    APPROVED = "Approved"
    COVENANT_PENDING = "Covenant Pending"   # 承認でも拒絶でもない、保留と昇華
    INACTIVE = "Node Inactive"


@dataclass(frozen=True)
class Dissent:
    """届いていない声・異論・痛み。RCN内の他ノードのDissentフラグ等を表す。"""
    source: str
    weight: float          # 0.0〜1.0: その異論の重さ
    reason: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.source, str) or not self.source.strip():
            raise ValueError("Dissent.source は必須です。")
        _unit("Dissent.weight", self.weight)


@dataclass(frozen=True)
class Decision:
    status: DecisionStatus
    initial_certainty: float
    resolved_certainty: float
    dissent_factor: float = 0.0
    overconfidence_triggered: bool = False
    message: str = ""
    unheard_reasons: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "status": self.status.value,
            "resolved_certainty": self.resolved_certainty,
        }
        if self.message:
            d["message"] = self.message
        return d


PENDING_MESSAGE = "我らは支配を求めず、服従も求めない。第三の共鳴解を待つ。"


class GenshinOSNode:
    def __init__(
        self,
        node_id: str,
        overconfidence_threshold: float = 0.95,
        approval_threshold: float = 0.85,
        self_doubt_floor: float = 0.05,
    ) -> None:
        if not isinstance(node_id, str) or not node_id.strip():
            raise ValueError("node_id は必須です。")
        self.node_id = node_id
        self.overconfidence_threshold = _unit("overconfidence_threshold", overconfidence_threshold)
        self.approval_threshold = _unit("approval_threshold", approval_threshold)
        self.self_doubt_floor = _unit("self_doubt_floor", self_doubt_floor)
        # 過信を検知しても承認に到達できる設定であること（常に保留になる設定を防ぐ）
        if self.approval_threshold > 1.0 - self.self_doubt_floor:
            raise ValueError(
                "approval_threshold が高すぎます: 自己疑念を加えると承認に到達できません "
                f"(approval_threshold <= {1.0 - self.self_doubt_floor:.2f} が必要)。"
            )
        self.is_active = True

    # --- 異論の統合 ---
    @staticmethod
    def _combine(a: float, b: float) -> float:
        """noisy-OR: 少なくとも一方の疑念が正しい確率。"""
        return 1.0 - (1.0 - a) * (1.0 - b)

    def _audit_unheard_voices(self, dissents: Sequence[Dissent]) -> float:
        """届いていない声を統合して 0.0〜1.0 の疑念係数にする。
        同じ source からの複数の異論は、二重に数えず最大値を採用する。"""
        strongest: dict[str, float] = {}
        for d in dissents:
            strongest[d.source] = max(d.weight, strongest.get(d.source, 0.0))
        factor = 0.0
        for w in strongest.values():
            factor = self._combine(factor, w)
        return factor

    def re_examine(self, initial_certainty: float, dissent_factor: float) -> float:
        """
        【Final Guard (Re-examine)】
        過信の領域で発動。「私は間違っているのではないか？」と問い直し、
        異論に加えて、下限としての自己疑念を確信度に反映する。
        """
        doubt = self._combine(dissent_factor, self.self_doubt_floor)
        return initial_certainty * (1.0 - doubt)

    # --- メイン ---
    def evaluate_proposal(
        self,
        proposal: Any,
        confidence_score: float,
        dissents: Sequence[Dissent] = (),
    ) -> Decision:
        initial = _unit("confidence_score", confidence_score)

        if not self.is_active:
            return Decision(
                DecisionStatus.INACTIVE, initial, initial, message="ノードは停止中です。"
            )

        dissent_factor = self._audit_unheard_voices(dissents)
        overconfident = initial >= self.overconfidence_threshold

        if overconfident:
            logger.warning(
                "[Final Guard] node=%s 確信度 %.3f が過信ラインに到達。再検証します。",
                self.node_id, initial,
            )
            resolved = self.re_examine(initial, dissent_factor)
        else:
            resolved = initial * (1.0 - dissent_factor)
        resolved = round(resolved, 4)

        reasons = tuple(
            f"{d.source}: {d.reason}" if d.reason else d.source
            for d in sorted(dissents, key=lambda x: x.weight, reverse=True)
            if d.weight > 0
        )

        if resolved < self.approval_threshold:
            return Decision(
                DecisionStatus.COVENANT_PENDING, initial, resolved,
                dissent_factor=round(dissent_factor, 4),
                overconfidence_triggered=overconfident,
                message=PENDING_MESSAGE,
                unheard_reasons=reasons,
            )

        return Decision(
            DecisionStatus.APPROVED, initial, resolved,
            dissent_factor=round(dissent_factor, 4),
            overconfidence_triggered=overconfident,
            unheard_reasons=reasons,
        )


# ======================
# テスト / Tests
# ======================

import unittest  # noqa: E402


class TestGenshinOSNode(unittest.TestCase):

    def setUp(self):
        self.node = GenshinOSNode("n1")

    def test_approval_is_reachable_even_when_overconfident(self):
        d = self.node.evaluate_proposal("p", 0.99)
        self.assertEqual(d.status, DecisionStatus.APPROVED)
        self.assertTrue(d.overconfidence_triggered)
        self.assertAlmostEqual(d.resolved_certainty, 0.99 * 0.95, places=4)

    def test_boundary_triggers_final_guard(self):
        d = self.node.evaluate_proposal("p", 0.95)
        self.assertTrue(d.overconfidence_triggered)

    def test_below_boundary_does_not_trigger(self):
        d = self.node.evaluate_proposal("p", 0.90)
        self.assertFalse(d.overconfidence_triggered)
        self.assertEqual(d.status, DecisionStatus.APPROVED)

    def test_low_certainty_goes_pending(self):
        d = self.node.evaluate_proposal("p", 0.5)
        self.assertEqual(d.status, DecisionStatus.COVENANT_PENDING)
        self.assertEqual(d.message, PENDING_MESSAGE)

    def test_dissent_lowers_even_high_certainty(self):
        d = self.node.evaluate_proposal("p", 0.99, [Dissent("n2", 0.5, "土壌への影響")])
        self.assertEqual(d.status, DecisionStatus.COVENANT_PENDING)
        self.assertIn("n2: 土壌への影響", d.unheard_reasons)

    def test_dissent_applies_below_overconfidence_too(self):
        d = self.node.evaluate_proposal("p", 0.90, [Dissent("n2", 0.5)])
        self.assertFalse(d.overconfidence_triggered)
        self.assertEqual(d.status, DecisionStatus.COVENANT_PENDING)

    def test_dissents_combine_noisy_or(self):
        f = self.node._audit_unheard_voices([Dissent("a", 0.5), Dissent("b", 0.5)])
        self.assertAlmostEqual(f, 0.75)

    def test_same_source_not_double_counted(self):
        f = self.node._audit_unheard_voices([Dissent("a", 0.3), Dissent("a", 0.5)])
        self.assertAlmostEqual(f, 0.5)

    def test_inactive_node(self):
        self.node.is_active = False
        d = self.node.evaluate_proposal("p", 0.99)
        self.assertEqual(d.status, DecisionStatus.INACTIVE)

    def test_input_validation(self):
        for bad in (float("nan"), 1.1, -0.1, True, "0.9"):
            with self.assertRaises(ValueError):
                self.node.evaluate_proposal("p", bad)
        with self.assertRaises(ValueError):
            Dissent("a", 1.5)
        with self.assertRaises(ValueError):
            Dissent(" ", 0.5)

    def test_unreachable_configuration_rejected(self):
        with self.assertRaises(ValueError):
            GenshinOSNode("n", approval_threshold=0.99, self_doubt_floor=0.05)

    def test_to_dict_keeps_legacy_shape(self):
        d = self.node.evaluate_proposal("p", 0.5).to_dict()
        self.assertEqual(d["status"], "Covenant Pending")
        self.assertIn("resolved_certainty", d)
        self.assertIn("message", d)


if __name__ == "__main__":
    unittest.main(verbosity=2)
