These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

Gates are learned valves. They let a recurrent cell **keep** a bit of memory for many steps instead of overwriting it every time. LSTM and GRU are the two you will meet. They do not remove vanishing gradients; they make a near-1 path available.

---

## 1. LSTM: a highway plus three gates

Hochreiter and Schmidhuber (1997). A **cell state** \(\boldsymbol{c}_t\) moves down the chain with mostly multiplies and adds, not a stack of \(\tanh\)s. Three sigmoid gates, each in \((0,1)\):

| Gate | Role |
| ---- | ---- |
| Forget \(\boldsymbol{f}_t\) | How much of \(\boldsymbol{c}_{t-1}\) to keep |
| Input \(\boldsymbol{i}_t\) | How much new candidate to write |
| Output \(\boldsymbol{o}_t\) | How much of \(\tanh(\boldsymbol{c}_t)\) becomes \(\boldsymbol{h}_t\) |

\[
\boldsymbol{c}_t = \boldsymbol{f}_t \odot \boldsymbol{c}_{t-1} + \boldsymbol{i}_t \odot \tilde{\boldsymbol{c}}_t,
\qquad
\boldsymbol{h}_t = \boldsymbol{o}_t \odot \tanh(\boldsymbol{c}_t).
\]

If \(\boldsymbol{f}_t \approx \boldsymbol{1}\) and \(\boldsymbol{i}_t \approx \boldsymbol{0}\), the cell copies. That is the long-range path.

![LSTM gates around a cell highway](files/data-643/graphics/2.3-lstm-gru/lstm-gates.png)

---

## 2. GRU: two gates, no extra cell

Cho et al. (2014). Reset \(\boldsymbol{r}_t\) and update \(\boldsymbol{z}_t\). The hidden state *is* the memory.

\[
\boldsymbol{h}_t = (1-\boldsymbol{z}_t)\odot \boldsymbol{h}_{t-1} + \boldsymbol{z}_t \odot \tilde{\boldsymbol{h}}_t.
\]

Fewer parameters, often similar quality on medium sequences. Use LSTM when you want an explicit cell; use GRU when you want a smaller default.

![GRU reset and update](files/data-643/graphics/2.3-lstm-gru/gru-gates.png)

---

## 3. What gates do not buy you

The loop is still sequential. You still cannot fill a GPU the way a transformer can. Long context is better than vanilla, worse than attention. For this course, gates are the reason we can talk about “memory” before Week 3, and a baseline in speech/time-series projects.

Bidirectional LSTM: run one net forward and one backward, concatenate. Fine for classification. Illegal for next-token generation (you would peek at the future).

---

## 4. Practice

1. If the forget gate is stuck at 0, what happens to \(\boldsymbol{c}_t\)?

2. Why is a bidirectional LSTM the wrong cell for a language model that must emit token \(t+1\)?

3. Name one reason you might still pick a GRU over a transformer in a project.
