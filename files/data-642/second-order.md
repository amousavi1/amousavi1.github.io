These notes walk through the lecture slides. The original deck is unchanged; use **(slides)** on the course hub if you want that PDF.

The notes follow Deisenroth, Faisal, and Ong, *Mathematics for Machine Learning*.

## 1. Newton’s method

Second-order methods replace \(J\) by a local quadratic that is easy to minimize. **Newton** uses the second-order Taylor expansion at the current point \(\boldsymbol{\theta}^{(k)}\):

\[
J(\boldsymbol{\theta})
\approx
J(\boldsymbol{\theta}^{(k)})
+\boldsymbol{\delta}^\top\nabla J(\boldsymbol{\theta}^{(k)})
+\tfrac12\boldsymbol{\delta}^\top H(\boldsymbol{\theta}^{(k)})\boldsymbol{\delta},
\]

where \(H(\boldsymbol{\theta}^{(k)})=\nabla^2 J(\boldsymbol{\theta}^{(k)})\) is the **Hessian** and \(\boldsymbol{\delta}=\boldsymbol{\theta}-\boldsymbol{\theta}^{(k)}\). Minimize that quadratic by solving the linear system

\[
H(\boldsymbol{\theta}^{(k)})\boldsymbol{\delta}=-\nabla J(\boldsymbol{\theta}^{(k)}),
\]

then \(\boldsymbol{\theta}^{(k+1)}=\boldsymbol{\theta}^{(k)}+\boldsymbol{\delta}\). On a convex quadratic, **one** Newton step is exact.

---

## 2. When Newton breaks

If \(H\) is not **positive definite**, the local quadratic is not a bowl. The step can go uphill or blow up.

A cheap fix is to solve \((H+\lambda I)\boldsymbol{\delta}=-\nabla J\) (**Levenberg–Marquardt**). Large \(\lambda\) looks like gradient descent. Small \(\lambda\) looks like Newton.

Analytical second derivatives are often unpleasant. Finite differences are possible and do not guarantee an SPD Hessian.

---

## 3. Quasi-Newton and BFGS

Do not form \(H\). Keep a symmetric positive-definite stand-in \(\mathbf{H}_*\) for \(H^{-1}\), and iterate:

1. Set \(\boldsymbol{\delta}^{(k)}=-\mathbf{H}_*(\boldsymbol{\theta}^{(k)})\nabla J(\boldsymbol{\theta}^{(k)})\).
2. Line-search along \(\boldsymbol{\delta}^{(k)}\) to get \(\boldsymbol{\theta}^{(k+1)}=\boldsymbol{\theta}^{(k)}+\alpha^{(k)}\boldsymbol{\delta}^{(k)}\).
3. Update \(\mathbf{H}_*^{(k)}\) to \(\mathbf{H}_*^{(k+1)}\).

**BFGS** (Broyden–Fletcher–Goldfarb–Shanno) is the update you should be able to name. Rank-two updates of the inverse-Hessian approximation, stays SPD, no explicit second derivatives. Often faster and more stable than raw Newton on medium-scale problems. Still heavier than SGD on a million-example net.

---

## 4. Practice

1. On a convex quadratic, why can one Newton step finish the job that steepest descent crawls?

2. What goes wrong if the Hessian is not positive definite, and what does Levenberg–Marquardt change in the linear system?

3. What does BFGS store and update instead of \(\nabla^2 J\), and why is that cheaper than Newton when analytical second derivatives are painful?
