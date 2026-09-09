## 1. Line search

Almost every method in this note is

\[
\boldsymbol{\theta}^{(k+1)} = \boldsymbol{\theta}^{(k)} + \alpha^{(k)}\mathbf{s}^{(k)}.
\]

1. Pick a **direction** \(\mathbf{s}^{(k)}\).
2. Pick a **step** \(\alpha^{(k)}\) (learning rate) so that \(J\) decreases along that ray.
3. Take the step.

A direction is a **descent** direction when \(\mathbf{s}^\top\nabla J < 0\). Steepest descent uses \(\mathbf{s}=-\nabla J\).

---

## 2. Why steepest descent zigzags

On a quadratic \(J(\boldsymbol{\theta})=\tfrac12\boldsymbol{\theta}^\top\mathbf{Q}\boldsymbol{\theta}\) with \(\mathbf{Q}\) SPD, the contours are ellipses. The axis ratio is the **condition number** of \(\mathbf{Q}\) (largest over smallest eigenvalue). A long thin valley makes \(-\nabla J\) point into the walls. Exact line search still hops. That is not a bug in your code. It is the geometry.

---

## 3. Momentum

Remember the last step and refuse to turn on a dime:

\[
\boldsymbol{\theta}^{(k+1)}
=
\boldsymbol{\theta}^{(k)}
-\alpha^{(k)}\nabla J(\boldsymbol{\theta}^{(k)})
+\beta\Delta\boldsymbol{\theta}^{(k)},
\]

with \(\beta\in[0,1]\). A heavy ball in a valley: oscillations damp, progress along the floor improves. Noisy gradients (SGD) benefit because the memory averages them.

---

## 4. SGD and mini-batches

If \(J=\sum_i j_i\), **batch** GD uses \(\nabla J\) (all \(i\)). **SGD** uses one \(j_i\) (or a random subset). **Mini-batch** sits in between (Lab 2 uses size 20).

SGD is cheaper per step and noisier. The noise is sometimes useful: it keeps you from sitting in a sharp hole. The path in \(\boldsymbol{\theta}\)-space looks like a drunk walk toward the bowl, not a straight slide.

Lab 2 asks you to draw those three paths on linear-looking data and to say which one arrives.
