These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

**CLIP** (Radford et al., 2021) is the coordinated, contrastive model that made zero-shot vision–language the default. After training you have a **similarity score** between an image and a text, not a captioner. Note **4.3** already taught InfoNCE and the zero-shot trick. This note is the two-tower product: what you keep, what you call at test time, and why batch size and temperature are part of the method.

---

## 1. What CLIP is

**CLIP** is two towers and a cosine. An **image encoder** (ResNet or ViT) and a **text encoder** (a transformer) both emit a vector in the same dimension. Training is InfoNCE on the batch (note **4.3**). After training you keep both towers; you do not keep a fused head. The model scores image–text pairs. It does not write a caption.

![CLIP image and text towers](files/data-643/graphics/5.1-clip/clip-towers.png)

The text tower never sees pixels. Retrieval still works because training put matched pairs at high cosine. A query string is just another text vector.

Open-source copies (OpenCLIP, SigLIP) change the loss or the data. The picture is stable. SigLIP replaces the softmax InfoNCE with a sigmoid on each pair; you still have two towers and a score.

Write the API on the board: `encode_image`, `encode_text`, `cosine`. Three calls. No `generate`.

---

## 2. Why we use it

One model that retrieves and zero-shot classifies without a detector or a decoder. That is the product reason CLIP became the default vision–language backbone.

- **Zero-shot** classification via prompts (`a photo of a dog`).
- **Cross-modal retrieval:** image \(\to\) text and text \(\to\) image (note **5.3**).
- A **frozen** image backbone for later captioners and diffusion models (Week 12).

What it is not: a captioner (it does not decode a sentence), a detector with boxes, or a guarantee of factual correctness. It scores pairs.

**CoCa** is next after CLIP: add a decoder with a captioning loss. That generation job is note **5.2** (BLIP). Do not skip from CLIP to LLaVA in this hour.

Prompt wording is part of the method. A single phrase can be too peaked; ensembling `"a photo of"`, `"a drawing of"`, and similar templates is optional engineering, not a new model.

---

## 3. Architecture

Two separate encoders, a shared embedding dimension, and a cosine. No concatenated pixels-and-tokens vector during pretraining.

The image tower can be a ResNet or a ViT (note **4.2**). The text tower is a transformer that encodes a whole caption into one vector. Both outputs are \(\ell_2\)-normalized before the cosine, so the score is a dot product of unit vectors.

You never call `generate`. Hugging Face `CLIPModel` plus a processor is enough for Lab 5’s *idea*; the lab itself uses a toy space so nobody waits on a download. If a project cites “CLIP,” name the Hugging Face id. Freezing is allowed. Pretending freeze is fine-tune is not.

SigLIP keeps the same two-tower picture and changes the pairwise loss. Do not treat a new checkpoint name as a new architecture unless the paper adds a decoder.

---

## 4. How it works, step by step

Train on web image–text pairs. At test, embed the image and a list of prompts. Note 5.2 adds a decoder (BLIP).

1. **Index a batch.** \(N\) images, \(N\) captions, already matched as web pairs.
2. **Encode.** `encode_image` and `encode_text`. \(\ell_2\)-normalize.
3. **Score.** Fill the \(N\times N\) cosine matrix. InfoNCE wants the diagonal, both directions, with temperature \(\tau\) (often learned, around \(0.07\)).
4. **Keep both towers.** Throw away the training matrix. You now have two encoders you can call independently.
5. **Zero-shot or retrieve.** Embed the image once; embed prompts or gallery texts; rank by cosine.

Temperature \(\tau\) sharpens the batch softmax. Small \(\tau\) makes off-diagonal competition brutal; that is why CLIP wanted huge batches.

CLIP-style models **rely on batch size** to learn fine-grained concepts. A batch of 8 has 7 negatives. A batch of 32{,}768 has 32{,}767. You still will not see both “a mug in grass” and “grass in a mug” in one batch; compositionality is a later paper, not this lecture.

A batch of 2 still has only **one** negative. CLIP cannot emit “a cat sits on a mat” unless that string is already in your gallery. That generation job is BLIP.

---

## 5. Mathematical formulas

Same InfoNCE as note **4.3**, with a learned temperature. For \(\ell_2\)-normalized vectors, cosine is a dot product. The image-to-text term on row \(i\) uses logits \(S_{ij}/\tau\):

\[
\mathcal{L}_{\text{i2t}}=-\frac{1}{N}\sum_i\log\frac{\exp(S_{ii}/\tau)}{\sum_j\exp(S_{ij}/\tau)},\qquad S_{ij}=\boldsymbol{v}_i^{\top}\boldsymbol{t}_j.
\]

