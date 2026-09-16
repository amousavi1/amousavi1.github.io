These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

Self-attention is a weighted sum of **values**, with weights from a comparison of **queries** to **keys**. Every token plays all three roles. That is the calculation, and Lab 3. By the end you should be able to write the scaled-dot formula, fill a \(2\times 2\) softmax table, and mask the future with \(-\infty\), not zero.

---

## 1. What self-attention is

**Self-attention** is the calculation inside a transformer layer. A weighted sum of **values**, with weights from **queries** compared to **keys**. Every token plays all three roles.

For a sequence matrix \(X\in\mathbb{R}^{T\times d}\),

\[
Q = X W_Q,\quad K = X W_K,\quad V = X W_V.
\]

**Query:** what this token is looking for. **Key:** what another token looks like to be found. **Value:** what you actually add into the representation.

Row \(t\) of \(QK^{\top}\) is “how much token \(t\) wants each position.” Softmax makes that a distribution. Then you mix **values**, not keys. Mixing keys is a common lab bug.

![Query, key, value, then a mix of values](files/data-643/graphics/3.2-self-attention/qkv.png)

**Self** versus **cross.** Self-attention: \(Q,K,V\) all from the same sequence. Cross-attention (encoder–decoder, later BLIP): queries from one sequence, keys and values from another. Same formula.

---

## 2. Why we use it

RNNs mix left-to-right through \(h_t\). Self-attention mixes any pair in one layer, in parallel. Note 3.1 argued for path length 1; this note is the arithmetic that implements it.

**Why \(\sqrt{d_k}\).** If the coordinates of \(q\) and \(k\) are roughly independent with variance 1, the dot product has variance \(d_k\). Large \(d_k\) pushes softmax toward a one-hot. Dividing by \(\sqrt{d_k}\) puts the logits back in a range where softmax still mixes. Skipping the scale, or dividing by \(d_k\) instead, is the other common exam slip.

Several heads in parallel let different slices of the channels track syntax, a name, or a comma. One head is enough to compute by hand in Lab 3; multi-head is why the layer is not a single average.

---

## 3. Architecture

Three matrices map \(X\) to \(Q,K,V\). Scores are \(QK^{\top}/\sqrt{d_k}\), softmax over keys, then mix \(V\):

\[
A = \mathrm{softmax}\left(\frac{Q K^{\top}}{\sqrt{d_k}}\right),
\qquad
\mathrm{Attention}(Q,K,V) = A V.
\]

**Multi-head:** several \((W_Q,W_K,W_V)\) in parallel, each on a slice of the channels (head dimension \(d_k=d/h\)). Concatenate the head outputs, then a linear \(W_O\). Concat is not a residual, and \(W_O\) is part of attention’s parameter count in note 3.3.

![Two heads, concatenate, project](files/data-643/graphics/3.2-self-attention/multihead.png)

Lab 3 computes **one** head by hand. You do not need eight heads on the board.

For next-token prediction you **mask** future keys (set scores to \(-\infty\) before softmax). Otherwise the model cheats. BERT does not mask the future; it masks random **tokens** and reconstructs them (note **3.4**). Those are two different uses of the word *mask*.

Zero is the wrong fill-in: \(\mathrm{softmax}([1,0])\) still puts mass on the “zero.” \(-\infty\) becomes probability \(0\).

![Causal mask zeros out the future](files/data-643/graphics/3.2-self-attention/causal-mask.png)

---

## 4. How it works, step by step

1. Form \(Q,K,V\) from \(X\) (or, in a tiny drill, start from scores \(S=QK^{\top}\) already).
2. Scale: divide by \(\sqrt{d_k}\).
3. If this is a language model, set illegal future scores to \(-\infty\).
4. Softmax **over keys** (last dim / each row), not over columns.
5. Multiply the resulting distribution by \(V\). Output row \(t\) is a mix of **values**.

Row \(t\) of \(A\) is a distribution over the sequence. Large mass on a name is “this pronoun just looked at that name.”

![Attention weights for one head](files/data-643/graphics/3.2-self-attention/attn-heatmap.png)

If two keys are equal, the softmax splits mass equally between them (given the same query). That is not a tie-break bug; it is the definition.

Lab 3 is this procedure at \(T=4\): one head by hand, then a causal mask. Do not start that notebook until the \(2\times 2\) arithmetic below has been done once on paper.

---

## 5. Mathematical formulas

The layer:

\[
\operatorname{Attention}(Q,K,V)=\operatorname{softmax}\bigl(QK^{\top}/\sqrt{d_k}\bigr)V,
\]

