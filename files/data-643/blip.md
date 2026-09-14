These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

**BLIP** (Li et al., 2022) is a vision–language model that **matches** and **writes**. CLIP scores pairs. BLIP also decodes a caption, and it tries to **clean** the noisy web pairs CLIP trained on.

---

## 1. Bootstrap the data

Web alt-text is messy. BLIP’s captioner generates synthetic captions; a filter keeps the ones that still match the image (ITM: image–text matching). The cleaned pairs retrain the model. That loop is the “bootstrapped pretraining” in the syllabus.

![Noisy pairs, filter, matching and language losses](files/data-643/graphics/5.2-blip/blip-pipeline.png)

Alt-text like “IMG_4032” or a product SKU is a bad caption. Generating a sentence and then asking “does this still match?” is the filter. You will not run that loop in lab; you will remember it when your project scrapes the web.

---

## 2. Three losses, one backbone

| Loss | Job |
| ---- | --- |
| ITC (contrastive) | CLIP-style alignment |
| ITM (matching) | Binary: does this caption belong to this image? |
| LM (language modeling) | Decode the caption, causal on text, cross-attend to the image |

The image tower is a ViT. The text side is a transformer that can encode or decode depending on the head. **BLIP-2** later freezes a strong image encoder and trains a thin **Q-Former**; you can treat that as “same idea, cheaper.”

ITC needs a batch of negatives. ITM can use a **hard** negative (a caption that almost matches). LM is why BLIP can caption at all.

Whisper, which you will watch, is an encoder–decoder for **speech \(\to\) text**. BLIP is encoder–decoder for **image \(\to\) text**, plus ITC and ITM. That is the analog, not the same paper.

---

## 3. Captioning versus retrieval

Retrieval (CLIP) returns an existing string from a gallery. Captioning (BLIP) **generates** a new string. Evaluation: CIDEr / CLIP-score / human, not just recall@k. Hallucinated objects are the usual failure (“a red bike” when there is none).

CLIP-score as a caption metric is circular if your captioner was trained to match CLIP. Prefer at least one human or task-specific check. CIDEr rewards n-gram overlap with reference captions; it punishes valid paraphrases. Report both and show two example captions, one good and one hallucinated.

---

## 4. Teaching this note

**30–40 minutes.** CLIP retrieves vs BLIP writes, then the three-loss table, then one numeric ITM vs ITC contrast. Reading: the BLIP paper (ITC+ITM+LM). Play the Whisper video as the **encoder–decoder analog** for captioning (**full ~12 min**, or **0:00–8:00**). Say explicitly: Whisper does not add ITC+ITM; **BLIP does**.

Minute plan: 8 min retrieve vs generate; 10 min ITC/ITM/LM table; 8 min ITM numbers; 12 min Whisper clip plus the one-sentence BLIP add-on.

---

## 5. Worked example

One image, two captions: true “a red mug on a desk,” false “a blue bicycle.”

ITC (\(N=2\)): softmax over the batch; the false caption is one negative among many in a real batch.

ITM: a classifier on the fused `[CLS]` (or matched vs unmatched pair) with labels \(1\) and \(0\). Suppose logits \(s_{+}=2\), \(s_{-}=-1\). Sigmoid probabilities \(\sigma(2)\approx 0.88\), \(\sigma(-1)\approx 0.27\). Binary cross-entropy on those is the ITM term.

LM: decode `a`, `red`, `mug`, … with cross-attention into ViT patch tokens. Loss is next-token, like GPT, but the “prefix” includes the image.

If alt-text was `DSC0001.jpg`, LM on that string teaches garbage. Filter first, then LM.

ITC wants a **batch**. ITM can score one pair. LM wants a **token sequence**. If your project only retrieves, stop at ITC (or CLIP). If it must write, you need LM. If web text is junk, you need the filter (ITM).

---

## 6. Where students get stuck

- Using recall@k as the only captioning metric.
- Thinking ITM and ITC are the same softmax.
- Skipping the filter and training LM on raw alt-text.

---

## 7. Video

Keep the **BLIP paper** as the reading (Li et al., 2022). For a lecture clip, watch [OpenAI’s Whisper Model Explained](https://www.youtube.com/watch?v=uFOkMme19Zs) as an **encoder–decoder analog for captioning**: audio encoder, text decoder. Pause on that cross-attention picture.

Then say: **BLIP adds ITC + ITM + LM** on image–text pairs, and bootstraps noisy web captions. Whisper transcribes; BLIP captions and matches.

---

## 8. Practice

1. Why filter generated captions instead of trusting every alt-text on the web?

2. ITM vs ITC: one is a binary matcher, one is a softmax over the batch. When would ITM catch a pair ITC misses?

3. Name one metric you would report in a captioning project that CLIP retrieval would not need.

4. ITM logits \(s=0\) vs \(s=2\) for a matched pair. Compute \(\sigma(s)\) in both cases. Write the binary-CE term \(-\log\sigma(s)\).

5. A caption of 6 tokens (including `EOS`). LM loss is mean token NLL. If five tokens have probability \(0.5\) and `EOS` has probability \(0.25\), what is the mean NLL? (Use \(\log\) base \(e\): \(-\log 0.5\approx 0.69\), \(-\log 0.25\approx 1.39\).)
