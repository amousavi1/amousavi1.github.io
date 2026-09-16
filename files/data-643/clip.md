These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

**CLIP** (Radford et al., 2021) is the coordinated, contrastive model that made zero-shot vision–language the default. After training you have a **similarity score** between an image and a text, not a captioner.

---

> **First time this method appears.** **CLIP** is two towers and a cosine. It scores image–text pairs. It does not write a caption.
>
> **What.** Image encoder + text encoder, InfoNCE on the batch, keep both towers.
> **Why.** One model that retrieves and zero-shot classifies without a detector or a decoder.
> **Architecture.** `encode_image`, `encode_text`, cosine. No `generate`.
> **How.** Train on web pairs. At test, embed the image and a list of prompts. Note 5.2 adds a decoder (BLIP).
> **Formula.** Same InfoNCE as 4.3 with learned \(\tau\). API is three calls.
> **Tradeoffs.** + Zero-shot and retrieval. − Not a captioner; hungry for batch size; prompt wording is method; bias next note.
>
## 1. Two towers

An **image encoder** (ResNet or ViT) and a **text encoder** (a transformer). Both emit a vector in the same dimension. Training: InfoNCE on the batch (note **4.3**). After training you keep both towers; you do not keep a fused head.

![CLIP image and text towers](files/data-643/graphics/5.1-clip/clip-towers.png)

The text tower never sees pixels. Retrieval still works because training put matched pairs at high cosine. A query string is just another text vector.

Open-source copies (OpenCLIP, SigLIP) change the loss or the data. The picture is stable. SigLIP replaces the softmax InfoNCE with a sigmoid on each pair; you still have two towers and a score.

Write the API on the board: `encode_image`, `encode_text`, `cosine`. Three calls. No `generate`.

---

## 2. What CLIP is good at, and what it is not

- **Zero-shot** classification via prompts (`a photo of a dog`).
- **Cross-modal retrieval:** image \(\to\) text and text \(\to\) image (note **5.3**).
- A **frozen** image backbone for later captioners and diffusion models (Week 12).

What it is not: a captioner (it does not decode a sentence), a detector with boxes, or a guarantee of factual correctness. It scores pairs.

**CoCa** is next after CLIP: add a decoder with a captioning loss. That generation job is note **5.2** (BLIP). Do not skip from CLIP to LLaVA in this hour.

Prompt wording is part of the method. A single phrase can be too peaked; ensembling `"a photo of"`, `"a drawing of"`, … is optional engineering, not a new model.

---

## 3. Temperature and batch size

Temperature \(\tau\) (often learned, around \(0.07\)) sharpens the batch softmax. Small \(\tau\) makes off-diagonal competition brutal; that is why CLIP wanted huge batches.

CLIP-style models **rely on batch size** to learn fine-grained concepts. A batch of 8 has 7 negatives. A batch of 32{,}768 has 32{,}767. You still will not see both “a mug in grass” and “grass in a mug” in one batch; compositionality is a later paper, not this lecture.

Hugging Face `CLIPModel` plus a processor is enough for Lab 5’s *idea*; the lab itself uses a toy space so nobody waits on a download. If a project cites “CLIP,” name the Hugging Face id. Freezing is allowed. Pretending freeze is fine-tune is not.

---

## 4. Teaching this note

**30–40 minutes.** Two towers, cosine, “not a captioner,” then the \(\tau\) and batch-size arithmetic. Play the **CLIP paper video** in class as **selected chapters**: towers **4:40–9:00**, contrastive **14:40–22:25**. Students can finish the hour as homework. Lab 5 is a 2-D fake CLIP, not OpenAI weights.

Minute plan: 10 min two towers; 10 min worked \(N=2\) and \(\tau\); 5 min “cannot decode a sentence”; 12 min video chapters. Assign robustness to note **5.3**.

---

## 5. Worked example

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

## 6. Where students get stuck

- Asking CLIP to **write** a caption.
- Fine-tuning a fused head and throwing away the text tower (you can no longer query with words).
- Ignoring \(\tau\) and wondering why a 2-D toy with \(\tau=1\) looks “softer” than the paper.
- Using \([0.1, 0.9]\) and calling it unit length. Check \(\|\boldsymbol{t}\|_2=1\) before you trust the cosine.

---

## 7. Video

Watch [Yannic Kilcher: OpenAI CLIP, Connecting Text and Images](https://www.youtube.com/watch?v=T9XSU0pKX2E) (full paper video).

In class, pause on two towers, the InfoNCE matrix, zero-shot prompts, and the remark that prompt wording is engineering. Watch the rest after class.

---

## 8. Practice

1. CLIP’s text tower never sees the pixels. How can a typed query retrieve a photo?

2. Why does a batch of 8 give weaker negatives than a batch of 1024?

3. You need generated captions, not retrieval. Which Week 5 model is the closer ancestor?

4. For logits \([2, 0]\) (already divided by \(\tau\)), compute the softmax probability on the positive. Repeat for \([2/0.07,\, 0]\). Which temperature makes the positive dominate?

5. Two gallery texts \(\boldsymbol{t}_{\text{cat}}=\begin{bmatrix}1\\0\end{bmatrix}\), \(\boldsymbol{t}_{\text{dog}}=\begin{bmatrix}0\\1\end{bmatrix}\), query image \(\boldsymbol{v}=\begin{bmatrix}0.6\\0.8\end{bmatrix}\) (already unit). Rank the texts by cosine. Who is retrieved at rank 1?
