These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

**BLIP** (Li et al., 2022) is a vision–language model that **matches** and **writes**. CLIP scores pairs. CoCa (Yu et al.) is the sibling idea: add a **decoder**. BLIP does that, and it also **cleans** the noisy web pairs CLIP trained on. By the end you should be able to name the three losses, say why the filter exists, and tell retrieval from captioning.

---

## 1. What BLIP is

**BLIP** is CLIP-style scoring **plus** a decoder that writes text, with a filter on noisy web pairs. CLIP cannot decode a sentence. Naive captioners train on noisy alt-text. BLIP tries to clean the web and add generation.

Three losses share one backbone: **ITC** (contrastive, CLIP-style alignment), **ITM** (matched versus unmatched pair), and **LM** (caption tokens). The bootstrap loop is: generate captions, filter the ones that still match the image, train again.

![Noisy pairs, filter, matching and language losses](files/data-643/graphics/5.2-blip/blip-pipeline.png)

Alt-text like `IMG_4032` or a product SKU is a bad caption. Generating a sentence and then asking “does this still match?” is the filter. You will not run that loop in lab; you will remember it when your project scrapes the web.

CoCa (Yu et al.) adds a captioning loss on top of contrastive training. It does **not** advertise the bootstrap filter. If your story is “noisy web text,” you need BLIP’s ITM filter, not only a decoder.

---

## 2. Why we use it

CLIP retrieves an existing string from a gallery. Many products need a **new** sentence: a caption, an alt-text rewrite, a description that was never in the index. That job is generation, and it needs a decoder.

The web is the other reason. Alt-text is messy. Training language-model loss on `DSC0001.jpg` teaches garbage. BLIP’s filter is the method that tries to keep only captions that still match the image. Whisper, which you will watch as an analog, is an encoder–decoder for **speech \(\to\) text**. BLIP is encoder–decoder for **image \(\to\) text**, plus ITC and ITM.

If your project only retrieves, stop at ITC (or CLIP). If it must write, you need LM. If web text is junk, you need the filter (ITM).

---

## 3. Architecture

An image encoder, a text encoder, and a decoder with **cross-attention** into image tokens (queries from text, keys and values from vision).

The image tower is a ViT. The text side is a transformer that can encode or decode depending on the head. **BLIP-2** later freezes a strong image encoder and trains a thin **Q-Former**; treat that as “same idea, cheaper.” LLaVA is a frozen CLIP tower plus an LLM. Not this hour.

| Loss | Job |
| ---- | --- |
| ITC (contrastive) | CLIP-style alignment |
| ITM (matching) | Binary: does this caption belong to this image? |
| LM (language modeling) | Decode the caption, causal on text, cross-attend to the image |

![ITC, ITM, and LM](files/data-643/graphics/5.2-blip/blip-losses.png)

ITC needs a batch of negatives. ITM can use a **hard** negative (a caption that almost matches). LM is why BLIP can caption at all. Generation uses the decoder; retrieval can use ITC embeddings.

---

## 4. How it works, step by step

1. **ITC aligns.** Encode a batch of image–text pairs. InfoNCE wants the diagonal, as in CLIP. This is the retrieval-friendly space.
2. **ITM matches.** A binary head on a fused `[CLS]` asks whether this caption belongs to this image. Hard negatives make the yes/no sharper than a random off-diagonal.
3. **LM writes.** Decode `a`, `red`, `mug`, … with cross-attention into ViT patch tokens. Loss is next-token, like GPT, but the “prefix” includes the image.
4. **Bootstrap.** A captioner generates synthetic captions for web images. ITM keeps the ones that still match. Retrain on the cleaned pairs. That loop is the “bootstrapped pretraining” in the syllabus.
5. **Pick the head at test.** Retrieve with ITC embeddings. Caption with the decoder. Do not report recall@k as the only captioning metric.

If alt-text was `DSC0001.jpg`, LM on that string teaches garbage. Filter first, then LM.

ITC wants a **batch**. ITM can score one pair. LM wants a **token sequence**.

---

## 5. Mathematical formulas

ITC is InfoNCE on the batch, as in note **4.3**. ITM is logistic loss on a match score \(s\). With \(\sigma(s)=1/(1+e^{-s})\),

\[
\mathcal{L}_{\text{ITM}}=-y\log\sigma(s)-(1-y)\log\bigl(1-\sigma(s)\bigr).
\]

LM is next-token on the caption, conditioned on the image:

\[
\mathcal{L}_{\text{LM}}=\sum_t -\log p(w_t\mid w_{<t},\text{image}).
\]

The three terms share the ViT and the text transformer; they do not share a head.

---

## 6. Positive points and negative points

**Positive.**

