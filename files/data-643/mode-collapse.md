These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

A GAN has no likelihood you can read as “this model covers the data.” The usual failure is not blur. It is **mode collapse**: the generator finds one (or a few) fakes that fool \(D\) and repeats them.

---

## 1. One mode is enough to fool \(D\)

Suppose the reals are two well-separated clusters. If \(G\) parks all of its mass on cluster A, \(D\) learns “cluster A might be fake; cluster B is real.” \(G\) then jumps to B. You cycle. Or \(G\) never leaves A, and every sample looks plausible while half the world is missing.

![All fakes piled on one of two real modes](files/data-643/graphics/11.3-mode-collapse/collapse.png)

Collapse is a **coverage** failure. Each fake can look fine. The set of fakes does not.

This is the 1-D spike example from note **11.1** with motion. \(D\) only needs to be wrong on the support of \(G\). Modes that \(G\) never visits do not appear in \(G\)’s loss at all.

---

## 2. Quality is not coverage

Eyeballing a grid of images checks **fidelity** (does this one look real?). It does not check whether you missed a mode. Two numbers you want in a report:

| Question | Informal name |
| -------- | ------------- |
| Are the fakes realistic? | precision / fidelity |
| Did we hit the real support? | recall / coverage |

On images, people cite FID or precision–recall in Inception space. Those are proxies. They need a large sample, and they inherit the classifier’s biases. On Lab 11 you can skip Inception: count how many fakes fall near each Gaussian mean.

Latent interpolations are a third check. A short step in \(\boldsymbol{z}\) should change the sample a little. A jump from “shoe” to “face” is a symptom of a broken map, not a feature.

A coverage statistic for two modes: assign each fake to the nearest mean, report the two fractions. Lab 11 calls it collapse if either bin is under \(10\%\). Write both percentages in the report even when they look like \(48/52\): that is the evidence, not a screenshot of two clouds.

---

## 3. What you do about it

There is no single switch. Practical habits: do not let \(D\) become perfect; try more noise dimensions; unrolled or Wasserstein losses in a later paper; **mixture data** in the lab so collapse is visible. For a project, write the coverage check *before* you train. “The pictures look nice” is not a metric.

GANs stay useful for fast sampling. Diffusion (Week 12) is slower and usually covers better, which is why text-to-image moved there. The evaluation lesson does not move: always measure the mode you might have dropped.

---

## 4. Teaching this note

About **30 minutes** at the board, then **~10 minutes** of video. Lab 11 should start in this same class meeting.

- **0–10 min.** Replay the two-spike cartoon. Collapse vs oscillation.
- **10–20 min.** Fidelity vs coverage table. Write the Lab 11 binning rule on the board.
- **20–30 min.** Worked count: 100 fakes, 92 / 8. Precision high, recall not.
- **Then** play CS231N **64:00–74:00** (training is unstable; you do not have \(p(x)\); samples can look good anyway). Pause on the “cons” / summary slide and name that gap **coverage**.

---

## 5. Worked example

Lab 11 means: \(\boldsymbol{\mu}_A=(-2,0)\), \(\boldsymbol{\mu}_B=(2,0)\). You sample 100 fakes. Euclidean nearest-mean assignment:

- 92 fakes closer to \(\boldsymbol{\mu}_A\)
- 8 closer to \(\boldsymbol{\mu}_B\)

Coverage fractions: \(0.92\) and \(0.08\). The \(8\%\) bin is under \(10\%\): **collapse** (or heavy imbalance) by the lab rule.

A human looking at the 92 points near A says they look like reals. Fidelity is high on A. Recall of the mixture is not.

Generator loss can still be small: \(D\) only fights A, so \(D\) on A drifts toward \(0.5\), and \(G\) is paid for staying there. The 8 points on B are not a rescue; they are leftover jitter.

If a second seed gives 47 / 53, write **covered**. Same architecture, different outcome. That is why you report the bin fractions, not only `lossG`.

---

## 6. Where students get stuck

- Equating “sharp samples” with a trained GAN. Sharp and identical is collapse.
- Using \(G\)’s loss as a coverage metric. It has no term for missing modes.
- Averaging FID (or a 2-D MSE to the origin) across a collapsed cloud and calling it a pass.

---

## 7. Video

Watch [Stanford CS231N 2017 lecture 13, Generative Models](https://www.youtube.com/watch?v=5WoItGTWV54), **64:00–74:00**.

Pause on instability and the recap that GANs do not give you \(p(\boldsymbol{x})\) or inference queries. The lecture’s word is “unstable”; your word in this course is **mode collapse / coverage**. Same URL as **11.1** and **11.2**.

---

## 8. Practice

1. Why can a generator loss look healthy while half the training clusters have no fakes?

2. High precision, low recall: what did the GAN do?

3. You have two 2-D Gaussians as reals. Write one coverage statistic you would print in Lab 11 that is not a loss.

4. 200 fakes; 186 assigned to mean A, 14 to mean B. Do you write collapse under the lab’s \(10\%\) rule? What are the two fractions?

5. \(D(G(z))=0.48\) on every fake, all fakes sit on mode A, and \(D=0.99\) on mode B. Why is \(G\) not pulled toward B?
