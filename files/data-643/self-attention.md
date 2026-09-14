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

---

## 2. A row of weights

Row \(t\) of \(A\) is a distribution over the sequence. Large mass on a name is “this pronoun just looked at that name.”

![Attention weights for one head](files/data-643/graphics/3.2-self-attention/attn-heatmap.png)

**Multi-head:** several \((W_Q,W_K,W_V)\) in parallel, concatenate, project. Different heads can track syntax, a name, or a comma. Lab 3 will compute one head by hand.

---

## 3. Masks

For next-token prediction you **mask** future keys (set scores to \(-\infty\) before softmax). Otherwise the model cheats. BERT does not mask the future; it masks random tokens and reconstructs them (note **3.4**).

---

## 4. Practice

1. If two tokens have identical keys, what does the softmax do to their weights?

2. Why divide by \(\sqrt{d_k}\)?

3. Write \(A\) for \(T=2\) with \(Q=K=V=I\) (identity), no mask. What is \(AV\)?
