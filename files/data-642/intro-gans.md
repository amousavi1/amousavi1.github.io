These notes walk through the lecture slides. The original deck is unchanged; use **(slides)** on the course hub if you want that PDF.

Figures and notes follow Géron, *Hands-On Machine Learning*; Deisenroth, Faisal, and Ong, *Mathematics for Machine Learning*; and Theodoridis, *Machine Learning: A Bayesian and Optimization Perspective*.

## 1. Generative adversarial networks

**Generative adversarial networks** (GANs) are from Goodfellow et al., 2014. The idea caught on immediately; stable training took years.

A GAN is two neural nets.

![Generator from noise; discriminator guesses fake versus real](files/data-642/graphics/15.1-intro-gans/GAN.png)

---

## 2. Applications

| Use | Sketch |
| --- | ------ |
| Image generation and editing | Faces, objects, landscapes; inpainting missing patches. |
| Data augmentation | Extra synthetic rows when labels are expensive. |
| Text-to-image | A sentence in, a matching scene out. |
| Style transfer | Copy the look of one image onto another. |
| Molecular generation | New drug-like or materials structures. |
| Anomaly detection | Train on normal data; flag points far from that law. |
| Domain adaptation | Map a source domain onto a target domain and keep the meaning. |

---

## 3. Generator

The **generator** takes a random draw (usually Gaussian) and emits a sample, often an image.

Treat that draw as a **latent coding**. Functionally this is the decoder of a VAE: Gaussian noise in, a new image out. The training rule is different.

Write \(\boldsymbol{z}\) for the noise and

\[
\boldsymbol{x} = G(\boldsymbol{z};\boldsymbol{\theta}_g)
\]

for a fake sample with the same dimension as a real observation \(\boldsymbol{x}_n\), \(n=1,\dots,N\). \(\boldsymbol{\theta}_g\) are the generator weights. Training aims to make the fakes statistically indistinguishable from the reals.

---

## 4. Discriminator

The **discriminator** sees either a fake from \(G\) or a real training image, and guesses which. It is a binary classifier. On input \(\boldsymbol{x}\) it returns

\[
y = D(\boldsymbol{x};\boldsymbol{\theta}_d),
\]

the probability that \(\boldsymbol{x}\) is real. Then \(1 - D(\boldsymbol{x};\boldsymbol{\theta}_d)\) is the probability it is fake. \(\boldsymbol{\theta}_d\) are the discriminator weights.

---

## 5. Training

Opposite goals. The discriminator wants to tell fakes from reals. The generator wants fakes that fool the discriminator. You cannot train this as one ordinary net. Each iteration has two phases.

1. **Train the discriminator.** A batch of reals, plus as many fakes from the current generator. Labels: 0 fake, 1 real. One binary-cross-entropy step. Backprop updates **only** \(\boldsymbol{\theta}_d\).
2. **Train the generator.** A fresh batch of fakes. No reals. Every label is 1 (real): you want the discriminator to be *wrong*. Freeze \(\boldsymbol{\theta}_d\); backprop updates **only** \(\boldsymbol{\theta}_g\).

---

## 6. The cost function

A two-player min-max game:

\[
\min_{\boldsymbol{\theta}_g}\max_{\boldsymbol{\theta}_d} J(\boldsymbol{\theta}_g,\boldsymbol{\theta}_d),
\]

\[
J(\boldsymbol{\theta}_g,\boldsymbol{\theta}_d)
=
\mathbb{E}_{\boldsymbol{x}\sim p_r(\boldsymbol{x})}\bigl[ \ln D(\boldsymbol{x};\boldsymbol{\theta}_d) \bigr]
+
\mathbb{E}_{\boldsymbol{z}\sim p_{\boldsymbol{z}}(\boldsymbol{z})} \bigl[ \ln \bigl(1 - D(G(\boldsymbol{z};\boldsymbol{\theta}_g);\boldsymbol{\theta}_d)\bigr) \bigr].
\]

\(p_r(\boldsymbol{x})\) is the real-data law. With \(\boldsymbol{\theta}_g\) held fixed, the discriminator is trained so that \(D(\boldsymbol{x};\boldsymbol{\theta}_d)\) is large on reals and \(1 - D(G(\boldsymbol{z};\boldsymbol{\theta}_g);\boldsymbol{\theta}_d)\) is large on fakes.

---

## 7. Algorithm

Initialize \(\boldsymbol{\theta}_d^{(0)}\) and \(\boldsymbol{\theta}_g^{(0)}\). Minibatch size \(K\). Let \(m\) be the number of discriminator steps per generator step (\(m=1\) in the original paper).

While \(\boldsymbol{\theta}_d\) and \(\boldsymbol{\theta}_g\) have not converged:

- For \(t = 1,\dots,m\):
  - Sample \(\boldsymbol{z}^{(i)}\), \(i=1,\dots,K\), from \(p_{\boldsymbol{z}}(\boldsymbol{z})\).
  - Sample \(\boldsymbol{x}^{(i)}\), \(i=1,\dots,K\), from \(p_{r}(\boldsymbol{x})\).
  - Ascend on \(\boldsymbol{\theta}_d\) using

\[
\nabla_{\boldsymbol{\theta}_d} \left\{\frac{1}{K} \sum_{i=1}^K \bigl(\ln D(\boldsymbol{x}^{(i)};\boldsymbol{\theta}_d) + \ln\bigl(1 - D(G(\boldsymbol{z}^{(i)};\boldsymbol{\theta}_g);\boldsymbol{\theta}_d)\bigr)\bigr) \right\}.
\]

- Then sample a new \(\boldsymbol{z}^{(i)}\), \(i=1,\dots,K\), from \(p_{\boldsymbol{z}}(\boldsymbol{z})\) and **descend** on \(\boldsymbol{\theta}_g\) using

\[
\nabla_{\boldsymbol{\theta}_g} \left\{\frac{1}{K} \sum_{i=1}^K \ln\bigl(1 - D(G(\boldsymbol{z}^{(i)};\boldsymbol{\theta}_g);\boldsymbol{\theta}_d)\bigr) \right\}.
\]

---

## Practice

1. What two networks are playing the GAN game, and what does each want?

2. In the generator step, why are all labels set to 1 (real), and which weights stay frozen?

3. With \(\boldsymbol{\theta}_g\) held fixed, what is the discriminator maximizing on real \(\boldsymbol{x}\) and on fake \(G(\boldsymbol{z})\)?
