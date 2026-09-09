## 1. Linear cost, linear inequalities

\[
\min_{\boldsymbol{\theta}\in\mathbb{R}^d} \mathbf{c}^\top\boldsymbol{\theta}
\quad\text{subject to}\quad
A\boldsymbol{\theta}\le\mathbf{b}.
\]

\(d\) variables, \(m\) constraints. Feasible set: a polyhedron. Level sets of \(\mathbf{c}^\top\boldsymbol{\theta}\): parallel hyperplanes. The min, if it exists, is at a vertex (or on a face). That is why simplex walks vertices and why interior-point methods hug the interior of the same polyhedron.

Feature selection and some ranking problems can be written this way. This course uses LP as the **simplest constrained** problem whose dual you can write by hand.

---

## 2. Dual of an LP

Lagrangian \(\mathcal{L}(\boldsymbol{\theta},\boldsymbol{\lambda})=\mathbf{c}^\top\boldsymbol{\theta}+\boldsymbol{\lambda}^\top(A\boldsymbol{\theta}-\mathbf{b})\) with \(\boldsymbol{\lambda}\ge\mathbf{0}\). Stationarity in \(\boldsymbol{\theta}\) forces

\[
\mathbf{c}+A^\top\boldsymbol{\lambda}=\mathbf{0}.
\]

The dual is then itself an LP,

\[
\max_{\boldsymbol{\lambda}\ge\mathbf{0}}\; -\mathbf{b}^\top\boldsymbol{\lambda}
\quad\text{subject to}\quad
\mathbf{c}+A^\top\boldsymbol{\lambda}=\mathbf{0}.
\]

The dual has \(m\) variables. If you have few variables and many constraints, solve the primal. The other way around, solve the dual. Same optimal value (when the LP is feasible and bounded).

Module 1 extra-credit homework asks you to do a tiny LP with KKT. That is this note, not a new topic.
