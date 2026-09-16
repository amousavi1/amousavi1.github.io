Work in a **Jupyter** notebook with **PyTorch** and `numpy`. Do notes **9.1–9.3** first. Optional file: [toy_prefs.csv](files/data-643/toy_prefs.csv) (`prompt`, `chosen`, `rejected`).

**First time you implement this.** The lecture notes this week already answered what the method is, why it exists, the architecture, the formula, and the tradeoffs. Read that first-time block before these exercises. This lab is the first time you **compute** it, not the first definition.

```python
import torch
import torch.nn.functional as F
import numpy as np
```

---

## 1. Two completions, a logistic RM

You will not download an LLM. Invent scalar features for each reply (length, a fake “keyword” score).

```python
torch.manual_seed(0)
# rows: [length, keyword_hit] for chosen then rejected, three prompts
chosen = torch.tensor([[12., 1.], [8., 1.], [20., 0.]])
rejected = torch.tensor([[40., 0.], [9., 0.], [6., 1.]])
```

1. A linear reward `r = w · h + b` with `w` of length 2. Loss for one pair is `-log σ(r_w - r_l)` (note **9.1**). Implement it with `F.binary_cross_entropy_with_logits(r_w - r_l, torch.ones(n))`.

2. Train `w,b` for a few hundred Adam steps. Print rewards. Chosen should outscore rejected on most rows.

3. If you loaded the CSV, tokenize naively with `.split()` and use `[len(tokens), float("paris" in text.lower())]` or a similar two-D feature. Same loss. Do not need pandas: `open` and `line.split(",", 2)` is enough if you are careful with commas, or just stay on the tensors above.

---

## 2. DPO-style loss on toy logits

Treat log-probs as given scalars (as if you already ran a forward pass).

```python
# log πθ and log πref for (winner, loser) on one prompt
logp_w, logp_l = torch.tensor(0.0, requires_grad=True), torch.tensor(-1.0, requires_grad=True)
logp_ref_w, logp_ref_l = torch.tensor(-0.2), torch.tensor(-0.4)
beta = 0.1
```

1. DPO logit:

```python
delta = beta * ((logp_w - logp_ref_w) - (logp_l - logp_ref_l))
loss = -F.logsigmoid(delta)
```

Print `loss`. Then set `logp_w = logp_ref_w` and `logp_l = logp_ref_l` (no grad needed). Loss should be \(-\log\sigma(0)=\log 2\).

2. Take one Adam step on `logp_w, logp_l` only (freeze the reference). After a few steps, `logp_w - logp_l` should grow. That is “prefer the chosen completion.”

---

## 3. Write-up

Four sentences: what the RM logistic compares, why a rejected fluent answer is still useful, what \(\beta\) does in DPO, and why this lab’s scalars are not a language model (no tokens, no KL over a vocabulary).
