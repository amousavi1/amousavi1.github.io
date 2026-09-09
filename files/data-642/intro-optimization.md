These notes walk through the lecture slides. The original deck is unchanged; use **(slides)** on the course hub if you want that PDF.

The figures follow Deisenroth, Faisal, and Ong, *Mathematics for Machine Learning*.

## 1. Training is optimization

Training a model is finding a good \(\boldsymbol{\theta}\). **Good** is whatever the **cost** (objective) \(J\) says it is.

![Training as optimization](files/data-642/graphics/2.1-intro-optimization/flow_chart.png)

Write \(J(\boldsymbol{\theta}):S\to\mathbb{R}\) and solve

\[
J(\hat{\boldsymbol{\theta}}) = \min_{\boldsymbol{\theta}\in S} J(\boldsymbol{\theta}).
\]

Usually \(S=\mathbb{R}^l\). This course always **minimizes**. Maximizing profit \(P\) is minimizing \(-P\).

---

## 2. Linear regression

Model \(y=\boldsymbol{\theta}^\top\mathbf{x}+\varepsilon\). Fit by minimizing mean squared error on \(m\) training rows:

\[
J(\boldsymbol{\theta})
=
\frac{1}{2m}
\sum_{i=1}^{m}
\bigl(\boldsymbol{\theta}^\top\boldsymbol{x}^{(i)}-y^{(i)}\bigr)^2.
\]

Each step that lowers \(J\) shrinks residuals. Better \(\boldsymbol{\theta}\) on the training set is the hope that predictions on new \(\mathbf{x}\) improve too. That hope is generalization; the math this week is the min.

---

## 3. Local versus global

A **local** minimum is lowest in a neighborhood: some \(\varepsilon>0\) such that \(\|\boldsymbol{\theta}-\hat{\boldsymbol{\theta}}\|<\varepsilon\) implies \(J(\hat{\boldsymbol{\theta}})\le J(\boldsymbol{\theta})\). A **global** minimum is lowest on all of \(S\).

A valley on a hike is local. The lowest point in the whole range is global. Neural-net costs look like the landscape below. Many valleys. The one you land in need not be the lowest.

![A nonconvex cost landscape](files/data-642/graphics/2.1-intro-optimization/NN_cost_function.jpeg)

If \(J\) is **convex**,

\[
J\bigl(t\boldsymbol{\theta}+(1-t)\boldsymbol{\beta}\bigr)
\le
t J(\boldsymbol{\theta})+(1-t)J(\boldsymbol{\beta})
\]

for all \(\boldsymbol{\theta},\boldsymbol{\beta}\in S\) and all \(t\in(0,1)\), then every local min is global.

![Convex versus nonconvex](files/data-642/graphics/2.1-intro-optimization/convex_vs_non.png)

| Convex \(J\) (this course) | Not convex |
| -------------------------- | ---------- |
| Linear regression (MSE) | Deep nets |
| Logistic regression (log loss) | \(k\)-means |
| Soft-margin SVM | GMM likelihood |

Convex: gradient descent that reaches a local min has the global min. Nonconvex: you can stop in a valley that is not the bottom.

---

## 4. First- and second-order tests

**First-order (necessary).** At a local min of a smooth unconstrained \(J\), \(\nabla J(\hat{\boldsymbol{\theta}})=\mathbf{0}\). The slope is flat.

**Second-order (sufficient).** If that point also has Hessian \(\nabla^2 J(\hat{\boldsymbol{\theta}})\) **positive definite**, it is a local min.

A zero gradient is not enough: a saddle is flat and is not a min. Week 2’s algorithms either follow \(-\nabla J\) or invert \(\nabla^2 J\).

---

## 5. Practice

1. When does a local minimum fail to be global?

2. Why does this course write every learning problem as a **min**, even when the story is “maximize likelihood”?

3. At a point with \(\nabla J=\mathbf{0}\), what extra fact about \(\nabla^2 J\) lets you call it a local min rather than a saddle?
