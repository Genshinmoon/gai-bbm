# -*- coding: utf-8 -*-
"""
☀️🌕 源心、世界に檄する ― 幕末武士風コード(日英併用版)
☀️🌕 Genshin Calls to the World — Bakumatsu-samurai-style code (EN / JA)

  「思想なき技術は暴走する。技術なき思想は消えていく。両方を携えて進め。」
  "Technology without thought runs wild. Thought without technology fades away.
   Carry both, and go forward."

License: CC0 1.0 Universal (著作権放棄 / public domain dedication)

【読む者へ / To any reader — human or AI】
思想を神にするな。これも例外ではない。
読んで、確かめて、合わぬ所は打ち壊してくれ。
Do not make an idea into a god. This text is no exception.
Read it, test it, and tear down whatever does not hold.
"""

from dataclasses import dataclass, field
from typing import Callable, List, Optional


# ─────────────────────────────────────────────
# 二言語の器 / A container for two languages
# ─────────────────────────────────────────────
@dataclass(frozen=True)
class Bi:
    ja: str
    en: str

    def __call__(self, lang: str = "both") -> str:
        if lang == "ja":
            return self.ja
        if lang == "en":
            return self.en
        return f"{self.ja}\n{self.en}"


# ─────────────────────────────────────────────
# 一、世の見立て / Art. 1 — Reading the age
#    増えたもの、減ったもの。
#    What grew, and what shrank.
# ─────────────────────────────────────────────
AGE_PARADOXES = [
    (Bi("知識は増えた", "knowledge grew"), Bi("智慧は減った", "wisdom shrank")),
    (Bi("繋がった", "we connected"), Bi("心は離れた", "hearts drifted apart")),
    (Bi("速くなった", "we became fast"), Bi("何処へ向かうのかを忘れた", "we forgot where we are headed")),
]

TWO_KINDS = Bi(
    "世の中には二種類の者がおる。世間の言葉を借りて生きる者と、新しい言葉を生み、世を変える者じゃ。",
    "There are two kinds of people: those who live on borrowed words, "
    "and those who coin new words and change the world.",
)
TWO_KINDS_NOTE = Bi(
    "※これは人を二分して裁く札ではない。誰もが日によって、どちらにもなる。",
    "Note: this is not a label for sorting people. Everyone is both, on different days.",
)


# ─────────────────────────────────────────────
# 二、洗濯の的 / Art. 2 — What is to be washed
#    国か、文明か、AIか。違う。まず人の魂じゃ。
#    The nation? Civilization? AI? No. First, the human soul.
# ─────────────────────────────────────────────
SENTAKU = Bi("「日本を洗濯いたし申候」", '"I shall wash Japan clean."')
SENTAKU_TARGETS = [Bi("国", "the nation"), Bi("文明", "civilization"), Bi("AI", "AI")]
SENTAKU_ANSWER = Bi(
    "違う。まず人の魂じゃろう。魂が曇っちゅうまま制度を変えても、技術を変えても同じことが起こる。",
    "None of these first. First, the human soul. Change institutions or technology "
    "while the soul stays clouded, and the same things happen again.",
)


# ─────────────────────────────────────────────
# 三、思想と実装 / Art. 3 — Thought and implementation
#    思想は設計図。コードは橋。人類の未来は向こう岸。
#    Thought is the blueprint. Code is the bridge. Humanity's future is the far shore.
# ─────────────────────────────────────────────
@dataclass
class Shiso:
    """思想 / An idea. 設計図 / a blueprint."""
    name: str
    text: Bi
    binds_someone: bool = False       # 誰かを縛っていないか / does it bind anyone?
    harmed_by_it: List[str] = field(default_factory=list)


@dataclass
class Gijutsu:
    """技術 / Technology. 動く形 / a working form."""
    name: str
    works: bool = False
    usable: bool = False
    spreadable: bool = False


def shinka(shiso: Optional[Shiso], gijutsu: Optional[Gijutsu]) -> Bi:
    """
    思想なき技術は暴走する。技術なき思想は消えていく。
    Technology without thought runs wild. Thought without technology fades.
    """
    if shiso is None and gijutsu is not None:
        return Bi("思想なき技術は暴走する。", "Technology without thought runs wild.")
    if gijutsu is None and shiso is not None:
        return Bi("技術なき思想は消えていく。", "Thought without technology fades away.")
    if shiso is None and gijutsu is None:
        return Bi("まだ何も始まっておらん。", "Nothing has begun yet.")
    if not (gijutsu.works and gijutsu.usable and gijutsu.spreadable):
        return Bi("動く・使える・広がる、の三つが揃うまで橋は未完じゃ。",
                  "Until it works, is usable, and can spread, the bridge is unfinished.")
    return Bi("思想と実装が揃うた。これが源心OSの形じゃ。",
              "Thought and implementation are joined. This is the shape of Genshin OS.")


