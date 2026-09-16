Work in a **Jupyter** notebook with **numpy**, **PyTorch**, and `matplotlib`. Do notes **6.1–6.3** first. No pretrained Whisper or CLAP: construct the waveform yourself.

**First time you implement this.** The lecture notes this week already answered what the method is, why it exists, the architecture, the formula, and the tradeoffs. Read that first-time block before these exercises. This lab is the first time you **compute** it, not the first definition.

```python
import numpy as np
import torch
import matplotlib.pyplot as plt
```

---

## 1. A sine mixture

Sampling rate \(f_s=8000\), one second.

```python
fs = 8000
t = np.arange(0, 1.0, 1 / fs)
x = 0.6 * np.sin(2 * np.pi * 440 * t) + 0.4 * np.sin(2 * np.pi * 880 * t)
```

1. Plot `x[:800]` (0.1 s). Guess where the beats sit before you zoom.

2. Write an STFT with a Hann window, `n_fft=256`, `hop=128`. For each frame \(i\), take `np.fft.rfft` of the windowed slice. Stack **magnitudes** into `S` with shape `(n_freq, n_frames)`.

3. Plot `np.log1p(S)` as an image (`origin="lower"`, aspect auto). You should see two horizontal bands near 440 Hz and 880 Hz. Convert a frequency bin index to hertz with \(f = k \cdot f_s / N\).

---

## 2. Patches as tokens

Treat `S` as a one-channel image.

1. Crop `S` so both axes are divisible by 8. Cut non-overlapping \(8\times 8\) tiles. How many tokens \(N\)? Flatten each tile to length 64.

2. Map tiles with `nn.Linear(64, 16)` (random weights are fine). Print the tensor shape `(N, 16)`. This is the ViT move from Lab 4, on a spectrogram instead of RGB.

---

## 3. Concat versus add

Two modality vectors in 4-D (pretend audio and text):

```python
a = torch.tensor([1.0, 0.0, 1.0, 0.0])
b = torch.tensor([0.0, 1.0, 0.0, 1.0])
```

1. Concatenate (`torch.cat`) and print the length. Add them and print the length. Which one can you feed to a linear layer that still expects width 4?

2. L2-normalize `a` and `b`, then print cosine. Concat does not have a cosine until you define one; add already lives in the same \(\mathbb{R}^4\).

3. Write four sentences: what a spectrogram frame is, why a hop that is too large smears 440 Hz versus 880 Hz in time, what a patch token threw away (phase, exact bin phase), and one fusion choice (concat vs add vs cross-attention) you would pick if the text vector were width 768 and the audio vector were width 512.
