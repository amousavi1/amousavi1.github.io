These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

**Contrastive learning** pulls matched pairs together and pushes unmatched pairs apart, in a shared space. **Zero-shot** transfer is what you get when one side of the pair can be a class name written as text. This is a **coordination** loss: two towers, a similarity, no fused decoder.

Week 5 will put CLIP’s data and retrieval on the table. This note is the loss and the zero-shot trick.

---

> **First time this method appears.** **Contrastive learning** pulls matched pairs together and pushes the rest apart. **Zero-shot** is classify by nearest prompt, not a \(C\)-way trained head.
>
> **What.** InfoNCE on a batch of \(N\) matched pairs. Zero-shot: embed class phrases, pick \(\arg\max_c \cos(f(x),g(\text{prompt}_c))\).
> **Why.** You may not have labels for every class at train time. A similarity space transfers to new names.
> **Architecture.** Two encoders (or two views of one). A batch matrix of scores. Softmax over the row (or bidirectional).
> **How.** Lab 4: four pairs, heatmap of the \(N\times N\) scores. The diagonal should win.
> **Formula.** \(\mathcal{L}=-\frac{1}{N}\sum_i \log \frac{\exp(s_{ii}/\tau)}{\sum_j \exp(s_{ij}/\tau)}\), \(s_{ij}=\cos(u_i,v_j)\).
> **Tradeoffs.** + No \(C\)-way head, works with prompts. − Needs big batches (many negatives); temperature \(\tau\) is a knob; compositionality is not free.
>
## 1. A batch of matches

\(N\) images and \(N\) captions. Encode both. Cosine similarities form an \(N\times N\) matrix. The loss (InfoNCE; Oord et al. 2018) wants the **diagonal** hot: image \(i\) with caption \(i\), not caption \(j\).

![Matched pairs on the diagonal](files/data-643/graphics/4.3-contrastive-zeroshot/contrastive.png)

This is coordinated representation (note **4.1**) with a specific loss. You never fuse pixels and words into one vector during pretraining; you only score pairs. SimCLR is the vision-only cousin (two crops of the same image). We cite it; we do not assign it.

InfoNCE, one direction, row \(i\):

\[
-\log \frac{\exp(\mathrm{sim}(\boldsymbol{v}_i,\boldsymbol{t}_i)/\tau)}{\sum_{j=1}^{N}\exp(\mathrm{sim}(\boldsymbol{v}_i,\boldsymbol{t}_j)/\tau)}.
\]

CLIP uses **both** directions (image-to-text and text-to-image). Temperature \(\tau\) sharpens the softmax. Small \(\tau\) makes the diagonal even more peaked, but the **argmax** of a row does not change if you only rescale that row.

The negative set is the rest of the batch. Small batches \(\Rightarrow\) easy negatives \(\Rightarrow\) a weak space. CLIP’s real batch was tens of thousands. Lab 4 is \(N=4\) so you can see the matrix, not so you can match ImageNet.

---

## 2. Zero-shot classification

At test time, encode the image once. Encode prompts `"a photo of a dog"`, `"a photo of a cat"`, … Take the nearest prompt. There is no trained softmax over ImageNet. New classes are new strings.

![Class names as text embeddings](files/data-643/graphics/4.3-contrastive-zeroshot/zeroshot.png)

CLIP was trained on **phrases**. The raw label `"dog"` often loses to `"a photo of a dog"`. Prompt **ensembling** (average several phrasings) is a test-time trick, not a new model. We mention it; Lab 4 does not require it.

A class the text tower never saw as a phrase will not magically appear. Open-vocabulary is not infinite-vocabulary.

---

## 3. Linear probe versus zero-shot

![A trained C-way head versus nearest prompt](files/data-643/graphics/4.3-contrastive-zeroshot/probe-vs-zeroshot.png)

**Linear probe:** freeze the image encoder, train a \(C\)-way softmax on labeled images. Needs a training set for those \(C\) classes.

**Zero-shot:** no extra weights. The classifier is the text tower. Adding a class is adding a string.

Both are transfer. Zero-shot is what makes CLIP a **foundation** model. Captioning, LLaVA, and Flamingo wait for later weeks.

Web pairs are noisy (Week 5: BLIP filters them). Contrastive spaces can still be **biased** (Week 5.3).

---

## 4. Teaching this note

**~18 minutes.** Draw the \(N\times N\) grid, mark the diagonal, write InfoNCE for \(N=2\), then swap the text side for class prompts, then probe vs zero-shot. Play the CLIP video on **zero-shot** and **the similarity matrix** (**9:00–22:25**). Lab 4’s tiny InfoNCE is this grid with \(N=4\).

---

## 5. Worked example

Two pairs. Cosine matrix (already normalized):

\[
S=\begin{bmatrix}0.9&0.1\\0.2&0.8\end{bmatrix},\qquad \tau=1.
\]

Row 0 softmax: \(e^{0.9}\approx 2.46\), \(e^{0.1}\approx 1.11\), so \([0.69,\,0.31]\). InfoNCE term \(-\log 0.69\approx 0.37\).

![Two-row InfoNCE](files/data-643/graphics/4.3-contrastive-zeroshot/infonce-numeric.png)

If every caption is the same vector, every row of \(S\) is constant, softmax is uniform, and the diagonal is not special: **the loss cannot learn matching**.

Zero-shot: image \(\boldsymbol{v}=\begin{bmatrix}1\\0\end{bmatrix}\), prompts \(\text{dog}=\begin{bmatrix}0.9\\0.1\end{bmatrix}\), \(\text{cat}=\begin{bmatrix}0.1\\0.9\end{bmatrix}\). Cosines \(0.99\) vs \(0.10\). Predict dog. Dividing by \(\tau=0.07\) before softmax does **not** change that argmax.

---

## 6. Where students get stuck

- Treating off-diagonal as “don’t care” instead of **negatives**.
- Adding a class at test time that the text tower cannot spell.
- Using batch size 4 in a real CLIP run and expecting ImageNet-level negatives.
- Calling zero-shot a trained ImageNet head.

---

## 7. Video

Watch [Yannic Kilcher: OpenAI CLIP, Connecting Text and Images](https://www.youtube.com/watch?v=T9XSU0pKX2E).

Pause on **zero-shot** (**9:00**) — class names as text — and on **InfoNCE / the \(N\times N\) matrix** (**14:40**). That matrix is the whole note.

---

## 8. Practice

1. If every caption in the batch is the word *photo*, what happens to the diagonal?

2. Why is `"a photo of a golden retriever"` often better than `"golden retriever"` for CLIP-style zero-shot?

3. Name one class you **cannot** add at test time by typing it.

4. For \(S=\begin{bmatrix}1&0\\0&1\end{bmatrix}\), \(\tau=1\), write the two InfoNCE row-losses (they should be \(0\)). Now change \(S_{01}\) to \(1\). Recompute row 0’s softmax and \(-\log p_{\text{diag}}\).

5. Three prompts with cosines to one image \(0.2, 0.5, 0.1\). Which class wins zero-shot? If you divide the cosines by \(\tau=0.07\) before softmax, does the **argmax** change?

6. Linear probe versus zero-shot: which one needs a labeled training set for the \(C\) classes?

7. CLIP uses both image-to-text and text-to-image InfoNCE. Why is one direction not enough if you also want to retrieve images from a caption?