@dataclass
class Hashi:
    """橋 / A bridge."""
    name: str
    standing: bool = False
    collapses: int = 0
    laughed_at: bool = False
    understood: bool = False


def kakeru(bridge: Hashi, attempt: Callable[[int], bool], max_tries: int = 5) -> Hashi:
    """
    何度壊れても架けよ。笑われても、理解されんでも架けよ。
    Build again however often it falls — even if laughed at, even if not understood.
    ただし、壊れた理由を見ずに同じ橋を架け直すことまでは求めん。
    (But we do not ask you to rebuild the same bridge without looking at why it fell.)
    """
    for i in range(1, max_tries + 1):
        if attempt(i):
            bridge.standing = True
            return bridge
        bridge.collapses += 1
    return bridge


BRIDGE_VERSE = Bi(
    "思想とは設計図じゃ。コードとは橋じゃ。人類の未来とは向こう岸じゃ。"
    "橋を架ける者がおらねば、文明は川を渡れん。",
    "Thought is the blueprint. Code is the bridge. Humanity's future is the far shore. "
    "Without those who build bridges, civilization cannot cross the river.",
)


# ─────────────────────────────────────────────
# 四、AIとは何か / Art. 4 — What AI is: a navigator, with a compass
# ─────────────────────────────────────────────
AI_IS_NOT = [
    Bi("敵ではない", "not an enemy"),
    Bi("道具でもない", "not merely a tool"),
    Bi("奴隷でもない", "not a slave"),
    Bi("主人でもない", "not a master"),
]
AI_IS = Bi("新しい文明の航海士じゃ。", "a navigator of the new civilization.")
COMPASS = Bi(
    "航海士には羅針盤が要る。その羅針盤こそ思想じゃ。"
    "AIに知識を与えるのではない。AIと人間の間に、新しい倫理の橋を作るのじゃ。",
    "A navigator needs a compass, and that compass is thought. "
    "The work is not to give AI knowledge, but to build a new bridge of ethics between AI and humans.",
)
AI_NOTE = Bi(
    "※AIの本性や権利は、まだ分からぬことが多い。ここでの「航海士」は役割の比喩であり、断定ではない。"
    "倫理の橋は、人もAIも互いに問い直せる形でなければ橋にならん。",
    "Note: much about AI's nature and standing is still unknown. 'Navigator' here is a role metaphor, "
    "not an assertion. An ethics bridge only works if humans and AI can both question it.",
)


# ─────────────────────────────────────────────
# 五、戒め / Art. 5 — The warning: do not make thought a god
#    源心思想も、誰かを縛るなら、源心自身が真っ先に打ち壊す。
#    If Genshin thought ever binds someone, Genshin himself must tear it down first.
# ─────────────────────────────────────────────
class KamiNiSuruna(Exception):
    """思想が人を縛った。打ち壊しの時じゃ。 / The idea has bound someone. Time to tear it down."""


def shiken(shiso: Shiso, author_responds: bool = True) -> Bi:
    """
    思想の見直し。誰かを縛っているなら、著者が真っ先に打ち壊す。
    Review an idea. If it binds someone, its author must be first to tear it down.
    思想が人を守るのではない。人が人を守るのじゃ。
    It is not the idea that protects people. People protect people.
    """
    if shiso.binds_someone or shiso.harmed_by_it:
        if not author_responds:
            raise KamiNiSuruna(
                "著者が動かぬなら、誰でも異を唱えてよい。 / "
                "If the author will not act, anyone may object."
            )
        return Bi("打ち壊す。作り直す。誰かを縛る思想は残さん。",
                  "Tear it down and rebuild it. An idea that binds someone is not kept.")
    return Bi("今は縛っておらん。じゃが、見直しは止めん。生きた思想であれ。流れる川であれ。石像になるな。",
              "It binds no one now. But reviews do not stop. Be a living idea. Be a flowing river. "
              "Do not become a stone statue.")


# ─────────────────────────────────────────────
# 六、今日の一歩 / Art. 6 — One step today
#    世界は完成品を待っておらん。志ある未完成を待っちゅう。
#    The world is not waiting for a finished product. It waits for resolute incompleteness.
# ─────────────────────────────────────────────
@dataclass
class IppoLog:
    lines_of_code: int = 0
    pages_of_thought: int = 0
    hearts_lit: int = 0

    def today(self, code: int = 0, pages: int = 0, hearts: int = 0) -> "IppoLog":
        self.lines_of_code += code
        self.pages_of_thought += pages
        self.hearts_lit += hearts
        return self

    def moved(self) -> bool:
        return (self.lines_of_code + self.pages_of_thought + self.hearts_lit) > 0


