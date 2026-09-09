These notes walk through the lecture slides. The original deck is unchanged; use **(slides)** on the course hub if you want that PDF.

The notes follow Deisenroth, Faisal, and Ong, *Mathematics for Machine Learning*.

## 1. Quadratic cost, linear constraints

A **quadratic program** keeps linear inequalities and lets the objective be quadratic. That is the next step past an LP: nonlinear models whose cost is a bowl, plus the same polyhedron as before.

This is also how **regularization** enters: a quadratic penalty on \(\boldsymbol{\theta}\) is still a QP when the constraints stay linear. Soft-margin **SVM** is the example this course cares about.

\[
\min_{\boldsymbol{\theta}\in\mathbb{R}^d}
\tfrac12\boldsymbol{\theta}^\top Q\boldsymbol{\theta}+\mathbf{c}^\top\boldsymbol{\theta}
\quad\text{subject to}\quad
A\boldsymbol{\theta}\le\mathbf{b},
\]

with \(A\in\mathbb{R}^{m\times d}\), \(\mathbf{b}\in\mathbb{R}^m\), \(\mathbf{c}\in\mathbb{R}^d\), and \(Q\in\mathbb{R}^{d\times d}\) symmetric **positive definite**. Then the objective is **convex**, so a local min is the unique global min. Still \(d\) variables and \(m\) linear constraints.

---

## 2. Dual

Lagrangian

\[
\mathcal{L}(\boldsymbol{\theta};\boldsymbol{\lambda})
=
\tfrac12\boldsymbol{\theta}^\top Q\boldsymbol{\theta}
+\mathbf{c}^\top\boldsymbol{\theta}
+\boldsymbol{\lambda}^\top(A\boldsymbol{\theta}-\mathbf{b}).
\]

Stationarity in \(\boldsymbol{\theta}\):

\[
Q\boldsymbol{\theta}+(\mathbf{c}+A^\top\boldsymbol{\lambda})=\mathbf{0}.
\]

If \(Q\) is invertible,

\[
\boldsymbol{\theta}=-Q^{-1}(\mathbf{c}+A^\top\boldsymbol{\lambda}).
\]

Substitute back. The dual Lagrangian is the concave quadratic

\[
D(\boldsymbol{\lambda})
=
-\tfrac12(\mathbf{c}+A^\top\boldsymbol{\lambda})^\top Q^{-1}(\mathbf{c}+A^\top\boldsymbol{\lambda})
-\boldsymbol{\lambda}^\top\mathbf{b}.
\]

The dual problem is therefore

\[
\max_{\boldsymbol{\lambda}\in\mathbb{R}^m}
-\tfrac12(\mathbf{c}+A^\top\boldsymbol{\lambda})^\top Q^{-1}(\mathbf{c}+A^\top\boldsymbol{\lambda})
-\boldsymbol{\lambda}^\top\mathbf{b}
\quad\text{subject to}\quad
\boldsymbol{\lambda}\ge\mathbf{0}.
\]

Week 5 does the same substitution for the SVM dual, then replaces inner products by a kernel.

---

## 3. Why SVM is a QP

Soft-margin SVM:

\[
\begin{aligned}
\min_{\boldsymbol{\theta}\in\mathbb{R}^l}
&\quad
\tfrac12\|\boldsymbol{\theta}\|^2
+C\sum_{n=1}^N\xi_n
\\
\text{subject to}
&\quad
y_n(\boldsymbol{x}_n^\top\boldsymbol{\theta}+b)\ge 1-\xi_n,
\quad
\xi_n\ge 0.
\end{aligned}
\]

- \(\boldsymbol{\theta}\): hyperplane weights.
- \(C\): trade-off between margin size and slack.
- \(\xi_n\): slack; a point may sit on the wrong side of the margin, at a linear cost.

Quadratic objective, linear inequalities: a **QP**, not an LP, because of \(\|\boldsymbol{\theta}\|^2\).

---

## 4. Practice

1. Why is a soft-margin SVM a quadratic program?

2. What does \(Q\) positive definite buy you that a general quadratic objective does not?

3. After \(\boldsymbol{\theta}=-Q^{-1}(\mathbf{c}+A^\top\boldsymbol{\lambda})\), what variables does the dual still optimize, and what constraint remains on them?
