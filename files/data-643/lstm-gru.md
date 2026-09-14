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

The candidate \(\tilde{\boldsymbol{c}}_t\) is a \(\tanh\) of a linear mix of \(\boldsymbol{x}_t\) and \(\boldsymbol{h}_{t-1}\). You do not need every matrix name on the first pass. You need: **forget \(\times\) old, plus input \(\times\) new**.

If \(\boldsymbol{f}_t=\boldsymbol{1}\) for many steps, \(\partial \boldsymbol{c}_t / \partial \boldsymbol{c}_{t-1}\) can stay near 1 along that coordinate. That is why the vanishing plot in 2.2 had a gated curve.

---

## 2. GRU: two gates, no extra cell

Cho et al. (2014). Reset \(\boldsymbol{r}_t\) and update \(\boldsymbol{z}_t\). The hidden state *is* the memory.

\[
\boldsymbol{h}_t = (1-\boldsymbol{z}_t)\odot \boldsymbol{h}_{t-1} + \boldsymbol{z}_t \odot \tilde{\boldsymbol{h}}_t.
\]

Fewer parameters, often similar quality on medium sequences. Use LSTM when you want an explicit cell; use GRU when you want a smaller default.

![GRU reset and update](files/data-643/graphics/2.3-lstm-gru/gru-gates.png)

Read \(\boldsymbol{z}_t\) as “how much to replace.” If \(\boldsymbol{z}_t\approx\boldsymbol{0}\), you copy \(\boldsymbol{h}_{t-1}\). Reset \(\boldsymbol{r}_t\) controls how much past goes into the candidate \(\tilde{\boldsymbol{h}}_t\).

---

## 3. What gates do not buy you

The loop is still sequential. You still cannot fill a GPU the way a transformer can. Long context is better than vanilla, worse than attention. For this course, gates are the reason we can talk about “memory” before Week 3, and a baseline in speech/time-series projects.

Bidirectional LSTM: run one net forward and one backward, concatenate. Fine for classification. Illegal for next-token generation (you would peek at the future).

---

## 4. Teaching this note

**30–40 minutes.** Table of three LSTM gates, then the copy regime \(\boldsymbol{f}\approx 1,\boldsymbol{i}\approx 0\), then the numeric cell update. GRU as “two knobs, hidden state is the memory.” Play StatQuest LSTM **0:00–12:00** (forget/input intuition). Assign the GRU video as a 10-minute clip after class, or play **0:00–8:00** if the room is still with you.

---

## 5. Worked example

Scalar LSTM cell (drop the output gate for a minute). Suppose \(c_{t-1}=2\), \(f_t=0.9\), \(i_t=0.1\), \(\tilde{c}_t=5\):

\[
c_t = 0.9\cdot 2 + 0.1\cdot 5 = 1.8+0.5=2.3.
\]

Most of the old memory survived; a little new content landed. If instead \(f_t=0\), \(c_t=0.5\) and the \(2\) is gone.

Copy regime: \(f_t=1\), \(i_t=0\) \(\Rightarrow\) \(c_t=c_{t-1}\). Ten such steps: \(c_{t+10}=c_t\). Gradient along that path is \(1^{10}=1\).

GRU: \(h_{t-1}=4\), \(z_t=0.25\), \(\tilde{h}_t=0\) gives \(h_t=(1-0.25)\cdot 4 + 0.25\cdot 0=3\). You kept 75% of the past.

---

## 6. Where students get stuck

- Mixing up forget vs. input (zeroing \(f\) when they meant “write nothing new”).
- Claiming LSTMs “solved vanishing gradients” in every coordinate, always.
- Using a bidirectional LSTM for a generator that must not see \(t+1\).

---

## 7. Video

Watch [StatQuest: Long Short-Term Memory (LSTM), Clearly Explained](https://www.youtube.com/watch?v=YCzL96nL7j0).

Pause when the forget gate is a number in \((0,1)\) multiplying the cell, and when the cell is drawn as a highway. Then [StatQuest: Gated Recurrent Units (GRU), Clearly Explained](https://www.youtube.com/watch?v=tOuXgORsXJ4) — play the update-gate mix; skip if time is gone.

---

## 8. Practice

1. If the forget gate is stuck at 0, what happens to \(\boldsymbol{c}_t\)?

2. Why is a bidirectional LSTM the wrong cell for a language model that must emit token \(t+1\)?

3. Name one reason you might still pick a GRU over a transformer in a project.

4. Compute \(c_t\) for \(c_{t-1}=1\), \(f_t=0.5\), \(i_t=0.5\), \(\tilde{c}_t=-1\). Then compute \(h_t\) if \(o_t=1\) and \(h_t=o_t\tanh(c_t)\).

5. GRU with \(h_{t-1}=\begin{bmatrix}2\\0\end{bmatrix}\), \(z_t=\begin{bmatrix}1\\0\end{bmatrix}\), \(\tilde{h}_t=\begin{bmatrix}0\\3\end{bmatrix}\). Compute \(\boldsymbol{h}_t\). Which coordinate copied, and which replaced?
