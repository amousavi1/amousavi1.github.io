These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

A **GAN** (Goodfellow et al., 2014) is two networks in a contest: a generator that paints fakes, and a discriminator that tries to catch them. You do not write down \(p(\boldsymbol{x})\) and maximize likelihood. You train a sampler. By the end you should be able to draw the two-player diagram, name what each net sees, and explain why one pretty fake is not a trained generator.

---

## 1. What a GAN is

A **GAN** is two nets with opposite jobs. A **generator** \(G\) samples in one pass: noise \(\boldsymbol{z}\) in, a fake \(\boldsymbol{x}=G(\boldsymbol{z};\boldsymbol{\theta}_g)\) out, the same shape as a real observation. A **discriminator** \(D(\boldsymbol{x};\boldsymbol{\theta}_d)\) is a binary classifier that scores whether \(\boldsymbol{x}\) looks real. You give up on writing \(p(\boldsymbol{x})\). You keep a one-forward-pass sampler.

\(G\) is a decoder without an encoder. It does not reconstruct a particular training point. It maps latent draws into data space. The job of \(G\) is to make the **distribution** of fakes look like the distribution of reals. One pretty sample is not a trained generator. If every \(\boldsymbol{z}\) maps to the same pretty point, \(G\) has failed, even if that point fools a human.

\(D\) never sees \(\boldsymbol{z}\). It only sees the sample. On a real batch it should sit near 1; on \(G(\boldsymbol{z})\) it should sit near 0. Then \(1-D(\boldsymbol{x})\) is the probability it calls the point fake.

This is an **implicit** density and a **direct** sample. Name what you cannot do: \(p(\boldsymbol{x})\), \(p(\boldsymbol{z}\mid\boldsymbol{x})\), a test log-likelihood. Name what you can do: draw fakes in one forward pass. That pair of sentences is the exam answer for “why a GAN versus why a diffusion model.”

---

## 2. Why we use it

Likelihood models can be blurry, or slow to sample, or both. An autoencoder reconstructs a particular point; it is not asked to cover a distribution of fakes. GANs aim for **sharp one-pass samples** (images, and later the coverage bugs in note **11.3**). Diffusion (Week 12) will give you an explicit noise schedule instead of an adversary, but sampling there is iterative, not one shot.

You need two players because a single net is the wrong teacher. If you trained only \(G\) against a frozen \(D\), \(G\) would overfit whatever \(D\) currently likes. If you trained only \(D\), it would become a perfect detector of yesterday’s fakes and give \(G\) a useless (flat) gradient. The pair has to stay in tension. Note **11.2** writes that as a min-max game; note **11.3** is what happens when \(G\) finds one easy fake and stops covering the rest.

For this course, GANs are the implicit generator you meet before diffusion. Text-to-image later in the module still needs a way to **condition** (Week 5’s CLIP is one). Draw the two-player figure on the board and leave it up: everything later in Week 11 is a comment on that picture.

---

## 3. Architecture

The boxes connect in a fixed order. Sample \(\boldsymbol{z}\sim p(z)\) (usually isotropic Gaussian). Push it through \(G\). Hand the fake to \(D\). Independently, hand a real \(\boldsymbol{x}\) from the data to the same \(D\). There is no encoder and no reconstruction loss. \(G\) never sees a real \(\boldsymbol{x}\) on its own update. \(D\) never sees \(\boldsymbol{z}\).

![Generator from noise; discriminator scores real versus fake](files/data-643/graphics/11.1-gan-idea/players.png)

In this course \(G\) is a tiny MLP (Lab 11: 8-D noise \(\to\) 2-D point). The same picture is a CNN or a transformer decoder when \(\boldsymbol{x}\) is an image or a spectrogram. The algebra does not change: sample \(\boldsymbol{z}\), push it through \(G\), hand the fake to \(D\).

\(D\) is ordinary supervised learning on a **moving** dataset: reals with label 1, fakes with label 0. The catch is that the fake distribution changes every time you update \(G\). You never have a fixed classification problem.

---

## 4. How it works, step by step

Training both nets, with the actual losses, is the next note. The idea you need today is what each player sees and what a Bayes-optimal \(D\) would say.

1. Draw noise \(\boldsymbol{z}\) and form a fake \(G(\boldsymbol{z})\). \(G\) does not compare that fake to the nearest real (that would be an autoencoder). The only teacher is \(D\)’s scalar.
2. \(D\) scores a mixed batch: reals from the data, fakes from the current \(G\).
3. Update \(D\) so reals go toward 1 and fakes toward 0, then update \(G\) so \(D(G(z))\) goes toward 1. The min-max details live in note **11.2**.
4. Read the Bayes-optimal discriminator. Where \(G\) matches the data, that optimum is a coin flip: \(D^*=1/2\). Where \(G\) never goes, \(p_G=0\) and \(D^*=1\). \(G\)’s loss never sees that missing location.

Suppose the reals are two spikes and an untrained \(G\) always emits the right-hand spike. A Bayes-optimal \(D\) is then \(1/2\) on that spike (half real, half fake) and \(1\) on the left spike (only reals). \(G\) is “winning” at the right spike in the sense that \(D(G(z))=0.5\). It is losing as a **distribution**: the left mode has zero fake mass. The worked example below puts numbers on that cartoon.

---

## 5. Mathematical formulas

The discriminator is a probability in \((0,1)\):

