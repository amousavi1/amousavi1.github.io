These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

GPT and BERT are the same block with different **masks** and **objectives**. That choice is the difference between a generator and a bidirectional encoder.

---

## 1. Two attention patterns

**GPT** (decoder-only): each token may attend to itself and the past. The pretraining job is **next-token** prediction. Sampling is ancestral: emit \(t\), then condition on it.

**BERT** (encoder-only): every token may attend to every token. The pretraining job is **masked language modeling** (and originally next-sentence prediction). You cannot sample a paragraph left-to-right without extra machinery.

![Causal versus bidirectional attention](files/data-643/graphics/3.4-gpt-bert/gpt-bert.png)

Causal mask: a lower-triangular pattern of legal scores. BERT’s “mask” is a **token** `[MASK]` in the input, not a future-key mask. Those two uses of the word confuse people all semester.

---

## 2. Objectives, in one table

| | GPT | BERT |
| - | --- | ---- |
| Mask | causal | none (random tokens hidden) |
| Loss | \(p(x_t \mid x_{<t})\) | \(p(x_{\text{masked}} \mid x_{\text{rest}})\) |
| Default use | generate, chat, complete | classify, tag, embed a span |
| Peek at the future? | no | yes, by design |

Modern “BERT-like” encoders (RoBERTa, T5’s encoder, embedding models) keep the bidirectional idea. Modern LLMs are GPT-style stacks, often with extra alignment (Weeks 8–9).

Do not fine-tune BERT as if it were GPT. A `[MASK]` model is not a chat decoder. You *can* classify with a decoder via a prompt; you cannot stream tokens from BERT without a separate head.

---

## 3. Scaling, briefly

The same block, bigger: more layers, wider \(d\), more heads, more data. Week 7 is scaling laws and efficiency. This week: if the mask is causal, you have a language model; if not, you have a contextual encoder. Do not fine-tune BERT as if it were GPT.

For the project: generation, RAG, and tool-use sit on a decoder. Classification into a small label set can still use an encoder, or a decoder with a prompt.

---

## 4. Teaching this note

**30–40 minutes.** Draw the two attention triangles, fill the objective table, then the \(2\times 2\) causal-softmax example. Play Karpathy **Let’s build GPT** **0:00–12:00** (tokens in, next token out). Then **0:00–8:00** of CodeEmporium BERT (MLM / `[MASK]`). If you only have one clip, keep Karpathy and assign BERT.

---

## 5. Worked example

Two tokens, raw scores \(S=\begin{bmatrix}1&2\\3&4\end{bmatrix}\).

GPT (causal): illegal future is \(S_{12}\). Set it to \(-\infty\):

\[
S_{\text{GPT}}=\begin{bmatrix}1&-\infty\\3&4\end{bmatrix}.
\]

Softmax row 1: \([1,0]\). Row 2: \(\mathrm{softmax}([3,4])\approx [0.27,\,0.73]\) because \(e^{3}\approx 20.1\), \(e^{4}\approx 54.6\).

BERT (bidirectional): softmax both rows of the original \(S\). Row 1: \(\mathrm{softmax}([1,2])\approx [0.27,\,0.73]\). Token 1 **does** look at token 2.

Objective contrast: GPT loss on this pair is \(-\log p(x_2\mid x_1)\). BERT, if token 1 is `[MASK]`, is \(-\log p(x_1\mid x_2)\) (and any other masked sites).

---

## 6. Where students get stuck

- Using BERT when the demo must **stream** tokens.
- Masking GPT scores with \(0\) instead of \(-\infty\).
- Calling every transformer “a GPT.”

---

## 7. Video

Watch [Karpathy: Let’s build GPT](https://www.youtube.com/watch?v=kCc8FmEb1nY) through the first attention / causal-mask implementation (start **0:00–12:00** in class; the attention code is later if you assign homework).

Also [CodeEmporium: BERT Neural Network — EXPLAINED!](https://www.youtube.com/watch?v=xI0HHN5XKDo). Pause on masked language modeling and next-sentence prediction. You do not need to train BERT today.

---

## 8. Practice

1. Why is BERT the wrong pretrained model if your demo must stream tokens?

2. A sentiment classifier: encoder or decoder? Give one reason for each.

3. What does a causal mask set the illegal scores to before the softmax, and why not zero?

4. Scores \(\begin{bmatrix}0& 0\\ 0& 0\end{bmatrix}\), causal mask. Write \(A\). (Uniform among **legal** keys.)

5. BERT hides 15% of tokens. In a sequence of length \(20\), how many tokens are masked in expectation? If the loss is only on those positions, how many terms enter the mean that step?
