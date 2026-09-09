## 1. Extra conditions on \(\boldsymbol{\theta}\)

Unconstrained: \(\min_{\boldsymbol{\theta}} J(\boldsymbol{\theta})\). Constrained: the same min, but \(\boldsymbol{\theta}\) must sit in

\[
S=\{\boldsymbol{\theta}: g_i(\boldsymbol{\theta})=0\text{ or }g_i(\boldsymbol{\theta})\le 0\}.
\]

A box \(-1\le\theta_j\le 1\) is already a constraint set. The unconstrained min can fall **outside** the box. The constrained min is then on the boundary (the star, not the circle, on the usual contour cartoon).

Lab 3 is one equality: \(4\theta_1+2\theta_2=12\), quadratic \(J\). You will write a Lagrangian and set every partial to zero.

---

## 2. The Lagrangian

Turn the constrained problem into an unconstrained one in more variables. For inequalities \(g_i(\boldsymbol{\theta})\le 0\),

\[
\mathcal{L}(\boldsymbol{\theta},\boldsymbol{\lambda})
=
J(\boldsymbol{\theta})+\boldsymbol{\lambda}^\top\mathbf{g}(\boldsymbol{\theta})
\]

(sign conventions differ; stay consistent). \(\boldsymbol{\lambda}\) are **multipliers**. They are the prices of the constraints. If a constraint is slack, its multiplier is zero (KKT complementary slackness). If it is tight, the multiplier says how much \(J\) would improve if you relaxed it.

Why convert? Most algorithms, and most theory, are written for unconstrained maps. The Lagrangian is the conversion.

---

## 3. Primal and dual

The **primal** is the original problem in \(\boldsymbol{\theta}\). The **dual** is an optimization in \(\boldsymbol{\lambda}\), obtained by minimizing \(\mathcal{L}\) in \(\boldsymbol{\theta}\) first (when that min is easy). Weak duality: dual objective \(\le\) primal objective. Strong duality (typical for convex problems that satisfy a constraint qualification): the values match, and the multipliers at the saddle recover the primal \(\boldsymbol{\theta}\).

Week 3 notes **3.2** and **3.3** do this for an LP and a QP. The SVM dual in Module 3 is the same move with a quadratic \(J\).
