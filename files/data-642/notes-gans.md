These notes walk through the lecture slides. The original deck is unchanged; use **(slides)** on the course hub if you want that PDF.

Figures and notes follow Géron, *Hands-On Machine Learning*; Deisenroth, Faisal, and Ong, *Mathematics for Machine Learning*; and Theodoridis, *Machine Learning: A Bayesian and Optimization Perspective*.

## 1. Difficulties of training GANs

The generator and the discriminator are in a zero-sum game. Each is trying to beat the other. That contest can settle at a **Nash equilibrium**: neither player can do better unless the other changes strategy.

Everyone driving on the left is a Nash equilibrium. Switching lanes alone is worse. Everyone driving on the right is another. Start in a different place, land in a different equilibrium.

Sometimes the equilibrium is one shared rule (pick the same side of the road). Sometimes it is two competing rules that still lock (predator chases, prey runs; neither wants to switch).

---

## 2. Mode collapse

The original GAN paper shows there is a single Nash point you *want*: the generator’s images are perfectly realistic, and the discriminator is reduced to a coin flip (50% real, 50% fake). Train long enough, in theory, and you should arrive there with a perfect generator.

Nothing guarantees you ever get there.

The main failure is **mode collapse**. Diversity dies. If the generator gets good at shoes, it may emit mostly shoes. The discriminator then spends its capacity on fake shoes and ignores the rest. The generator jumps to another class. You cycle through a few modes and never cover the training distribution.

---

## 3. Vanishing gradients

**Vanishing gradients**: the backprop signal becomes tiny, often early in training. Updates stall. The two nets need a usable gradient to keep competing; without it, samples stop improving.

Mitigations from the slides: careful initialization, activations that do not saturate, gradient clipping, batch normalization.

The two nets also push on each other, so \(\boldsymbol{\theta}_g\) and \(\boldsymbol{\theta}_d\) can **oscillate**. Training looks fine, then diverges. Many knobs affect that dynamics, so GANs are hypersensitive to hyperparameters.

---

## 4. Ethical considerations

- **Deceptive uses.** Photorealistic fakes: news, fraud, fabricated media.
- **Bias in generated data.** The net copies (and can amplify) biases in the training set.
- **Privacy.** Faces of people who did not consent; identity theft, harassment, surveillance.
- **Law and regulation.** IP, data-privacy rules, and who is accountable for generated content are still being written.
- **Mitigation.** Transparency, accountability, and guidelines. Technologists, ethicists, policymakers, and civil society have to share the problem; it is not only an architecture issue.

---

## Practice

1. What is mode collapse, and why does it stop a GAN from covering the training distribution?

2. The encouraging Nash equilibrium for a GAN is “perfect fakes, discriminator at 50/50.” Why is that not a training guarantee?

3. Name one ethical risk of photorealistic GAN images besides “they look fake.”
