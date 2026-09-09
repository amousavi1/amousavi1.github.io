These notes walk through the lecture slides. The original deck is unchanged; use **(slides)** on the course hub if you want that PDF.

Figures and notes follow Géron, *Hands-On Machine Learning*; Deisenroth, Faisal, and Ong, *Mathematics for Machine Learning*; and Theodoridis.

## 1. Why regularize

A deep net may have tens of thousands of parameters, sometimes millions. That freedom fits complicated data. It also **overfits**. You need **regularization**.

---

## 2. \(\ell_1\) and \(\ell_2\) (weight decay)

Both drop into backpropagation as a change to the loss. For \(\ell_2\),

\[
J_{\mathrm{reg}}(\boldsymbol{\theta}) = J(\boldsymbol{\theta}) + \lambda\sum_{i=1}^{n}\theta_i^{2}.
\]

\(J\) is the original loss. \(\lambda\) is the strength.

On the backward pass you add the gradient of that penalty to the gradient of \(J\). The update is ordinary descent on \(J_{\mathrm{reg}}\).

Effect: weights are **shrunk toward zero**. They cannot grow without bound. Larger \(\lambda\) means stronger shrinkage. This is **weight decay**: deterministic given \(\boldsymbol{\theta}\).

---

## 3. Dropout

Hinton, 2012. At each training step, every neuron (inputs included, **outputs never**) is dropped with probability \(p\): ignored for that step, maybe present on the next. \(p\) is the **dropout rate**, often **50%**. After training, nothing is dropped.

![Dropout at train time](files/data-642/graphics/13.4-regularization/dropout.png)

Overfitting: raise \(p\). Underfitting: lower \(p\). Large layers can take a higher rate than small ones. Many strong nets drop out only after the **last hidden layer** if full dropout is too strong.

Dropout **slows** convergence and usually **improves** the fitted model when \(p\) is right.

---

## 4. Monte Carlo dropout

Gal and Ghahramani, 2016.

- A net with dropout before every weight layer is **approximate Bayesian** inference. That is a justification, not a slogan.
- **MC dropout** can improve a *already-trained* dropout model: no retraining, no architecture change.
- It also gives a better **uncertainty** estimate.
- It is simple to implement.

---

## Practice

1. Dropout versus weight decay: which one is stochastic at train time?

2. In \(\ell_2\) regularization, what does raising \(\lambda\) do to the weights?

3. You already trained a dropout net. What extra does MC dropout give you without a second training run?
