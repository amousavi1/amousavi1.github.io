These notes walk through the lecture slides. The original deck is unchanged; use **(slides)** on the course hub if you want that PDF.

Figures and notes follow Géron, *Hands-On Machine Learning*; Deisenroth, Faisal, and Ong, *Mathematics for Machine Learning*; and Theodoridis.

## 1. Why bother

Training a large deep net with plain gradient descent is slow. A faster **optimizer** is a large speedup.

---

## 2. Momentum

Polyak, 1964. A bowling ball on a gentle slope: slow at first, then it picks up **momentum** until terminal velocity. Plain gradient descent ignores past gradients. If the local gradient is tiny, it crawls.

Momentum keeps a velocity \(\boldsymbol{m}\). Subtract the local gradient (times the learning rate \(\alpha\)) from \(\boldsymbol{m}\); add \(\boldsymbol{m}\) to the weights:

\[
\boldsymbol{m}^{(k+1)} = \gamma\boldsymbol{m}^{(k)} - \alpha^{(k)}\nabla J\bigl(\boldsymbol{\theta}^{(k)}\bigr),
\]

\[
\boldsymbol{\theta}^{(k+1)} = \boldsymbol{\theta}^{(k)} + \boldsymbol{m}^{(k+1)}.
\]

If \(\gamma=0.9\), terminal velocity is **ten times** \(\alpha\nabla J\). Plateaus and some local optima are easier to leave. Without batch normalization, upper layers often see badly scaled inputs; momentum helps.

The ball can overshoot, come back, and **oscillate**. A bit of friction (the \(\gamma<1\) decay) damps that. Cost: one more hyperparameter. \(\gamma=0.9\) is a usual default and is almost always faster than plain GD.

---

## 3. Nesterov accelerated gradient

**NAG** measures the gradient **slightly ahead**, in the direction of the current momentum, not at the current \(\boldsymbol{\theta}\):

\[
\boldsymbol{m}^{(k+1)} = \gamma\boldsymbol{m}^{(k)} - \alpha^{(k)}\nabla J\bigl(\boldsymbol{\theta}^{(k)}+\gamma\boldsymbol{m}^{(k)}\bigr),
\]

\[
\boldsymbol{\theta}^{(k+1)} = \boldsymbol{\theta}^{(k)} + \boldsymbol{m}^{(k+1)}.
\]

The momentum vector usually already points toward the optimum, so the lookahead gradient is a better estimate.

![Regular momentum versus Nesterov lookahead](files/data-642/graphics/13.2-faster-optimizers/regvsnest.png)

---

## 4. AdaGrad

On a long thin valley, gradient descent dives down the steep walls, then creeps along the floor. AdaGrad **scales down** the gradient on the steep coordinates:

\[
\boldsymbol{s}^{(k+1)} = \boldsymbol{s}^{(k)} + \nabla J\bigl(\boldsymbol{\theta}^{(k)}\bigr)\otimes\nabla J\bigl(\boldsymbol{\theta}^{(k)}\bigr),
\]

\[
\boldsymbol{\theta}^{(k+1)} = \boldsymbol{\theta}^{(k)} - \alpha^{(k)}\,\nabla J\bigl(\boldsymbol{\theta}^{(k)}\bigr)\oslash\sqrt{\boldsymbol{s}^{(k+1)}+\epsilon}.
\]

\(\otimes\) and \(\oslash\) are elementwise. \(\boldsymbol{s}\) accumulates squared gradients. \(\epsilon\) (often \(10^{-10}\)) avoids division by zero.

That is an **adaptive learning rate**: steep directions decay faster than gentle ones. Updates point more toward the global optimum, and \(\alpha\) needs less tuning.

On simple quadratics this works. On deep nets AdaGrad often **stops too early**: \(\boldsymbol{s}\) grows until the effective rate is essentially zero. Do not train a deep net with it. Know it so the later adaptive methods make sense.

![AdaGrad correcting the path in a long valley](files/data-642/graphics/13.2-faster-optimizers/adagrad.png)

---

## 5. RMSProp

AdaGrad remembers **every** squared gradient. RMSProp remembers a **recent** average, with exponential decay:

\[
\boldsymbol{s}^{(k+1)} = \gamma\boldsymbol{s}^{(k)} + (1-\gamma)\,\nabla J\bigl(\boldsymbol{\theta}^{(k)}\bigr)\otimes\nabla J\bigl(\boldsymbol{\theta}^{(k)}\bigr),
\]

and the same \(\boldsymbol{\theta}\) update as AdaGrad. Typical \(\gamma=0.9\).

---

## 6. Why not Hessians

Everything above uses **first** derivatives (Jacobians). Second-order methods use **Hessians**. For \(n\) parameters you store on the order of \(n^2\) Hessian entries per output, versus \(n\) Jacobian entries. Deep nets have tens of thousands of parameters. The Hessian often will not fit in memory; computing it is too slow even when it does.

---

## 7. Learning-rate schedules

If \(\alpha\) is too small, you will get there, late.

![Loss versus iteration for different learning rates](files/data-642/graphics/13.2-faster-optimizers/loss.png)

One hunt: start large, divide by 3 until training stops diverging. You land near a rate that learns quickly and still converges.

Other schedules, with iteration \(k\) and a scale \(s\):

| Schedule | Rule |
| -------- | ---- |
| **Power** | \(\alpha^{(k)}=\alpha^{(0)}/(1+k/s)^{c}\) |
| **Exponential** | \(\alpha^{(k)}=\alpha^{(0)}\,0.1^{k/s}\) |
| **Piecewise constant** | e.g. \(0.1\) for five epochs, then \(0.001\) for fifty, … |
| **Performance** | Every \(N\) steps, if validation error has stalled, multiply \(\alpha\) by \(\lambda\) (same idea as early stopping) |

---

## Practice

1. If momentum uses \(\gamma=0.9\), how does terminal velocity compare to a plain gradient step of the same \(\alpha\)?

2. AdaGrad and RMSProp share an adaptive \(\boldsymbol{s}\). What does RMSProp change so that training need not freeze?

3. Nesterov evaluates \(\nabla J\) where, relative to ordinary momentum?
