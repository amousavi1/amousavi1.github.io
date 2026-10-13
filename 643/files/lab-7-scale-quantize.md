Work in a **Jupyter** notebook with **PyTorch** and `matplotlib`. Do notes **7.1–7.3** first. No Hugging Face weights this week.

```python
import torch
import matplotlib.pyplot as plt
```

---

## 1. Fit a toy scaling law

Construct compute \(C\) and loss \(L = a C^{-b} + c\) plus a little noise. You will recover \(a,b,c\).

```python
torch.manual_seed(0)
a_true, b_true, c_true = 2.0, 0.15, 1.4
C = torch.logspace(2, 6, 16)          # 1e2 .. 1e6
L = a_true * C.pow(-b_true) + c_true
L = L + 0.02 * torch.randn_like(L)
```

1. Scatter \(\log C\) versus \(L\). Guess whether \(c\) is near 1.4 before you fit.

2. Fit with Adam on unconstrained parameters, but keep \(a>0\), \(b>0\) via softplus:

```python
p = torch.nn.Parameter(torch.tensor([1.0, 0.1, 1.0]))  # raw a,b,c
opt = torch.optim.Adam([p], lr=0.05)
for _ in range(2000):
    a, b, c = torch.nn.functional.softplus(p[0]), torch.nn.functional.softplus(p[1]), p[2]
    pred = a * C.pow(-b) + c
    loss = ((pred - L) ** 2).mean()
    opt.zero_grad(); loss.backward(); opt.step()
```

Print fitted \(a,b,c\) versus truth. Overlay `pred` on the scatter.

3. In one sentence: if you only observed the four smallest \(C\), would \(c\) still be identified?

---

## 2. Affine int8-ish quantization

```python
torch.manual_seed(1)
x = torch.randn(256)
qmin, qmax = -128, 127
```

1. Compute `scale = (x.max() - x.min()) / (qmax - qmin)` and `zp = qmin - x.min() / scale`. Quantize with

```python
q = torch.clamp(torch.round(x / scale + zp), qmin, qmax)
xhat = (q - zp) * scale
```

Print MSE `(x - xhat).pow(2).mean()`. It should be small relative to `x.var()`.

2. Repeat after replacing `x` with `x.clone(); x[0] = 50.0` (one outlier). MSE should jump. Why do activation outliers break naive INT8?

3. Histogram `x` and `xhat` on one figure.

---

## 3. Write-up

Four sentences: what \(C^{-b}\) says about diminishing returns, why Chinchilla would not only grow \(a\)’s “model” without growing tokens, what scale and zero-point are for, and one reason speculative decoding is not the same as distillation.
