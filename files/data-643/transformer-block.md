These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

A transformer **block** is attention, a residual add, layer norm, then a token-wise MLP, another residual and norm. Stack \(N\) of those. Attention mixes across positions; the MLP mixes across channels at one position.

---

## 1. Positions have to be added

Attention is a set operation: permute the tokens, the weights permute with them. Language is ordered. **Positional encodings** (sinusoids in the original paper, or learned vectors) are added to token embeddings before the first block.

![Sinusoidal position channels](files/data-643/graphics/3.3-transformer-block/positional.png)

Relative or rotary positions (RoPE) appear in later LLMs. The idea is the same: put order into the vectors because the mixing layer will not.

Without positions, `dog bites man` and `man bites dog` can produce the same bag of contextual vectors up to permutation. That is fatal for language.

---

## 2. The block

![One transformer block, bottom to top](files/data-643/graphics/3.3-transformer-block/block.png)

**Residual:** add the input of the sublayer to its output. That is another highway, like the LSTM cell, so gradients can skip a messy attention map.

**Layer norm:** normalize across features of one token. Pre-norm versus post-norm is an implementation detail you will meet in Hugging Face configs.

**MLP:** usually two linear maps with a GELU, hidden width \(4d\). Most of the parameters live here, not in attention.

Count, roughly: attention’s \(W_Q,W_K,W_V,W_O\) are four \(d\times d\) maps \(\approx 4d^{2}\). MLP is \(d\times 4d\) and \(4d\times d\) \(\approx 8d^{2}\). The MLP is heavier. Stack \(N\) blocks; GPT-2 small is \(N=12\), \(d=768\).

Pre-norm (layer-norm, then sublayer, then residual) is the usual modern default; it trains more stably at depth. Post-norm (sublayer, residual, then norm) is the 2017 paper. You will see `pre_norm` in configs. Do not swap them casually and call it an ablation of “the architecture.”

---

## 3. Encoder–decoder

The original transformer has an **encoder** (bidirectional self-attention on the source) and a **decoder** (causal self-attention plus **cross-attention** into the encoder). Translation is the picture. GPT keeps only a decoder. BERT keeps only an encoder. You do not need both unless the task is sequence-to-sequence.

Cross-attention: queries from the decoder, keys/values from the encoder. Captioning (BLIP) uses that pattern with **image** tokens as the encoder side.

---

## 4. Teaching this note

**30–40 minutes.** Positions first (one counterexample sentence), then walk the block bottom-to-top with residuals as \(x + \mathrm{sublayer}(x)\). Do the numeric residual add. Play Umar Jamil’s **block walkthrough** (about **10:00–25:00**: embeddings, positions, one encoder layer). Skip the long from-scratch coding if this is a board day.

---

## 5. Worked example

Token vector \(\boldsymbol{x}=\begin{bmatrix}1\\2\end{bmatrix}\). Attention sublayer emits \(\boldsymbol{a}=\begin{bmatrix}0.3\\-0.1\end{bmatrix}\). Residual:

\[
\boldsymbol{x}+\boldsymbol{a}=\begin{bmatrix}1.3\\1.9\end{bmatrix}.
\]

If attention were zero (uniform mix that cancels, or a dead head), you still pass \(\boldsymbol{x}\) through. That is the highway.

Parameter sketch: \(d=4\). Attention \(\approx 4\cdot 16=64\) weights (ignoring biases). MLP \(\approx 8\cdot 16=128\). The MLP has twice as many.

Positions: add \(\boldsymbol{p}_0=\begin{bmatrix}0\\1\end{bmatrix}\) to token A and \(\boldsymbol{p}_1=\begin{bmatrix}1\\0\end{bmatrix}\) to token B **before** the first block. Swapping tokens now swaps different vectors, not identical ones.

---

## 6. Where students get stuck

- Dropping positions and then being shocked that order vanished.
- Thinking attention holds most of the parameters.
- Residual as “replace \(x\)” instead of “add to \(x\).”

---

## 7. Video

Watch [Umar Jamil: Transformer Neural Network — architecture and PyTorch](https://www.youtube.com/watch?v=bCz4OMemCcA).

Play the architecture / block walkthrough (roughly **10:00–25:00**). Pause on positional encodings and on the residual+norm sandwich. The hour of typing `nn.Linear` is optional homework, not this meeting.

---

## 8. Practice

1. If you drop positional encodings, what two sentences become indistinguishable?

2. Residual connections help training. Which earlier idea in Week 2 is the cousin of that?

3. Where do most of the weights sit: \(W_Q,W_K,W_V\) or the MLP?

4. \(d=8\). Using the \(4d^{2}\) vs \(8d^{2}\) sketch, how many attention weights vs MLP weights (ignore biases and the extra \(W_O\) if you already folded it into the \(4d^{2}\))? What is the ratio MLP / attention?

5. Layer-norm a 2-D vector \(\boldsymbol{u}=\begin{bmatrix}3\\1\end{bmatrix}\) by subtracting the mean and dividing by the standard deviation of its two coordinates (population std, no \(\varepsilon\)). Write the normalized vector.
