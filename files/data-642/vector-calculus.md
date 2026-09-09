## 1. Gradient

\(J(\boldsymbol{\theta}):\mathbb{R}^l\to\mathbb{R}\). Vary one coordinate, hold the others. Those partials, stacked, are the gradient. This course writes it as a **row**

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

If \(J=J(\theta_1(t),\theta_2(t))\), then

\[
\frac{\mathrm{d}J}{\mathrm{d}t}
=
\frac{\partial J}{\partial\theta_1}\frac{\mathrm{d}\theta_1}{\mathrm{d}t}
+
\frac{\partial J}{\partial\theta_2}\frac{\mathrm{d}\theta_2}{\mathrm{d}t}.
\]

That is a gradient times a Jacobian. Back-propagation (Module 6) is this rule applied to a long composition. You do not need the neural-net story yet. You do need to be willing to write the product.

---

## 3. Hessian

If \(J\) is twice differentiable,

\[
\nabla^2 J
=
\begin{bmatrix}
\partial^2 J/\partial\theta_1^2 & \partial^2 J/\partial\theta_1\partial\theta_2 \\
\partial^2 J/\partial\theta_2\partial\theta_1 & \partial^2 J/\partial\theta_2^2
\end{bmatrix}.
\]

The mixed partials match (Schwarz), so the Hessian is **symmetric**. It measures **curvature**.

At a critical point \(\nabla J=\mathbf{0}\):

- \(\nabla^2 J\) positive definite \(\Rightarrow\) local **minimum**;
- negative definite \(\Rightarrow\) local **maximum**;
- indefinite \(\Rightarrow\) saddle.

Newton’s method (week 2) solves a linear system with this matrix every step. Eigenvalues of \(\nabla^2 J\) are why a long thin valley makes steepest descent zigzag.
