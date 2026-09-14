These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

Module 2 leaves pure text. **Multimodal** systems see more than one stream: image and caption, video and audio, a PDF’s pixels and its words. The hard parts are the same list as Baltrušaitis, Ahuja, and Morency: representation, translation, alignment, fusion, co-learning.

---

## 1. Why more than one stream

A photo of a bottle does not say “flammable.” The label does. A transcript does not show who is speaking; the face does. Complementary signal, and redundant signal (lip motion plus audio). Language models in this course become **conditioned** on other modalities, or retrieve across them.

---

## 2. Joint versus coordinated

**Joint:** mash the streams into **one** vector (early fusion, a concatenating MLP). Missing a modality at test time hurts.

**Coordinated:** keep a tower per modality, then pull the towers together with a similarity (CLIP is this). You can query with either side.

![Joint fusion versus coordinated towers](files/data-643/graphics/4.1-multimodal-foundations/joint-coord.png)

---

## 3. Alignment and fusion, in slogans

**Alignment:** which region of the image goes with which phrase. Attention is the default modern tool.

**Fusion:** when you combine. Early (features), late (decisions), or hybrid (cross-attention).

**Translation:** captioning, text-to-image, speech-to-text. Week 5’s BLIP is a translation model with a matching loss.

**Zero-shot / co-learning:** use a rich modality to help a poor one. Week **4.3**.

---

## 4. Practice

1. Your app must search photos with a typed query. Joint or coordinated? Why?

2. Give one example of alignment that is not “the whole image vs the whole caption.”

3. What breaks if a joint model never saw audio-only examples and you drop the image at test time?