with \(Q=XW_Q\), \(K=XW_K\), \(V=XW_V\).

Causal mask: before the softmax, illegal (future) entries of \(QK^{\top}/\sqrt{d_k}\) are set to \(-\infty\), so those probabilities become 0.

Multi-head: \(h\) heads, each of width \(d_k=d/h\); concatenate, then \(W_O\). If two heads each emit a 2-D vector and the model width is \(d=4\), \(W_O\) maps the concatenated 4-D vector back to width 4.

---

## 6. Positive points and negative points

**Positive.**

- Parallel over tokens, path length 1: any pair can interact in one layer.
- Multi-head specialization: different heads can track syntax, a name, or a comma.
- The same formula covers self-attention and cross-attention; only which sequence supplies \(Q\) versus \(K,V\) changes.
- A heatmap of \(A\) is a debug tool (Lab 3), not just a picture.

**Negative.**

- \(O(T^2)\) scores per head per layer, as note 3.1 already billed.
- Mixing **keys** instead of values is a common bug; the softmax weights multiply \(V\).
- No positions until note 3.3: attention is a set operation unless you add order.
- Dividing by \(d_k\) instead of \(\sqrt{d_k}\), or skipping the scale, peaks or flattens softmax for the wrong reason.
- Masking with \(0\) instead of \(-\infty\) still puts mass on the illegal key.
- Softmax over the wrong axis (columns instead of keys) silently permutes the mix.

**When not to.** If the task is next-token prediction, bidirectional self-attention is cheating. Use a causal mask. BERT’s token mask is a different objective (note 3.4), not a substitute for that triangular mask.

---

## 7. Teaching this note

**~18 minutes.** Define Q, K, V in one sentence each, write the scaled-dot formula, grind the \(2\times 2\) table (including \(\sqrt{d_k}\)), then the causal mask. Play **the QKV and softmax stretch** of 3Blue1Brown attention (about **4:00–16:00**). Lab 3 is \(T=4\); do not start that notebook until this arithmetic is done once by hand.

---

## 8. Worked example

\(T=2\), \(d_k=2\), skip \(W_Q\) and take scores \(S=QK^{\top}\) already:

\[
S=\begin{bmatrix}2&0\\0&2\end{bmatrix},\qquad
\frac{S}{\sqrt{2}}\approx\begin{bmatrix}1.41&0\\0&1.41\end{bmatrix}.
\]

Row 1 softmax: \(e^{1.41}\approx 4.10\), \(e^{0}=1\), so \([4.10,1]/5.10\approx [0.80,\,0.20]\).

Row 2 is the same on the diagonal: \(A\approx\begin{bmatrix}0.80&0.20\\0.20&0.80\end{bmatrix}\).

![Scaled scores to a mix of values](files/data-643/graphics/3.2-self-attention/qkv-numeric.png)

If \(V=I\), then \(AV=A\). Each output is 80% “self” and 20% “the other token.”

Causal mask on row 1: set the future score to \(-\infty\). Then row 1 softmax is \([1,0]\): token 1 cannot look at token 2.

Without the \(\sqrt{2}\), row 1 would be \(\mathrm{softmax}([2,0])\approx [0.88,0.12]\): more peaked. That is the scale’s job.

---

## 9. Where students get stuck

- Softmax over the wrong axis (columns instead of keys / last dim).
- Dividing by \(d_k\) instead of \(\sqrt{d_k}\), or skipping the scale.
- Masking with \(0\) instead of \(-\infty\).
- Mixing keys instead of values.

---

## 10. Video

Watch [3Blue1Brown: Attention in transformers, visually explained](https://www.youtube.com/watch?v=eMlx5fFNoYc).

Pause when queries and keys meet as a grid of dots, when softmax turns a row into a distribution, and when values are mixed. That grid is Lab 3’s heatmap.

---

## 11. Practice

1. If two tokens have identical keys, what does the softmax do to their weights?

2. Why divide by \(\sqrt{d_k}\)?

3. Write \(A\) for \(T=2\) with \(Q=K=V=I\) (identity), no mask. What is \(AV\)?

4. Softmax the row \([0, 2]\). Then softmax \([0, 2]/\sqrt{2}\). Did the larger entry gain or lose probability after scaling?

5. Scores \(\begin{bmatrix}1& 3\\ 0& 1\end{bmatrix}\), causal mask (upper triangle \(-\infty\)). Write the masked score matrix, then \(A\) (row-wise softmax).

6. Self-attention versus cross-attention: which matrices come from which sequence?

7. Two heads each emit a 2-D vector. After concat, what width does \(W_O\) map back to if the model width is \(d=4\)?
