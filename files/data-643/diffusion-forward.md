These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

A **diffusion** model learns to denoise. The forward process is not learned. You add Gaussian noise on a schedule until the sample is almost prior noise. Training later asks a net to predict that noise.

---

## 1. Destroy the sample on purpose

Start from data \(\boldsymbol{x}_0\). A variance schedule \(0<\beta_t<1\) (small at first, larger later) defines

\[
\alpha_t = 1-\beta_t,\qquad
\bar{\alpha}_t = \prod_{s=1}^{t}\alpha_s.
\]

The Markov step is \(q(\boldsymbol{x}_t\mid\boldsymbol{x}_{t-1})=\mathcal{N}(\boldsymbol{x}_t;\sqrt{\alpha_t}\,\boldsymbol{x}_{t-1},\beta_t\mathbf{I})\). You do not have to simulate every hop. The marginal is closed form:

\[
q(\boldsymbol{x}_t\mid\boldsymbol{x}_0)
=
\mathcal{N}\bigl(\boldsymbol{x}_t;\,\sqrt{\bar{\alpha}_t}\,\boldsymbol{x}_0,\,(1-\bar{\alpha}_t)\mathbf{I}\bigr).
\]

In code: \(\boldsymbol{x}_t=\sqrt{\bar{\alpha}_t}\,\boldsymbol{x}_0+\sqrt{1-\bar{\alpha}_t}\,\boldsymbol{\varepsilon}\) with \(\boldsymbol{\varepsilon}\sim\mathcal{N}(\boldsymbol{0},\mathbf{I})\).

![A clean point becoming isotropic noise over t](files/data-643/graphics/12.1-diffusion-forward/forward.png)

---

## 2. What the schedule is doing

\(\bar{\alpha}_t\) starts near 1 (the point is still itself) and falls toward 0 (the point is almost \(\boldsymbol{\varepsilon}\)). Linear, cosine, and learned \(\beta_t\) are all ways to spend more steps where structure dies. Too fast a schedule and early \(t\) is already junk; too slow and you waste capacity on near-copies of \(\boldsymbol{x}_0\).

\(T\) (often 1000 in image papers) is a discretization. Lab 12 uses a small \(T\) in 2-D so you can plot the path.

---

## 3. Why this is nicer than a GAN to train

The forward kernel is **fixed**. There is no discriminator to race. The training signal at each \(t\) is a denoising regression against a known \(\boldsymbol{\varepsilon}\). You still have to pick \(\{\beta_t\}\) and \(T\). Sampling will be a reverse chain (note **12.2**), which is slower than one GAN forward pass.

---

## 4. Practice

1. If \(\bar{\alpha}_t=1\), what is \(\boldsymbol{x}_t\)? If \(\bar{\alpha}_t=0\), what is \(\boldsymbol{x}_t\)?

2. Why can you sample \(\boldsymbol{x}_t\) in one line instead of looping \(t\) steps of \(q(\boldsymbol{x}_s\mid\boldsymbol{x}_{s-1})\)?

3. A classmate sets every \(\beta_t=0.9\). What goes wrong in the first few \(t\)?
