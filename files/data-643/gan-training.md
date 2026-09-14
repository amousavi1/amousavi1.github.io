These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

The two nets have opposite goals. You cannot treat a GAN as one ordinary loss. Each step is a small fight: first improve \(D\), then improve \(G\), and try not to let either win too hard.

---

## 1. The min-max game

Goodfellow et al. write a two-player objective

\[
\min_{\boldsymbol{\theta}_g}\max_{\boldsymbol{\theta}_d} J(\boldsymbol{\theta}_g,\boldsymbol{\theta}_d),
\]

\[
J
=
\mathbb{E}_{\boldsymbol{x}\sim p_r}\bigl[\log D(\boldsymbol{x})\bigr]
+
\mathbb{E}_{\boldsymbol{z}\sim p_z}\bigl[\log\bigl(1-D(G(\boldsymbol{z}))\bigr)\bigr].
\]

\(D\) wants \(J\) large (correct labels). \(G\) wants \(J\) small (fakes that look real). A Nash point you *hope* for: \(G\) matches \(p_r\), and \(D\) is a coin flip. Training does not guarantee you land there.

![Generator and discriminator losses pulling in opposite directions](files/data-643/graphics/11.2-gan-training/dynamics.png)

---

## 2. Two phases per iteration

1. **Train \(D\).** A batch of reals (label 1) and fakes from the current \(G\) (label 0). Binary cross-entropy. Update **only** \(\boldsymbol{\theta}_d\).
2. **Train \(G\).** Fresh noise, fresh fakes. Labels are all 1: you want \(D\) to be *wrong*. Freeze \(\boldsymbol{\theta}_d\); update **only** \(\boldsymbol{\theta}_g\).

In code you often maximize \(\log D(G(\boldsymbol{z}))\) instead of minimizing \(\log(1-D(G(\boldsymbol{z})))\). Early in training \(D\) is too good and the second form saturates.

---

## 3. The tension

If \(D\) is too weak, \(G\) gets a noisy, lying teacher. If \(D\) is too strong, \(G\)’s gradient vanishes. The two parameter vectors can **oscillate**: losses look fine, then the samples jump. Learning rates, how many \(D\) steps per \(G\) step, and batch size all move that balance.

Watching \(J\) is not evaluation. A falling generator loss can mean better fakes *or* a collapsing \(D\). You still have to look at samples and at **coverage** (note **11.3**). Lab 11 is a 2-D version of this fight on purpose: you will see the tension in a scatter plot, not in a single scalar.

---

## 4. Practice

1. In phase 2 the fake labels are 1. Who is being lied to, and why is that the generator’s loss?

2. Why might two discriminator steps per generator step help early training, and how could it hurt later?

3. The generator loss dropped and the pictures got worse. Give one explanation that is not “the learning rate is wrong.”
