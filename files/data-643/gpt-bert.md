These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

GPT and BERT are the same block with different **masks** and **objectives**. That choice is the difference between a generator and a bidirectional encoder. Princeton COS 484 L10 is the matching pretraining hour; CS224N’s pretraining lecture is the same fork.

---

## 1. Static versus contextual

Week 1’s embedding table gave *bank* **one** vector. A transformer gives *bank* a vector that depends on the sentence: river bank versus money bank. That is a **contextual** representation. ELMo did this with LSTMs; GPT and BERT do it with the Week 3 block.

![The same type, two contexts](files/data-643/graphics/3.4-gpt-bert/contextual.png)

Pretrain once on unlabeled text, then fine-tune a small head (or the whole stack) on a labeled task. CS224N’s slogan: **pretrain once, fine-tune many times.**

---

## 2. Two attention patterns

**GPT** (decoder-only): each token may attend to itself and the past. The pretraining job is **next-token** (causal language modeling). Sampling is ancestral: emit \(t\), then condition on it.

**BERT** (encoder-only): every token may attend to every token. The pretraining job is **masked language modeling** (and originally next-sentence prediction; later work often drops NSP). You cannot sample a paragraph left-to-right without extra machinery.

![Causal versus bidirectional attention](files/data-643/graphics/3.4-gpt-bert/gpt-bert.png)

Causal mask: a lower-triangular pattern of legal scores. BERT’s “mask” is a **token** `[MASK]` in the input, not a future-key mask. Those two uses of the word confuse people all semester.

![Next-token versus `[MASK]`](files/data-643/graphics/3.4-gpt-bert/mlm-clm.png)

---

## 3. Objectives, in one table

| | GPT | BERT |
| - | --- | ---- |
| Stack | decoder | encoder |
| Mask | causal | none on keys (random **tokens** hidden) |
| Loss | \(p(x_t \mid x_{1:t-1})\) | \(p(x_{\text{masked}} \mid x_{\text{rest}})\) |
| Default use | generate, chat, complete | classify, tag, embed a span |
| Peek at the future? | no | yes, by design |

Modern “BERT-like” encoders (RoBERTa, embedding models) keep the bidirectional idea. Modern LLMs are GPT-style stacks, often with extra alignment (Weeks 8–9). Encoder–decoder models (T5, BART) exist; they are the original transformer, not a third mystery architecture.

Do not fine-tune BERT as if it were GPT. A `[MASK]` model is not a chat decoder. You *can* classify with a decoder via a prompt; you cannot stream tokens from BERT without a separate head.

BERT-base, one line: \(N=12\), \(d=768\), 12 heads, about 110M parameters. GPT-1 was the same size on a decoder. The fork is the mask and the loss, not the width.

---

## 4. Scaling, briefly

The same block, bigger: more layers, wider \(d\), more heads, more data. Week 7 is scaling laws and efficiency. This week: if the mask is causal, you have a language model; if not, you have a contextual encoder.

For the project: generation, RAG, and tool-use sit on a decoder. Classification into a small label set can still use an encoder, or a decoder with a prompt.

---

## 5. Teaching this note

**~16 minutes.** Static vs contextual *bank*, then the two attention triangles, then the objective table, then the \(2\times 2\) causal-softmax example. Play Karpathy **Let’s build GPT** **0:00–12:00** (tokens in, next token out). Then **0:00–8:00** of CodeEmporium BERT (MLM / `[MASK]`). If you only have one clip, keep Karpathy and assign BERT.

---

## 6. Worked example

Two tokens, raw scores \(S=\begin{bmatrix}1&2\\3&4\end{bmatrix}\).

GPT (causal): illegal future is \(S_{12}\). Set it to \(-\infty\):

\[
S_{\text{GPT}}=\begin{bmatrix}1&-\infty\\3&4\end{bmatrix}.
\]

Softmax row 1: \([1,0]\). Row 2: \(\mathrm{softmax}([3,4])\approx [0.27,\,0.73]\) because \(e^{3}\approx 20.1\), \(e^{4}\approx 54.6\).

BERT (bidirectional): softmax both rows of the original \(S\). Row 1: \(\mathrm{softmax}([1,2])\approx [0.27,\,0.73]\). Token 1 **does** look at token 2.

Objective contrast: GPT loss on this pair is \(-\log p(x_2\mid x_1)\). BERT, if token 1 is `[MASK]`, is \(-\log p(x_1\mid x_2)\) (and any other masked sites).

---

## 7. Where students get stuck

- Using BERT when the demo must **stream** tokens.
- Masking GPT scores with \(0\) instead of \(-\infty\).
- Calling every transformer “a GPT.”
- Thinking `[MASK]` is the same object as a causal key mask.

---

## 8. Video

Watch [Karpathy: Let’s build GPT](https://www.youtube.com/watch?v=kCc8FmEb1nY) through the first attention / causal-mask implementation (start **0:00–12:00** in class; the attention code is later if you assign homework).

Also [CodeEmporium: BERT Neural Network — EXPLAINED!](https://www.youtube.com/watch?v=xI0HHN5XKDo). Pause on masked language modeling and next-sentence prediction. You do not need to train BERT today.

The matching university lecture is Princeton COS 484 L10 (contextualized representations, GPT, BERT), with CS224N W26 pretraining as the second source for “pretrain once, fine-tune many.” We do not copy those slides.

---

## 9. Practice

1. Why is BERT the wrong pretrained model if your demo must stream tokens?

2. A sentiment classifier: encoder or decoder? Give one reason for each.

3. What does a causal mask set the illegal scores to before the softmax, and why not zero?

4. Scores \(\begin{bmatrix}0& 0\\ 0& 0\end{bmatrix}\), causal mask. Write \(A\). (Uniform among **legal** keys.)

5. BERT hides 15% of tokens. In a sequence of length \(20\), how many tokens are masked in expectation? If the loss is only on those positions, how many terms enter the mean that step?

6. *bank* in “river bank” versus “money bank”: what did Week 1’s table do, and what does BERT do?

7. Name one encoder-only, one decoder-only, and one encoder–decoder model. Which one is the default stack for this course’s generation projects?
