These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

**CLIP** (Radford et al., 2021) is the coordinated, contrastive model that made zero-shot vision–language the default. Two towers, a cosine, a large batch of image–caption pairs from the web.

---

## 1. Two towers

An **image encoder** (ResNet or ViT) and a **text encoder** (a transformer). Both emit a vector in the same dimension. Training: InfoNCE on the batch (note **4.3**). After training you keep both towers; you do not keep a fused head.

![CLIP image and text towers](files/data-643/graphics/5.1-clip/clip-towers.png)

Open-source copies (OpenCLIP, SigLIP) change the loss or the data. The picture is stable.

The text tower never sees pixels. Retrieval still works because training put matched pairs at high cosine. A query string is just another text vector.

---

## 2. What CLIP is good at

- **Zero-shot** classification via prompts.
- **Cross-modal retrieval:** image \(\to\) text and text \(\to\) image (note **5.3**).
- A **frozen** image backbone for later captioners and diffusion models (Week 12).

What it is not: a captioner (it does not decode a sentence), a detector with boxes, or a guarantee of factual correctness. It scores pairs.

Temperature \(\tau\) (often learned, around \(0.07\)) sharpens the batch softmax. Small \(\tau\) makes off-diagonal competition brutal; that is why CLIP wanted huge batches.

---

## 3. Practical notes

Temperature \(\tau\) (often \(0.07\)) sharpens the softmax. Batch size wants to be large. Hugging Face `CLIPModel` plus a processor is enough for Lab 5’s *idea*; the lab itself uses a toy space so nobody waits on a download.

For a project: cite the checkpoint, freeze versus fine-tune, and write the prompts you used. Prompt choice is part of the method, not a footnote.

OpenCLIP and SigLIP are the checkpoints you can actually download. SigLIP replaces the softmax InfoNCE with a sigmoid on each pair; the two-tower picture does not change. If your project cites “CLIP,” name the Hugging Face id.

A frozen CLIP image tower is a common backbone for captioners (BLIP-2) and latent diffusion (Week 12). You are allowed to freeze it. You are not allowed to pretend freezing is fine-tuning.

---

## 4. Teaching this note

**30–40 minutes.** Two towers, cosine, “not a captioner,” then the \(\tau\) and batch-size arithmetic. Play the **full CLIP paper video** in class only as **selected chapters**: towers **4:40–9:00**, contrastive **14:40–22:25**, and a slice of results. Students can finish the hour as homework. Lab 5 is a 2-D fake CLIP, not OpenAI weights.

Minute plan: 10 min two towers; 10 min worked \(N=2\) and \(\tau\); 5 min “cannot decode a sentence”; 12 min video chapters. Assign the robustness half to note **5.3**.

---

## 5. Worked example

Batch \(N=2\). Image vectors \(\boldsymbol{v}_1=\begin{bmatrix}1\\0\end{bmatrix}\), \(\boldsymbol{v}_2=\begin{bmatrix}0\\1\end{bmatrix}\). Text \(\boldsymbol{t}_1=\begin{bmatrix}1\\0\end{bmatrix}\), \(\boldsymbol{t}_2=\begin{bmatrix}0.1\\0.9\end{bmatrix}\) (already \(\ell_2\)-normalized).

Cosines: \(S_{11}=1\), \(S_{12}=0.1\), \(S_{21}=0\), \(S_{22}=0.9\).

With \(\tau=1\), row 1 softmax on \([1, 0.1]\) is already peaked on the match. With \(\tau=0.07\), the logits are \([1/0.07,\,0.1/0.07]\approx[14.3,\,1.43]\). The diagonal probability is essentially \(1\). Small batches still have only **one** negative; a batch of 1024 has 1023.

CLIP cannot emit “a cat sits on a mat” unless that string is already in your gallery. That generation job is BLIP.

Write the API on the board: `encode_image`, `encode_text`, `cosine`. Three calls. No `generate`. If a student wants captions, point them at note **5.2**.

---

## 6. Where students get stuck

- Asking CLIP to **write** a caption.
- Fine-tuning a fused head and throwing away the text tower (you can no longer query with words).
- Ignoring \(\tau\) and wondering why a 2-D toy with \(\tau=1\) looks “softer” than the paper.

---

## 7. Video

Watch [Yannic Kilcher: OpenAI CLIP, Connecting Text and Images](https://www.youtube.com/watch?v=T9XSU0pKX2E) (full paper video).

In class, pause on two towers, the InfoNCE matrix, zero-shot prompts, and the remark that prompt wording is engineering. Watch the rest after class.

---

## 8. Practice

1. CLIP’s text tower never sees the pixels. How can a typed query retrieve a photo?

2. Why does a batch of 8 give weaker negatives than a batch of 1024?

3. You need generated captions, not retrieval. Which Week 5 model is the closer ancestor?

4. For logits \([2, 0]\) (already divided by \(\tau\)), compute the softmax probability on the positive. Repeat for \([2/0.07,\, 0]\). Compare the exponents \(2\) vs \(2/0.07\): which temperature makes the positive dominate?

5. Two gallery texts \(\boldsymbol{t}_{\text{cat}}=\begin{bmatrix}1\\0\end{bmatrix}\), \(\boldsymbol{t}_{\text{dog}}=\begin{bmatrix}0\\1\end{bmatrix}\), query image \(\boldsymbol{v}=\begin{bmatrix}0.6\\0.8\end{bmatrix}\). Rank the texts by cosine. Who is retrieved at rank 1?
