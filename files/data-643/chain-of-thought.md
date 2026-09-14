These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

**Chain-of-thought** (CoT) is the habit of writing **steps** before the answer. You are not changing the weights. You are changing what the decoder is asked to emit.

---

## 1. Steps are part of the string

A direct prompt is “What is 17 × 24?” A CoT prompt is “Show your work, then give the number.” Few-shot CoT puts worked examples in the context; zero-shot CoT is often the sentence *Let’s think step by step.*

![Scratch work, then a boxed answer](files/data-643/graphics/13.1-chain-of-thought/cot.png)

The model still predicts tokens. Intermediate tokens can allocate compute: they store partial products, units, or a plan. That helps **multi-step** arithmetic, symbolic puzzles, and some school-science items. It does not magically add retrieval (Week 14) or tools. A longer string is not “thinking” in the everyday sense; it is extra decoding you can inspect.

---

## 2. When it helps, when it does not

CoT tends to help when the gold answer needs several dependent hops. It can hurt on tasks that are a single lookup: extra steps are extra chances to wander. Longer traces cost latency and dollars. For a project, CoT is a **method knob**, not a personality.

You still need a metric on the **answer**, and a separate look at the trace (note **13.3**). A correct box after a wrong derivation is not the same system as a correct derivation. Self-consistency (note **13.2**) is what you do when one chain is too noisy to trust.

---

## 3. How to write it in a report

Say whether the prompt was zero-shot or few-shot, paste the exact instruction, and freeze decoding settings (temperature, max tokens). Do not claim the model “reasoned” unless you have a check on the steps. Lab 13 will grade traces as strings, with no API.

---

## 4. Practice

1. Why might CoT raise accuracy on a four-hop word problem and lower it on “What is the capital of France?”

2. Few-shot CoT puts examples in context. What goes wrong if those examples are a different task than the test item?

3. Name one number you would report besides final-answer accuracy if your project uses CoT.