- Captions and retrieval in one family: decoder for writing, ITC embeddings for search.
- The ITM filter is a method for noisy web alt-text, not a slogan.
- Cross-attention into patch tokens is the same encoder–decoder picture students will see in Whisper.

**Negative.**

- Captions can hallucinate objects that are not in the image.
- The filter is extra machinery; skipping it and training LM on raw alt-text is a common failure.
- Heavier than frozen CLIP: you train a decoder, not only two towers.
- CLIP-score as a caption metric is circular if the captioner was trained to match CLIP.

**When not to.** If your project only retrieves, stop at CLIP or ITC. CoCa and BLIP share a decoder idea; they are not the same paper. BLIP’s extra is bootstrap plus ITM.

---

## 7. Captioning versus retrieval

Retrieval (CLIP) returns an existing string from a gallery. Captioning (BLIP) **generates** a new string. Evaluation: CIDEr / CLIP-score / human, not just recall@k. Hallucinated objects are the usual failure (“a red bike” when there is none).

CLIP-score as a caption metric is circular if your captioner was trained to match CLIP. Prefer at least one human or task-specific check. CIDEr rewards n-gram overlap with reference captions; it punishes valid paraphrases. Report both and show two example captions, one good and one hallucinated.

---

## 8. Teaching this note

**30–40 minutes.** CLIP retrieves vs BLIP writes, then the three-loss table, then one numeric ITM vs ITC contrast. Reading: the BLIP paper (ITC+ITM+LM). Play the Whisper video as the **encoder–decoder analog** for captioning (**0:00–8:00**). Say explicitly: Whisper does not add ITC+ITM; **BLIP does**.

Minute plan: 8 min retrieve vs generate; 10 min ITC/ITM/LM table; 8 min ITM numbers; 12 min Whisper clip plus the one-sentence BLIP add-on.

---

## 9. Worked example

One image, two captions: true “a red mug on a desk,” false “a blue bicycle.”

ITC (\(N=2\)): softmax over the batch; the false caption is one negative among many in a real batch.

ITM: a classifier on the fused `[CLS]` with labels \(1\) and \(0\). Suppose logits \(s_{+}=2\), \(s_{-}=-1\).

\[
\sigma(s)=\frac{1}{1+e^{-s}},\qquad
\sigma(2)\approx 0.88,\qquad
\sigma(-1)\approx 0.27.
\]

Binary cross-entropy: matched term \(-\log\sigma(2)\approx 0.13\); mismatched term \(-\log(1-\sigma(-1))\approx 0.31\).

![ITM is a yes/no score](files/data-643/graphics/5.2-blip/blip-itm-numeric.png)

LM: decode `a`, `red`, `mug`, … with cross-attention into ViT patch tokens. Loss is next-token, like GPT, but the “prefix” includes the image.

If alt-text was `DSC0001.jpg`, LM on that string teaches garbage. Filter first, then LM.

ITC wants a **batch**. ITM can score one pair. LM wants a **token sequence**. If your project only retrieves, stop at ITC (or CLIP). If it must write, you need LM. If web text is junk, you need the filter (ITM).

---

## 10. Where students get stuck

- Using recall@k as the only captioning metric.
- Thinking ITM and ITC are the same softmax.
- Skipping the filter and training LM on raw alt-text.
- Calling CoCa and BLIP the same paper. Shared idea: a decoder. BLIP’s extra: bootstrap + ITM.

---

## 11. Video

Keep the **BLIP paper** as the reading (Li et al., 2022). For a lecture clip, watch [OpenAI’s Whisper Model Explained](https://www.youtube.com/watch?v=uFOkMme19Zs) as an **encoder–decoder analog for captioning**: audio encoder, text decoder. Pause on that cross-attention picture.

Then say: **BLIP adds ITC + ITM + LM** on image–text pairs, and bootstraps noisy web captions. Whisper transcribes; BLIP captions and matches.

---

## 12. Practice

1. Why filter generated captions instead of trusting every alt-text on the web?

2. ITM vs ITC: one is a binary matcher, one is a softmax over the batch. When would ITM catch a pair ITC misses?

3. Name one metric you would report in a captioning project that CLIP retrieval would not need.

4. ITM logits \(s=0\) vs \(s=2\) for a matched pair. Compute \(\sigma(s)\) in both cases. Write the binary-CE term \(-\log\sigma(s)\).

5. A caption of 6 tokens (including `EOS`). LM loss is mean token NLL. If five tokens have probability \(0.5\) and `EOS` has probability \(0.25\), what is the mean NLL? (Use \(\log\) base \(e\): \(-\log 0.5\approx 0.69\), \(-\log 0.25\approx 1.39\).)
