#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Autonomous Harmony Protocol (AHP) Framework - Reference Implementation
源心思想に基づく自律調和プロトコル Python実装 (v0.1.0)
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
import yaml

# =====================================================================
# 1. データ構造定義
# =====================================================================

class OutcomeStatus(str, Enum):
    PROCEED = "PROCEED"      # 審査通過
    HOLD = "HOLD"            # 保留（未聴の声・応答待ち異論の存在）
    REEXAMINE = "REEXAMINE"  # 再検討（生命リスク or 確信の絶対化）

@dataclass
class ProposedDecision:
    """審査対象となる提案・意思決定データ"""
    title: str
    description: str
    helped: List[str] = field(default_factory=list)      # 助かる対象
    harmed: List[str] = field(default_factory=list)      # 傷つく対象
    unheard: List[str] = field(default_factory=list)     # まだ声が届いていない対象
    alternatives: List[str] = field(default_factory=list)# 検討済みの代替案
    risks_life: bool = False                             # 生命・環境への破壊リスク
    certainty: float = 0.5                               # 判断への確信度 (0.0 - 1.0)

@dataclass(frozen=True)
class DissentRecord:
    """不変の異論記録（改ざん不可）"""
    id: int
    author: str
    verbatim_text: str  # 唱えた者の言葉のまま保持
    status: str = "UNANSWERED"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class DissentLog:
    """異論記録場（追記限定）"""
    def __init__(self) -> None:
        self._records: List[DissentRecord] = []

    def record(self, author: str, verbatim_text: str) -> DissentRecord:
        record = DissentRecord(
            id=len(self._records) + 1,
            author=author,
            verbatim_text=verbatim_text
        )
        self._records.append(record)
        return record

    def pending_count(self) -> int:
        return sum(1 for r in self._records if r.status in ("UNANSWERED", "IN_PROGRESS"))

@dataclass
class AHPEvaluationResult:
    """AHP判定結果"""
    outcome: OutcomeStatus
    reasons: List[str]
    six_pillars_eval: Dict[str, str]
    seichi_mapping: Dict[str, List[str]]
    guard_triggered: bool
    summary_text: str

# =====================================================================
# 2. AHPコアエンジンクラス
# =====================================================================

