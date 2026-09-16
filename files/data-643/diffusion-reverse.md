These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

Generation walks the forward process **backward**. You start from \(\boldsymbol{x}_T\sim\mathcal{N}(\boldsymbol{0},\mathbf{I})\) and, step by step, remove a bit of noise until you have \(\boldsymbol{x}_0\).

---

> **First time the reverse process appears.** The **reverse** is: predict the noise you added, take a step toward \(x_0\), repeat \(T\) times.
>
> **What.** A net \(\varepsilon_\theta(x_t,t)\) predicts \(\varepsilon\). Training is MSE on that noise. Sampling starts from \(x_T\sim\mathcal{N}(0,I)\) and denoises.
> **Why.** You cannot write the true reverse in closed form for images. Predicting \(\varepsilon\) is equivalent (under the usual parameterization) to predicting the posterior mean.
> **Architecture.** U-Net or DiT on \(x_t\) with a time embedding. Lab 12 uses an **oracle** mean so you see the geometry without training.
> **How.** Loss: \(\mathbb{E}\lVert\varepsilon-\varepsilon_\theta(x_t,t)\rVert^2\). Sample: \(T\) reverse steps (or fewer with a faster sampler, later papers).
> **Formula.** \(x_{t-1}\) from \(\varepsilon_\theta\) via the standard DDPM mean; cartoon: subtract a scaled \(\varepsilon_\theta\) and add a little noise (except \(t=1\)).
> **Tradeoffs.** + MSE is easier than GAN min-max. − Many steps at sample time; quality vs speed; classifier-free guidance is next note.
>
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

Training is ordinary regression. Sample \(t\) uniformly, form \(x_t\) with the one-liner from **12.1**, predict \(\varepsilon\), take MSE. No adversary.

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

The oracle is a teaching crutch. A trained \(\boldsymbol{\varepsilon}_\theta\) is what replaces the known \(\boldsymbol{\varepsilon}\) (and therefore the known \(x_0\)) at sample time.

---

## 3. Sampling cost

You pay \(T\) network calls (or fewer with DDIM / distilled samplers). That is the trade: stable regression training, slow ancestral sampling. GANs (Week 11) sample in one forward pass and fight mode collapse instead.

For a project, report the sampler (\(T\), DDPM vs DDIM) next to the metric. Changing \(T\) at test time is part of the method.

---

## 4. Teaching this note

About **35 minutes** at the board, then **~6 minutes** of video.

- **0–10 min.** MSE on \(\varepsilon\). Same \(x_t\) formula as **12.1**.
- **10–22 min.** Write one reverse-step mean. Circle the \(\varepsilon_\theta\) term.
- **22–33 min.** Worked scalar reverse step, then the Lab 12 oracle story.
- **Then** play Umar Jamil **13:00–16:36** (training loop, then sampling loop). Pause when he draws one denoising step.

---

## 5. Worked example

Reuse \(x_0=1.0\), \(\bar{\alpha}_t=0.64\), \(\varepsilon=2.0\), so \(x_t=2.0\) as in note **12.1**. Take \(\alpha_t=0.64\) for a single-step cartoon (so \(\sqrt{\alpha_t}=0.8\), \(1-\alpha_t=0.36\), \(\sqrt{1-\bar{\alpha}_t}=0.6\)).

Suppose \(\varepsilon_\theta=\varepsilon=2.0\) exactly, and drop \(\sigma_t z\) for the mean:

\[
x_{t-1}
=
\frac{1}{0.8}
\left(
2.0
-
\frac{0.36}{0.6}\cdot 2.0
\right)
=
1.25\bigl(2.0-1.2\bigr)
=
1.25\times 0.8
=
1.0.
\]

The reverse mean lands on \(x_0\). That is the oracle: if you predict the true noise, one algebraic step peels it off (here \(\alpha_t=\bar{\alpha}_t\), a first-step special case). At a generic \(t\) you do not jump all the way to \(x_0\); you move **closer**. Lab 12 checks \(\|x_t-x_0\|\) vs \(\|\hat{x}-x_0\|\) at \(t=20\) and wants the second smaller.

If \(\varepsilon_\theta=0\) (the net refuses to denoise), the subtracted term vanishes and you mostly rescale \(x_t\), which is not a sample from the data.

![Oracle reverse mean: \(2.0\) peels back to \(1.0\)](files/data-643/graphics/12.2-diffusion-reverse/reverse-mean.png)

CS231N L14: sampling is an **iterative** procedure. You pay \(T\) network calls (or fewer with DDIM). A GAN still samples in one pass and fights collapse instead.

---

## 6. Where students get stuck

- Training a U-Net in Lab 12. The lab uses the **true** posterior mean because you know \(x_0\).
- Omitting \(t\) as an input to \(\varepsilon_\theta\). The same \(x_t\) is a different problem at \(t=10\) and at \(t=900\).
- Forgetting \(\sigma_t z\) on the way down and then wondering why every sample looks identical.

---

## 7. Video

Watch [Umar Jamil, How diffusion models work](https://www.youtube.com/watch?v=I1sPXkm2NH4), **13:00–16:36**.

Pause on the training objective (predict the noise) and on the sampling loop (many reverse steps). Same URL as note **12.1**; do not replay 7:35–13:00 unless needed.

---

## 8. Practice

1. If \(\boldsymbol{\varepsilon}_\theta=\boldsymbol{\varepsilon}\) exactly, what should happen to \(\|\boldsymbol{x}_{t-1}-\boldsymbol{x}_0\|\) relative to \(\|\boldsymbol{x}_t-\boldsymbol{x}_0\|\), in expectation, for mid-range \(t\)?

2. Why add \(\sigma_t\boldsymbol{z}\) on the way down instead of always taking the mean?

3. You may not train a score network in Lab 12. What replaces \(\boldsymbol{\varepsilon}_\theta\) for that one reverse step?

4. \(x_t=3\), \(\alpha_t=0.25\), \(\bar{\alpha}_t=0.25\), \(\varepsilon_\theta=2\), no extra noise. Compute the reverse mean. (\(\sqrt{\alpha_t}=0.5\), \(\sqrt{1-\bar{\alpha}_t}=\sqrt{0.75}\approx 0.866\), \(1-\alpha_t=0.75\).)

5. Training samples \(t\) uniformly from \(1\ldots T\) and one \(\varepsilon\). Why is that enough, instead of a full reverse chain inside the loss?
