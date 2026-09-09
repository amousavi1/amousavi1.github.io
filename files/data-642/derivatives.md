## 1. A derivative is a slope

Take a smooth map \(J:\mathbb{R}\to\mathbb{R}\). A small step \(\varepsilon_x\) in the input makes a small step \(\varepsilon_y\) in the output. Near a point \(p\), if \(J\) has no corners,

\[
\varepsilon_y \approx a\,\varepsilon_x.
\]

The number \(a = J'(p)\) is the **derivative** at \(p\).

- \(a<0\): a small increase in \(x\) **decreases** \(J\).
- \(a>0\): a small increase in \(x\) **increases** \(J\).
- \(|a|\) is how fast that happens.

To **minimize** \(J\), walk against the sign of \(a\). That one sentence is gradient descent in one dimension.

---

## 2. Continuity is not enough

Continuity says a small input change cannot jump the output. Smoothness says the graph has no kinks, so a linear approximation exists. Optimization algorithms in this course assume at least that much. ReLU networks are allowed later; they are smooth almost everywhere. You still write a gradient.

---

## 3. Higher dimensions: the gradient

A function of two scalars, \(J(x,y)=z\), is a surface. The analogue of \(a\) is the **gradient** \(\nabla J\): a vector of partial derivatives. It points to the direction of **steepest increase**. Descent uses \(-\nabla J\).

Week 1 note **1.4** writes the gradient and the Hessian in the \(\boldsymbol{\theta}\) notation of the rest of the course. Week 2 uses both.
