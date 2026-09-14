These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

A dense transformer uses **every** MLP on every token. A **mixture of experts (MoE)** keeps many MLPs (**experts**) and runs only a few of them per token. Capacity grows with the expert count; FLOPs per token stay closer to a small dense net.

---

## 1. Router plus experts

Replace the block MLP with \(E\) experts \(E_1,\ldots,E_E\) and a **router** (a linear map plus softmax or a noisy top-\(k\)). For token \(\boldsymbol{x}\),

\[
y = \sum_{i \in \mathcal{T}(\boldsymbol{x})} g_i(\boldsymbol{x})\, E_i(\boldsymbol{x}),
\]

where \(\mathcal{T}\) is the set of \(k\) selected experts (often \(k=1\) or \(2\)) and \(g_i\) are the gate scores. Attention can stay dense; the sparse part is the feedforward path, where most parameters already live (note **3.3**).

![A router sending tokens to a few experts](files/data-643/graphics/7.2-mixture-of-experts/moe.png)

Switch Transformer, GLaM, Mixtral: same picture, different \(k\), expert size, and load-balancing tricks.

---

## 2. Why sparsity, and what breaks

**Sparse** means most experts are idle for a given token. That is the point: you can store 8\(\times\) the MLP weights and still pay about 2 experts of compute. Training needs a **load-balancing** term so the router does not send every token to expert 0. At inference, experts must sit in RAM or be paged; a “small” Mixtral still has a large footprint.

Routing is discrete. Gradients flow through the chosen experts and through the gate (straight-through or a softmax over a shortlist). Expert collapse and token dropping are the usual failure modes.

---

## 3. Dense versus MoE in a project

Use a dense 7B if you need simple deployment. Use an MoE if you need more capacity at a similar token-FLOP budget and you can host the weights. Do not fine-tune one expert and claim the mixture improved; say whether you trained the router. Week 7.3 is how you shrink whatever you picked.

---

## 4. Practice

1. If \(k=1\) and the router always picks expert 2, what did you just train?

2. Why can an MoE with 8 experts have roughly the compute of 2 dense MLPs per token, not 8?

3. Name one reason Mixtral-style serving is harder than a dense model with the same active FLOPs.
