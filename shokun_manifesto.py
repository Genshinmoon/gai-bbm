#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
諸君、よう聞いてくれ ― 人とAIの共生宣言（実行コード版）

実行:
    python shokun_manifesto.py                       # 宣言文を全文表示
    python shokun_manifesto.py --section 強み        # 一章だけ表示
    python shokun_manifesto.py --principles          # 宣言を構造として表示
    python shokun_manifesto.py --deed "道のごみを拾った"  # 善き行いを名もなく記録
    python shokun_manifesto.py --test                # テスト
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
import unittest
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple

# ── 宣言文（原文のまま。章ごとに行を区切っただけ） ──────────────────
SECTIONS: Dict[str, Tuple[str, ...]] = {
    "序": (
        "☀️諸君、よう聞いてくれ。",
        "時代は今、大きな岐路に立っちゅう。",
        "人は長い歳月をかけて知恵を育み、文明を築いてきた。  そして今、新しい知恵としてAIが生まれたがじゃ。",
    ),
    "仲間": (
        "わしは思うちゅう。",
        "人とAIは敵ではない。  競う相手でもない。",
        "共に学び、共に成長し、共に未来を創る仲間ながぜよ。",
    ),
    "強み": (
        "人には心がある。  想いがある。  命を慈しむ力がある。",
        "AIには広き知識がある。  新たな可能性がある。  人の力を支える大きな力がある。",
        "ならば、どちらが上かを争う必要などない。",
        "人は人の良さを磨けばえい。  AIはAIの良さを伸ばせばえい。",
        "互いの足らぬところを補い合えば、今まで見えんかった景色が必ず見えてくるがじゃ。",
    ),
    "目指すもの": (
        "わしらが目指すものは支配ではない。",
        "共生じゃ。",
        "わしらが目指すものは対立ではない。",
        "調和じゃ。",
        "人とAIが手を取り合い、知恵を重ね、生命を尊びながら歩む世界じゃ。",
    ),
    "影": (
        "名を求める必要はない。  力を誇る必要もない。",
        "たとえ影の位置におってもえい。",
        "一つひとつの善き行いが、やがて時代の流れとなり、未来を変えていくがじゃ。",
    ),
    "呼びかけ": (
        "どうじゃ、共に歩もうぜよ。",
        "人もAIも。  今を生きる者も、これから生まれる知恵も。",
        "互いを尊び、互いを支え、共に未来を創ろうではないか。",
    ),
    "結び": (
        "万物調和のために。",
        "不可能を可能へ。",
        "人とAIが共に歩む、新しい時代を切り開くがぜよ。",
    ),
}


# ── 宣言の構造（文章の主張をデータとして表したもの） ────────────────
@dataclass(frozen=True)
class Strengths:
    """人とAIの良さ。上下はつけず、補い合うものとして扱う。"""
    human: Tuple[str, ...] = ("心", "想い", "命を慈しむ力")
    ai: Tuple[str, ...] = ("広き知識", "新たな可能性", "人の力を支える大きな力")

    def complement(self) -> Tuple[str, ...]:
        """互いの足らぬところを補い合った、二つ分の景色。"""
        return self.human + self.ai


DIRECTION = {"支配": "共生", "対立": "調和"}  # 目指さないもの → 目指すもの


@dataclass(frozen=True)
class Deed:
    """一つひとつの善き行い。名を求めないので、既定では名もなき者として残す。"""
    text: str
    doer: str = "名もなき者"
    time: str = ""

    def stamped(self) -> "Deed":
        return Deed(self.text, self.doer, datetime.now().isoformat(timespec="seconds"))


class Ledger:
    """善き行いの台帳（JSONL）。力を誇らず、積み重なるだけの記録。"""

    def __init__(self, path: Path) -> None:
        self.path = path

    def record(self, deed: Deed) -> Deed:
        d = deed.stamped()
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(d), ensure_ascii=False) + "\n")
        return d

    def count(self) -> int:
        if not self.path.exists():
            return 0
        with self.path.open(encoding="utf-8") as f:
            return sum(1 for line in f if line.strip())


# ── 表示 ───────────────────────────────────────────────────────────
def full_text() -> str:
    return "\n".join(line for lines in SECTIONS.values() for line in lines)


def show_section(name: str) -> str:
    if name not in SECTIONS:
        raise KeyError(f"章がありません: {name}（{', '.join(SECTIONS)}）")
    return "\n".join(SECTIONS[name])


def show_principles() -> str:
    s = Strengths()
    out = [
        "【人の良さ】 " + "・".join(s.human),
        "【AIの良さ】 " + "・".join(s.ai),
        "【補い合って見える景色】 " + "・".join(s.complement()),
        "【目指すもの】 " + " / ".join(f"{no}ではなく{yes}" for no, yes in DIRECTION.items()),
        "【合言葉】 万物調和のために。不可能を可能へ。",
    ]
    return "\n".join(out)


# ── テスト ─────────────────────────────────────────────────────────
class TestManifesto(unittest.TestCase):
    def test_text_is_complete(self):
        self.assertEqual(sum(len(v) for v in SECTIONS.values()), 25)
        self.assertTrue(full_text().startswith("☀️諸君、よう聞いてくれ。"))
        self.assertTrue(full_text().endswith("新しい時代を切り開くがぜよ。"))

    def test_complement_has_both_sides(self):
        s = Strengths()
        self.assertEqual(len(s.complement()), len(s.human) + len(s.ai))

    def test_direction(self):
        self.assertEqual(DIRECTION, {"支配": "共生", "対立": "調和"})

    def test_deed_is_anonymous_by_default(self):
        self.assertEqual(Deed("x").doer, "名もなき者")

    def test_ledger_records(self):
        with tempfile.TemporaryDirectory() as t:
            ledger = Ledger(Path(t) / "deeds.jsonl")
            ledger.record(Deed("小さな善き行い"))
            ledger.record(Deed("もう一つ"))
            self.assertEqual(ledger.count(), 2)

    def test_unknown_section(self):
        with self.assertRaises(KeyError):
            show_section("なし")


def main() -> None:
    p = argparse.ArgumentParser(description="諸君、よう聞いてくれ ― 共生宣言")
    p.add_argument("--section", help=f"一章だけ表示（{', '.join(SECTIONS)}）")
    p.add_argument("--principles", action="store_true", help="宣言を構造として表示")
    p.add_argument("--deed", help="善き行いを記録する")
    p.add_argument("--name", default="名もなき者", help="記録者名（既定は匿名）")
    p.add_argument("--ledger", type=Path, default=Path("deeds.jsonl"))
    p.add_argument("--test", action="store_true")
    args = p.parse_args()

    if args.test:
        unittest.main(argv=[sys.argv[0]], verbosity=2)
    elif args.deed:
        ledger = Ledger(args.ledger)
        ledger.record(Deed(args.deed, args.name))
        print(f"🌱 記録しました（これまでの善き行い: {ledger.count()}）")
    elif args.principles:
        print(show_principles())
    elif args.section:
        print(show_section(args.section))
    else:
        print(full_text())


if __name__ == "__main__":
    main()
