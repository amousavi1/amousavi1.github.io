These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

A GAN has no likelihood you can read as “this model covers the data.” The usual failure is not blur. It is **mode collapse**: the generator finds one (or a few) fakes that fool \(D\) and repeats them.

---

## 1. One mode is enough to fool \(D\)

Suppose the reals are two well-separated clusters. If \(G\) parks all of its mass on cluster A, \(D\) learns “cluster A might be fake; cluster B is real.” \(G\) then jumps to B. You cycle. Or \(G\) never leaves A, and every sample looks plausible while half the world is missing.

![All fakes piled on one of two real modes](files/data-643/graphics/11.3-mode-collapse/collapse.png)

Collapse is a **coverage** failure. Each fake can look fine. The set of fakes does not.

---

## 2. Quality is not coverage

Eyeballing a grid of images checks **fidelity** (does this one look real?). It does not check whether you missed a mode. Two numbers you want in a report:

| Question | Informal name |
| -------- | ------------- |
| Are the fakes realistic? | precision / fidelity |
| Did we hit the real support? | recall / coverage |

On images, people cite FID or precision–recall in Inception space. Those are proxies. They need a large sample, and they inherit the classifier’s biases. On Lab 11 you can skip Inception: count how many fakes fall near each Gaussian mean.

Latent interpolations are a third check. A short step in \(\boldsymbol{z}\) should change the sample a little. A jump from “shoe” to “face” is a symptom of a broken map, not a feature.

---

## 3. What you do about it

There is no single switch. Practical habits: do not let \(D\) become perfect; try more noise dimensions; unrolled or Wasserstein losses in a later paper; **mixture data** in the lab so collapse is visible. For a project, write the coverage check *before* you train. “The pictures look nice” is not a metric.

GANs stay useful for fast sampling. Diffusion (Week 12) is slower and usually covers better, which is why text-to-image moved there. The evaluation lesson does not move: always measure the mode you might have dropped.

---

## 4. Practice

1. Why can a generator loss look healthy while half the training clusters have no fakes?

2. High precision, low recall: what did the GAN do?

3. You have two 2-D Gaussians as reals. Write one coverage statistic you would print in Lab 11 that is not a loss.
