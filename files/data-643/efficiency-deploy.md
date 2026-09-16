These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

This is the first full lecture on **shipping** a model that is too big for the box you have. Scaling (note **7.1**) made the net. **Efficiency** is prune, quantize, distill, or speculate. Treat each as a new method. They are not LoRA (note **8.3**).

---

## 1. What these methods are

Four different jobs, one hour.

- **Pruning:** set some weights to zero (unstructured) or drop heads, neurons, or layers (structured). The graph gets smaller or sparser.
- **Quantization:** store the **same** architecture in fewer bits (INT8, 4-bit). The count of weights does not change; the bytes do.
- **Distillation:** a frozen **teacher** produces logits (or hidden states); a smaller **student** matches them, plus labels. You buy a cheaper net, not a new capability.
- **Speculative decoding:** a cheap **draft** model proposes several tokens; the large **target** checks them in one parallel pass. The **distribution** stays the target’s.

---

## 2. Why we use them

A 7B fp16 file is about 14 GB. Laptops, phones, and batch servers do not all hold that. Retraining a tiny model from scratch may be worse than compressing a good large one. Decode is serial: one token per large forward. Speculation tries to pay one large forward for several tokens when the draft is often right.

---

## 3. Architecture

**Prune / quantize / distill** change what you **store** or **train**. **Speculative decoding** changes only the **sampler** at serve time: draft model + target model + accept/reject. You still have the original transformer; you wrap it.

![Prune, quantize, distill](files/data-643/graphics/7.3-efficiency-deploy/compress.png)

![Draft tokens verified by the large model](files/data-643/graphics/7.3-efficiency-deploy/speculative.png)

Stanford CS224N 2025 L11 puts pruning next to LoRA (fewer weights vs a small \(\Delta\)). Distill and speculate stay on this board.

---

## 4. How each one works

**Prune.** Score weights (magnitude, or a more careful criterion). Zero the small ones, or drop a structure. Then a short recovery train, or quality falls off a cliff.

**Quantize.** Map a real tensor to integers with a **scale** \(s\) and **zero-point** \(z\). Lab 7 does this on a toy tensor and reports MSE. Outliers in activations break naive INT8.

**Distill.** Run the teacher on your batches. Train the student so its logits match (KL or MSE) and so labels are still right. If the teacher is already wrong on your domain, the student copies that.

**Speculate.** Draft emits \((t_1,\ldots,t_n)\). Target, in one forward, scores them. Accept the prefix the target agrees with; at the first mismatch, sample from the **target** and drop the rest of the draft.

---

## 5. Mathematical formulas

Affine quantization:

\[
x \approx s\,(q - z), \qquad q \in \{0,\ldots,2^b-1\}.
\]

![INT8 with a zero-point](files/data-643/graphics/7.3-efficiency-deploy/int8-numeric.png)

Symmetric INT8 on \([-1,1]\): \(s=2/255\), \(z=128\). Dropping \(z\) cannot represent negatives.

Speculative accept: if the target’s next-token distribution assigns the draft token enough mass (exact rule: sample from target; accept if it matches the draft’s proposal in the standard algorithm), you keep it. Teaching form: **agree \(\Rightarrow\) keep; disagree \(\Rightarrow\) resample from the target.** Expected tokens per large forward \(>1\) when the draft is accurate. The law of the output is still \(p_{\mathrm{target}}\).

---

## 6. Positive points and negative points

**Positive.** INT4 can drop a 7B from ~14 GB toward ~3.5 GB plus overhead. Distill gives a small student you can actually run. Speculation can raise tokens/s without changing answers in distribution. Pruning can cut FLOPs if structured.

**Negative.** Quality drop if you skip recovery (prune) or ignore outliers (INT8). Distill cannot exceed a bad teacher. Speculation adds a draft model and can slow you down if the draft is often wrong. Reporting only perplexity hides downstream damage. None of these is a new architecture for the project write-up.

**When not to.** If the model already fits and latency is fine, leave it in fp16. If you need a new skill, train (SFT/LoRA); do not only quantize.

---

## 7. What to report

Bits, which layers you quantized, whether you distilled, tokens per second versus fp16, and the **same** downstream eval as the uncompressed model.

---

## 8. Teaching this note

About **45 minutes**. Name all four methods before INT8 arithmetic.

- **0–10 min.** What / why: four jobs, not one slogan.
- **10–25 min.** Affine INT8. Zero-point. Lab 7 tensor.
- **25–38 min.** Speculative accept/reject. Then one sentence each on prune and distill.
- **38–45 min.** Pros / cons. LoRA is next week.
- Play LoRA video **0:00–~15:00** as “deploy a small delta,” then return to this board.

---

## 9. Worked example

Weights in \([-1,1]\), \(b=8\), \(q\in\{0,\ldots,255\}\):

\[
s = \frac{2}{255},\qquad z=128,\qquad x \approx s(q-128).
\]

\(q=128\mapsto 0\); \(q=255\mapsto s\cdot 127\approx 0.996\).

Speculative: draft emits four tokens. Target agrees on the first two, rejects the third. Commit two, sample a new third from the **target**, throw the fourth away.

Memory: 7B fp16 \(\approx 14\) GB. INT4 weights \(\approx 3.5\) GB plus overhead.

---

## 10. Where students get stuck

- Quantizing without a zero-point when the tensor is not \(\ge 0\).
- Thinking speculation **changes** the target distribution.
- Reporting perplexity only after 4-bit.
- Calling all four methods “LoRA.”

---

## 11. Video

[Umar Jamil — LoRA explained](https://www.youtube.com/watch?v=PXWYUTMt-AU). Play about **0:00–15:00**. **Prune, quantize, and speculative decoding stay on the board.** Full LoRA is note **8.3**.

---

## 12. Practice

1. In one sentence each: prune vs quantize vs distill vs speculate.

2. Why does a scale-and-zero-point map need \(z\), not only \(s\), if \(x\) is not centered at zero?

3. Speculative decoding must not change the target distribution. Where does a rejected draft token get replaced?

4. Map \(x\in[-2,2]\) to INT8 with \(q\in\{0,\ldots,255\}\). Give \(s\) and \(z\) so that \(q=0\) is \(-2\) and \(q=255\) is \(2\).

5. A draft proposes 5 tokens; the target accepts the first 4. How many **target** forwards did you pay for those 4 tokens, and what happens to token 5?
