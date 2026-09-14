These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

GPT and BERT are the same block with different **masks** and **objectives**. That choice is the difference between a generator and a bidirectional encoder.

---

## 1. Two attention patterns

**GPT** (decoder-only): each token may attend to itself and the past. The pretraining job is **next-token** prediction. Sampling is ancestral: emit \(t\), then condition on it.

**BERT** (encoder-only): every token may attend to every token. The pretraining job is **masked language modeling** (and originally next-sentence prediction). You cannot sample a paragraph left-to-right without extra machinery.

![Causal versus bidirectional attention](files/data-643/graphics/3.4-gpt-bert/gpt-bert.png)

---

## 2. Objectives, in one table

| | GPT | BERT |
| - | --- | ---- |
| Mask | causal | none (random tokens hidden) |
| Loss | \(p(x_t \mid x_{<t})\) | \(p(x_{\text{masked}} \mid x_{\text{rest}})\) |
| Default use | generate, chat, complete | classify, tag, embed a span |
| Peek at the future? | no | yes, by design |

Modern “BERT-like” encoders (RoBERTa, T5’s encoder, embedding models) keep the bidirectional idea. Modern LLMs are GPT-style stacks, often with extra alignment (Weeks 8–9).

---

## 3. Scaling, briefly

The same block, bigger: more layers, wider \(d\), more heads, more data. Week 7 is scaling laws and efficiency. This week: if the mask is causal, you have a language model; if not, you have a contextual encoder. Do not fine-tune BERT as if it were GPT.

For the project: generation, RAG, and tool-use sit on a decoder. Classification into a small label set can still use an encoder, or a decoder with a prompt.

---

## 4. Practice

1. Why is BERT the wrong pretrained model if your demo must stream tokens?

2. A sentiment classifier: encoder or decoder? Give one reason for each.

3. What does a causal mask set the illegal scores to before the softmax, and why not zero?
