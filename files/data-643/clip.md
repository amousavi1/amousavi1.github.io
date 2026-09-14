These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

**CLIP** (Radford et al., 2021) is the coordinated, contrastive model that made zero-shot vision–language the default. Two towers, a cosine, a large batch of image–caption pairs from the web.

---

## 1. Two towers

An **image encoder** (ResNet or ViT) and a **text encoder** (a transformer). Both emit a vector in the same dimension. Training: InfoNCE on the batch (note **4.3**). After training you keep both towers; you do not keep a fused head.

![CLIP image and text towers](files/data-643/graphics/5.1-clip/clip-towers.png)

Open-source copies (OpenCLIP, SigLIP) change the loss or the data. The picture is stable.

---

## 2. What CLIP is good at

- **Zero-shot** classification via prompts.
- **Cross-modal retrieval:** image \(\to\) text and text \(\to\) image (note **5.3**).
- A **frozen** image backbone for later captioners and diffusion models (Week 12).

What it is not: a captioner (it does not decode a sentence), a detector with boxes, or a guarantee of factual correctness. It scores pairs.

---

## 3. Practical notes

Temperature \(\tau\) (often \(0.07\)) sharpens the softmax. Batch size wants to be large. Hugging Face `CLIPModel` plus a processor is enough for Lab 5’s *idea*; the lab itself uses a toy space so nobody waits on a download.

For a project: cite the checkpoint, freeze versus fine-tune, and write the prompts you used. Prompt choice is part of the method, not a footnote.

---

## 4. Practice

1. CLIP’s text tower never sees the pixels. How can a typed query retrieve a photo?

2. Why does a batch of 8 give weaker negatives than a batch of 1024?

3. You need generated captions, not retrieval. Which Week 5 model is the closer ancestor?
