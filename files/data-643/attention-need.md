These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

An RNN compresses the whole past into one vector. Token 1 can affect token 40 only by surviving 39 overwrites. **Attention** lets every token look at every other token in one step. That is the move from this week’s recurrences to the rest of the course.

---

## 1. The bottleneck

To answer “what does *it* refer to?” the model needs a path from *it* to a name that may be far left (or right). In an RNN that path is a chain. In attention it is one matrix of scores.

![A chain versus all-pairs links](files/data-643/graphics/3.1-attention-need/rnn-vs-attention.png)

Bahdanau et al. (2015) added attention on top of an encoder–decoder RNN so the decoder could reread the source. Vaswani et al. (2017) dropped the recurrence: **self-attention** is the layer.

---

## 2. What you gain and what you pay

| | RNN | Self-attention |
| - | --- | -------------- |
| Path length, token 1 to \(T\) | \(T\) | \(1\) |
| Parallel over time | no | yes |
| Cost in \(T\) | \(O(T)\) | \(O(T^2)\) memory/time for full attention |

Long documents (Week 7: efficiency) will force approximations. For this course’s default, full attention is the model.

---

## 3. Practice

1. Why can a transformer GPU-batch a whole sentence’s updates at once, while an LSTM cannot?

2. A 4k-token policy PDF: what is the quadratic cost complaining about?

3. In one sentence, what information did \(\boldsymbol{h}_t\) have to store that an attention row can fetch instead?
