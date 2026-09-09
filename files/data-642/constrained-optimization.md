These notes walk through the lecture slides. The original deck is unchanged; use **(slides)** on the course hub if you want that PDF.

The figures follow Deisenroth, Faisal, and Ong, *Mathematics for Machine Learning*.

## 1. Extra conditions on \(\boldsymbol{\theta}\)

Unconstrained: \(\min_{\boldsymbol{\theta}} J(\boldsymbol{\theta})\) with \(J:\mathbb{R}^l\to\mathbb{R}\). Constrained: the same min, plus real-valued \(g_i\) that \(\boldsymbol{\theta}\) must obey,

\[
\min_{\boldsymbol{\theta}} J(\boldsymbol{\theta})
\quad\text{subject to}\quad
g_i(\boldsymbol{\theta})\le 0,\qquad i=1,\dots,m.
\]

The feasible set can mix equalities and inequalities:

\[
S=\{\boldsymbol{\theta}: g_i(\boldsymbol{\theta})=0\text{ or }g_i(\boldsymbol{\theta})\le 0\}.
\]

\(J\) and the \(g_i\) need not be convex. The LP and QP notes take the convex case.

A box \(-1\le\theta_j\le 1\) is already a constraint set. The unconstrained min can fall **outside** the box. The constrained min is then on the boundary (the star, not the circle).

![Unconstrained min versus a box constraint](files/data-642/graphics/3.1-constrained-optimization/constrained_optimization.png)

---

## 2. The primal

The **primal** is the original problem in \(\boldsymbol{\theta}\): minimize \(J\) subject to \(g_i(\boldsymbol{\theta})\le 0\). Its solution is the feasible \(\boldsymbol{\theta}\) you actually want, and the optimal \(J\). Direct search can be ugly once the constraints or \(J\) are messy.

Why turn it into an unconstrained problem in more variables?

| Reason | What you get |
| ------ | ------------ |
| Simplicity | Most solvers are written for unconstrained maps |
| Algorithms | You can use methods from Week 2 |
| Theory | Stationarity and convergence statements are cleaner |
| Hard problems | Nonlinear / nonconvex constraints become a Lagrangian you can differentiate |

---

## 3. The Lagrangian

For inequalities \(g_i(\boldsymbol{\theta})\le 0\),

\[
\mathcal{L}(\boldsymbol{\theta},\boldsymbol{\lambda})
=
J(\boldsymbol{\theta})-\sum_{i=1}^m\lambda_i g_i(\boldsymbol{\theta})
=
J(\boldsymbol{\theta})-\boldsymbol{\lambda}^\top\mathbf{g}(\boldsymbol{\theta}),
\]

with multipliers \(\boldsymbol{\lambda}\in\mathbb{R}^m\). (Sign conventions differ across books; stay consistent with the slide that introduced \(g_i\).)

Stationarity of the Lagrangian:

\[
\nabla_{\boldsymbol{\theta}}\mathcal{L}(\boldsymbol{\theta},\boldsymbol{\lambda})=\mathbf{0},
\qquad
\nabla_{\boldsymbol{\lambda}}\mathcal{L}(\boldsymbol{\theta},\boldsymbol{\lambda})=\mathbf{0}.
\]

A multiplier is the rate of change of \(J\) if you nudge the corresponding constraint. It is the **price** of that constraint.

---

## 4. The dual

Minimize \(\mathcal{L}\) in \(\boldsymbol{\theta}\) first (when that min is easy). What remains is a function of \(\boldsymbol{\lambda}\):

\[
D(\boldsymbol{\lambda})=\min_{\boldsymbol{\theta}}\mathcal{L}(\boldsymbol{\theta};\boldsymbol{\lambda}).
\]

The **Lagrange dual** is

\[
\max_{\boldsymbol{\lambda}\in\mathbb{R}^m} D(\boldsymbol{\lambda})
\quad\text{subject to}\quad
\boldsymbol{\lambda}\ge\mathbf{0}.
\]

| What the dual gives you | Why it matters |
| ----------------------- | -------------- |
| A **lower bound** on the primal min | You can score a candidate \(\boldsymbol{\theta}\) |
| Multipliers as sensitivities | How much \(J\) moves if a constraint moves |
| Sometimes a cheaper solve | Dual decomposition, cutting planes; \(m\) vs \(l\) can flip which problem is small |

---

## 5. SVM as a constrained problem

Soft-margin SVM is already in this shape:

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

![Maximum-margin hyperplane](files/data-642/graphics/3.1-constrained-optimization/svm.png)

Form the Lagrangian, pass to the dual, and the multipliers become the story of which points sit on the margin. Notes **3.2** and **3.3** write the same move for an LP and a QP. Week 5 returns to this primal.

---

## 6. Practice

1. What does a Lagrange multiplier charge you for?

2. In the box-constraint picture, why can the star (constrained min) differ from the circle (unconstrained min)?

3. Why might you solve the dual instead of the primal, even though the primal is the problem you stated?
