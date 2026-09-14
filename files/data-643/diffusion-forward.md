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

That one-liner is the whole point of this note. Training (note **12.2**) samples a random \(t\), draws \(\boldsymbol{\varepsilon}\), forms \(\boldsymbol{x}_t\) in one shot, and asks a net to guess \(\boldsymbol{\varepsilon}\). You never need to walk \(1,2,\ldots,t\) unless you want a picture of the path.

---

## 2. What the schedule is doing

\(\bar{\alpha}_t\) starts near 1 (the point is still itself) and falls toward 0 (the point is almost \(\boldsymbol{\varepsilon}\)). Linear, cosine, and learned \(\beta_t\) are all ways to spend more steps where structure dies. Too fast a schedule and early \(t\) is already junk; too slow and you waste capacity on near-copies of \(\boldsymbol{x}_0\).

\(T\) (often 1000 in image papers) is a discretization. Lab 12 uses a small \(T\) in 2-D so you can plot the path. Print \(\bar{\alpha}_1\), \(\bar{\alpha}_{T/2}\), \(\bar{\alpha}_T\): they should fall.

---

## 3. Why this is nicer than a GAN to train

The forward kernel is **fixed**. There is no discriminator to race. The training signal at each \(t\) is a denoising regression against a known \(\boldsymbol{\varepsilon}\). You still have to pick \(\{\beta_t\}\) and \(T\). Sampling will be a reverse chain (note **12.2**), which is slower than one GAN forward pass.

Coverage is not automatic, but you are not playing a min-max game. That is the trade this week is for.

---

## 4. Teaching this note

About **35 minutes** at the board, then **~6 minutes** of video. First of three Week-12 notes.

- **0–12 min.** Markov step vs closed-form marginal. Write \(\alpha_t\) and \(\bar{\alpha}_t\).
- **12–22 min.** The one-line reparameterization. Draw \(x_0\) mixing with \(\varepsilon\).
- **22–33 min.** Worked scalar step. Change \(\bar{\alpha}_t\) from 1 to 0 and watch \(x_t\).
- **Then** play Umar Jamil **7:35–13:00** (forward/reverse cartoon, then the math of \(q\)). Pause on the closed-form \(q(x_t\mid x_0)\).

---

## 5. Worked example

Take a 1-D point \(x_0=1.0\) and a draw \(\varepsilon=2.0\). Then

\[
x_t=\sqrt{\bar{\alpha}_t}\,x_0+\sqrt{1-\bar{\alpha}_t}\,\varepsilon.
\]

| \(\bar{\alpha}_t\) | \(\sqrt{\bar{\alpha}_t}\,x_0\) | \(\sqrt{1-\bar{\alpha}_t}\,\varepsilon\) | \(x_t\) |
| --- | --- | --- | --- |
| \(1\) | \(1.0\) | \(0\) | \(1.0\) |
| \(0.64\) | \(0.8\) | \(0.6\times 2.0=1.2\) | \(2.0\) |
| \(0\) | \(0\) | \(2.0\) | \(2.0\) |

At \(\bar{\alpha}_t=0.64\) you already sit at \(2.0\): more noise than signal. At \(\bar{\alpha}_t=0\) you have thrown \(x_0\) away; \(x_t\) is just \(\varepsilon\).

Same arithmetic in Lab 12 with a vector \(x_0=(1.5,-0.8)\) and a vector \(\varepsilon\). The square roots are scalar; they multiply every coordinate.

You can jump to any \(t\) without simulating \(q(x_s\mid x_{s-1})\) for \(s=1,\ldots,t\). That is why training is a single Gaussian draw, not a loop of length \(t\).

---

## 6. Where students get stuck

- Simulating all \(T\) Markov steps at train time. You sample \(t\) and use \(q(x_t\mid x_0)\).
- Mixing up \(\beta_t\), \(\alpha_t\), and \(\bar{\alpha}_t\). Write the three definitions every time.
- Setting every \(\beta_t\) huge. Then \(\bar{\alpha}_t\) crashes in a few steps and the net never sees a lightly noised \(x_0\).

---

## 7. Video

Watch [Umar Jamil, How diffusion models work](https://www.youtube.com/watch?v=I1sPXkm2NH4), **7:35–13:00**.

Pause on the forward process \(q\) (no \(\theta\)) and the closed-form jump to \(x_t\). Skip the U-Net coding (after ~16:30) in this class. Note **12.2** continues the same video at the training/sampling chapters.

---

## 8. Practice

1. If \(\bar{\alpha}_t=1\), what is \(\boldsymbol{x}_t\)? If \(\bar{\alpha}_t=0\), what is \(\boldsymbol{x}_t\)?

2. Why can you sample \(\boldsymbol{x}_t\) in one line instead of looping \(t\) steps of \(q(\boldsymbol{x}_s\mid\boldsymbol{x}_{s-1})\)?

3. A classmate sets every \(\beta_t=0.9\). What goes wrong in the first few \(t\)?

4. \(x_0=4\), \(\bar{\alpha}_t=0.25\), \(\varepsilon=-1\). Compute \(x_t\). (\(\sqrt{0.25}=0.5\), \(\sqrt{0.75}\approx 0.866\).)

5. \(\beta_1=0.1\), \(\beta_2=0.2\). Compute \(\alpha_1,\alpha_2,\bar{\alpha}_2\).
