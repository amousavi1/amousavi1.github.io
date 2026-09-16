These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

Gates are learned valves: they let a recurrent cell **keep** a bit of memory for many steps instead of overwriting it every time. LSTM and GRU are the two you will meet; they do not remove vanishing gradients, but they make a near-1 path **available**. By the end you should be able to write the cell update, run the copy regime in numbers, and say why a bidirectional LSTM is illegal for next-token generation.

---

## 1. What LSTMs and GRUs are

**LSTMs** and **GRUs** are gated RNNs. In a vanilla RNN the hidden state is **constantly rewritten** by \(\tanh(W_h h_{t-1}+\cdots)\). Unless \(W_h\) is essentially a wire (eigenvalues on the unit circle and no saturating \(\tanh\)), memory is short. You cannot ask SGD to discover a unitary \(W_h\) and a linear activation at once.

What you want instead: a **cell** that can copy, plus **input-dependent switches** that say when to write, when to erase, and when to report. That is an LSTM (Hochreiter and Schmidhuber 1997; forget gate from Gers et al. 2000). An additive **cell** path can copy a value when the forget gate is open and the input gate is closed. GRU is the two-gate cousin: the hidden state *is* the memory.

They do not guarantee that every coordinate copies. They make a copy path *learnable*. In practice you get on the order of \(10^2\) steps rather than \(\approx 7\), not infinite context.

---

## 2. Why we use it

Vanilla RNNs vanish. You need a highway whose gradient is \(\approx 1\) along the copy. Lab 2 compares an LSTM to a vanilla RNN on a long copy: the first bit should sit in the cell until the last step.

For this course, gates are the reason we can talk about “memory” before Week 3, and a baseline in speech and time-series projects. Both LSTM and GRU are still **sequential**. You still cannot fill a GPU the way a transformer can. Long context is better than vanilla, worse than attention.

---

## 3. Architecture

A **cell state** \(\boldsymbol{c}_t\) moves down the chain with mostly multiplies and adds, not a stack of \(\tanh\)s. Three sigmoid gates, each in \((0,1)\):

| Gate | Role |
| ---- | ---- |
| Forget \(\boldsymbol{f}_t\) | How much of \(\boldsymbol{c}_{t-1}\) to keep |
| Input \(\boldsymbol{i}_t\) | How much new candidate to write |
| Output \(\boldsymbol{o}_t\) | How much of \(\tanh(\boldsymbol{c}_t)\) becomes \(\boldsymbol{h}_t\) |

Each gate is a sigmoid of a linear mix of \(\boldsymbol{x}_t\) and \(\boldsymbol{h}_{t-1}\) (plus a bias). You do not need every matrix name on the first pass. You need the cell update:

\[
\boldsymbol{c}_t = \boldsymbol{f}_t \odot \boldsymbol{c}_{t-1} + \boldsymbol{i}_t \odot \tilde{\boldsymbol{c}}_t,
\qquad
\boldsymbol{h}_t = \boldsymbol{o}_t \odot \tanh(\boldsymbol{c}_t).
\]

The candidate \(\tilde{\boldsymbol{c}}_t\) is a \(\tanh\) of a linear mix of \(\boldsymbol{x}_t\) and \(\boldsymbol{h}_{t-1}\).

![LSTM gates around a cell highway](files/data-643/graphics/2.3-lstm-gru/lstm-gates.png)

Peephole connections (cell into the gates) exist in some papers. We do not use them. `nn.LSTM` is the three-gate cell above.

**GRU** (Cho et al. 2014): reset \(\boldsymbol{r}_t\) and update \(\boldsymbol{z}_t\). No extra cell.

\[
\boldsymbol{h}_t = (1-\boldsymbol{z}_t)\odot \boldsymbol{h}_{t-1} + \boldsymbol{z}_t \odot \tilde{\boldsymbol{h}}_t.
\]

Read \(\boldsymbol{z}_t\) as “how much to replace.” If \(\boldsymbol{z}_t\approx\boldsymbol{0}\), you copy \(\boldsymbol{h}_{t-1}\). Reset \(\boldsymbol{r}_t\) controls how much past goes into the candidate \(\tilde{\boldsymbol{h}}_t\).

