These notes walk through the lecture slides. The original deck is unchanged; use **(slides)** on the course hub if you want that PDF.

Figures and notes follow *Diversity in Independent Component and Vector Analyses* and Anderson, *Development of ICA and IVA Algorithms*.

## 1. Latent variable methods

For matrix factorization, write observations \(\mathbf{X}\in\mathbb{R}^{P\times V}\) as \(\mathbf{X}=\mathbf{B}\mathbf{C}\), with latent matrix \(\mathbf{C}\in\mathbb{R}^{M\times V}\).

![Blind source separation as a factorization](files/data-642/graphics/7.3-iva/BlindSourceSeparation.png)

A typical cost:

\[
\min_{\mathbf{B},\mathbf{C}}
\|\mathbf{X}-\mathbf{B}\mathbf{C}\|_p^2
+\lambda_1\sum_{m=1}^M h(\mathbf{b}_m)
+\lambda_2\sum_{v=1}^V g(\mathbf{c}_v).
\]

---

## 2. Independent component analysis (ICA)

ICA (1980s–90s) separates a multivariate signal into sources. Hérault and Jutten, 1985.

The **cocktail party** picture: several people talk at once; several microphones hear mixtures; recover each voice.

![Cocktail party and ICA](files/data-642/graphics/7.3-iva/ICA.png)

The model:

\[
\mathbf{x} = \mathbf{A}\mathbf{s},
\]

with observations \(\mathbf{x}\) and latent sources \(\mathbf{s}\) mixed by \(\mathbf{A}\).

![ICA mixing model](files/data-642/graphics/7.3-iva/ICA_matrix.png)

ICA can identify the sources up to **scale** and **permutation** if the sources are **statistically independent**.

---

## 3. The ICA objective

One ICA objective is **mutual information** among the estimated sources: the KL distance between the joint source density and the product of the marginals. With \(p_{\mathbf{s}}(\mathbf{W}\mathbf{x})=p_{\mathbf{x}}(\mathbf{x})\,|\det(\mathbf{W})|^{-1}\),

\[
\begin{aligned}
J_{\mathrm{ICA}}(\mathbf{W})
&=
\mathbb{E}\Biggl\{-\log\Biggl[\frac{p_{s_1}(y_1)\,p_{s_2}(y_2)\cdots p_{s_N}(y_N)}{p_{s_1 s_2\dots s_N}(y_1,y_2,\dots,y_N)}\Biggr]\Biggr\} \\
&=
\mathbb{E}\Biggl\{-\sum_{n=1}^N\log p_{s_n}(y_n)\Biggr\}
+\mathbb{E}\{\log p_{\mathbf{s}}(\mathbf{y})\} \\
&=
\sum_{n=1}^N H(y_n) - H(\mathbf{y}) \\
&=
\sum_{n=1}^N H(y_n) - \log|\det(\mathbf{W})| - H(\mathbf{x}),
\end{aligned}
\]

where \(H(y_n)\) and \(H(\mathbf{x})\) are the differential entropies of the source estimates and of the mixtures.

---

## 4. ICA algorithms

The **score function** can be estimated in three styles.

**Parametric.** **FastICA**, **EFICA**, **Infomax**. A fixed nonlinearity or a fixed source density. Cheap. Separation suffers when the true sources are far from that model.

**Nonparametric.** **RADICAL** uses entropy estimates. Parameter choices are awkward. Cost grows with sample size.

**Semi-parametric.** **ICA-EBM** and **ICA-EMK**. Flexible density matching via measuring functions from the maximum-entropy principle. Broad PDFs; sometimes expensive.

---

## 5. Independent vector analysis (IVA)

In practice you often have **several** data sets that depend on one another.

![IVA model across data sets](files/data-642/graphics/7.3-iva/IVA_model.png)

IVA uses a **source component vector (SCV)**: the \(n\)th source from each of the \(K\) data sets, stacked,

