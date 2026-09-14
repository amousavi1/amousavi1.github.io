These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

A **GAN** (Goodfellow et al., 2014) is two networks in a contest: a generator that paints fakes, and a discriminator that tries to catch them. You do not write down \(p(\boldsymbol{x})\) and maximize likelihood. You train a sampler.

---

## 1. The generator

Noise \(\boldsymbol{z}\) (usually isotropic Gaussian) in; a sample \(\boldsymbol{x}=G(\boldsymbol{z};\boldsymbol{\theta}_g)\) out, same shape as a real observation. \(G\) is a decoder without an encoder: it does not reconstruct a particular training point. It maps latent draws into data space.

![Generator from noise; discriminator scores real versus fake](files/data-643/graphics/11.1-gan-idea/players.png)

The job of \(G\) is to make the **distribution** of fakes look like the distribution of reals. One pretty sample is not a trained generator.

---

## 2. The discriminator

\(D(\boldsymbol{x};\boldsymbol{\theta}_d)\) is a binary classifier: the probability that \(\boldsymbol{x}\) is real. On a real batch it should sit near 1; on \(G(\boldsymbol{z})\) it should sit near 0. It never sees \(\boldsymbol{z}\). It only sees the sample.

\[
y = D(\boldsymbol{x};\boldsymbol{\theta}_d)\in(0,1).
\]

Then \(1-D(\boldsymbol{x})\) is the probability it calls the point fake.

---

## 3. Why two players

If you trained only \(G\) against a frozen \(D\), \(G\) would overfit whatever \(D\) currently likes. If you trained only \(D\), it would become a perfect detector of yesterday’s fakes and give \(G\) a useless (flat) gradient. The pair has to stay in tension. Note **11.2** writes that as a min-max game; note **11.3** is what happens when \(G\) finds one easy fake and stops covering the rest.

For this course, GANs are the first **implicit** generator you meet. Diffusion (Week 12) will give you an explicit noise schedule instead of an adversary. Text-to-image later in the module still needs a way to **condition** (Week 5’s CLIP is one).

---

## 4. Practice

1. \(G\) never sees a real image on its own update (only through \(D\)’s scores). How can it learn the data distribution?

2. Why is a perfect \(D\) (always 1 on reals, always 0 on fakes) a problem for \(G\)’s gradient?

3. Name one task where a GAN is a natural fit and one where an explicit likelihood model would be easier to evaluate.