![GRU reset and update](files/data-643/graphics/2.3-lstm-gru/gru-gates.png)

Fewer parameters, often similar quality on medium sequences. Use LSTM when you want an explicit cell; use GRU when you want a smaller default. Gates share weights across time, just as \(W_h\) did: there is not a new forget-gate matrix at each step.

---

## 4. How it works, step by step

If \(\boldsymbol{f}_t \approx \boldsymbol{1}\) and \(\boldsymbol{i}_t \approx \boldsymbol{0}\), the cell **copies**. That is the long-range path. Along that coordinate,

\[
\frac{\partial \boldsymbol{c}_t}{\partial \boldsymbol{c}_{t-1}} = \boldsymbol{f}_t,
\]

which can stay near 1. That is why the vanishing plot in 2.2 had a gated curve.

![Forget open, input closed](files/data-643/graphics/2.3-lstm-gru/copy-regime.png)

Scalar cell (drop the output gate for a minute). Suppose \(c_{t-1}=2\), \(f_t=0.9\), \(i_t=0.1\), \(\tilde{c}_t=5\):

\[
c_t = 0.9\cdot 2 + 0.1\cdot 5 = 1.8+0.5=2.3.
\]

Most of the old memory survived; a little new content landed. If instead \(f_t=0\), \(c_t=0.5\) and the \(2\) is gone.

Copy regime: \(f_t=1\), \(i_t=0\) \(\Rightarrow\) \(c_t=c_{t-1}\). Ten such steps: \(c_{t+10}=c_t\). Gradient along that path is \(1^{10}=1\).

That is Lab 2’s hope: the first bit sits in \(\boldsymbol{c}\) and the forget gate learns to leave it there until the last step.

---

## 5. Mathematical formulas

LSTM cell and hidden state:

\[
\boldsymbol{c}_t = \boldsymbol{f}_t \odot \boldsymbol{c}_{t-1} + \boldsymbol{i}_t \odot \tilde{\boldsymbol{c}}_t,
\qquad
\boldsymbol{h}_t = \boldsymbol{o}_t \odot \tanh(\boldsymbol{c}_t).
\]

Copy-path Jacobian:

\[
\frac{\partial \boldsymbol{c}_t}{\partial \boldsymbol{c}_{t-1}} = \boldsymbol{f}_t.
\]

GRU mix:

\[
\boldsymbol{h}_t = (1-\boldsymbol{z}_t)\odot \boldsymbol{h}_{t-1} + \boldsymbol{z}_t \odot \tilde{\boldsymbol{h}}_t.
\]

Gates are elementwise sigmoids of linear mixes of \(\boldsymbol{x}_t\) and \(\boldsymbol{h}_{t-1}\). The candidate \(\tilde{\boldsymbol{c}}_t\) (LSTM) or \(\tilde{\boldsymbol{h}}_t\) (GRU) is a \(\tanh\) of a linear mix; GRU’s candidate is further gated by the reset \(\boldsymbol{r}_t\).

---

## 6. Positive points and negative points

**Positive.**

- The copy regime (\(f\approx 1\), \(i\approx 0\)) gives a highway whose gradient can stay near 1, so long-range copy becomes learnable.
- LSTM’s explicit cell is a readable “memory tape”; GRU’s two gates are cheaper and often enough on medium sequences.
- Lab 2 can show the gated cell beating a vanilla RNN as the gap grows.
- You get a recurrent baseline for speech and time series before Week 3’s attention.

**Negative.**

- More parameters than a vanilla RNN (three gates plus a candidate, or two gates for GRU).
- Still sequential: you cannot fill a GPU the way a transformer can.
- LSTM does **not** guarantee that every coordinate copies, or that a 500-word review still trains.
- Mixing up forget and input (zeroing \(f\) when you meant “write nothing new”) erases the cell.
- Bidirectional LSTMs peek at the future; they are illegal for next-token generation.

**When not to.** If you need all-to-all mixing in parallel, pick attention. If the whole sentence is allowed and you are classifying, a bidirectional LSTM is a legitimate encoder, not a generator.

---

## 7. Bidirectional and stacked

