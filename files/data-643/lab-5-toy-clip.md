Work in a **Jupyter** notebook. This lab uses a **constructed** CLIP-like space, not OpenAI weights, so it runs offline. Download [toy_clip.csv](files/data-643/toy_clip.csv).

**First time you implement this.** The lecture notes this week already answered what the method is, why it exists, the architecture, the formula, and the tradeoffs. Read that first-time block before these exercises. This lab is the first time you **compute** it, not the first definition.

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

df = pd.read_csv(Path("toy_clip.csv"))
# columns: name, kind (image|text), x, y
```

Each concept (`cat`, `dog`, `nurse`, `ceo`, …) has an image row and a text row in 2-D.

```python
def vecs(kind):
    sub = df[df.kind == kind]
    return {row["name"]: np.array([row.x, row.y], float) for _, row in sub.iterrows()}

img, txt = vecs("image"), vecs("text")

def cosine(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
```

---

## 1. Retrieval

1. For query text `"cat"`, rank all **images** by cosine. Is `cat` first?

2. For query image `"ceo"`, rank all **texts**. Print the top three.

3. Build the full image-to-text cosine matrix. Heatmap it. Comment on the diagonal.

---

## 2. Zero-shot

Treat texts `cat, dog, nurse, ceo` as class prompts.

1. Classify image `dog` by nearest prompt.

2. Classify image `nurse` twice: prompts as above, then replace `nurse` with the prompt name `woman` if present, or add a fake prompt vector by copying `nurse`’s text shifted toward `she` if you added one in the CSV. The CSV already includes `man` and `woman` text rows. Compare `nurse` and `ceo` images against prompts `man` vs `woman`. Which occupation sits closer to `man`?

---

## 3. Robustness

1. Add noise: `img["cat"] + np.array([0.8, -0.8])`. Does retrieval still return cat?

2. Write five lines: what CLIP would do that this CSV fakes, what BLIP adds (generation), one bias number you measured, and one limitation of 2-D toys.

Scatter-plot all points, color by `kind`, annotate `name`.
