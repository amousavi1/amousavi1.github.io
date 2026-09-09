These notes walk through the lecture slides. The original deck is unchanged; use **(slides)** on the course hub if you want that PDF.

Figures and notes follow Deisenroth, Faisal, and Ong, *Mathematics for Machine Learning*; Theodoridis; and Géron.

## 1. PCA and singular value decomposition (SVD)

**Eigendecomposition.** From the covariance \(\mathbf{S}=\frac{1}{N}\sum_{n=1}^N\boldsymbol{x}_n\boldsymbol{x}_n^{\top}\), compute eigenvalues \(\lambda_i\) and eigenvectors \(\boldsymbol{u}_i\). The \(\boldsymbol{u}_i\) are the principal components. Each \(\lambda_i\) is the variance along that component.

**SVD.** Factor the centered data matrix: \(\mathbf{X}=\mathbf{U}\boldsymbol{\Sigma}\mathbf{V}^{\top}\). The **right singular vectors** \(\mathbf{V}\) are the principal components. The singular values on the diagonal of \(\boldsymbol{\Sigma}\) are the square roots of the eigenvalues of \(\mathbf{X}^{\top}\mathbf{X}\).

The two routes agree. That is the link between the maximum-variance view of PCA and the SVD of \(\mathbf{X}\).

---

## 2. PCA and low-rank approximations

Because \(\hat{\mathbf{X}}\) is the best rank-\(m\) approximation of \(\mathbf{X}\) in the **Frobenius** sense,

\[
\|\hat{\mathbf{X}} - \mathbf{X}\|_F^2 = \sum_{n=1}^N \|\hat{\boldsymbol{x}}_n - \boldsymbol{x}_n\|^2
\]

is minimum.

So PCA also **minimizes the sum of squared reconstruction errors**. The same components that maximize variance are the ones that keep as much of the original points as an \(m\)-dimensional picture can.

---

## 3. Latent variable perspective

So far PCA had no probabilistic model: maximum variance and projection only. A probabilistic model would:

- come with a **likelihood**, so noise in the observations is explicit;
- allow Bayesian model comparison via the **marginal likelihood**;
- treat PCA as a **generative** model (simulate new data);
- make connections to related algorithms straightforward;
- handle dimensions **missing at random** by Bayes;
- give a notion of how **novel** a new point is;
- extend cleanly, e.g. to a **mixture** of PCA models;
- recover the PCA of the earlier sections as a special case;
- allow a fully Bayesian treatment by integrating out parameters.

---

## 4. History of probabilistic PCA

A continuous latent \(\boldsymbol{z}\in\mathbb{R}^M\) lets you write PCA as a probabilistic latent-variable model. Tipping and Bishop (1999) called this **probabilistic PCA (PPCA)**. It addresses most of the list above. Ordinary PCA — maximize projected variance, or minimize reconstruction error — is **maximum likelihood** in the noise-free limit.

---

## 5. The PPCA model

Assume a continuous latent \(\boldsymbol{z}\in\mathbb{R}^M\) with standard-normal prior \(p(\boldsymbol{z})=\mathcal{N}(\mathbf{0},\mathbf{I})\), and a linear map to the observation \(\boldsymbol{x}\):

\[
\boldsymbol{x} = \boldsymbol{B}\boldsymbol{z} + \boldsymbol{\mu} + \epsilon \in \mathbb{R}^D,
\]

where \(\epsilon\sim\mathcal{N}(\mathbf{0},\sigma^2\mathbf{I})\) is Gaussian observation noise, \(\boldsymbol{B}\in\mathbb{R}^{D\times M}\), and \(\boldsymbol{\mu}\in\mathbb{R}^D\). The conditional is

\[
p(\boldsymbol{x}\mid\boldsymbol{z}; \boldsymbol{B}, \boldsymbol{\mu}, \sigma^2) = \mathcal{N}\bigl(\boldsymbol{x} \mid \boldsymbol{B}\boldsymbol{z} + \boldsymbol{\mu},\, \sigma^2\mathbf{I}\bigr).
\]

The generative process:

\[
\boldsymbol{z}_n \sim \mathcal{N}(\boldsymbol{z}\mid\mathbf{0},\mathbf{I})
\]

and

\[
\boldsymbol{x}_n \mid \boldsymbol{z}_n \sim \mathcal{N}(\boldsymbol{x}\mid \boldsymbol{B}\boldsymbol{z}_n + \boldsymbol{\mu},\, \sigma^2\mathbf{I}).
\]

To draw a typical point, use **ancestral sampling**: first \(\boldsymbol{z}_n\sim p(\boldsymbol{z})\), then \(\boldsymbol{x}_n\sim p(\boldsymbol{x}\mid\boldsymbol{z}_n; \boldsymbol{B},\boldsymbol{\mu},\sigma^2)\).

The joint is

\[
p(\boldsymbol{x},\boldsymbol{z}\mid \boldsymbol{B},\boldsymbol{\mu},\sigma^2) = p(\boldsymbol{x}\mid\boldsymbol{z},\boldsymbol{B},\boldsymbol{\mu},\sigma^2)\, p(\boldsymbol{z}).
\]

---

## 6. An illustration of PPCA

Blue dots: two-dimensional PCA latents for MNIST digits “8”. Query any \(\boldsymbol{z}_{*}\) in that plane and generate \(\tilde{\boldsymbol{x}}_{*}=\boldsymbol{B}\boldsymbol{z}_{*}\) (here \(\boldsymbol{\mu}=\mathbf{0}\) and identity covariance). The image looks like an “8”.

![PPCA latent space and generated eights](files/data-642/graphics/6.3-pca-special/PPCA.png)

Eight generated images sit with their latent coordinates. Where you query the latent plane changes shape, rotation, size.

---

## Practice

1. In the SVD view of PCA, which factor of \(\mathbf{X}=\mathbf{U}\boldsymbol{\Sigma}\mathbf{V}^{\top}\) holds the principal components?

2. Besides maximizing variance, what reconstruction quantity does a rank-\(m\) PCA minimize?

3. In PPCA, what extra random object appears that ordinary PCA never named, and what prior does it get?
