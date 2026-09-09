These notes walk through the lecture slides. The original deck is unchanged; use **(slides)** on the course hub if you want that PDF.

The figures follow Deisenroth, Faisal, and Ong, *Mathematics for Machine Learning*, Theodoridis, and Géron, *Hands-On Machine Learning*.

## 1. The main idea

Think of open and filled circles as houses in two villages. A road between them should be as wide as possible and should demolish as few houses as possible. No sensible engineer picks the dash-dotted path in the figure.

A classifier should sit between the dense regions of the two classes, in a sparse belt, leaving the **largest possible margin**. That is the usual requirement for **generalization**: small error on points that were not in the training set.

![Maximum-margin road between two villages](files/data-642/graphics/5.3-svms/svm.png)

---

## 2. Linearly separable classes

If the classes are linearly separable, infinitely many hyperplanes classify the training set with zero error. From that family one can always keep those that satisfy

\[
y_n(\boldsymbol{\theta}^\top\boldsymbol{x}_n+\theta_0)\ge 1,\qquad n=1,\dots,N.
\]

The SVM picks the one with smallest norm:

\[
\begin{aligned}
\underset{\boldsymbol{\theta}\in\mathbb{R}^{l}}{\text{minimize}}
&\quad
\frac{\|\boldsymbol{\theta}\|^2}{2}\\
\text{subject to}
&\quad
y_n(\boldsymbol{\theta}^\top\boldsymbol{x}_n+\theta_0)\ge 1,\quad n=1,\dots,N.
\end{aligned}
\]

\(\|\boldsymbol{\theta}\|\) is tied directly to the **margin**.

---

## 3. Primal, dual, and support vectors

The constrained problem is the **primal**. It has a **dual**. In general the dual only lower-bounds the primal; under convexity (and regularity of the constraints) the values match. SVM meets those conditions, so you may solve either.

The Lagrangian is

\[
\mathcal{L}(\boldsymbol{\theta},\theta_0,\boldsymbol{\lambda})
=
\frac12\|\boldsymbol{\theta}\|^2
-\sum_{n=1}^N\lambda_n\bigl(y_n(\boldsymbol{\theta}^\top\boldsymbol{x}_n+\theta_0)-1\bigr).
\]

KKT stationarity gives

\[
\nabla_{\boldsymbol{\theta}}\mathcal{L}=\mathbf{0}
\quad\Rightarrow\quad
\hat{\boldsymbol{\theta}}=\sum_{n=1}^N\lambda_n y_n\boldsymbol{x}_n.
\]

and

\[
\nabla_{\theta_0}\mathcal{L}=0
\quad\Rightarrow\quad
\sum_{n=1}^N\lambda_n y_n=0,
\quad
\lambda_n\bigl(y_n(\boldsymbol{\theta}^\top\boldsymbol{x}_n+\theta_0)-1\bigr)=0,
\quad
\lambda_n\ge 0.
\]

Plug that expansion into \(\mathcal{L}\) and solve the dual with a **quadratic program**:

\[
\begin{aligned}
\underset{\boldsymbol{\lambda}}{\text{minimize}}
&\quad
\frac12\sum_{n=1}^{N}\sum_{m=1}^{N}\lambda_n\lambda_m y_n y_m\boldsymbol{x}_n^\top\boldsymbol{x}_m
-\sum_{n=1}^N\lambda_n\\
\text{subject to}
&\quad
\lambda_n\ge 0,
\quad
\sum_{n=1}^N\lambda_n y_n=0.
\end{aligned}
\]

With a dual solution \(\hat{\boldsymbol{\lambda}}\),

\[
\hat{\boldsymbol{\theta}}=\sum_{n=1}^{N_s}\lambda_n y_n\boldsymbol{x}_n,
\]

where \(N_s\) is the number of **nonzero** multipliers. Only points that meet the inequality as an equality, \(y_n(\boldsymbol{\theta}^\top\boldsymbol{x}_n+\theta_0)=1\), have \(\lambda_n\neq 0\). Those points are the **support vectors**. Recover \(\hat{\theta}_0\) from any such equality.

---

## 4. Notes

- The SVM solution is **unique**: the cost is strictly convex.
- The **dual** is usually faster than the primal.
- The dual is what makes the **kernel trick** possible. In an RKHS the predictor is

\[
\hat{y}(\boldsymbol{x})=\sum_{n=1}^{N_s}\lambda_n y_n\kappa(\boldsymbol{x},\boldsymbol{x}_n)+\theta_0.
\]

---

## 5. Non-separable classes

When the classes overlap, allow slack:

\[
\begin{aligned}
\underset{\boldsymbol{\theta}\in\mathbb{R}^{l}}{\text{minimize}}
&\quad
\frac{\|\boldsymbol{\theta}\|^2}{2}+C\sum_{n=1}^N\xi_n\\
\text{subject to}
&\quad
y_n(\boldsymbol{\theta}^\top\boldsymbol{x}_n+\theta_0)\ge 1-\xi_n,\quad\xi_n\ge 0.
\end{aligned}
\]

A **margin error** is \(y_n(\boldsymbol{\theta}^\top\boldsymbol{x}_n+\theta_0)<1\), i.e. \(\xi_n>0\). If \(\xi_n=0\) that point does not add to the cost. The optimizer tries to drive as many \(\xi_n\) as possible to zero.

The user parameter \(C\) trades the two terms. Large \(C\): a **small** margin, fewer margin errors. Small \(C\): the opposite.

---

## 6. Choice of hyper-parameters

\(C\) is almost always chosen by **cross-validation** on held-out data.

The other choice is the **kernel**. Different kernels, different performance. A Gaussian kernel needs enough training points to fill the input space, because \(\kappa(\boldsymbol{x},\boldsymbol{x}_n)\) matches \(\boldsymbol{x}\) to the stored point \(\boldsymbol{x}_n\). Training-set size matters.

| Kernel | Formula | Typical use |
| ------ | ------- | ----------- |
| Linear | \(\kappa(\boldsymbol{x},\boldsymbol{x}')=\boldsymbol{x}^\top\boldsymbol{x}'\) | Linearly separable data, or many features relative to \(N\) |
| Polynomial | \(\kappa(\boldsymbol{x},\boldsymbol{x}')=(\boldsymbol{x}^\top\boldsymbol{x}'+c)^d\) | Polynomial-shaped boundaries (e.g. some image tasks) |
| Gaussian RBF | \(\kappa(\boldsymbol{x},\boldsymbol{x}')=\exp\bigl(-\|\boldsymbol{x}-\boldsymbol{x}'\|^2/(2\sigma^2)\bigr)\) | Complex nonlinear relations |
| Sigmoid | \(\kappa(\boldsymbol{x},\boldsymbol{x}')=\tanh(\alpha\boldsymbol{x}^\top\boldsymbol{x}'+c)\) | Periodic or sigmoid-like relations (e.g. some time series) |

---

## 7. Practice

1. Where do the support vectors appear in the SVM dual?

2. What does a large \(C\) do to the margin and to margin errors?

3. Why does the dual make the kernel trick possible?
