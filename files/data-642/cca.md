These notes walk through the lecture slides. The original deck is unchanged; use **(slides)** on the course hub if you want that PDF.

Figures and notes follow Deisenroth, Faisal, and Ong, *Mathematics for Machine Learning*; Theodoridis; and Géron.

## 1. Canonical correlation analysis (CCA)

PCA reduces dimension for **one** data set. Often you have **several** related sets from different sources.

**Canonical correlation analysis (CCA)** processes **two** sets together. The correlation of two random vectors depends on the coordinate system you write them in.

CCA looks for a pair of **linear** maps, one per set, so that the transformed variables are **maximally correlated**.

Two objects to keep straight:

- **Canonical variables** (variates)
- **Canonical correlation**

---

## 2. The math

Two random vectors \(\mathbf{x}\in\mathbb{R}^p\) and \(\mathbf{y}\in\mathbb{R}^q\), observations \(\boldsymbol{x}_n,\boldsymbol{y}_n\) for \(n=1,\dots,N\).

As in PCA, start with one pair of directions, \(\boldsymbol{u}_{x,1}\) and \(\boldsymbol{u}_{y,1}\), that maximize the correlation of the projections.

Equivalently, the constrained problem

\[
\begin{aligned}
& \underset{\boldsymbol{u}_x,\,\boldsymbol{u}_y}{\max}
&& \boldsymbol{u}_x^{\top}\hat{\boldsymbol{\Sigma}}_{x,y}\boldsymbol{u}_y\\
& \text{subject to}
&& \boldsymbol{u}_x^{\top}\hat{\boldsymbol{\Sigma}}_{x,x}\boldsymbol{u}_x = 1,\quad \boldsymbol{u}_y^{\top}\hat{\boldsymbol{\Sigma}}_{y,y}\boldsymbol{u}_y = 1,
\end{aligned}
\]

where \(\boldsymbol{\Sigma}_{x,y}\) is the **cross-covariance**.

Compared with PCA: two directions, not one; the constraints use a **weighted \(\boldsymbol{\Sigma}\) norm**, not the Euclidean norm; the objective is **correlation of the two projections**, not variance of one.

Lagrangian:

\[
\mathcal{L}(\boldsymbol{u}_x,\boldsymbol{u}_y,\lambda_x,\lambda_y)
=
\boldsymbol{u}_x^{\top}\hat{\boldsymbol{\Sigma}}_{x,y}\boldsymbol{u}_y
-\tfrac{\lambda_x}{2}(\boldsymbol{u}_x^{\top}\hat{\boldsymbol{\Sigma}}_{x,x}\boldsymbol{u}_x-1)
-\tfrac{\lambda_y}{2}(\boldsymbol{u}_y^{\top}\hat{\boldsymbol{\Sigma}}_{y,y}\boldsymbol{u}_y-1).
\]

Gradients in \(\boldsymbol{u}_x\) and \(\boldsymbol{u}_y\) set to zero give \(\lambda_x=\lambda_y=\lambda\) and

\[
\hat{\boldsymbol{\Sigma}}_{x,y}\boldsymbol{u}_y = \lambda\hat{\boldsymbol{\Sigma}}_{x,x}\boldsymbol{u}_x,
\qquad
\hat{\boldsymbol{\Sigma}}_{y,x}\boldsymbol{u}_x = \lambda\hat{\boldsymbol{\Sigma}}_{y,y}\boldsymbol{u}_y.
\]

Solve the second for \(\boldsymbol{u}_y\) (assuming \(\hat{\boldsymbol{\Sigma}}_{y,y}\) invertible) and substitute:

\[
\hat{\boldsymbol{\Sigma}}_{x,y}\hat{\boldsymbol{\Sigma}}_{y,y}^{-1}\hat{\boldsymbol{\Sigma}}_{y,x}\boldsymbol{u}_x = \lambda^2\hat{\boldsymbol{\Sigma}}_{x,x}\boldsymbol{u}_x
\]

and

\[
\boldsymbol{u}_y = \frac{1}{\lambda}\hat{\boldsymbol{\Sigma}}_{y,y}^{-1}\hat{\boldsymbol{\Sigma}}_{y,x}\boldsymbol{u}_x.
\]

If \(\hat{\boldsymbol{\Sigma}}_{x,x}\) is invertible too, this is an ordinary eigenproblem:

\[
\bigl(\hat{\boldsymbol{\Sigma}}_{x,x}^{-1}\hat{\boldsymbol{\Sigma}}_{x,y}\hat{\boldsymbol{\Sigma}}_{y,y}^{-1}\hat{\boldsymbol{\Sigma}}_{y,x}\bigr)\boldsymbol{u}_x = \lambda^2\boldsymbol{u}_x.
\]

So \(\boldsymbol{u}_{x,1}\) is an eigenvector of that product. Take the eigenvector for the **largest** eigenvalue \(\lambda^2\) to maximize the correlation.

\(\boldsymbol{u}_{x,1}\) and \(\boldsymbol{u}_{y,1}\) are the **normalized canonical correlation basis vectors**. The eigenvalue \(\lambda^2\) is the **squared canonical correlation**. The projections \(\boldsymbol{u}_{x,1}^{\top}\mathbf{x}\) and \(\boldsymbol{u}_{y,1}^{\top}\mathbf{y}\) are the **canonical variates**.

---

## 3. What to read off in practice

Two questions after you fit CCA:

- **Canonical correlation.** How much is each canonical variable from set 1 correlated with its counterpart in set 2?
- **Canonical variates.** Which original variables does each variate represent?

---

## Practice

1. CCA needs two views of the same objects. Name a pair.

2. What is CCA maximizing that PCA is not, and what replaces the unit-Euclidean constraint?

3. After you compute \(\boldsymbol{u}_{x,1}\), how do you get \(\boldsymbol{u}_{y,1}\)?
