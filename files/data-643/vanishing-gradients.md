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

---

## 2. Vanishing versus exploding

Same product, opposite problem. If \(\lVert W_h\rVert\) is large, the signal blows up, weights become NaNs, and training stops. **Gradient clipping** (rescale if the global norm exceeds a threshold) is the usual bandage for exploding. It does not fix vanishing.

![Vanishing versus exploding along depth](files/data-643/graphics/2.2-vanishing-gradients/vanish-explode.png)

---

## 3. What this means for language

A vanilla RNN can learn “the next word looks like the last few.” It struggles with “the negation was at the start of the review.” Transformers side-step the chain: every token attends to every other token in one step (Week 3). Gates (Week 2.3) were the fix *inside* the recurrent family.

In a project, if you still train an RNN on long documents, watch the gradient norm. If it is always \(\approx 0\) on early positions, the net is not using the beginning of the sequence.

---

## 4. Practice

1. Why is \(\tanh'\) a problem when the state saturates at \(\pm 1\)?

2. Clipping stops explosions. Why does it not restore a vanished signal?

3. In one sentence: what would you plot in TensorBoard to see this failure in Lab 2?
