## 1. Training is optimization

A model is a function of **parameters** \(\boldsymbol{\theta}\). A **cost** \(J(\boldsymbol{\theta})\) says how well those parameters explain the data. Training is

\[
\hat{\boldsymbol{\theta}} \in \arg\min_{\boldsymbol{\theta}} J(\boldsymbol{\theta}).
\]

Three pictures you will see again:

- **Linear regression.** \(\boldsymbol{\theta}\) are weights. \(J\) is squared error (or a likelihood).
- **Auto-encoders** (Module 6). \(\boldsymbol{\theta}\) are layer weights. \(J\) is reconstruction error. The chain rule is how you differentiate through the stack.
- **Gaussian mixtures** (Module 5). \(\boldsymbol{\theta}\) are means, covariances, and mixture weights. \(J\) is a (negative) likelihood.

If you cannot write \(J\) and say what \(\boldsymbol{\theta}\) is, you do not yet have a learning problem.

---

## 2. Linear regression, written so the calculus is visible

Training pairs \((y_n, \mathbf{x}_n)\), \(n=1,\dots,N\). Prediction \(\hat y_n = \hat{\boldsymbol{\theta}}^\top \mathbf{x}_n\). Cost

\[
J(\boldsymbol{\theta}) = \sum_{n=1}^N \bigl(y_n - \boldsymbol{\theta}^\top \mathbf{x}_n\bigr)^2.
\]

Set \(\nabla J = \mathbf{0}\). In matrix form that is the **normal equation**

\[
(\mathbf{X}^\top\mathbf{X})\hat{\boldsymbol{\theta}} = \mathbf{X}^\top\mathbf{y},
\qquad
\hat{\boldsymbol{\theta}} = (\mathbf{X}^\top\mathbf{X})^{-1}\mathbf{X}^\top\mathbf{y}
\]

when \(\mathbf{X}^\top\mathbf{X}\) is invertible. The inverse existing is a linear-algebra fact (full column rank). The \(\nabla J=\mathbf{0}\) step is calculus.

For two weights the surface \(J\) is a convex bowl. One local minimum, and it is global. Neural nets will not be this kind.

---

## 3. What Module 1 still owes you

To minimize a smooth \(J\) you need:

- a **gradient** (first derivatives) — when to stop, which way is downhill;
- a **Hessian** (second derivatives) — how curved the bowl is;
- later, **constraints** (week 3) when \(\boldsymbol{\theta}\) is not free in \(\mathbb{R}^l\).

The next two notes are those derivatives. Week 2 turns them into algorithms.
