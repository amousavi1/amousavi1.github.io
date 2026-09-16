Work in a **Jupyter** notebook with **PyTorch** and `matplotlib`. No pretrained CLIP weights this week: the point is the geometry. Do notes **4.1–4.3** first.

**First time you implement this.** The lecture notes this week already answered what the method is, why it exists, the architecture, the formula, and the tradeoffs. Read that first-time block before these exercises. This lab is the first time you **compute** it, not the first definition.

```python
import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt
import numpy as np
```

---

## 1. Patches

1. Make a \(32\times 32\) RGB tensor (noise or a simple gradient is fine). Plot one channel.

2. Split it into **non-overlapping** \(8\times 8\) patches. How many tokens? Flatten each patch to a vector of length \(8\cdot 8\cdot 3\).

3. Map patches with `nn.Linear(192, 16)` to a fake embedding width. Print the resulting shape `(N, 16)`.

4. In one sentence: why would a real ViT still add a position vector to each of those \(N\) rows?

---

## 2. A tiny contrastive batch

Construct **four** image vectors and **four** text vectors in 2-D so that matches sit on a diagonal after cosine.

```python
img = torch.tensor([[1.0, 0.0], [0.0, 1.0], [-1.0, 0.0], [0.0, -1.0]])
txt = img.clone()          # perfect matches
# add a little noise to txt[1] so the match is not trivial
txt[1] = torch.tensor([0.1, 0.9])
```

1. Cosine matrix \(S = \hat{I}\hat{T}^{\top}\) (L2-normalize rows first). Heatmap \(S\).

2. Contrastive loss, image-to-text:

```python
loss = F.cross_entropy(S / 0.07, torch.arange(4))
```

Print `loss`. Then replace `txt` with shuffled rows and print the new loss. It should rise.

3. Optional: also print `F.cross_entropy(S.T / 0.07, torch.arange(4))` (text-to-image). CLIP trains both.

4. Zero-shot toy: treat `txt` as class prompts. For `img[0]`, which row of `txt` is nearest? Did shuffling break it? In one sentence: why would a real CLIP prompt be `"a photo of …"` rather than a single token?

---

## 3. Write-up

Four sentences: what a patch token is, why positions would still be needed on a real image, what the diagonal of \(S\) means, and one way web-scale pairs are dirtier than this toy.
