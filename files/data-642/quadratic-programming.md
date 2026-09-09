## 1. Quadratic cost, linear constraints

\[
\min_{\boldsymbol{\theta}\in\mathbb{R}^d}
\tfrac12\boldsymbol{\theta}^\top Q\boldsymbol{\theta}+\mathbf{c}^\top\boldsymbol{\theta}
\quad\text{subject to}\quad
A\boldsymbol{\theta}\le\mathbf{b},
\]

with \(Q\) symmetric **positive definite**. Then the objective is strictly convex, so a local min is the unique global min. Linear constraints keep the feasible set a polyhedron. Soft-margin SVM is exactly this shape.

Ridge regression without inequalities is the unconstrained special case \(A\) empty: \(\hat{\boldsymbol{\theta}}=-(Q)^{-1}\mathbf{c}\) if you write the quadratic that way.

---

## 2. Dual

Lagrangian

\[
\mathcal{L}(\boldsymbol{\theta};\boldsymbol{\lambda})
=
\tfrac12\boldsymbol{\theta}^\top Q\boldsymbol{\theta}+\mathbf{c}^\top\boldsymbol{\theta}+\boldsymbol{\lambda}^\top(A\boldsymbol{\theta}-\mathbf{b}).
\]

Stationarity: \(Q\boldsymbol{\theta}+\mathbf{c}+A^\top\boldsymbol{\lambda}=\mathbf{0}\), so \(\boldsymbol{\theta}=-Q^{-1}(\mathbf{c}+A^\top\boldsymbol{\lambda})\). Plug back in. The dual is a concave quadratic in \(\boldsymbol{\lambda}\ge\mathbf{0}\). You maximize it. Module 3 will do the same substitution for the SVM dual and then replace inner products by a kernel.

---

## 3. Why SVM is a QP

Primal sketch (soft margin):

\[
\min_{\boldsymbol{\theta},\,b,\,\boldsymbol{\xi}}
\;
\tfrac12\|\boldsymbol{\theta}\|^2
+C\sum_n\xi_n
\quad\text{s.t.}\quad
y_n(\mathbf{x}_n^\top\boldsymbol{\theta}+b)\ge 1-\xi_n,\;\xi_n\ge 0.
\]

Quadratic objective, linear inequalities. \(C\) trades margin size against slack. Week 5 writes this carefully. This week you only need to recognize the type: **QP, not LP**, because of \(\|\boldsymbol{\theta}\|^2\).
