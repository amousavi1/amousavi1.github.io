These notes walk through the lecture slides. The original deck is unchanged; use **(slides)** on the course hub if you want that PDF.

The figures follow Deisenroth, Faisal, and Ong, *Mathematics for Machine Learning*.

## 1. Linear cost, linear inequalities

A **linear program** is the special case where \(J\) and the constraints are linear. In machine learning that is how you optimize a linear model under linear limits, and how you write some feature-selection and dimension-reduction tasks so a solver can hit the feasible set.

Level sets of a linear cost are parallel hyperplanes. Inequality constraints are half-spaces. The feasible set is a polyhedron (shaded). The min, if it exists, sits at a vertex or on a face.

![Linear program: level curves and inequality half-spaces](files/data-642/graphics/3.2-linear-programming/fig.png)

---

## 2. The primal

\[
\min_{\boldsymbol{\theta}\in\mathbb{R}^d}
\mathbf{c}^\top\boldsymbol{\theta}
\quad\text{subject to}\quad
A\boldsymbol{\theta}\le\mathbf{b},
\]

with \(A\in\mathbb{R}^{m\times d}\) and \(\mathbf{b}\in\mathbb{R}^m\). That is \(d\) variables and \(m\) linear constraints.

---

## 3. Dual of an LP

Lagrangian, with \(\boldsymbol{\lambda}\ge\mathbf{0}\),

\[
\mathcal{L}(\boldsymbol{\theta},\boldsymbol{\lambda})
=
\mathbf{c}^\top\boldsymbol{\theta}
+\boldsymbol{\lambda}^\top(A\boldsymbol{\theta}-\mathbf{b}).
\]

Collect terms in \(\boldsymbol{\theta}\):

\[
\mathcal{L}(\boldsymbol{\theta},\boldsymbol{\lambda})
=
\bigl(\mathbf{c}+A^\top\boldsymbol{\lambda}\bigr)^\top\boldsymbol{\theta}
-\boldsymbol{\lambda}^\top\mathbf{b}.
\]

Stationarity in \(\boldsymbol{\theta}\) forces

\[
\mathbf{c}+A^\top\boldsymbol{\lambda}=\mathbf{0}.
\]

Then \(D(\boldsymbol{\lambda})=-\boldsymbol{\lambda}^\top\mathbf{b}\), and the dual is itself an LP with \(m\) variables:

\[
\max_{\boldsymbol{\lambda}\in\mathbb{R}^m}
-\mathbf{b}^\top\boldsymbol{\lambda}
\quad\text{subject to}\quad
\mathbf{c}+A^\top\boldsymbol{\lambda}=\mathbf{0},
\quad
\boldsymbol{\lambda}\ge\mathbf{0}.
\]

Solve the **primal** if \(d\) is small. Solve the **dual** if \(m\) is small. Same optimal value when the LP is feasible and bounded.

---

## 4. Practice

1. In the figure, why is the minimizer of a feasible bounded LP at a vertex (or on a face), not in the interior of the polyhedron?

2. After forming the Lagrangian, what equation knocks \(\boldsymbol{\theta}\) out and leaves a dual only in \(\boldsymbol{\lambda}\)?

3. You have few variables and many constraints. Do you prefer the primal or the dual, and why?