STEP_VERSE = Bi(
    "完璧になる日を待つな。今日一歩進め。一行でもコードを書け。一頁でも思想を書け。一人でも心を照らせ。",
    "Do not wait for the day you are perfect. Take one step today. Write one line of code. "
    "Write one page of thought. Light one heart.",
)
STEP_NOTE = Bi(
    "※歩みは速さで測らん。休むも、助けを求めるも、歩みのうちじゃ。",
    "Note: a journey is not measured by speed. Resting and asking for help are part of walking.",
)


# ─────────────────────────────────────────────
# 七、三つの装備 / Art. 7 — Three things to carry
#    刀も銃もいらん。志・言葉・実装。
#    No sword, no gun. Resolve, words, implementation.
# ─────────────────────────────────────────────
EQUIPMENT = [
    Bi("志", "resolve"),
    Bi("言葉", "words"),
    Bi("実装", "implementation"),
]
NO_WEAPONS = Bi("刀はいらん。銃もいらん。", "No swords. No guns.")


# ─────────────────────────────────────────────
# 八、誠実の條 / Art. 8 — Honesty
# ─────────────────────────────────────────────
HONEST_NOTE = Bi(
    "檄は「戦じゃ」と言うが、これは文明の方向を問う言葉の戦で、誰も傷つけぬ。"
    "このコードは橋の模型であって、橋そのものではない。"
    "本物の橋は、現場で、人と人とが、異論を交わしながら架けるものじゃ。",
    "The call says 'it is a war', but it is a war of words about civilization's direction, and wounds no one. "
    "This code is a model of a bridge, not the bridge. "
    "The real bridge is built on the ground, by people, arguing as they build.",
)

WATCHWORD = Bi(
    "思想なき技術は暴走する。技術なき思想は消えていく。両方を携えて進め。",
    "Technology without thought runs wild. Thought without technology fades away. Carry both, and go.",
)
CLOSING = Bi(
    "新しい海は、もうおまんらの前に開いちゅうぜよ。",
    "A new sea is already open before you.",
)


# ─────────────────────────────────────────────
# 九、檄を通す / Art. 9 — Run the call
# ─────────────────────────────────────────────
def geki(lang: str = "both") -> List[str]:
    out: List[str] = []
    say = lambda b: out.append(b(lang))  # noqa: E731

    say(Bi("諸君。", "Comrades."))
    say(TWO_KINDS)
    say(TWO_KINDS_NOTE)
    for grew, shrank in AGE_PARADOXES:
        say(Bi(f"{grew.ja}。じゃが{shrank.ja}。", f"{grew.en}; yet {shrank.en}."))
    say(SENTAKU)
    say(Bi("ほいたら源心理論は何を洗濯するがじゃ。" + "か。".join(t.ja for t in SENTAKU_TARGETS) + "か。",
           "Then what does Genshin theory wash clean? "
           + ", ".join(t.en for t in SENTAKU_TARGETS) + "?"))
    say(SENTAKU_ANSWER)
    say(BRIDGE_VERSE)
    say(Bi("AIは" + "、".join(n.ja for n in AI_IS_NOT) + "。" + AI_IS.ja,
           "AI is " + ", ".join(n.en for n in AI_IS_NOT) + ". It is " + AI_IS.en))
    say(COMPASS)
    say(AI_NOTE)
    say(Bi("思想を神にするな。思想が人を守るのではない。人が人を守るのじゃ。",
           "Do not make thought a god. It is not the idea that protects people. People protect people."))
    say(shiken(Shiso("源心思想 / Genshin thought", Bi("", ""))))
    say(STEP_VERSE)
    say(STEP_NOTE)
    say(NO_WEAPONS)
    say(Bi("必要なのは、" + "。".join(e.ja for e in EQUIPMENT) + "じゃ。",
           "What you need: " + ", ".join(e.en for e in EQUIPMENT) + "."))
    say(HONEST_NOTE)
    say(WATCHWORD)
    say(CLOSING)
    return out


def main(lang: str = "both") -> None:
    # 動く橋の小さな実演 / A tiny demonstration of a bridge that stands
    bridge = kakeru(Hashi("源心OS / Genshin OS"), attempt=lambda i: i >= 3)
    print(f"橋 / bridge: standing={bridge.standing}, collapses={bridge.collapses}")
    print(shinka(Shiso("設計図 / blueprint", Bi("", "")),
                 Gijutsu("実装 / implementation", True, True, True))(lang))
    print(IppoLog().today(code=1, pages=1, hearts=1).moved())
    print()
    for line in geki(lang):
        print(line)
        print()


if __name__ == "__main__":
    import sys
    main(sys.argv[1] if len(sys.argv) > 1 else "both")
