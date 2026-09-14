These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

Self-attention is a weighted sum of **values**, with weights from a comparison of **queries** to **keys**. Every token plays all three roles.

---

## 1. Q, K, V

For a sequence matrix \(X\in\mathbb{R}^{T\times d}\),

\[
Q = X W_Q,\quad K = X W_K,\quad V = X W_V.
\]

Scores are scaled dot products, then a softmax over keys:

\[
A = \mathrm{softmax}\left(\frac{Q K^{\top}}{\sqrt{d_k}}\right),
\qquad
\mathrm{Attention}(Q,K,V) = A V.
\]

The \(\sqrt{d_k}\) keeps the dots from saturating the softmax when \(d_k\) is large.

![Query, key, value, then a mix of values](files/data-643/graphics/3.2-self-attention/qkv.png)

**Query:** what this token is looking for. **Key:** what another token looks like to be found. **Value:** what you actually add into the representation.

Row \(t\) of \(QK^{\top}\) is “how much token \(t\) wants each position.” Softmax makes that a distribution. Then you mix **values**, not keys. Mixing keys is a common lab bug.

---

## 2. A row of weights

Row \(t\) of \(A\) is a distribution over the sequence. Large mass on a name is “this pronoun just looked at that name.”

![Attention weights for one head](files/data-643/graphics/3.2-self-attention/attn-heatmap.png)

**Multi-head:** several \((W_Q,W_K,W_V)\) in parallel, concatenate, project. Different heads can track syntax, a name, or a comma. Lab 3 will compute one head by hand.

If two keys are equal, the softmax splits mass equally between them (given the same query). That is not a tie-break bug; it is the definition.

---

## 3. Masks

For next-token prediction you **mask** future keys (set scores to \(-\infty\) before softmax). Otherwise the model cheats. BERT does not mask the future; it masks random tokens and reconstructs them (note **3.4**).

Zero is the wrong mask fill-in: \(\mathrm{softmax}([1,0])\) still puts mass on the “zero.” \(-\infty\) becomes probability \(0\).

---

## 4. Teaching this note

**30–40 minutes.** Define Q, K, V in one sentence each, write \(A=\mathrm{softmax}(QK^{\top}/\sqrt{d_k})\), then grind the \(2\times 2\) worked example on the board (including \(\sqrt{d_k}\)). Play **the QKV and softmax stretch** of 3Blue1Brown attention (about **4:00–16:00**). Lab 3 is \(T=4\); do not start that notebook until this arithmetic is done once by hand.

---

## 5. Worked example

\(T=2\), \(d_k=2\), skip \(W_Q\) and take scores \(S=QK^{\top}\) already:

\[
S=\begin{bmatrix}2&0\\0&2\end{bmatrix},\qquad
\frac{S}{\sqrt{2}}\approx\begin{bmatrix}1.41&0\\0&1.41\end{bmatrix}.
\]

Row 1 softmax: \(e^{1.41}\approx 4.10\), \(e^{0}=1\), so \([4.10,1]/5.10\approx [0.80,\,0.20]\).

Row 2 is the same on the diagonal: \(A\approx\begin{bmatrix}0.80&0.20\\0.20&0.80\end{bmatrix}\).

If \(V=\begin{bmatrix}1&0\\0&1\end{bmatrix}\), then \(AV\approx A\). Each output is 80% “self” and 20% “the other token.”

Causal mask on row 1: set the future score to \(-\infty\). Then row 1 softmax is \([1,0]\): token 1 cannot look at token 2.

---

## 6. Where students get stuck

- Softmax over the wrong axis (columns instead of keys / last dim).
- Dividing by \(d_k\) instead of \(\sqrt{d_k}\), or skipping the scale.
- Masking with \(0\) instead of \(-\infty\).

---

## 7. Video

Watch [3Blue1Brown: Attention in transformers, visually explained](https://www.youtube.com/watch?v=eMlx5fFNoYc).

Pause when queries and keys meet as a grid of dots, when softmax turns a row into a distribution, and when values are mixed. That grid is Lab 3’s heatmap.

---

## 8. Practice

1. If two tokens have identical keys, what does the softmax do to their weights?

2. Why divide by \(\sqrt{d_k}\)?

3. Write \(A\) for \(T=2\) with \(Q=K=V=I\) (identity), no mask. What is \(AV\)?

4. Softmax the row \([0, 2]\). Then softmax \([0, 2]/\sqrt{2}\). Did the larger entry gain or lose probability after scaling?

5. Scores \(\begin{bmatrix}1& 3\\ 0& 1\end{bmatrix}\), causal mask (upper triangle \(-\infty\)). Write the masked score matrix, then \(A\) (row-wise softmax).
