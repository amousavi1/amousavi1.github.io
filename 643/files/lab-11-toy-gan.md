Work in a **Jupyter** notebook with **PyTorch**. Do notes **11.1–11.3** first. CPU is enough; keep the nets tiny and stop around a few hundred steps.

```python
import torch
from torch import nn
import matplotlib.pyplot as plt

torch.manual_seed(0)

MEANS = torch.tensor([[-2.0, 0.0], [2.0, 0.0]])

def real_batch(n=64):
    m = torch.randint(0, 2, (n,))
    return MEANS[m] + 0.25 * torch.randn(n, 2)
```

Two well-separated 2-D Gaussians. That is the whole dataset. You are checking whether \(G\) covers **both** modes, not whether it paints faces.

---

## 1. Tiny MLP \(G\) and \(D\)

```python
G = nn.Sequential(nn.Linear(8, 32), nn.ReLU(), nn.Linear(32, 2))
D = nn.Sequential(nn.Linear(2, 32), nn.ReLU(), nn.Linear(32, 1))
optG = torch.optim.Adam(G.parameters(), lr=1e-3)
optD = torch.optim.Adam(D.parameters(), lr=1e-3)
bce = nn.BCEWithLogitsLoss()
ones = lambda n: torch.ones(n, 1)
zeros = lambda n: torch.zeros(n, 1)
```

1. Confirm `real_batch(512)` really has two clouds: scatter-plot it. Mark the means.

2. Draw `z = torch.randn(512, 8)`, plot `G(z)` **before** training. It should look like a blob at the origin, not like the data.

---

## 2. A short adversarial loop

For 400 steps (you may stop at 200 if the plot already moves):

```python
n = 64
for step in range(400):
    real = real_batch(n)
    fake = G(torch.randn(n, 8)).detach()
    lossD = bce(D(real), ones(n)) + bce(D(fake), zeros(n))
    optD.zero_grad(); lossD.backward(); optD.step()

    fake = G(torch.randn(n, 8))
    lossG = bce(D(fake), ones(n))
    optG.zero_grad(); lossG.backward(); optG.step()
```

Print `lossD` and `lossG` every 100 steps. Do not treat them as quality.

After training, scatter 512 reals and 512 fakes on one plot (two colors).

---

## 3. Did you miss a mode?

Assign each fake to the nearest of the two means. Report the fraction in each bin.

1. If either bin is under \(10\%\) of the fakes, write **collapse** (or heavy imbalance). If both sit near \(50\%\), write **covered**.

2. Train once more from a new seed, or with 800 steps, only if the first run is a pancake on one mean. One extra run is enough. This lab is allowed to collapse; reporting it is the point.

3. Four sentences: what \(G\) and \(D\) each wanted, why a low generator loss is not coverage, which mode (if any) you missed, and one change you would try (noise dim, \(D\) steps, or more training) without claiming it is a cure.
