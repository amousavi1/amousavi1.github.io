These notes walk through the lecture slides. The original deck is unchanged; use **(slides)** on the course hub if you want that PDF.

The figures follow Deisenroth, Faisal, and Ong, *Mathematics for Machine Learning*, and Theodoridis, *Machine Learning: A Bayesian and Optimization Perspective*.

## 1. LASSO

Ridge’s penalty \(\lambda\sum_{j}\theta_j^2\) shrinks every coefficient toward zero but **never sets one exactly to zero**. That is not **sparsity**.

**LASSO** (least absolute shrinkage and selection operator) uses an \(\ell_1\) penalty instead:

\[
\sum_{n=1}^N \Bigl(y_n - \theta_0 - \sum_{j=1}^l \theta_j x_j \Bigr)^2 + \lambda \sum_{j=1}^l |\theta_j|,
\]

where \(\sum_{j=1}^l|\theta_j|\) is the \(\ell_1\)-norm of \((\theta_1,\dots,\theta_l)^\top\).

---

## 2. Geometry

![LASSO geometry: ellipse and diamond](files/data-642/graphics/4.3-lasso/lasso.png)

The \(\ell_1\) constraint is a **diamond**. As \(l\) grows, that diamond has more corners, so some coefficients land on an axis and become **zero**. LASSO therefore shrinks **and** does subset selection.

---

## 3. The objective

\[
J(\boldsymbol{\theta})
=
\frac{1}{2N}\|\mathbf{y}-\mathbf{X}\boldsymbol{\theta}\|_2^2
+\lambda\|\boldsymbol{\theta}\|_1.
\]

Squared error plus \(\ell_1\). The \(\ell_1\) term is **not differentiable** at \(\theta_j=0\), so ordinary gradients are not enough.

A **subgradient** generalizes the gradient. One subgradient of this \(J\) is

\[
g(\boldsymbol{\theta},\lambda)
=
-\frac{1}{N}\mathbf{X}^\top(\mathbf{y}-\mathbf{X}\boldsymbol{\theta})
+\lambda
\begin{bmatrix}
\mathrm{sgn}(\theta_1)\\
\mathrm{sgn}(\theta_2)\\
\vdots\\
\mathrm{sgn}(\theta_l)
\end{bmatrix},
\]

with

\[
\mathrm{sgn}(\theta_j)
=
\begin{cases}
-1 & \text{if }\theta_j<0,\\
\text{any value in }[-1,1] & \text{if }\theta_j=0,\\
1 & \text{if }\theta_j>0.
\end{cases}
\]

Subgradient descent (or a cousin) iterates until \(\boldsymbol{\theta}\) settles.

---

## 4. Comments

1. LASSO does **variance reduction**, gives accurate predictions, and is built for **variable selection**.
2. A little regularization is usually wise. Ridge is a safe default. Prefer LASSO if you believe **only a few** features matter.
3. If the columns of \(\mathbf{X}\) are **orthonormal**, LASSO has the closed form

\[
\hat{\theta}_j
=
\mathrm{sgn}(\hat{\theta}_{\mathrm{LS}})\bigl(|\hat{\theta}_{\mathrm{LS}}|-\lambda/2\bigr)_+.
\]

That is **soft thresholding**: \((\cdot)_+\) is the positive part (the argument if it is nonnegative, otherwise zero).
4. In the same orthonormal case, ridge is a uniform shrink: \(\hat{\boldsymbol{\theta}}_R=\frac{1}{1+\lambda}\hat{\boldsymbol{\theta}}_{\mathrm{LS}}\).

---

## 5. Computational complexity

A closed form exists only in special cases (orthonormal columns). Otherwise use (sub)gradient descent, especially when there are many features or too many rows for memory.

Soft thresholding is one solver. Another is to approximate \(\ell_1\) by a family of smooth quadratics,

\[
\lim_{\epsilon\to 0}\sum_{i=0}^l\sqrt{\theta_i^2+\epsilon}.
\]

---

## 6. Practice

1. What does soft thresholding do to a coordinate of the LASSO?

2. Why is the LASSO objective not differentiable at \(\theta_j=0\)?

3. When would you prefer LASSO to ridge?