\[
\mathbf{s}_n = \bigl[s_n^{[1]},\dots,s_n^{[K]}\bigr]^{\top},
\]

a \(K\)-dimensional random vector.

**Goal.** Estimate \(K\) demixing matrices so that \(\mathbf{y}^{[k]}=\mathbf{W}^{[k]}\mathbf{x}^{[k]}\) and each SCV is **maximally independent** of the other SCVs.

The noiseless model, i.i.d. samples, is ICA repeated \(K\) times,

\[
\mathbf{x}^{[k]} = \mathbf{A}^{[k]}\mathbf{s}^{[k]},\qquad k=1,\dots,K,
\]

with invertible \(\mathbf{A}^{[k]}\in\mathbb{R}^{N\times N}\) and \(\mathbf{s}^{[k]}=[s_1^{[k]},\dots,s_N^{[k]}]^{\top}\). Within each \(\mathbf{s}^{[k]}\) the components are **independent**. Across data sets, **corresponding** components of \(\mathbf{s}^{[k]}\) may **depend**.

---

## 6. The IVA objective

Maximum likelihood again, but the parameter is a set of demixing matrices \(\mathbf{W}^{[1]},\ldots,\mathbf{W}^{[K]}\), packed as a three-way array \(\mathcal{W}\in\mathbb{R}^{N\times N\times K}\). Mutual information:

\[
J_{\mathrm{IVA}}(\mathcal{W})
=
\sum_{n=1}^N H(\mathbf{y}_n)
-\sum_{k=1}^K\log\bigl|\det(\mathbf{W}^{[k]})\bigr|
- H(\mathbf{x}^{[1]},\dots,\mathbf{x}^{[K]}),
\]

where \(H(\mathbf{y}_n)\) is the entropy of the \(n\)th SCV. The last term is constant.

---

## 7. Gradient and updates

Differentiating in each demixing matrix, as in ICA,

\[
\frac{\partial J_{\mathrm{IVA}}(\mathcal{W})}{\partial\mathbf{W}^{[k]}}
=
\mathbb{E}\bigl\{\boldsymbol{\phi}^{[k]}(\mathbf{x}^{[k]})^{\top}\bigr\}
-(\mathbf{W}^{[k]})^{-\top},
\]

with

\[
\boldsymbol{\phi}^{[k]}
=
-\Biggl[
\frac{\partial\log p_{s_1}(y_1)}{\partial y_1^{[k]}},
\dots,
\frac{\partial\log p_{s_N}(y_N)}{\partial y_N^{[k]}}
\Biggr]^{\top}.
\]

Each of the \(K\) matrices steps by

\[
(\mathbf{W}^{[k]})^{\mathrm{new}}
\leftarrow
(\mathbf{W}^{[k]})^{\mathrm{old}}
-\gamma\frac{\partial J_{\mathrm{IVA}}(\mathcal{W})}{\partial\mathbf{W}^{[k]}},
\]

with step size \(\gamma\).

---

## 8. IVA algorithms

Most IVA methods estimate the score **parametrically**.

| Method | Assumption |
| ------ | ---------- |
| **IVA-L** (Laplacian) | Higher-order statistics; Laplacian SCVs |
| **IVA-G** (Gaussian) | Linear dependence only, no HOS; Gaussian sources. Gradient simplifies; Hessian positive definite; Newton-type updates become practical |
| **IVA-GGD** / **IVA-A-GGD** | Second- and higher-order statistics; multivariate generalized Gaussian. Gaussian and Laplacian are special cases |
| **IVA-M-EMK** | Multivariate entropy maximization with kernels, when the matching multidimensional PDF matters. Can be cheaper as \(K\) and \(N\) grow |

---

## Practice

1. What extra assumption does IVA add on top of ICA?

2. ICA identifies sources only up to two ambiguities. What are they, and what statistical assumption buys uniqueness?

3. What is a **source component vector**, and what does IVA want of distinct SCVs?
