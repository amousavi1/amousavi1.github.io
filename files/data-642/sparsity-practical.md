These notes walk through the lecture slides. The original deck is unchanged; use **(slides)** on the course hub if you want that PDF.

The figures follow Deisenroth, Faisal, and Ong, *Mathematics for Machine Learning*, and Theodoridis, *Machine Learning: A Bayesian and Optimization Perspective*.

## 1. Paths under \(\ell_1\) and \(\ell_2\)

![Gradient paths with \(\ell_1\) and \(\ell_2\) penalties](files/data-642/graphics/4.4-sparsity-practical/Optimization.png)

**Left.** Contours of unregularized MSE plus an \(\ell_1\) penalty with \(\lambda=0.5\). The global min sits on the \(\theta_2=0\) axis. Gradient descent hits \(\theta_2=0\) first, then walks along the axis to the min.

**Right.** The same MSE plus an \(\ell_2\) penalty.

On the LASSO cost the path **bounces** around the min after it reaches an axis. Shrink the **learning rate** during training so the steps get smaller and the walk can converge.

---

## 2. Elastic Net

**Elastic Net** puts both penalties on a linear model: \(\ell_1\) (LASSO) and \(\ell_2\) (ridge).

- LASSO: **sparsity** and feature selection.
- Ridge: **multicollinearity** and more stable coefficients.

\[
J(\boldsymbol{\theta})
=
\frac{1}{2N}\|\mathbf{y}-\mathbf{X}\boldsymbol{\theta}\|_2^2
+\lambda_1\|\boldsymbol{\theta}\|_1
+\lambda_2\|\boldsymbol{\theta}\|_2^2.
\]

---

## 3. Advantages and disadvantages

| Advantages | Disadvantages |
| ---------- | ------------- |
| High-dimensional data with multicollinearity | Two penalty weights to tune |
| Feature selection with correlated predictors | Less intuitive than LASSO or ridge alone |
| A compromise between LASSO and ridge | Higher computational cost; less sparse than LASSO; sensitive to feature correlations |

---

## 4. Practice

1. Why does gradient descent on the LASSO cost bounce near an axis, and what do you change so it can settle?

2. What two penalties does Elastic Net mix, and what does each one contribute?

3. Name one advantage and one disadvantage of Elastic Net relative to LASSO.
