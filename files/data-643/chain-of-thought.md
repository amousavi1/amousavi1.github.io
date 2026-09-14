These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

**Chain-of-thought** (CoT) is the habit of writing **steps** before the answer. You are not changing the weights. You are changing what the decoder is asked to emit.

---

## 1. Steps are part of the string

A direct prompt is “What is 17 × 24?” A CoT prompt is “Show your work, then give the number.” Few-shot CoT puts worked examples in the context; zero-shot CoT is often the sentence *Let’s think step by step.*

![Scratch work, then a boxed answer](files/data-643/graphics/13.1-chain-of-thought/cot.png)

The model still predicts tokens. Intermediate tokens can allocate compute: they store partial products, units, or a plan. That helps **multi-step** arithmetic, symbolic puzzles, and some school-science items. It does not magically add retrieval (Week 14) or tools. A longer string is not “thinking” in the everyday sense; it is extra decoding you can inspect.

Karpathy’s phrase is System 2 as more tokens. Same idea: each token is a fixed-size compute step, so a hard problem needs a longer tape.

Zero-shot vs few-shot is a method choice. Few-shot CoT is only as good as the traces you paste: same task, same answer format, same units. A mismatch is not “the model cannot reason”; it is a context that points at the wrong procedure.

---

## 2. When it helps, when it does not

CoT tends to help when the gold answer needs several dependent hops. It can hurt on tasks that are a single lookup: extra steps are extra chances to wander. Longer traces cost latency and dollars. For a project, CoT is a **method knob**, not a personality.

You still need a metric on the **answer**, and a separate look at the trace (note **13.3**). A correct box after a wrong derivation is not the same system as a correct derivation. Self-consistency (note **13.2**) is what you do when one chain is too noisy to trust.

---

## 3. How to write it in a report

Say whether the prompt was zero-shot or few-shot, paste the exact instruction, and freeze decoding settings (temperature, max tokens). Do not claim the model “reasoned” unless you have a check on the steps. Lab 13 will grade traces as strings, with no API.

Temperature 0 is a single greedy chain: useful as a baseline, not as a vote (note **13.2**). If you raise temperature to get diverse traces, you must still parse a final answer the same way every time.

---

## 4. Teaching this note

About **30 minutes** at the board, then **~8 minutes** of video. First of three Week-13 notes; Lab 13 is constructed traces, not an API.

- **0–10 min.** Direct vs CoT prompt. Tokens as scratch paper.
- **10–20 min.** When CoT helps (multi-hop) vs hurts (lookup). Cost.
- **20–30 min.** Worked 17 × 24 on the board, then a one-hop counterexample.
- **Then** play Karpathy intro **35:00–38:02** (Thinking, System 1/2). Pause on “models need tokens to think.”

---

## 5. Worked example

Prompt: \(17\times 24\). Direct decode might jump to a familiar number (400, 408, 428) with no check.

A CoT string that actually computes:

1. \(10\times 24=240\)
2. \(7\times 24=168\)
3. \(240+168=408\)

Three intermediate tokens (here, three lines) hold partial products. The boxed answer is 408. Gold is 408. This trace is also **faithful** (note **13.3**): the last computed value matches the box.

A one-hop item, “Capital of France?”, does not need hops. A CoT prompt can invent a story (“Lyon was the capital in…”) and then still say Paris—or wander to Lyon. Extra decode is extra risk. That is why you report **answer accuracy** and, separately, a trace check, not a vibe that the model “showed work.”

Lab 13’s `23+19` traces are the same algebra with smaller numbers.

---

## 6. Where students get stuck

- Calling CoT a fine-tune. It is a **prompt / decoding** choice unless you trained on traces.
- Scoring only the box. Wrong steps plus a lucky 408 will look like a win until note **13.3**.
- Pasting few-shot examples from a different task (math shots, then a policy question) and blaming the model.

---

## 7. Video

Watch [Andrej Karpathy, Intro to Large Language Models](https://www.youtube.com/watch?v=zjkBMFhNj_g), **35:00–38:02**.

Pause on System 1 vs System 2: the model gets more compute by emitting more tokens. Optional nearby: **38:02–40:45** (self-improvement) is not required for this note. Notes **14.1–14.2** and **15.1** reuse this same URL at other minutes.

---

## 8. Practice

1. Why might CoT raise accuracy on a four-hop word problem and lower it on “What is the capital of France?”

2. Few-shot CoT puts examples in context. What goes wrong if those examples are a different task than the test item?

3. Name one number you would report besides final-answer accuracy if your project uses CoT.

4. Write a three-line CoT for \(17\times 24\) that ends in 408. Then write one line that is CoT-shaped but computes \(17\times 20=340\) and boxes 408. Which is unfaithful?

5. Direct prompt, temperature \(0\), one sample: accuracy \(0.62\). CoT, temperature \(0\), one sample: accuracy \(0.71\), mean tokens \(4\times\) longer. What two numbers belong in the table besides \(0.71\)?