\[
y = D(\boldsymbol{x};\boldsymbol{\theta}_d)\in(0,1).
\]

The Bayes-optimal discriminator for a fixed generator (Goodfellow et al.) is

\[
D^*(x)=\frac{p_{\mathrm{data}}(x)}{p_{\mathrm{data}}(x)+p_G(x)}.
\]

At a perfect \(G\), \(p_G=p_{\mathrm{data}}\) and \(D^*=1/2\) everywhere the mass lives. That \(1/2\) is success as a **distribution**, not a trophy for a single pretty fake. Where \(G\) never goes, \(p_G=0\) and \(D^*=1\).

---

## 6. Positive points and negative points

**Positive.**

- Sampling is one forward pass through \(G\), not a long reverse chain.
- When training holds, samples can be sharp rather than a blurry average of modes.
- The same two-player picture scales from Lab 11’s 2-D MLP to images and spectrograms without changing the algebra.
- You get an implicit generator when writing \(p(\boldsymbol{x})\) is the wrong tool.

**Negative.**

- There is no likelihood, no \(p(\boldsymbol{z}\mid\boldsymbol{x})\), and no test log-likelihood to report.
- Training is unstable (note **11.2**): the classification problem moves every time \(G\) updates.
- Mode collapse (note **11.3**) is the usual coverage failure, not blur.
- This is not an LLM method. Do not mix it with next-token training.

**When not to use a GAN.** A task that needs a number for \(p(\boldsymbol{x})\) or an inference query \(p(\boldsymbol{z}\mid\boldsymbol{x})\). Diffusion (Week 12) if you would rather train a denoiser than fight an adversary, and you can afford iterative sampling.

---

## 7. Teaching this note

About **35 minutes** at the board, then **~8 minutes** of video. This is the first of three GAN notes in a two-hour class; Lab 11 uses the rest of the block.

- **0–12 min.** Implicit vs explicit. You cannot write \(p(\boldsymbol{x})\) for a GAN. You can sample. Sketch the two-player diagram.
- **12–24 min.** What \(G\) and \(D\) each see. \(G\) never sees a real \(\boldsymbol{x}\) on its own update. \(D\) never sees \(\boldsymbol{z}\).
- **24–34 min.** Worked 1-D two-mode example. Leave the numbers on the board; note **11.3** will reuse them.
- **Then** play **46:45–54:00** of the assigned video (GAN setup: give up on density, noise through a generator). Pause when the two-player cartoon appears.

---

## 8. Worked example

Reals are two spikes in 1-D: half the mass at \(x=-2\), half at \(x=+2\). (Lab 11 is the same idea in 2-D, means \((-2,0)\) and \((2,0)\).)

Suppose an untrained \(G\) ignores \(\boldsymbol{z}\) and always emits \(G(z)=+2\).

A Bayes-optimal \(D\) then scores:

| location | what \(D\) sees | \(D(x)\) |
| -------- | --------------- | -------- |
| \(x=+2\) | half real, half fake | \(0.5\) |
| \(x=-2\) | only reals | \(1\) |
| anywhere else | only fakes, if any | near \(0\) |

\(G\) is “winning” at \(+2\) in the sense that \(D(G(z))=0.5\), a coin flip. It is losing as a **distribution**: the left mode has zero fake mass. One sample at \(+2\) looks perfect. The generator is not trained.

If you now let \(G\) move and it jumps all mass to \(-2\), the table flips: \(D(-2)=0.5\), \(D(+2)=1\). That oscillation is the seed of note **11.3**.

![Bayes \(D\) when \(G\) parks on \(+2\)](files/data-643/graphics/11.1-gan-idea/d-bayes.png)

The optimal discriminator is \(D^*(x)=p_r(x)/(p_r(x)+p_g(x))\). Where \(G\) never goes, \(p_g=0\) and \(D^*=1\). \(G\)’s loss never sees that location.

---

## 9. Where students get stuck

- Treating one pretty fake as success. \(G\) is a distribution, not a Photoshop filter.
- Thinking \(G\) is trained by comparing \(G(z)\) to the nearest real (an autoencoder). It is not. The only teacher is \(D\)’s scalar.
- Forgetting that \(D\)’s data distribution moves. A \(D\) that was perfect last step is scoring a different \(G\) this step.

---

## 10. Video

Watch [Generative models: GAN setup](https://www.youtube.com/watch?v=5WoItGTWV54), **46:45–54:00**.

Pause at the two-player setup: noise \(\boldsymbol{z}\) through a generator, no explicit density. Skip PixelCNN/VAE (the first 45 minutes) in class; those are not this note. Notes **11.2** and **11.3** reuse the same URL at later pause points.

---

## 11. Practice

1. \(G\) never sees a real image on its own update (only through \(D\)’s scores). How can it learn the data distribution?

2. Why is a perfect \(D\) (always 1 on reals, always 0 on fakes) a problem for \(G\)’s gradient?

3. Name one task where a GAN is a natural fit and one where an explicit likelihood model would be easier to evaluate.

4. In the 1-D example, \(G(z)=+2\) always and reals are equal spikes at \(\pm 2\). What is the Bayes-optimal \(D(+2)\)? What is \(D(-2)\)?

5. You draw 10 fakes and all 10 equal \(+2\). A classmate says “\(D\) is 0.5 there, so \(G\) is done.” Write one sentence that disagrees, using coverage.
