These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

Scaling (note **7.1**) makes a model that may not fit on the box you have. **Efficiency** is how you ship it: fewer weights, fatter arithmetic, a smaller student, or fewer expensive forward passes at decode time.

---

## 1. Shrink the weights

**Prune:** set small weights to zero (unstructured) or drop heads, neurons, or layers (structured). You need a pass of recovery training or the quality drop is ugly.

**Quantize:** store weights (and sometimes activations) in fewer bits. INT8 and 4-bit GPTQ/AWQ are the ones you will see in Hugging Face. Affine quantization uses a **scale** and **zero-point**:

\[
x \approx s\,(q - z), \qquad q \in \{0,\ldots,2^b-1\}.
\]

Lab 7 does this on a toy tensor and reports MSE. The curve is not free: outliers in activations break naive INT8.

**Distill:** a frozen **teacher** produces logits or hidden states; a smaller **student** matches them (plus the usual labels). You buy a model that is cheaper to run, not a new capability.

![Prune, quantize, distill](files/data-643/graphics/7.3-efficiency-deploy/compress.png)

![INT8 with a zero-point](files/data-643/graphics/7.3-efficiency-deploy/int8-numeric.png)

---

## 2. Speculative decoding

Autoregressive decode is serial: one token, then another. **Speculative decoding** runs a cheap **draft** model for several tokens, then the large **target** checks them in one parallel pass. If the target agrees, you accept a block; if not, you roll back at the first mismatch and sample from the target. Expected speedup is \(>1\times\) when the draft is often right; the **distribution** is still the target’s.

![Draft tokens verified by the large model](files/data-643/graphics/7.3-efficiency-deploy/speculative.png)

This is not pruning. It is extra compute on a small net to save steps on a large net.

If the draft proposes 4 tokens and the target accepts 3, you paid one large forward for 3 tokens instead of 3 large forwards. Token 4 is resampled from the target.

---

## 3. What to report

Name bits, which layers you quantized, whether you distilled, and tokens per second versus a dense fp16 baseline. Quality: the same eval as the uncompressed model, not only perplexity. For a project, a 4-bit laptop demo is a deployment result; it is not a new architecture.

Stanford CS224N 2025 L11 puts **pruning** and **LoRA** in the same PEFT hour: fewer weights, or a small \(\Delta\) on a frozen \(W\). Distill and speculative decoding stay on this board; they are not LoRA. Note **8.3** owns the \(BA\) algebra.

---

## 4. Teaching this note

About **35 minutes** at the board: affine INT8 on a 1-D range, a 4-token speculative accept/reject, then one sentence on prune vs distill. Play LoRA **0:00–~15:00** as “deploy a small delta,” then return to prune/quantize/speculate. Lab 7’s toy quantize is studio, not this block.

---

## 5. Worked example

Weights in \([-1,1]\), \(b=8\) bits, \(q\in\{0,\ldots,255\}\). A symmetric affine map:

\[
s = \frac{2}{255},\qquad z=128,\qquad x \approx s(q-128).
\]

\(q=128\) \(\mapsto\) \(0\); \(q=255\) \(\mapsto\) \(s\cdot 127 \approx 0.996\). If you drop \(z\) and only use \(x\approx s q\), you cannot represent negatives.

Speculative: draft emits \((t_1,t_2,t_3,t_4)\). Target, in one forward, assigns probabilities. It agrees on \(t_1,t_2\), rejects \(t_3\). You commit \(t_1,t_2\), sample a new \(t_3'\) from the **target**, and throw \(t_4\) away. Speedup \(\approx 2\) large-tokens per large-forward this step, if the draft is that accurate on average.

Memory cartoon: 7B fp16 \(\approx 14\) GB. INT4 weights \(\approx 3.5\) GB plus overhead. Same architecture, different bits.

---

## 6. Where students get stuck

- Quantizing without a zero-point when the tensor is not \(\ge 0\).
- Thinking speculative decoding **changes** the target distribution. It must not; rejected drafts are resampled from the target.
- Reporting perplexity only after 4-bit. The project eval is the same downstream number as fp16.

---

## 7. Video

[Umar Jamil — LoRA explained](https://www.youtube.com/watch?v=PXWYUTMt-AU). Play about **0:00–15:00** (frozen \(W\), small \(BA\)). That is the deploy-small-deltas story. **Prune, quantize, and speculative decoding stay on the board**; they are not in this clip. Full LoRA is note **8.3**.

---

## 8. Practice

1. Why does a scale-and-zero-point map need \(z\), not only \(s\), if \(x\) is not centered at zero?

2. Distillation needs a teacher. What happens if the teacher is already calibrated badly on your domain?

3. Speculative decoding must not change the target distribution. Where does a rejected draft token get replaced?

4. Map \(x\in[-2,2]\) to INT8 with \(q\in\{0,\ldots,255\}\). Give \(s\) and \(z\) so that \(q=0\) is \(-2\) and \(q=255\) is \(2\).

5. A draft proposes 5 tokens; the target accepts the first 4. How many **target** forwards did you pay for those 4 tokens, and what happens to token 5?
