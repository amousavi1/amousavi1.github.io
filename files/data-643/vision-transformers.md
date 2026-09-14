These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

A **vision transformer (ViT)** is the Week 3 block on **patches** instead of words. Once an image is a sequence, every LLM trick (attention, positions, [CLS], later CLIP) applies.

---

## 1. Patches as tokens

Split a \(H\times W\) image into \(P\times P\) patches, flatten each patch, map with a linear layer to width \(d\). \(N = HW/P^2\) tokens. Add a learned **[CLS]** if you classify, and add **positions** (row-column, or a 1-D index).

![An image cut into a sequence of patches](files/data-643/graphics/4.2-vision-transformers/patches.png)

A CNN shares a small kernel and builds a hierarchy. A ViT sees global context in layer 1, at \(O(N^2)\) cost. For a 224 image and \(P=16\), \(N=196\), which is a short paragraph.

---

## 2. The same stack

![Patches, positions, transformer, features](files/data-643/graphics/4.2-vision-transformers/vit.png)

Dosovitskiy et al. (2021): ViTs need more data than ResNets if trained from scratch; they shine with scale. In this course you will almost always **start from a pretrained** ViT (CLIP’s image tower, or a Hugging Face checkpoint), not from random pixels.

Hybrid: a small CNN stem, then a transformer. Same idea.

---

## 3. Practice

1. Count tokens for a \(384\times 384\) image, patch \(16\).

2. Why add positions if attention already sees all patches?

3. A medical image dataset with 800 scans: from-scratch ViT or a pretrained tower? Why?
