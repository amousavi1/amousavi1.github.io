These notes walk through the lecture slides. The original deck is unchanged; use **(slides)** on the course hub if you want that PDF.

The figures follow Deisenroth, Faisal, and Ong, *Mathematics for Machine Learning*, and Theodoridis, *Machine Learning: A Bayesian and Optimization Perspective*.

## 1. Shrinkage methods

Among the \(\ell_p\)-norms with \(p\ge 1\), only \(\ell_1\) treats small coordinates with any respect. The others squeeze small values further and spend their attention on large ones.

**Regularization** is also there to make an estimator easier to **interpret**.

Least squares fits \(\theta_0,\theta_1,\dots,\theta_l\) by

\[
\sum_{n=1}^N \Bigl(y_n - \theta_0 - \sum_{j=1}^l \theta_j x_j \Bigr)^2.
\]

**Ridge** instead minimizes

\[
\sum_{n=1}^N \Bigl(y_n - \theta_0 - \sum_{j=1}^l \theta_j x_j \Bigr)^2 + \lambda \sum_{j=1}^l \theta_j^2,
\]

with hyper-parameter \(\lambda\ge 0\).

---

## 2. What \(\lambda\) does

The penalty \(\lambda\sum_{j=1}^l\theta_j^2\) forces the fit to keep the coefficients **small**. Add it only while **training**. Evaluate the trained model with the unregularized metric.

| \(\lambda\) | Effect |
| ----------- | ------ |
| \(\lambda=0\) | Ridge is ordinary least squares |
| \(\lambda\to\infty\) | Ridge coefficients approach **zero** (they do not hit zero for finite \(\lambda\)) |

The penalty hits \(\theta_1,\dots,\theta_l\), **not** \(\theta_0\). If every column of \(\mathbf{X}\in\mathbb{R}^{N\times l}\) is centered,

\[
\hat{\theta}_0 = \bar{y} = \sum_{n=1}^N y_n/N.
\]

---

## 3. Geometry

![Ridge geometry: ellipse and circle](files/data-642/graphics/4.2-ridge-regression/ridge.png)

For \(l=2\) the ridge constraint is a **circle**

\[
\theta_1^2 + \theta_2^2 \le t,
\]

where \(\sqrt{t}\) is the radius. The RSS contours are ellipses. The ridge estimate is the point where the ellipse and the circle **touch**.

- \(\lambda=0\): you only shrink the ellipse (inner ellipses have smaller RSS). Highly correlated features make that geometry unpleasant.
- Small \(\lambda\): more **variance**, less **bias**. Large \(\lambda\): some bias, less variance.

---

## 4. The closed form

\[
J(\boldsymbol{\theta}) = (\mathbf{y}-\mathbf{X}\boldsymbol{\theta})^\top(\mathbf{y}-\mathbf{X}\boldsymbol{\theta}) + \lambda\boldsymbol{\theta}^\top\boldsymbol{\theta}.
\]

Expand:

\[
J(\boldsymbol{\theta})
=
\mathbf{y}^\top\mathbf{y}
-\mathbf{y}^\top\mathbf{X}\boldsymbol{\theta}
-\boldsymbol{\theta}^\top\mathbf{X}^\top\mathbf{y}
+\boldsymbol{\theta}^\top\mathbf{X}^\top\mathbf{X}\boldsymbol{\theta}
+\lambda\boldsymbol{\theta}^\top\boldsymbol{\theta}.
\]

Set the derivative to zero:

\[
\frac{\partial J(\boldsymbol{\theta})}{\partial\boldsymbol{\theta}}
=
-2\mathbf{X}^\top\mathbf{y}
+2\mathbf{X}^\top\mathbf{X}\boldsymbol{\theta}
+2\lambda\boldsymbol{\theta}
=\mathbf{0}.
\]

Then

\[
(\mathbf{X}^\top\mathbf{X}+\lambda\mathbf{I})\boldsymbol{\theta}=\mathbf{X}^\top\mathbf{y},
\]

so

\[
\hat{\boldsymbol{\theta}}_R = (\mathbf{X}^\top\mathbf{X}+\lambda\mathbf{I})^{-1}\mathbf{X}^\top\mathbf{y}.
\]

---

## 5. Comments

1. Ridge gives accurate predictions and **reduced variance**.
2. Penalizing coefficient size **controls overfitting**: the model is less free to memorize noise.
3. Ridge is the usual tool for **multicollinearity**. Shrinking correlated coefficients stabilizes the estimates.

---

## 6. Computational complexity

You can use the closed form or **gradient descent**, as with linear regression. The closed form inverts an \(l\times l\) matrix (Cholesky and friends). That gets slow when the number of features is large. If there are too many features, or too many rows to fit in memory, use gradient descent.

---

## 7. Practice

1. Why can ridge shrink coefficients but not set them to zero?

2. What happens as \(\lambda\to\infty\), and which coefficient is never penalized?

3. Why does adding \(\lambda\mathbf{I}\) help when columns of \(\mathbf{X}\) are highly correlated?
