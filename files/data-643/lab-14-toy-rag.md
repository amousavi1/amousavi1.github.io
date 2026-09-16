Work in a **Jupyter** notebook with **NumPy** and **pandas**. Do notes **14.1–14.2** first. Offline only. Download [toy_docs.csv](files/data-643/toy_docs.csv).

**First time you implement this.** The lecture notes this week already answered what the method is, why it exists, the architecture, the formula, and the tradeoffs. Read that first-time block before these exercises. This lab is the first time you **compute** it, not the first definition.

```python
import re
import numpy as np
import pandas as pd
from pathlib import Path

df = pd.read_csv(Path("toy_docs.csv"))  # columns: id, text
```

The rows are invented AU-toy campus snippets. They are for ranking practice, not real hours or policy.

---

## 1. Bag-of-words cosine

```python
def toks(s):
    return re.findall(r"[a-z0-9]+", s.lower())

vocab = sorted({w for t in df.text for w in toks(t)})
word_i = {w: i for i, w in enumerate(vocab)}

def bow(s):
    v = np.zeros(len(vocab), float)
    for w in toks(s):
        if w in word_i:
            v[word_i[w]] += 1.0
    return v

def cosine(a, b):
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    return float(np.dot(a, b) / (na * nb)) if na and nb else 0.0

X = np.stack([bow(t) for t in df.text])
ids = list(df.id)
```

Query `q = "What time does Bender Library close on a weekday?"`

1. Rank all rows by cosine of `bow(q)` with `X`. Print id, score, and a 60-character snippet.

2. Take **\(k=2\)**. Write a two-sentence answer that cites chunk ids (for example `[d1]`). If the second chunk is off-topic, say so in the answer.

3. Repeat for `"Where do I meet Clawdia?"`. Did `d3` win?

---

## 2. A dummy calculator in a ReAct loop

```python
def calc(expr):
    expr = expr.strip()
    if not re.fullmatch(r"[0-9+\s*/]+", expr):
        return "ERR"
    return str(eval(expr, {"__builtins__": {}}, {}))

def react_library_minutes():
    log = []
    log.append(("Thought", "Weekday close is 23:00; convert 23 hours to minutes after midnight."))
    log.append(("Action", "calc[23*60]"))
    obs = calc("23*60")
    log.append(("Observation", obs))
    log.append(("Thought", "Use the observation, not a new multiply."))
    log.append(("Answer", f"Bender Library closes at 23:00, which is {obs} minutes after midnight [d1]."))
    return log
```

1. Run `react_library_minutes()` and print the log. Confirm the observation is `1380`.

2. Write a second log by hand (same five roles) for `"12 minute shuttle loops, how many in 1 hour?"` with `calc[60/12]`. The observation should be `5.0`. Cite `[d2]` in the Answer.

---

## 3. Write-up

Four sentences: which ids you cited for the library query, one retrieval miss you saw, why cosine on counts is not CLIP, and what the observation is for in ReAct.
