These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

**Contrastive learning** pulls matched pairs together and pushes unmatched pairs apart, in a shared space. **Zero-shot** transfer is what you get when one side of the pair can be a class name written as text. This is a **coordination** loss: two towers, a similarity, no fused decoder. Week 5 will put CLIP’s data and retrieval on the table. This note is the loss and the zero-shot trick.

---

## 1. What contrastive learning and zero-shot classification are

**Contrastive learning** pulls matched pairs together and pushes the rest apart. Take \(N\) images and \(N\) captions. Encode both. Cosine similarities form an \(N\times N\) matrix. The loss (InfoNCE; Oord et al. 2018) wants the **diagonal** hot: image \(i\) with caption \(i\), not caption \(j\).

![Matched pairs on the diagonal](files/data-643/graphics/4.3-contrastive-zeroshot/contrastive.png)

This is coordinated representation (note **4.1**) with a specific loss. You never fuse pixels and words into one vector during pretraining; you only score pairs. SimCLR is the vision-only cousin (two crops of the same image). We cite it; we do not assign it.

**Zero-shot** classification is: classify by nearest prompt, not a \(C\)-way trained head. At test time, encode the image once. Encode prompts `"a photo of a dog"`, `"a photo of a cat"`, and so on. Take the nearest prompt. There is no trained softmax over ImageNet. New classes are new strings.

![Class names as text embeddings](files/data-643/graphics/4.3-contrastive-zeroshot/zeroshot.png)

CLIP was trained on **phrases**. The raw label `"dog"` often loses to `"a photo of a dog"`. Prompt **ensembling** (average several phrasings) is a test-time trick, not a new model. We mention it; Lab 4 does not require it.

A class the text tower never saw as a phrase will not magically appear. Open-vocabulary is not infinite-vocabulary.

---

## 2. Why we use it

You may not have labels for every class at train time. A similarity space transfers to new names: adding a class is adding a string, not training a new column of a softmax. That is why CLIP-style models are called foundation models for vision–language, and why this course treats contrastive learning as a method rather than a trick.

A \(C\)-way head is the older default. It works when you have a labeled set for those \(C\) classes. It fails when the next user wants a class you did not train. Zero-shot is the transfer story that does not need that labeled set.

Web pairs are noisy (Week 5: BLIP filters them). Contrastive spaces can still be **biased** (Week 5.3). The loss does not make the space fair; it only makes matched pairs closer than unmatched ones.

---

## 3. Architecture

Two encoders (or two views of one network). A batch matrix of scores. Softmax over the row (or both directions).

Image \(i\) maps to \(\boldsymbol{v}_i=f(x_i)\). Text \(j\) maps to \(\boldsymbol{t}_j=g(y_j)\). The interaction is cosine, not a concatenating MLP. CLIP uses **both** directions (image-to-text and text-to-image). Temperature \(\tau\) sharpens the softmax. Small \(\tau\) makes the diagonal even more peaked, but the **argmax** of a row does not change if you only rescale that row.

The negative set is the rest of the batch. Small batches \(\Rightarrow\) easy negatives \(\Rightarrow\) a weak space. CLIP’s real batch was tens of thousands. Lab 4 is \(N=4\) so you can see the matrix, not so you can match ImageNet.

At test time the architecture does not grow a classification head. The classifier **is** the text tower, queried with class phrases.

---

## 4. How it works, step by step

Lab 4: four pairs, heatmap of the \(N\times N\) scores. The diagonal should win.

1. **Encode a batch.** \(N\) matched \((x_i,y_i)\) pairs. Image tower and text tower.
2. **Fill the matrix.** \(s_{ij}=\cos(\boldsymbol{v}_i,\boldsymbol{t}_j)\). The diagonal is the true matches; the off-diagonal entries are **negatives**, not “don’t care.”
3. **InfoNCE on each row.** Softmax over captions for a fixed image; the loss is \(-\log\) of the diagonal probability. CLIP also does the other direction.
4. **Zero-shot at test.** Freeze both towers. Embed the image. Embed one prompt per class. Predict \(\arg\max_c \cos(f(x),g(\text{prompt}_c))\).
5. **Do not add a class the text tower cannot spell.** Open-vocabulary is not infinite-vocabulary.

If every caption is the same vector, every row of \(S\) is constant, softmax is uniform, and the diagonal is not special: **the loss cannot learn matching**.

---

## 5. Mathematical formulas

Let \(s_{ij}=\cos(u_i,v_j)\). InfoNCE, one direction, averaged over the batch:

\[
\mathcal{L}=-\frac{1}{N}\sum_i \log \frac{\exp(s_{ii}/\tau)}{\sum_j \exp(s_{ij}/\tau)}.
\]

Row \(i\) alone is