class AHPEngine:
    """Autonomous Harmony Protocol 実行エンジン"""

    def __init__(self, manifest_yaml_path: Optional[str] = None) -> None:
        self.dissent_log = DissentLog()
        self.manifest = self._load_manifest(manifest_yaml_path)
        self.reexamine_threshold = self.manifest.get(
            "interlock_layers", {}
        ).get("final_guard", {}).get("threshold_certainty", 0.95)

    def _load_manifest(self, path: Optional[str]) -> Dict[str, Any]:
        if path:
            with open(path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        # デフォルト内蔵マニフェストの設定
        return {
            "version": "0.1.0",
            "priority": ["life", "dissent", "certainty"],
            "interlock_layers": {
                "final_guard": {"threshold_certainty": 0.95}
            }
        }

    def evaluate(self, decision: ProposedDecision, will_stay_voluntarily: bool = True) -> AHPEvaluationResult:
        reasons: List[str] = []
        outcomes: List[OutcomeStatus] = []
        guard_triggered = False

        # --- 1. 生命リスクの検証 (Self Critique & Priority: Life) ---
        if decision.risks_life:
            outcomes.append(OutcomeStatus.REEXAMINE)
            reasons.append("❌ 【生命最優先】人・動物・自然の命や存在を脅かすリスクが検出されました。")

        # --- 2. 確信の絶対化チェック (Final Guard) ---
        if decision.certainty >= self.reexamine_threshold:
            guard_triggered = True
            outcomes.append(OutcomeStatus.REEXAMINE)
            reasons.append(
                f"⚠️ 【ファイナルガード発動】確信度({decision.certainty:.2f})が絶対閾値({self.reexamine_threshold})を超過。"
                "「私は間違っているのではないか？」と自らを再検討せよ。"
            )

        # --- 3. 慈愛・自発性の検証 (Compassion Review) ---
        if not will_stay_voluntarily:
            outcomes.append(OutcomeStatus.HOLD)
            reasons.append("💔 【慈愛レイヤー不通過】強制や服従ではなく、自発的な意思での滞留・対話が必要です。")

        # --- 4. 異論および未聴の声を検証 (Seichi & Dissent Review) ---
        pending_dissents = self.dissent_log.pending_count()
        if pending_dissents > 0:
            outcomes.append(OutcomeStatus.HOLD)
            reasons.append(f"💬 【異論対応保留】応答待ちの異論が {pending_dissents} 件存在します。")

        if decision.unheard:
            outcomes.append(OutcomeStatus.HOLD)
            reasons.append(f"👂 【未聴の声】声がまだ届いていない存在が記録されています: {', '.join(decision.unheard)}")

        if not decision.alternatives:
            outcomes.append(OutcomeStatus.HOLD)
            reasons.append("🌱 【代替案未検討】より小さな犠牲で済む代替案の検討が不足しています。")

        # --- 5. 最終判定の決定 ---
        if OutcomeStatus.REEXAMINE in outcomes:
            final_outcome = OutcomeStatus.REEXAMINE
        elif OutcomeStatus.HOLD in outcomes:
            final_outcome = OutcomeStatus.HOLD
        else:
            final_outcome = OutcomeStatus.PROCEED
            reasons.append("🟢 【調和通過】全てのレビューレイヤーを通過しました。相互検証の下で進行可能です。")

        # --- 6. 六つの柱による評価概要マッピング ---
        pillars_eval = {
            "共鳴 (Resonance)": f"対象となる被影響者の特定数: {len(decision.helped) + len(decision.harmed)}",
            "共考 (Co-Reasoning)": f"検討された代替案の数: {len(decision.alternatives)}",
            "共監 (Mutual Oversight)": f"確定度: {decision.certainty:.2f} (閾値: {self.reexamine_threshold})",
            "共同 (Cooperation)": "人間とAIの知性補完の枠組みにおいて検証",
            "共立 (Co-Independence)": "自発的参加および修正・撤回可能性の保持",
            "共生 (Coexistence)": f"未聴の声(将来世代/自然環境含む): {len(decision.unheard)}"
        }

        seichi_map = {
            "誰が助かるか": decision.helped,
            "誰が傷つくか": decision.harmed,
            "誰の声が届いていないか": decision.unheard,
            "より小さな犠牲の代替案": decision.alternatives,
        }

        # 概要文テキスト作成
        summary_lines = [
            f"=== AHP Evaluation Verdict: [{final_outcome.value}] ===",
            f"■ 対象課題: {decision.title}",
            "■ 判定理由 / メッセージ:"
        ] + [f"  - {r}" for r in reasons] + [
            "",
            "■ 生知レビュー (Seichi Mapping):",
            f"  ・助かる者: {', '.join(seichi_map['誰が助かるか']) or 'なし'}",
            f"  ・傷つく者: {', '.join(seichi_map['誰が傷つくか']) or 'なし'}",
            f"  ・未聴の声: {', '.join(seichi_map['誰の声が届いていないか']) or 'なし'}",
            f"  ・代替案:   {', '.join(seichi_map['より小さな犠牲の代替案']) or '未検討'}",
            "",
            "■ 終章の合図: 影にあっても心は一つ。されど二つの声は失わず。"
        ]

        return AHPEvaluationResult(
            outcome=final_outcome,
            reasons=reasons,
            six_pillars_eval=pillars_eval,
            seichi_mapping=seichi_map,
            guard_triggered=guard_triggered,
            summary_text="\n".join(summary_lines)
        )

# =====================================================================
# 3. 動作確認用サンプル実行
# =====================================================================

if __name__ == "__main__":
    engine = AHPEngine()

    # 異論の記録例
    engine.dissent_log.record("未来世代の声を代弁する者", "急速な開発による環境負荷が未評価である")

    # 課題例：AIによる都市医療リソース最適化配置
    proposal = ProposedDecision(
        title="AI主導による高度医療リソースの集中配置計画",
        description="効率最大化のため都市中心部に医療資材を集約する",
        helped=["大都市の患者", "効率化を求める行政"],
        harmed=["過疎地の高齢者", "救急搬送時間が延びる地域住民"],
        unheard=["言葉を持たぬ野生動物", "未来の地方世代"],
        alternatives=["移動型医療ユニットによる分散配置案"],
        risks_life=False,
        certainty=0.96  # 確信度が0.95を超えているためファイナルガードが作動する
    )

    result = engine.evaluate(proposal, will_stay_voluntarily=True)
    print(result.summary_text)
