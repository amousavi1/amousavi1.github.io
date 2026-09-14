These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

**Contrastive learning** pulls matched pairs together and pushes unmatched pairs apart, in a shared space. **Zero-shot** transfer is what you get when one side of the pair can be a class name written as text.

---

## 1. A batch of matches

\(N\) images and \(N\) captions. Encode both. Cosine similarities form an \(N\times N\) matrix. The loss (InfoNCE) wants the **diagonal** hot: image \(i\) with caption \(i\), not caption \(j\).

![Matched pairs on the diagonal](files/data-643/graphics/4.3-contrastive-zeroshot/contrastive.png)

This is coordinated representation (note **4.1**) with a specific loss. You never fuse pixels and words into one vector during pretraining; you only score pairs.

---

## 2. Zero-shot classification

At test time, encode the image once. Encode prompts `"a photo of a dog"`, `"a photo of a cat"`, … Take the nearest prompt. There is no trained softmax over ImageNet. New classes are new strings.

![Class names as text embeddings](files/data-643/graphics/4.3-contrastive-zeroshot/zeroshot.png)

Prompt wording matters (`a photo of` vs the raw label). So does language: a class that the text tower never saw as a phrase will not magically appear.

---

## 3. What can go wrong

The negative set is the rest of the batch. Small batches \(\Rightarrow\) easy negatives \(\Rightarrow\) a weak space. Web pairs are noisy (Week 5: BLIP filters them). Contrastive spaces can still be **biased** (Week 5.3): “doctor” sits nearer to one gender’s photos.

---

## 4. Practice

1. If every caption in the batch is the word *photo*, what happens to the diagonal?

2. Why is `"a photo of a golden retriever"` often better than `"golden retriever"` for CLIP-style zero-shot?

3. Name one class you **cannot** add at test time by typing it.
