## 1. Newton

Approximate \(J\) by a quadratic at the current point \(\boldsymbol{\theta}^{(k)}\):

\[
J(\boldsymbol{\theta}^{(k)}+\boldsymbol{\delta})
\approx
J(\boldsymbol{\theta}^{(k)})
+\boldsymbol{\delta}^\top\nabla J(\boldsymbol{\theta}^{(k)})
+\tfrac12\boldsymbol{\delta}^\top H(\boldsymbol{\theta}^{(k)})\boldsymbol{\delta},
\]

where \(H=\nabla^2 J\). Minimize that quadratic: solve

\[
H(\boldsymbol{\theta}^{(k)})\boldsymbol{\delta} = -\nabla J(\boldsymbol{\theta}^{(k)}),
\]

then \(\boldsymbol{\theta}^{(k+1)}=\boldsymbol{\theta}^{(k)}+\boldsymbol{\delta}\). On a convex quadratic, **one** Newton step is exact. That is the point of Lab 2, exercise 3: a badly scaled bowl that GD crawls and Newton finishes.

---

## 2. When Newton breaks

If \(H\) is not positive definite, the quadratic is not a bowl and the step can go uphill or blow up. A cheap fix is to solve \((H+\lambda I)\boldsymbol{\delta}=-\nabla J\) (**Levenberg–Marquardt**). Large \(\lambda\) looks like gradient descent. Small \(\lambda\) looks like Newton.

Analytical second derivatives are often unpleasant. Finite differences are possible and do not guarantee an SPD \(H\).

---

## 3. Quasi-Newton and BFGS

Do not form \(H\). Keep a symmetric positive-definite **stand-in** \(H_*\) for \(H^{-1}\), update it from the observed \(\Delta\boldsymbol{\theta}\) and \(\Delta(\nabla J)\), and set

\[
\boldsymbol{\delta}^{(k)} = -H_*(\boldsymbol{\theta}^{(k)})\nabla J(\boldsymbol{\theta}^{(k)}),
\]

then line-search. **BFGS** is the update you should be able to name. Rank-two, stays SPD, no explicit Hessian. Faster and more stable than raw Newton on many medium-scale problems; still heavier than SGD on a million-example net.

Module 6 will come back to first-order methods (Adam, RMSProp). The idea is the same: better than raw \(-\nabla J\), cheaper than \(H^{-1}\).