CLIP averages this with the text-to-image direction. The public API is three calls: \(f(i)\), \(g(t)\), then \(\cos(f(i),g(t))\).

Small \(\tau\) does not change the argmax of a row of \(S\); it changes how peaked the softmax is during training.

---

## 6. Positive points and negative points

**Positive.**

- Zero-shot classification and both directions of retrieval from one pair of towers.
- A frozen image backbone you can reuse in captioners and diffusion models.
- Open copies (OpenCLIP, SigLIP) keep the same picture if you name the checkpoint.

**Negative.**

- Not a captioner: there is no `generate`.
- Hungry for batch size; a batch of 8 is a weak negative set.
- Prompt wording is part of the method, not a footnote.
- Bias and typographic attacks wait for note **5.3**; a high cosine is not a fairness certificate.
- Fine-tuning a fused head and throwing away the text tower means you can no longer query with words.

**When not to.** You need generated captions, not retrieval. Use BLIP (or CoCa’s decoder), not CLIP.

---

## 7. Teaching this note

**30–40 minutes.** Two towers, cosine, “not a captioner,” then the \(\tau\) and batch-size arithmetic. Play the **CLIP paper video** in class as **selected chapters**: towers **4:40–9:00**, contrastive **14:40–22:25**. Students can finish the hour as homework. Lab 5 is a 2-D fake CLIP, not OpenAI weights.

Minute plan: 10 min two towers; 10 min worked \(N=2\) and \(\tau\); 5 min “cannot decode a sentence”; 12 min video chapters. Assign robustness to note **5.3**.

---

## 8. Worked example

Batch \(N=2\). Already \(\ell_2\)-normalized:

\[
\boldsymbol{v}_1=\begin{bmatrix}1\\0\end{bmatrix},\;
\boldsymbol{v}_2=\begin{bmatrix}0\\1\end{bmatrix},\;
\boldsymbol{t}_1=\begin{bmatrix}1\\0\end{bmatrix},\;
\boldsymbol{t}_2=\begin{bmatrix}0.6\\0.8\end{bmatrix}.
\]

Cosines (the matrix \(S\)):

\[
S=\begin{bmatrix}1.0 & 0.6\\ 0.0 & 0.8\end{bmatrix}.
\]

![A 2 by 2 cosine matrix](files/data-643/graphics/5.1-clip/clip-numeric.png)

InfoNCE on **row 1** uses logits \(S_{1j}/\tau\). With \(\tau=1\),

\[
\operatorname{softmax}([1.0,\,0.6])\approx [0.60,\,0.40],
\qquad -\log 0.60 \approx 0.51.
\]

With \(\tau=0.07\), the logits are \([14.3,\,8.6]\). The match probability is about \(0.997\). Same scores; the temperature did the work.

![Temperature sharpens the same scores](files/data-643/graphics/5.1-clip/clip-tau.png)

A batch of 2 still has only **one** negative. CLIP cannot emit “a cat sits on a mat” unless that string is already in your gallery. That generation job is BLIP.

---

## 9. Where students get stuck

- Asking CLIP to **write** a caption.
- Fine-tuning a fused head and throwing away the text tower (you can no longer query with words).
- Ignoring \(\tau\) and wondering why a 2-D toy with \(\tau=1\) looks “softer” than the paper.
- Using \([0.1, 0.9]\) and calling it unit length. Check \(\|\boldsymbol{t}\|_2=1\) before you trust the cosine.

---

## 10. Video

Watch [Yannic Kilcher: OpenAI CLIP, Connecting Text and Images](https://www.youtube.com/watch?v=T9XSU0pKX2E) (full paper video).

In class, pause on two towers, the InfoNCE matrix, zero-shot prompts, and the remark that prompt wording is engineering. Watch the rest after class.

---

## 11. Practice

1. CLIP’s text tower never sees the pixels. How can a typed query retrieve a photo?

2. Why does a batch of 8 give weaker negatives than a batch of 1024?

3. You need generated captions, not retrieval. Which Week 5 model is the closer ancestor?

4. For logits \([2, 0]\) (already divided by \(\tau\)), compute the softmax probability on the positive. Repeat for \([2/0.07,\, 0]\). Which temperature makes the positive dominate?

5. Two gallery texts \(\boldsymbol{t}_{\text{cat}}=\begin{bmatrix}1\\0\end{bmatrix}\), \(\boldsymbol{t}_{\text{dog}}=\begin{bmatrix}0\\1\end{bmatrix}\), query image \(\boldsymbol{v}=\begin{bmatrix}0.6\\0.8\end{bmatrix}\) (already unit). Rank the texts by cosine. Who is retrieved at rank 1?
