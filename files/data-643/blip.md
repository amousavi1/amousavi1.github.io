These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

**BLIP** (Li et al., 2022) is a vision–language model that **matches** and **writes**. CLIP scores pairs. BLIP also decodes a caption, and it tries to **clean** the noisy web pairs CLIP trained on.

---

## 1. Bootstrap the data

Web alt-text is messy. BLIP’s captioner generates synthetic captions; a filter keeps the ones that still match the image (ITM: image–text matching). The cleaned pairs retrain the model. That loop is the “bootstrapped pretraining” in the syllabus.

![Noisy pairs, filter, matching and language losses](files/data-643/graphics/5.2-blip/blip-pipeline.png)

---

## 2. Three losses, one backbone

| Loss | Job |
| ---- | --- |
| ITC (contrastive) | CLIP-style alignment |
| ITM (matching) | Binary: does this caption belong to this image? |
| LM (language modeling) | Decode the caption, causal on text, cross-attend to the image |

The image tower is a ViT. The text side is a transformer that can encode or decode depending on the head. **BLIP-2** later freezes a strong image encoder and trains a thin **Q-Former**; you can treat that as “same idea, cheaper.”

---

## 3. Captioning versus retrieval

Retrieval (CLIP) returns an existing string from a gallery. Captioning (BLIP) **generates** a new string. Evaluation: CIDEr / CLIP-score / human, not just recall@k. Hallucinated objects are the usual failure (“a red bike” when there is none).

---

## 4. Practice

1. Why filter generated captions instead of trusting every alt-text on the web?

2. ITM vs ITC: one is a binary matcher, one is a softmax over the batch. When would ITM catch a pair ITC misses?

3. Name one metric you would report in a captioning project that CLIP retrieval would not need.
