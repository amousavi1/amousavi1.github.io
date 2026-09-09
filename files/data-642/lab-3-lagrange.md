Work in a **Jupyter** notebook. Number the exercises. Do notes **3.1** through **3.3** first. You will need `numpy` and `matplotlib`.

The original assignment PDF is [lab-3-assignment.pdf](files/data-642/lab-3-assignment.pdf).

When you are done: **File → Download as → HTML**, then upload the HTML on Canvas.

---

## 1. One equality, by hand (3 points)

\[
\min_{\boldsymbol{\theta}}\; J(\boldsymbol{\theta})=5\theta_1^2+3\theta_2^2
\quad\text{subject to}\quad
g(\boldsymbol{\theta})=4\theta_1+2\theta_2-12=0.
\]

1. Write the Lagrangian \(\mathcal{L}(\boldsymbol{\theta},\lambda)=J(\boldsymbol{\theta})+\lambda\,g(\boldsymbol{\theta})\).
2. Set \(\nabla_{\boldsymbol{\theta}}\mathcal{L}=\mathbf{0}\) and \(g=0\). Solve for \(\theta_1\), \(\theta_2\), and \(\lambda\). Show the algebra in the notebook (markdown or comments), then check the numbers in code.
3. Say what \(\boldsymbol{\theta}\) and \(\lambda\) mean for a model whose parameters must satisfy a computational budget written as \(g=0\).

---

## 2. Picture (2 points)

Contour plot of \(J\) in the \((\theta_1,\theta_2)\) plane. Draw the line \(g=0\). Mark the constrained minimizer. The unconstrained min is the origin; your star should **not** be there.
