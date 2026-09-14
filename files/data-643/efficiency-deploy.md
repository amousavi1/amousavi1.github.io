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

---

## 2. Speculative decoding

Autoregressive decode is serial: one token, then another. **Speculative decoding** runs a cheap **draft** model for several tokens, then the large **target** checks them in one parallel pass. If the target agrees, you accept a block; if not, you roll back at the first mismatch and sample from the target. Expected speedup is \(>1\times\) when the draft is often right; the **distribution** is still the target’s.

![Draft tokens verified by the large model](files/data-643/graphics/7.3-efficiency-deploy/speculative.png)

This is not pruning. It is extra compute on a small net to save steps on a large net.

---

## 3. What to report

Name bits, which layers you quantized, whether you distilled, and tokens per second versus a dense fp16 baseline. Quality: the same eval as the uncompressed model, not only perplexity. For a project, a 4-bit laptop demo is a deployment result; it is not a new architecture.

---

## 4. Practice

1. Why does a scale-and-zero-point map need \(z\), not only \(s\), if \(x\) is not centered at zero?

2. Distillation needs a teacher. What happens if the teacher is already calibrated badly on your domain?

3. Speculative decoding must not change the target distribution. Where does a rejected draft token get replaced?
