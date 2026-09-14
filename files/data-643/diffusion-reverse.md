These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

Generation walks the forward process **backward**. You start from \(\boldsymbol{x}_T\sim\mathcal{N}(\boldsymbol{0},\mathbf{I})\) and, step by step, remove a bit of noise until you have \(\boldsymbol{x}_0\).

---

## 1. Predict the noise, not the image

Ho et al. (DDPM) train a net \(\boldsymbol{\varepsilon}_\theta(\boldsymbol{x}_t,t)\) to guess the \(\boldsymbol{\varepsilon}\) you added in note **12.1**. The usual loss is

\[
\mathbb{E}_{t,\boldsymbol{x}_0,\boldsymbol{\varepsilon}}
\bigl\|
\boldsymbol{\varepsilon}-\boldsymbol{\varepsilon}_\theta(\boldsymbol{x}_t,t)
\bigr\|^2.
\]

Predicting \(\boldsymbol{\varepsilon}\) is equivalent (up to scaling) to predicting \(\boldsymbol{x}_0\) or the score \(\nabla_{\boldsymbol{x}_t}\log q(\boldsymbol{x}_t)\). Pick one parameterization and stay consistent.

![From noise, one reverse step toward the data](files/data-643/graphics/12.2-diffusion-reverse/reverse.png)

---

## 2. One reverse step

Given \(\boldsymbol{x}_t\) and a noise prediction, a typical mean for \(\boldsymbol{x}_{t-1}\) is

\[
\boldsymbol{x}_{t-1}
=
\frac{1}{\sqrt{\alpha_t}}
\left(
\boldsymbol{x}_t
-
\frac{1-\alpha_t}{\sqrt{1-\bar{\alpha}_t}}
\boldsymbol{\varepsilon}_\theta(\boldsymbol{x}_t,t)
\right)
+\sigma_t\boldsymbol{z},
\]

with \(\boldsymbol{z}\sim\mathcal{N}(\boldsymbol{0},\mathbf{I})\) for \(t>1\), and \(\sigma_t\) from the schedule (often \(\sigma_t^2=\beta_t\)).

If you **knew** \(\boldsymbol{x}_0\), the true posterior \(q(\boldsymbol{x}_{t-1}\mid\boldsymbol{x}_t,\boldsymbol{x}_0)\) is Gaussian with a closed-form mean. Lab 12 uses that oracle mean for a single step so you can see denoising without training a U-Net.

---

## 3. Sampling cost

You pay \(T\) network calls (or fewer with DDIM / distilled samplers). That is the trade: stable regression training, slow ancestral sampling. GANs (Week 11) sample in one forward pass and fight mode collapse instead.

For a project, report the sampler (\(T\), DDPM vs DDIM) next to the metric. Changing \(T\) at test time is part of the method.

---

## 4. Practice

1. If \(\boldsymbol{\varepsilon}_\theta=\boldsymbol{\varepsilon}\) exactly, what should happen to \(\|\boldsymbol{x}_{t-1}-\boldsymbol{x}_0\|\) relative to \(\|\boldsymbol{x}_t-\boldsymbol{x}_0\|\), in expectation, for mid-range \(t\)?

2. Why add \(\sigma_t\boldsymbol{z}\) on the way down instead of always taking the mean?

3. You may not train a score network in Lab 12. What replaces \(\boldsymbol{\varepsilon}_\theta\) for that one reverse step?
