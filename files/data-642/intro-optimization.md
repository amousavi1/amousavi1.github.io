## 1. The problem

Pick a set \(S\) (usually \(\mathbb{R}^l\)) and a cost \(J:S\to\mathbb{R}\). Solve

\[
J(\hat{\boldsymbol{\theta}}) = \min_{\boldsymbol{\theta}\in S} J(\boldsymbol{\theta}).
\]

Maximizing profit \(P\) is minimizing \(-P\). This course always writes a **min**.

Linear regression is the first example. Model \(y=\boldsymbol{\theta}^\top\mathbf{x}+\varepsilon\). Average squared error

\[
J(\boldsymbol{\theta})=\frac{1}{2m}\sum_{i=1}^m\bigl(\boldsymbol{\theta}^\top\mathbf{x}^{(i)}-y^{(i)}\bigr)^2.
\]

Each gradient step is “make the residuals smaller.”

---

## 2. Local versus global

A **local** minimum is lowest in a neighborhood. A **global** minimum is lowest on all of \(S\).

On a mountain trail, a valley is local. Sea level in the whole range is global.

If \(J\) is **convex**,

\[
J\bigl(t\boldsymbol{\theta}+(1-t)\boldsymbol{\beta}\bigr)
\le
t J(\boldsymbol{\theta})+(1-t)J(\boldsymbol{\beta}),
\]

every local min is global. That is the property that makes Module 1 feel safe.

| Convex costs (this course) | Not convex |
| -------------------------- | ---------- |
| Linear regression (MSE) | Deep nets |
| Logistic regression (log loss) | \(k\)-means |
| Soft-margin SVM | GMM likelihood |

---

## 3. First- and second-order tests

**First-order (necessary).** At a local min of a smooth unconstrained \(J\), \(\nabla J(\hat{\boldsymbol{\theta}})=\mathbf{0}\). The slope is flat.

**Second-order (sufficient).** If also \(\nabla^2 J(\hat{\boldsymbol{\theta}})\) is positive definite, you have a local min.

A zero gradient is not enough: a saddle is flat and is not a min. The Hessian tells the two cases apart. Week 2’s algorithms either follow \(-\nabla J\) or invert \(\nabla^2 J\).
