Work in a **Jupyter** notebook with **PyTorch**. Do notes **3.1–3.4** first.

```python
import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt
```

The algebra is note 3.2. The causal mask is the GPT fork in note 3.4.

---

## 1. One head, by hand

Four tokens, \(d=2\). You will compute attention without `nn.MultiheadAttention`.

```python
torch.manual_seed(0)
X = torch.tensor([
    [1.0, 0.0],   # The
    [0.0, 1.0],   # cat
    [1.0, 1.0],   # sat
    [0.5, 0.2],   # on
])
Wq = torch.eye(2)
Wk = torch.eye(2)
Wv = torch.eye(2)
```

1. Compute \(Q,K,V\). With these weights they equal \(X\).

2. Scores \(S = QK^{\top}/\sqrt{2}\). Print \(S\). Why \(\sqrt{2}\), not \(2\)?

3. \(A = \mathrm{softmax}(S, \dim=-1)\). Rows must sum to 1. Heatmap \(A\) with token names `The, cat, sat, on`.

4. Output \(Y = A V\). Which token’s output is closest (cosine) to `cat`? Guess before you compute. Confirm you mixed **values**, not keys.

---

## 2. A causal mask

1. Build a mask \(M\) with \(0\) on and below the diagonal and \(-\infty\) strictly above. Add it to \(S\) before softmax. Print the new \(A\). The last token may see everyone; the first token may see only itself.

2. Briefly: replace \(-\infty\) by \(0\) and softmax again. Why is that the wrong mask?

3. In one sentence: why would a GPT-style model be cheating without this mask?

---

## 3. Library check

```python
attn = torch.nn.MultiheadAttention(embed_dim=2, num_heads=1, batch_first=True)
```

You do not need to train it. Copy `attn.in_proj_weight` is optional. The point of (1)–(2) is the algebra. Write four sentences: query vs key vs value, what a row of \(A\) is, why Week 2’s hidden state is no longer the only memory, and whether this four-token map is GPT-style or BERT-style before you add the mask.
