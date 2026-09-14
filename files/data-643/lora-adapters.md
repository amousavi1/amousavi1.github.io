These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

Full fine-tuning moves every entry of \(\boldsymbol{W}\). **LoRA** (Hu et al., 2021) freezes \(\boldsymbol{W}\) and learns a **low-rank residual**. You store a few megabytes per task instead of a second copy of the 7B.

---

## 1. \(W + BA\)

For a linear map \(\boldsymbol{W}\in\mathbb{R}^{d\times k}\),

\[
\boldsymbol{h} = \boldsymbol{W}\boldsymbol{x} + \frac{\alpha}{r}\boldsymbol{B}\boldsymbol{A}\boldsymbol{x},
\]

with \(\boldsymbol{A}\in\mathbb{R}^{r\times k}\), \(\boldsymbol{B}\in\mathbb{R}^{d\times r}\), rank \(r\ll \min(d,k)\). Initialize \(\boldsymbol{B}=\boldsymbol{0}\) so the adapter starts as the base model. Train only \(A,B\) (and maybe a bias). Attention projections and MLP up/down maps are the usual insertion points.

![Frozen W plus low-rank BA](files/data-643/graphics/8.3-lora-adapters/lora.png)

QLoRA quantizes \(\boldsymbol{W}\) to 4-bit and still trains float adapters. Same algebra. Lab 8 uses a \(4\times 4\) frozen \(\boldsymbol{W}\) so you can print \(BA\).

---

## 2. Rank, merge, many tasks

Small \(r\) (4, 8, 16) is often enough for style and instruction shifts; harder domain shifts may want larger \(r\) or more layers. At deploy time you can **merge** \(\boldsymbol{W}\leftarrow \boldsymbol{W}+(\alpha/r)BA\) and throw the adapter away, or keep several adapters and swap them.

One adapter per skill is how you avoid the XOR-then-AND overwrite (note **8.2**): the base stays, the skill is a file.

---

## 3. Federated adapters

Sites that cannot ship raw text can still train a LoRA locally and send **\(A,B\)** to a server. The server averages adapters (or stacks them) without seeing documents. That is **federated** fine-tuning in the sense this course needs: communication is the adapter, not the corpus. Privacy is not automatic (adapters can leak), but the footprint is the right size.

![Local adapters, shared base](files/data-643/graphics/8.3-lora-adapters/federated.png)

For a project: report \(r\), which modules you adapted, \(\alpha\), and whether you merged. Compare to a small full fine-tune if you can afford it.

---

## 4. Practice

1. If \(r=1\) and \(d=k=4\), how many trainable numbers are in \((A,B)\) versus \(\boldsymbol{W}\)?

2. Why initialize \(\boldsymbol{B}=\boldsymbol{0}\) rather than \(\boldsymbol{A}=\boldsymbol{0}\)?

3. A hospital trains a LoRA and sends it to you. What did they *not* send, and what can still leak?
