These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

The exam is cumulative. It asks you to **name a method** and **say what you would measure**. Trivia without a metric is not the point of DATA 443/643.

---

## 1. Four modules

| Module | Weeks | Spine |
| ------ | ----- | ----- |
| 1 | 1–3 | Neurons, embeddings, RNNs/gates, attention, GPT vs BERT |
| 2 | 4–6 | Multimodal, ViT patches, contrastive / CLIP / BLIP, audio as tokens |
| 3 | 7–10 | Scaling and efficiency, SFT and adapters, RLHF / DPO, safety and editing |
| 4 | 11–14 | GANs and mode coverage, diffusion and latent text conditioning, CoT / vote / faithfulness, RAG and ReAct |

You should be able to draw the picture (two GAN players; \(q(\boldsymbol{x}_t\mid\boldsymbol{x}_0)\); retrieve-then-generate) and attach **one number** to it (coverage, a denoising loss, recall@k, majority-vote accuracy, a faithfulness rate).

![Map of the four modules into the exam](files/data-643/graphics/15.1-exam-review/map.png)

---

## 2. How to study

Rework the labs on CPU: XOR and embeddings, long-range gates, one attention head, toy CLIP retrieval, 2-D GAN coverage, one reverse diffusion step, vote-and-flag traces, bag-of-words RAG. Redo each note’s three practice questions out loud. For every named method, write one sentence of the form “I would change \(X\); I would report \(Y\) on split \(Z\).”

Formulas worth being able to write: a neuron, InfoNCE’s diagonal story, attention softmax, GAN min-max, \(q(\boldsymbol{x}_t\mid\boldsymbol{x}_0)\), one reverse mean, cosine for retrieval. You do not need to memorize paper years.

---

## 3. What the exam asks

Typical item: given a failure (collapsed modes, ignored chunk, lucky CoT answer, biased CLIP hit), **name the method that was in play** and **the measurement** that would have caught it. Another item: pick GPT versus BERT, CLIP versus BLIP, GAN versus diffusion, CoT versus ReAct, and justify with the task plus the metric.

Project language belongs here: baseline, one justified change, ablation, failure case. That is the same spine as note **14.3**.

### Remaining talks

**Canvas is official** for who speaks when. If you still owe a presentation, bring a **failure case** (input, output, what broke), not only a demo that worked. Upload what Canvas asks. Time limits on the hub still apply.

---

## 4. Practice

1. A GAN’s fakes look sharp and every one is the same face. What do you measure besides looking?

2. A RAG answer cites `[d5]` but the claim only appears in `[d1]`. Method name, and the check.

3. CoT accuracy is high; a calculator disagrees with half the traces. What exam idea is that, and which week’s lab already scored it?
