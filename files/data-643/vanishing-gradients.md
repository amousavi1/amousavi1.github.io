These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

Backprop through an unrolled RNN multiplies one Jacobian per time step. If those matrices shrink, the early-token gradient **vanishes**. If they grow, it **explodes**. Either way, long-range learning dies.

---

## 1. A product along the chain

The loss at the last token, \(L(\boldsymbol{h}_T)\), depends on \(\boldsymbol{h}_1\) through

\[
\frac{\partial L}{\partial \boldsymbol{h}_1}
=
\frac{\partial L}{\partial \boldsymbol{h}_T}
\frac{\partial \boldsymbol{h}_T}{\partial \boldsymbol{h}_{T-1}}
\cdots
\frac{\partial \boldsymbol{h}_2}{\partial \boldsymbol{h}_1}.
\]

Each factor \(\partial \boldsymbol{h}_{t}/\partial \boldsymbol{h}_{t-1}\) contains \(W_h\) and \(\tanh'\). For \(\tanh\), \(\lvert\tanh'\rvert \le 1\), and it is \(\ll 1\) unless the pre-activation sits near 0. A product of twenty numbers smaller than 1 is tiny.

![Gradient scale versus steps back in time](files/data-643/graphics/2.2-vanishing-gradients/vanish.png)

The gated curve is the slogan for LSTM/GRU: keep a path whose multiplier can stay near 1.

In 1-D, if each factor is \(0.5\), ten steps give \(0.5^{10}\approx 0.001\). The early token still sits in the forward state as a faint trace, but the **learning signal** is gone.

---

## 2. Vanishing versus exploding

Same product, opposite problem. If \(\lVert W_h\rVert\) is large, the signal blows up, weights become NaNs, and training stops. **Gradient clipping** (rescale if the global norm exceeds a threshold) is the usual bandage for exploding. It does not fix vanishing.

![Vanishing versus exploding along depth](files/data-643/graphics/2.2-vanishing-gradients/vanish-explode.png)

Clipping: if \(\lVert\boldsymbol{g}\rVert>c\), replace \(\boldsymbol{g}\) by \(c\,\boldsymbol{g}/\lVert\boldsymbol{g}\rVert\). You shrink a huge vector. A vanished vector is already near \(\boldsymbol{0}\); multiplying it by 1 does nothing useful.

---

## 3. What this means for language

A vanilla RNN can learn “the next word looks like the last few.” It struggles with “the negation was at the start of the review.” Transformers side-step the chain: every token attends to every other token in one step (Week 3). Gates (Week 2.3) were the fix *inside* the recurrent family.

In a project, if you still train an RNN on long documents, watch the gradient norm. If it is always \(\approx 0\) on early positions, the net is not using the beginning of the sequence.

Lab 2 is a copy task: the first bit must survive many steps. Vanilla RNNs fail as the gap grows; that is this product, not a PyTorch bug.

---

## 4. Teaching this note

**30–40 minutes.** Write the product of Jacobians, then the 1-D geometric example (\(0.5^{T}\) vs \(1.5^{T}\)). Draw clipping as a cap on a tall arrow, not a resurrection of a dead one. Play the vanishing/exploding segment of CS224N L6 (about **45:00–58:00**; if chapter marks differ, jump to the Jacobian-product board). LSTM details wait for 2.3.

---

## 5. Worked example

Scalar RNN: \(h_t = \tanh(w h_{t-1})\). Then \(h_t'(h_{t-1}) = \tanh'(z_t)\, w\) with \(\lvert\tanh'\rvert\le 1\).

Take \(w=0.5\) and pretend \(\tanh'=1\) (best case). The factor per step is \(0.5\):

\[
0.5^{5}=0.03125,\qquad 0.5^{10}\approx 0.0010,\qquad 0.5^{20}\approx 9.5\times 10^{-7}.
\]

Now \(w=2\): \(2^{10}=1024\). Same chain, opposite disaster.

Clipping: gradient \(g=50\), threshold \(c=5\). New gradient \(5\). If instead \(g=10^{-6}\), clipping leaves it at \(10^{-6}\).

---

## 6. Where students get stuck

- Thinking clipping “fixes RNNs,” including vanishing.
- Forgetting \(\tanh'\le 1\) and blaming only \(W_h\).
- Plotting loss and missing a **per-position** gradient plot in Lab 2.

---

## 7. Video

Watch [Stanford CS224N Lecture 6 (RNNs / vanishing gradients)](https://www.youtube.com/watch?v=0LixFSa7yts).

Play the vanishing and exploding segment (roughly **45:00–58:00**). Pause on the product of Jacobians and on the plot of gradient size vs. steps back in time. Skip the rest of the lecture hour unless you want n-gram language modeling as optional homework.

---

## 8. Practice

1. Why is \(\tanh'\) a problem when the state saturates at \(\pm 1\)?

2. Clipping stops explosions. Why does it not restore a vanished signal?

3. In one sentence: what would you plot in TensorBoard to see this failure in Lab 2?

4. If each Jacobian factor has operator norm \(0.8\), the bound on \(\lVert\partial h_{20}/\partial h_{1}\rVert\) is \(0.8^{19}\). Compute \(0.8^{10}\) and \(0.8^{19}\) (calculator is fine). Is the 19-step bound closer to \(0.1\) or to \(0.01\)?

5. A clip threshold \(c=1\) meets a gradient of \([-6, 8]\) (Euclidean norm \(10\)). Write the clipped vector.