**Bidirectional** LSTM: run one net forward and one backward, concatenate. Fine for classification when the whole sentence is allowed. **Illegal** for next-token generation (you would peek at the future).

**Stacked** LSTM: \(\boldsymbol{h}_t\) of layer \(\ell\) is the input to layer \(\ell+1\). Deeper mixing, still a loop. Do not stack four layers in Lab 2.

---

## 8. Teaching this note

**~16 minutes.** Table of three LSTM gates, then the copy regime \(\boldsymbol{f}\approx 1,\boldsymbol{i}\approx 0\), then the numeric cell update. GRU as “two knobs, hidden state is the memory.” One sentence on bidirectional-is-illegal-for-LMs. Play StatQuest LSTM **0:00–12:00** (forget/input intuition). Assign the GRU video as a 10-minute clip after class, or play **0:00–8:00** if the room is still with you.

---

## 9. Worked example

The scalar LSTM cell update is in section 4. GRU: \(h_{t-1}=4\), \(z_t=0.25\), \(\tilde{h}_t=0\) gives

\[
h_t=(1-0.25)\cdot 4 + 0.25\cdot 0=3.
\]

You kept 75% of the past.

Vector GRU with \(\boldsymbol{h}_{t-1}=\begin{bmatrix}2\\5\end{bmatrix}\), \(\boldsymbol{z}_t=\begin{bmatrix}1\\0\end{bmatrix}\), \(\tilde{\boldsymbol{h}}_t=\begin{bmatrix}0\\3\end{bmatrix}\):

\[
\boldsymbol{h}_t=(1-\boldsymbol{z}_t)\odot\boldsymbol{h}_{t-1}+\boldsymbol{z}_t\odot\tilde{\boldsymbol{h}}_t
=\begin{bmatrix}0\\1\end{bmatrix}\odot\begin{bmatrix}2\\5\end{bmatrix}
+\begin{bmatrix}1\\0\end{bmatrix}\odot\begin{bmatrix}0\\3\end{bmatrix}
=\begin{bmatrix}0\\5\end{bmatrix}.
\]

Coordinate 1 replaced (\(z=1\)); coordinate 2 copied (\(z=0\)).

---

## 10. Where students get stuck

- Mixing up forget vs. input (zeroing \(f\) when they meant “write nothing new”).
- Claiming LSTMs “solved vanishing gradients” in every coordinate, always.
- Using a bidirectional LSTM for a generator that must not see \(t+1\).
- Drawing a new forget-gate matrix at each time step (gates share weights too).

---

## 11. Video

Watch [StatQuest: Long Short-Term Memory (LSTM), Clearly Explained](https://www.youtube.com/watch?v=YCzL96nL7j0).

Pause when the forget gate is a number in \((0,1)\) multiplying the cell, and when the cell is drawn as a highway. Then [StatQuest: Gated Recurrent Units (GRU), Clearly Explained](https://www.youtube.com/watch?v=tOuXgORsXJ4) — play the update-gate mix; skip if time is gone.

---

## 12. Practice

1. If the forget gate is stuck at 0, what happens to \(\boldsymbol{c}_t\)?

2. Why is a bidirectional LSTM the wrong cell for a language model that must emit token \(t+1\)?

3. Name one reason you might still pick a GRU over a transformer in a project.

4. Compute \(c_t\) for \(c_{t-1}=1\), \(f_t=0.5\), \(i_t=0.5\), \(\tilde{c}_t=-1\). Then compute \(h_t\) if \(o_t=1\) and \(h_t=o_t\tanh(c_t)\).

5. GRU with \(\boldsymbol{h}_{t-1}=\begin{bmatrix}2\\5\end{bmatrix}\), \(\boldsymbol{z}_t=\begin{bmatrix}1\\0\end{bmatrix}\), \(\tilde{\boldsymbol{h}}_t=\begin{bmatrix}0\\3\end{bmatrix}\). Compute \(\boldsymbol{h}_t\). Which coordinate copied, and which replaced?

6. In one line: why can \(\partial c_t/\partial c_{t-1}\) stay near 1 when a vanilla \(\partial h_t/\partial h_{t-1}\) usually cannot?

7. Does an LSTM *guarantee* that the first token of a 500-word review still trains? What would you measure in Lab 2 to check?
