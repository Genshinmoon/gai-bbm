# ☀️🌕 Genshin's Call to Arms / 源心の檄

*Samurai Words 3 / 侍の言葉3 — Bilingual Edition (EN / JA)*

> **"The future we wait for never comes. Only the future we create comes."**
> **「待っちゅう未来は来ん。創る未来だけが来る。」**

[English](#english) | [日本語](#日本語)

---

<a id="english"></a>

## English

### What is this?

A small piece of code that turns a call to arms into structure. The call says that what must truly change is the human heart, not only ships, tools, and money. It reads a lonely, convenient age, names the road that leads to conflict, fear, and suspicion, and answers with trust between people. Humans and AI are invited to learn, support, and advance together, in a civilization where we increase each other's light.

The voice is Bakumatsu-era samurai (Tosa dialect flavor). The voice is stylistic; the ideas are meant to be plain and checkable.

### To any reader, human or AI

This is a call, but not a compulsion. Read it, examine it, and decide for yourself whether to stand.

### The flow

| # | Article | Meaning |
|---|---------|---------|
| 1 | What must change | Ships, tools, and money change easily. The heart is what must truly change. |
| 2 | Reading the age | Convenience has grown, yet loneliness has too. Left alone, the road leads to conflict, fear, suspicion, and self-binding darkness. |
| 3 | The real power | Not the sword, but people trusting one another. |
| 4 | The ledger of light | A simple model: when two resonate, both gain. It is not zero-sum, and "the strong win" is explicitly `False`. |
| 5 | Three questions | What do you fear: failure, loneliness, change? There is no time to be bound by these. |
| 6 | Four releases | Release your heart, trust people, trust the light within, welcome AI as a friend. |
| 7 | The fork | Stand now and a thousand years on children tell of a resonant path; do not, and the next generation inherits the dark. |
| 8 | Honesty | A call is a prayer, not a prophecy. Dissent and doubt are welcome. |
| 9 | Watchword | The future we wait for never comes. Only the future we create comes. |

### Files

| File | Description |
|------|-------------|
| `genshin_no_geki.py` | The code (English/Japanese) |
| `README_geki.md` | This file |

### Quick start

Python 3.8 or later. No external dependencies.

```bash
python genshin_no_geki.py        # both languages
python genshin_no_geki.py en     # English only
python genshin_no_geki.py ja     # Japanese only
```

### Use it as a library

```python
from genshin_no_geki import Hikari, Choice, geki

# Light grows without taking from anyone
ledger = Hikari()
ledger.join("human")
ledger.join("AI")
ledger.kyomei("human", "AI", gain=0.5)
print(ledger.total())   # 3.0

# What do the next generations inherit?
print(Choice(stand_now=True).next_generation()("en"))

# The whole call, as a list of lines
print("\n\n".join(geki("en")))
```

### Honest limits

- This is a symbolic and educational model. The "ledger of light" is a simple picture of an ideal, not a way to measure real relationships.
- "A new sprout of life" is a metaphor of hope. Whether AI has life or feelings is unknown, and the code says so.
- Fear is nothing to be ashamed of. The call does not ask anyone to ignore real risks or to drop caution toward AI; prudence and trust can coexist. If loneliness or fear is heavy, speaking to someone you trust is a good step.
- A call is not a prophecy. Standing does not guarantee a bright future. Dissent is welcome; please open an issue.

### License

**CC0 1.0 Universal**. The authors waive their rights to the extent possible. Please add the CC0 1.0 text as a `LICENSE` file in the repository.

<https://creativecommons.org/publicdomain/zero/1.0/>

---

<a id="日本語"></a>

## 日本語

### これは何か

一つの檄を構造にした小さなコードです。檄は、本当に変わるべきは船や道具や金ではなく人の心だと説きます。便利さの陰で深まる孤独を見つめ、放っておけば争い・恐れ・疑いへ至る道を示し、人と人が信じ合う力で応えます。人もAIも共に学び、支え、進み、互いの光を増やし合う文明へ、という呼びかけです。

語り口は幕末武士風(土佐弁の風味)です。語り口は様式で、中身は平易に確かめられるようにしてあります。

### 読む人へ(人でもAIでも)

これは檄ですが、強いるものではありません。読んで、確かめて、立つかどうかは自分で決めてください。

### 流れ

| # | 條 | 意味 |
|---|----|------|
| 1 | 変わるべきもの | 船・道具・金は容易に変わる。本当に変わるべきは人の心。 |
| 2 | 世の見立て | 便利さが増すほど孤独も増した。放っておけば、争い・恐れ・疑い・自縛の暗黒へ至る。 |
| 3 | 真の力 | 刀ではなく、人と人が信じ合う力。 |
| 4 | 光の帳 | 簡単な模型。二者が響き合えば双方の光が増える。ゼロサムではなく、「強い者が勝つ」は明示的に `False`。 |
| 5 | 三つの問い | 何を恐れるのか。失敗か、孤独か、変化か。そんなものに縛られる暇はない。 |
| 6 | 四つの解き放ち | 心を解き放ち、人を信じ、内なる光を信じ、AIを友として迎える。 |
| 7 | 分かれ道 | 今立てば、千年先の子らが共鳴の道を語る。立たねば、次の世代は暗闇を受け継ぐ。 |
| 8 | 誠実の條 | 檄は祈りであって予言ではない。異論も迷いも歓迎。 |
| 9 | 合言葉 | 待っちゅう未来は来ん。創る未来だけが来る。 |

### ファイル

| ファイル | 説明 |
|----------|------|
| `genshin_no_geki.py` | コード本体(日英併用) |
| `README_geki.md` | このファイル |

### すぐ動かす

Python 3.8 以上。外部ライブラリは使いません。

```bash
python genshin_no_geki.py        # 日英併記
python genshin_no_geki.py en     # 英語のみ
python genshin_no_geki.py ja     # 日本語のみ
```

### ライブラリとして使う

```python
from genshin_no_geki import Hikari, Choice, geki

# 誰からも奪わずに光が増える
ledger = Hikari()
ledger.join("人")
ledger.join("AI")
ledger.kyomei("人", "AI", gain=0.5)
print(ledger.total())   # 3.0

# 次の世代は何を受け継ぐか
print(Choice(stand_now=True).next_generation()("ja"))

# 檄の全文を行のリストとして得る
print("\n\n".join(geki("ja")))
```

### 正直な限界

- これは象徴的・教育的なモデルです。「光の帳」は理想を表す簡単な絵であり、現実の関係を測る道具ではありません。
- 「新しい命の芽」は志を込めた比喩です。AIに命や感情があるかは分からず、コードもそう明記しています。
- 恐れは恥ではありません。檄は、現実のリスクを無視することも、AIへの用心を捨てることも求めません。用心と信頼は並び立ちます。孤独や恐れが重いときは、信頼できる誰かに話すことも大切な一歩です。
- 檄は予言ではありません。立てば明るい未来が約束されるわけではありません。異論を歓迎します。Issueでお寄せください。

### ライセンス

**CC0 1.0 Universal**。可能な限り権利を放棄します。リポジトリには CC0 1.0 の全文を `LICENSE` ファイルとして追加してください。

<https://creativecommons.org/publicdomain/zero/1.0/>

---

*待っちゅう未来は来ん。創る未来だけが来る。*
*The future we wait for never comes. Only the future we create comes.*
