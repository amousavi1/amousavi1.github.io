These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

Bigger models, trained on more data with more compute, tend to get better at next-token prediction. **Scaling laws** make that trend a curve you can fit, not a slogan. They do not promise a better chatbot; they promise a lower **pretraining loss** if the recipe stays the same.

---

## 1. Kaplan: loss as a power of compute

Kaplan et al. (2020) fit language-model cross-entropy against compute \(C\) (and against parameters \(N\), dataset size \(D\)) and saw smooth **power laws** over many orders of magnitude:

\[
L(C) \approx a\, C^{-b} + L_{\infty}.
\]

The irreducible term \(L_{\infty}\) is entropy of the data plus whatever the architecture cannot represent. The interesting bit is the slope \(-b\): extra FLOPs still buy loss, with diminishing returns.

![Pretraining loss versus compute](files/data-643/graphics/7.1-scaling-laws/compute-loss.png)

Fix two of \(\{N, D, C\}\) and the third is constrained. Early GPT-3-style runs were **compute-optimal for a short training budget** that underused data: a large \(N\), not enough tokens.

---

## 2. Chinchilla: tokens versus parameters

Hoffmann et al. (2022), **Chinchilla**: for a fixed FLOP budget, you should scale **tokens and parameters together**, not dump the budget into a huge model that sees the data once. Their fit said, roughly, equal scaling and about **20 tokens per parameter** for the models they trained.

![Chinchilla: more tokens for the same compute](files/data-643/graphics/7.1-scaling-laws/chinchilla.png)

A smaller model trained longer can beat a larger undertrained one. That is why later LLaMA-style recipes look “small” next to GPT-3 and still read well: they were fed more tokens.

---

## 3. What a law does not tell you

Downstream accuracy is not \(L\). Alignment (Weeks 8–9), data quality, mixture, and context length all sit off the curve. Inference cost scales with \(N\) even if you already paid for training. For a project: cite the checkpoint size and the token budget if you know them; do not claim “we scaled” because you trained two extra epochs on a toy set. Lab 7 fits \(L=a C^{-b}+c\) on constructed points so you see the algebra.

---

## 4. Practice

1. Two models, same FLOPs. One has \(4\times\) the parameters and \(1/4\) the tokens of the other. Who does Chinchilla pick, and why?

2. If \(L_{\infty}\) is already almost your measured loss, what does extra compute buy?

3. Why can a scaling law look great while a chat eval is flat?
