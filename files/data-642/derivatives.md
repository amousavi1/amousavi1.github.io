These notes walk through the lecture slides. The original deck is unchanged; use **(slides)** on the course hub if you want that PDF.

The figures follow Chollet, *Deep Learning with Python*, and Géron.

## 1. A derivative is a slope

Take a smooth map \(J(x)=y\) that sends a number to a number. You can draw it as a curve in the plane.

![A smooth scalar function](files/data-642/graphics/derivative-function.png)

Because \(J\) is **continuous**, a small change in \(x\) can only make a small change in \(y\). Increase \(x\) by a small \(\varepsilon_x\); \(y\) moves by a small \(\varepsilon_y\).

![A small step in \(x\) makes a small step in \(y\)](files/data-642/graphics/derivative-epsilon.png)

Because the curve has no kinks, when \(\varepsilon_x\) is small enough around a point \(p\) you may treat \(J\) as a line of slope \(a\):

\[
\varepsilon_y \approx a\,\varepsilon_x.
\]

The number \(a = J'(p)\) is the **derivative** at \(p\).

- \(a<0\): a small increase in \(x\) **decreases** \(J\).
- \(a>0\): a small increase in \(x\) **increases** \(J\).
- \(|a|\) (the **magnitude**) is how fast that happens.

![The derivative as the slope of the local line](files/data-642/graphics/derivative-slope.png)

To **minimize** \(J\), walk against the sign of \(a\). That one sentence is gradient descent in one dimension. Being able to differentiate is the main tool this course uses to find those \(x\).

---

## 2. Continuity is not enough

Continuity says a small input change cannot jump the output. Smoothness says the graph has no corners, so a linear approximation exists. The algorithms in Module 1 assume at least that much. ReLU networks are allowed later; they are smooth almost everywhere. You still write a gradient.

---

## 3. Higher dimensions: the gradient

A map from one scalar to one scalar is a curve. A map \(J(x,y)=z\) from a pair of scalars to a scalar is a **surface** in 3-space.

The analogue of \(a\) is the **gradient** \(\nabla J\): a vector of partial derivatives. It points to the direction of **steepest increase**. Descent uses \(-\nabla J\).

Week 1 note **1.4** writes the gradient and the Hessian in the \(\boldsymbol{\theta}\) notation of the rest of the course. Week 2 uses both.

---

## 4. Practice

1. At a point where \(J'(p)=0\), what does a small step in \(x\) do to \(J\), to first order? Why is that not enough to call \(p\) a minimum?

2. Why does a kink (a corner in the graph) break the “local line of slope \(a\)” story?

3. If \(\nabla J\) points uphill, what vector do you add to \(\boldsymbol{\theta}\) in a descent step, up to a step-size \(\alpha\)?