\[
-\log \frac{\exp(\mathrm{sim}(\boldsymbol{v}_i,\boldsymbol{t}_i)/\tau)}{\sum_{j=1}^{N}\exp(\mathrm{sim}(\boldsymbol{v}_i,\boldsymbol{t}_j)/\tau)}.
\]

Zero-shot: embed class phrases, pick

\[
\hat{c}=\arg\max_c \cos\bigl(f(x),g(\text{prompt}_c)\bigr).
\]

Dividing the cosines by \(\tau\) before a softmax changes the distribution, not the argmax of a single row of scores.

---

## 6. Positive points and negative points

**Positive.**

- No \(C\)-way head at train time; new classes can be new prompts.
- The same space supports retrieval (rank by cosine) and zero-shot classification.
- Lab 4’s \(N=4\) grid is the whole method in miniature.

**Negative.**

- Needs big batches so the negatives are hard enough.
- Temperature \(\tau\) is a knob: it sharpens, it does not change argmax on one row.
- Compositionality is not free; a batch of 4 will not teach “mug in grass” versus “grass in a mug.”
- A class the text tower never saw as a phrase will not appear at test time.

**When not to.** If you already have a labeled set for a fixed \(C\) and you only need those \(C\) classes, a linear probe on a frozen encoder can be the tighter transfer. Zero-shot is for names you did not train as a head.

---

## 7. Linear probe versus zero-shot

![A trained C-way head versus nearest prompt](files/data-643/graphics/4.3-contrastive-zeroshot/probe-vs-zeroshot.png)

**Linear probe:** freeze the image encoder, train a \(C\)-way softmax on labeled images. Needs a training set for those \(C\) classes.

**Zero-shot:** no extra weights. The classifier is the text tower. Adding a class is adding a string.

Both are transfer. Zero-shot is what makes CLIP a **foundation** model. Captioning, LLaVA, and Flamingo wait for later weeks.

---

## 8. Teaching this note

**~18 minutes.** Draw the \(N\times N\) grid, mark the diagonal, write InfoNCE for \(N=2\), then swap the text side for class prompts, then probe vs zero-shot. Play the CLIP video on **zero-shot** and **the similarity matrix** (**9:00–22:25**). Lab 4’s tiny InfoNCE is this grid with \(N=4\).

---

## 9. Worked example

Two pairs. Cosine matrix (already normalized):

\[
S=\begin{bmatrix}0.9&0.1\\0.2&0.8\end{bmatrix},\qquad \tau=1.
\]

Row 0 softmax: \(e^{0.9}\approx 2.46\), \(e^{0.1}\approx 1.11\), so \([0.69,\,0.31]\). InfoNCE term \(-\log 0.69\approx 0.37\).

![Two-row InfoNCE](files/data-643/graphics/4.3-contrastive-zeroshot/infonce-numeric.png)

If every caption is the same vector, every row of \(S\) is constant, softmax is uniform, and the diagonal is not special: **the loss cannot learn matching**.

Zero-shot: image \(\boldsymbol{v}=\begin{bmatrix}1\\0\end{bmatrix}\), prompts \(\text{dog}=\begin{bmatrix}0.9\\0.1\end{bmatrix}\), \(\text{cat}=\begin{bmatrix}0.1\\0.9\end{bmatrix}\). Cosines \(0.99\) vs \(0.10\). Predict dog. Dividing by \(\tau=0.07\) before softmax does **not** change that argmax.

---

## 10. Where students get stuck

- Treating off-diagonal as “don’t care” instead of **negatives**.
- Adding a class at test time that the text tower cannot spell.
- Using batch size 4 in a real CLIP run and expecting ImageNet-level negatives.
- Calling zero-shot a trained ImageNet head.

---

## 11. Video

Watch [Yannic Kilcher: OpenAI CLIP, Connecting Text and Images](https://www.youtube.com/watch?v=T9XSU0pKX2E).

Pause on **zero-shot** (**9:00**) — class names as text — and on **InfoNCE / the \(N\times N\) matrix** (**14:40**). That matrix is the whole note.

---

## 12. Practice

1. If every caption in the batch is the word *photo*, what happens to the diagonal?

2. Why is `"a photo of a golden retriever"` often better than `"golden retriever"` for CLIP-style zero-shot?

3. Name one class you **cannot** add at test time by typing it.

4. For \(S=\begin{bmatrix}1&0\\0&1\end{bmatrix}\), \(\tau=1\), write the two InfoNCE row-losses (they should be \(0\)). Now change \(S_{01}\) to \(1\). Recompute row 0’s softmax and \(-\log p_{\text{diag}}\).

5. Three prompts with cosines to one image \(0.2, 0.5, 0.1\). Which class wins zero-shot? If you divide the cosines by \(\tau=0.07\) before softmax, does the **argmax** change?

6. Linear probe versus zero-shot: which one needs a labeled training set for the \(C\) classes?

7. CLIP uses both image-to-text and text-to-image InfoNCE. Why is one direction not enough if you also want to retrieve images from a caption?
