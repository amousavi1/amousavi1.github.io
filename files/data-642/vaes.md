These notes walk through the lecture slides. The original deck is unchanged; use **(slides)** on the course hub if you want that PDF.

Figures and notes follow Géron, *Hands-On Machine Learning*; Deisenroth, Faisal, and Ong, *Mathematics for Machine Learning*; and Theodoridis, *Machine Learning: A Bayesian and Optimization Perspective*.

## 1. Variational autoencoders

A **variational autoencoder** (VAE) is a **probabilistic** autoencoder: after training, the output is still partly random. A denoising autoencoder uses noise only while it trains.

It is also **generative**: you can draw new points that look as if they came from the training set.

![VAE: encoder to \(\boldsymbol{\mu},\boldsymbol{\sigma}\), sample a coding, decode](files/data-642/graphics/14.3-vaes/var_auto.png)

The figure builds the coding as \(\boldsymbol{\mu}\) plus Gaussian noise times \(\boldsymbol{\sigma}\). The random draw is an input, not a node you cannot differentiate.

---

## 2. Applications

| Use | Sketch |
| --- | ------ |
| Image generation | Art, avatars, synthetic frames. |
| Anomaly detection | Odd transactions, factory defects, unusual medical images. |
| Data compression | A short latent vector for storage or transmission. |
| Drug discovery | New molecules with target properties. |
| NLP | Coherent text: chat, translation, copy. |

---

## 3. The procedure

The encoder does not emit one coding. It emits a mean \(\boldsymbol{\mu}\) and a standard deviation \(\boldsymbol{\sigma}\). The coding is then drawn from a Gaussian with that mean and that width. The decoder reconstructs from the draw, as usual.

Training pushes the cloud of codings toward a Gaussian blob in **latent space**. After that, generation is cheap: sample a coding from the Gaussian, decode it.

![Input to encoder, Gaussian over \(z\), sample, decoder reconstruction](files/data-642/graphics/14.3-vaes/VAEs.png)

---

## 4. The cost function

Two pieces.

1. **Reconstruction loss.** Make \(\hat{\boldsymbol{x}}\) look like \(\boldsymbol{x}\) (cross-entropy, or the negative log-likelihood of \(\boldsymbol{x}\) under a Gaussian).
2. **Latent loss.** Make the coding distribution look like a simple Gaussian. That term is the KL divergence between the actual coding law and the target Gaussian.

---

## 5. ELBO

The training objective is the **variational lower bound**, or **evidence lower bound (ELBO)**. It is a tractable stand-in for the true log-likelihood of the data.

Write \(\boldsymbol{x}\) for the observation, \(\boldsymbol{z}\) for the latent, \(\boldsymbol{\theta}\) for decoder parameters, \(\boldsymbol{\phi}\) for encoder parameters. The ELBO is

\[
\mathcal{L}(\boldsymbol{\theta}, \boldsymbol{\phi}; \boldsymbol{x}) = \mathbb{E}_{q(\boldsymbol{z}|\boldsymbol{x})}[\log p(\boldsymbol{x}|\boldsymbol{z})] - D_{\text{KL}}\bigl(q(\boldsymbol{z}|\boldsymbol{x}) \parallel p(\boldsymbol{z})\bigr),
\]

where \(p(\boldsymbol{x}|\boldsymbol{z})\) is the likelihood, \(q(\boldsymbol{z}|\boldsymbol{x})\) is the approximate posterior, and \(p(\boldsymbol{z})\) is the prior.

Maximize it in both parameter blocks:

\[
\max_{\boldsymbol{\theta}, \boldsymbol{\phi}} \mathcal{L}(\boldsymbol{\theta}, \boldsymbol{\phi}; \boldsymbol{x}).
\]

SGD or Adam is the usual optimizer. Reconstruction plus a Gaussian prior on \(\boldsymbol{z}\) is what you are buying: a latent space you can sample.

---

## 6. Gaussian assumption

If the decoder likelihood is Gaussian, the reconstruction term is a weighted squared error plus constants:

\[
\mathbb{E}_{q(\boldsymbol{z}|\boldsymbol{x})}[\log p(\boldsymbol{x}|\boldsymbol{z})] = -\frac{1}{2} \sum_{i=1}^{N} \left( \frac{(x_i - \hat{x}_i)^2}{\sigma_i^2} + \log(\sigma_i^2) + \log(2\pi) \right).
\]

Here \(N\) is the dimension of \(\boldsymbol{x}\), and \(\sigma_i^2\) is the variance on coordinate \(i\).

The KL between a diagonal Gaussian posterior and a standard Gaussian prior is closed form:

\[
D_{\text{KL}}\bigl(q(\boldsymbol{z}|\boldsymbol{x}) \parallel p(\boldsymbol{z})\bigr) = -\frac{1}{2} \sum_{i=1}^{N} \bigl(1 + \log(\sigma_i^2) - \mu_i^2 - \sigma_i^2 \bigr),
\]

with \(\mu_i\) the mean of latent coordinate \(i\).

Put the two together:

\[
\begin{aligned}
\mathcal{L}(\boldsymbol{\theta}, \boldsymbol{\phi}; \boldsymbol{x})
&= -\frac{1}{2} \sum_{i=1}^{N} \left( \frac{(x_i - \hat{x}_i)^2}{\sigma_i^2} + \log(\sigma_i^2) + \log(2\pi) \right) \\
&\quad -\frac{1}{2} \sum_{i=1}^{N} \bigl(1 + \log(\sigma_i^2) - \mu_i^2 - \sigma_i^2 \bigr).
\end{aligned}
\]

That is the ELBO when both the approximate posterior and the prior are Gaussian.

---

## Practice

1. What problem does the reparameterization trick solve?

2. Name the two terms in the VAE cost (the ELBO).

3. After training, how do you generate a new sample without feeding in a real \(\boldsymbol{x}\)?
