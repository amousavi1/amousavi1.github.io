These notes walk through the lecture slides. The original deck is unchanged; use **(slides)** on the course hub if you want that PDF.

The figures follow Deisenroth, Faisal, and Ong, *Mathematics for Machine Learning*, Theodoridis, and Géron, *Hands-On Machine Learning*.

## 1. Kernel ridge regression

Regularized empirical risk in an RKHS is

\[
\min_{f\in\mathbb{H}} J(f)
=
\sum_{n=1}^{N}\mathcal{L}\bigl(y_n,f(\mathbf{x}_n)\bigr)
+\lambda\,\Omega(\|f\|^2).
\]

The regularizer \(\Omega(\|f\|^2)\) is typically the squared RKHS norm \(\|f\|^2\).

---

## 2. Matrix notation

- \(\mathbf{y}\): targets.
- \(\mathbf{X}\): design matrix of inputs.
- \(\mathbf{K}\): **kernel matrix**.

The regularizer becomes \(\lambda\boldsymbol{\theta}^\top\mathbf{K}\boldsymbol{\theta}\), where \(\boldsymbol{\theta}\) holds the coefficients in the RKHS expansion of \(f\).

---

## 3. Gradient

The finite-dimensional problem is

\[
\min_{\boldsymbol{\theta}} J(\boldsymbol{\theta})
=
(\mathbf{y}-\mathbf{K}\boldsymbol{\theta})^\top(\mathbf{y}-\mathbf{K}\boldsymbol{\theta})
+\lambda\boldsymbol{\theta}^\top\mathbf{K}\boldsymbol{\theta}.
\]

Differentiate and set to zero:

\[
\frac{\partial J(\boldsymbol{\theta})}{\partial\boldsymbol{\theta}}
=
-2\mathbf{K}^\top(\mathbf{y}-\mathbf{K}\boldsymbol{\theta})
+2\lambda\mathbf{K}\boldsymbol{\theta}
=\mathbf{0}.
\]

---

## 4. Solving for \(\boldsymbol{\theta}\)

\[
\mathbf{K}^\top\mathbf{K}\boldsymbol{\theta}-\mathbf{K}^\top\mathbf{y}+\lambda\mathbf{K}\boldsymbol{\theta}=\mathbf{0},
\]

so

\[
(\mathbf{K}^\top\mathbf{K}+\lambda\mathbf{I})\boldsymbol{\theta}=\mathbf{K}^\top\mathbf{y},
\]

and

\[
\boldsymbol{\theta}=(\mathbf{K}^\top\mathbf{K}+\lambda\mathbf{I})^{-1}\mathbf{K}^\top\mathbf{y}.
\]

When \(\mathbf{K}\) can be cancelled, the usual kernel-ridge form is

\[
\boldsymbol{\theta}=(\mathbf{K}+\lambda\mathbf{I})^{-1}\mathbf{y}.
\]

---

## 5. Predictions

With that \(\boldsymbol{\theta}\),

\[
\hat{\mathbf{y}}=\mathbf{K}\boldsymbol{\theta}.
\]

The linear algebra is the same as ridge, but every inner product among features has been replaced by a kernel evaluation. The penalty still controls complexity and **overfitting**.

---

## 6. Practice

1. What does the kernel trick avoid computing?

2. Write the usual closed-form \(\boldsymbol{\theta}\) for kernel ridge in terms of \(\mathbf{K}\), \(\lambda\), and \(\mathbf{y}\).

3. Once you have \(\boldsymbol{\theta}\), how do you form the vector of training predictions?
