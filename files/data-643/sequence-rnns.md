These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

An MLP sees a vector and forgets. Language is a **sequence**: the meaning of *not* depends on what came before. A recurrent net keeps a **state** and updates it at every token.

This week is the historical path to transformers. You still need it: LSTMs show up in speech and time series, and the failure mode (a chain of Jacobians) is why Week 3 exists.

---

## 1. The cell

At step \(t\) the cell takes

- the new token embedding \(\boldsymbol{x}_t\), and
- the previous hidden state \(\boldsymbol{h}_{t-1}\).

It emits \(\boldsymbol{h}_t\), which is supposed to hold **both**. That vector is the memory.

![RNN cell: previous state and current input](files/data-643/graphics/2.1-sequence-rnns/rnn-cell.png)

The same weights are used at every step. That is weight sharing along time, the sequence analogue of a CNN’s shared filter.

Between two independent sequences (two reviews in a batch) you **reset** \(\boldsymbol{h}_0=\boldsymbol{0}\). The loop lives *inside* one sequence.

If you do not reset, review 2 starts with leftover sentiment from review 1. That is leakage, not transfer learning.

---

## 2. Unrolled in time

Write the loop as a chain. Three tokens, one set of weights:

\[
\boldsymbol{h}_t = \tanh\bigl(W_h \boldsymbol{h}_{t-1} + W_x \boldsymbol{x}_t + \boldsymbol{b}\bigr).
\]

![The same cell copied along the sentence](files/data-643/graphics/2.1-sequence-rnns/rnn-unroll.png)

A CNN looks at a **fixed** neighborhood, in parallel. An RNN looks at **everything so far**, in order, and cannot fully parallelize across time. That is the accuracy / speed tradeoff.

Unrolling is how you backprop. The picture is one graph with copies of \(W_h,W_x\). There are not three different matrices named \(W_h^{(1)},W_h^{(2)},W_h^{(3)}\).

---

## 3. What the state has to carry

If the first word is the subject of a verb twenty tokens later, \(\boldsymbol{h}_t\) must still contain that subject. The cell is a lossy compressor: every step overwrites. Week **2.2** is what happens to the gradient on that long path. Week **2.3** adds gates so the cell can choose what to keep.

A many-to-one RNN (sentiment) uses the last \(\boldsymbol{h}_T\). A many-to-many RNN (tagging, language modeling) emits at every \(t\). Next-token LM: predict \(x_{t+1}\) from \(\boldsymbol{h}_t\).

---

## 4. Teaching this note

**30–40 minutes.** Draw the cell, unroll three tokens with **shared** \(W_h\), then do the 2-D numeric example with \(\boldsymbol{h}_0=\boldsymbol{0}\). Play **0:00–12:00** of StatQuest RNNs (the loop and the unroll). Save vanishing gradients for note 2.2 even if the video teases them.

---

## 5. Worked example

Let \(d=2\), \(\boldsymbol{b}=\boldsymbol{0}\), \(\boldsymbol{h}_0=\boldsymbol{0}\),

\[
W_h=\begin{bmatrix}0.5&0\\0&0.5\end{bmatrix},\qquad
W_x=I,\qquad
\boldsymbol{x}_1=\begin{bmatrix}1\\0\end{bmatrix},\qquad
\boldsymbol{x}_2=\begin{bmatrix}0\\1\end{bmatrix}.
\]

Step 1: \(W_h\boldsymbol{h}_0+W_x\boldsymbol{x}_1=\boldsymbol{x}_1\), so \(\boldsymbol{h}_1=\tanh(\boldsymbol{x}_1)\approx\begin{bmatrix}0.76\\0\end{bmatrix}\) because \(\tanh(1)\approx 0.76\).

Step 2: \(W_h\boldsymbol{h}_1+W_x\boldsymbol{x}_2\approx\begin{bmatrix}0.38\\1\end{bmatrix}\), then \(\boldsymbol{h}_2=\tanh(\cdot)\approx\begin{bmatrix}0.36\\0.76\end{bmatrix}\).

The same \(W_h\) was used twice. Token 1 still has a **shrunk** footprint in \(\boldsymbol{h}_2\) (\(0.76\to 0.36\)). That shrinkage is the teaser for vanishing gradients.

---

## 6. Where students get stuck

- Drawing a new \(W_h\) at each time step (no sharing).
- Feeding the whole sentence as one concatenated vector “to make it an MLP.”
- Forgetting to reset \(\boldsymbol{h}\) between batch items.

---

## 7. Video

Watch [StatQuest: Recurrent Neural Networks, Clearly Explained](https://www.youtube.com/watch?v=AsNTP8Kwu80).

Pause on the first unroll (same weights copied) and on the moment the hidden state is described as memory. Skip any long software demo; the board math is the point.

---

## 8. Practice

1. Unroll three tokens on paper with \(d=2\), \(\boldsymbol{h}_0=\boldsymbol{0}\). Which matrices are reused?

2. Why reset the state between two unrelated documents in a batch?

3. Name one thing an RNN can mix that a kernel of size 5 cannot, in a single layer.

4. Using the worked example’s \(W_h,W_x\) and \(\boldsymbol{x}_3=\begin{bmatrix}1\\1\end{bmatrix}\), write the pre-activation \(W_h\boldsymbol{h}_2+W_x\boldsymbol{x}_3\) with \(\boldsymbol{h}_2\approx\begin{bmatrix}0.36\\0.76\end{bmatrix}\). Do not bother with \(\tanh\) if you are short on time; the linear mix is the lesson.

5. If every \(W_h\) were replaced by \(0.1 I\), and \(\boldsymbol{x}_t=\boldsymbol{0}\) after \(t=1\), approximately how does \(\lVert\boldsymbol{h}_t\rVert\) scale with \(t\)? (Geometric sequence.)
