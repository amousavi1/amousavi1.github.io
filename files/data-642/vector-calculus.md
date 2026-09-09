These notes walk through the lecture slides. The original deck is unchanged; use **(slides)** on the course hub if you want that PDF.

Notation follows Deisenroth, Faisal, and Ong, *Mathematics for Machine Learning*.

## 1. Gradient

The gradient is the derivative for several variables. Vary one coordinate of \(\boldsymbol{\theta}\), hold the others. Those **partial derivatives**, stacked, are the gradient.

For \(J(\boldsymbol{\theta}):\mathbb{R}^l\to\mathbb{R}\),

\[
\frac{\partial J}{\partial\theta_i},\qquad i=1,\dots,l.
\]

This course writes the collection as a **row**

\[
\nabla J
=
\Bigl[
\tfrac{\partial J}{\partial\theta_1}
\;
\tfrac{\partial J}{\partial\theta_2}
\;
\cdots
\;
\tfrac{\partial J}{\partial\theta_l}
\Bigr]
\in\mathbb{R}^{1\times l}.
\]

Some books write a column. Be consistent inside one derivation. Descent updates look like \(\boldsymbol{\theta}\leftarrow\boldsymbol{\theta}-\alpha(\nabla J)^\top\) if \(\nabla J\) is a row.

---

## 2. Chain rule

Let \(J:\mathbb{R}^2\to\mathbb{R}\) depend on \(\theta_1(t)\) and \(\theta_2(t)\). The derivative of \(J\) with respect to \(t\) is

\[
\frac{\mathrm{d}J}{\mathrm{d}t}
=
\Bigl[
\tfrac{\partial J}{\partial\theta_1}
\;
\tfrac{\partial J}{\partial\theta_2}
\Bigr]
\begin{bmatrix}
\partial\theta_1/\partial t \\
\partial\theta_2/\partial t
\end{bmatrix}
=
\frac{\partial J}{\partial\theta_1}\frac{\mathrm{d}\theta_1}{\mathrm{d}t}
+
\frac{\partial J}{\partial\theta_2}\frac{\mathrm{d}\theta_2}{\mathrm{d}t}.
\]

That is a gradient times a Jacobian. Back-propagation (Module 6) is this rule applied to a long composition. You do not need the neural-net story yet. You do need to be willing to write the product.

---

## 3. Hessian

If \(J(\theta_1,\theta_2)\) is twice differentiable, the **Hessian** is

\[
\nabla^2 J
=
\begin{bmatrix}
\partial^2 J/\partial\theta_1^2 & \partial^2 J/\partial\theta_1\partial\theta_2 \\
\partial^2 J/\partial\theta_2\partial\theta_1 & \partial^2 J/\partial\theta_2^2
\end{bmatrix}.
\]

The mixed partials match (Schwarz), so the Hessian is **symmetric**. It measures **curvature** of \(J\) around a point.

At a critical point \(\nabla J=\mathbf{0}\):

- \(\nabla^2 J\) positive definite \(\Rightarrow\) local **minimum**;
- negative definite \(\Rightarrow\) local **maximum**;
- indefinite \(\Rightarrow\) saddle.

Newton’s method (Week 2) solves a linear system with this matrix every step. Eigenvalues of \(\nabla^2 J\) are why a long thin valley makes steepest descent zigzag.

---

## 4. Practice

1. If a book prints \(\nabla J\) as a column, how does the descent update \(\boldsymbol{\theta}\leftarrow\boldsymbol{\theta}-\alpha\nabla J\) change compared with the row convention in these slides?

2. In the chain rule, which factor is “how \(J\) depends on \(\boldsymbol{\theta}\)” and which is “how \(\boldsymbol{\theta}\) depends on \(t\)”?

3. Why does a symmetric Hessian with one positive and one negative eigenvalue make a critical point a saddle, not a min?
