These notes walk through the lecture slides. The original deck is unchanged; use **(slides)** on the course hub if you want that PDF.

The figures follow Deisenroth, Faisal, and Ong, *Mathematics for Machine Learning*.

## 1. Training is optimization

Many algorithms in this course **optimize an objective** with respect to model parameters \(\boldsymbol{\theta}\) that control how well the model explains the data. Finding good parameters is an optimization problem. Three pictures you will see again:

- **Linear regression.** \(\boldsymbol{\theta}\) are weights. Maximize a likelihood, or minimize squared error.
- **Auto-encoders** (Module 6). \(\boldsymbol{\theta}\) are layer weights and biases. Minimize reconstruction error by repeated application of the chain rule.
- **Gaussian mixtures** (Module 5). \(\boldsymbol{\theta}\) are means, shapes, and mixture weights. Maximize the likelihood. Used in clustering and anomaly detection.

We write the objective as \(J(\boldsymbol{\theta}):\mathbb{R}^l\to\mathbb{R}\). Training is

\[
\hat{\boldsymbol{\theta}} \in \arg\min_{\boldsymbol{\theta}} J(\boldsymbol{\theta}).
\]

If you cannot write \(J\) and say what \(\boldsymbol{\theta}\) is, you do not yet have a learning problem.

---

## 2. Linear regression, written so the calculus is visible

Training pairs \((y_n, \boldsymbol{x}_n)\), \(n=1,\dots,N\). The prediction model is

\[
\hat y_n = \hat\theta_0 + \hat\theta_1 x_1 + \cdots + \hat\theta_l x_l = \hat{\boldsymbol{\theta}}^\top \boldsymbol{x}_n.
\]

Estimate \(\boldsymbol{\theta}\) by minimizing squared error

\[
J(\boldsymbol{\theta}) = \sum_{n=1}^N \bigl(y_n - \boldsymbol{\theta}^\top \boldsymbol{x}_n\bigr)^2.
\]

To minimize \(J\), solve \(\partial J / \partial \boldsymbol{\theta} = \mathbf{0}\). In matrix form that is the **normal equation**

\[
(\mathbf{X}^\top\mathbf{X})\hat{\boldsymbol{\theta}} = \mathbf{X}^\top\mathbf{y},
\qquad
\hat{\boldsymbol{\theta}} = (\mathbf{X}^\top\mathbf{X})^{-1}\mathbf{X}^\top\mathbf{y}
\]

when \(\mathbf{X}^\top\mathbf{X}\) is invertible. The inverse existing is a linear-algebra fact (full column rank). The \(\nabla J=\mathbf{0}\) step is calculus.

For two weights the surface \(J\) is a convex bowl. One local minimum, and it is global.

![Squared-error cost for two weights](files/data-642/graphics/linreg-cost.png)

Neural nets will not be this kind.

---

## 3. A map of the math

The next figure is the course’s reminder of which math shows up where. Module 1 lives in the vector-calculus and optimization blocks. Later modules reuse the same objects (gradients, Hessians, inner products, eigenvalues) on new models.

![Concepts used in machine learning](files/data-642/graphics/concepts-map.png)

To minimize a smooth \(J\) you need:

- a **gradient** (first derivatives) — when to stop, which way is downhill;
- a **Hessian** (second derivatives) — how curved the bowl is;
- later, **constraints** (Week 3) when \(\boldsymbol{\theta}\) is not free in \(\mathbb{R}^l\).

The next two notes are those derivatives. Week 2 turns them into algorithms.

---

## 4. Practice

1. Why is the normal equation a calculus problem, not a programming problem?

2. In the auto-encoder example, what is \(J\), and why does the chain rule appear?

3. If \(\mathbf{X}^\top\mathbf{X}\) is not invertible, what did the data do, and what do you change before you invert?
