These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

**Chain-of-thought** (CoT) is the habit of writing **steps** before the answer. You are not changing the weights. You are changing what the decoder is asked to emit. By the end you should be able to write a direct prompt and a CoT prompt for the same item, say when extra steps help, and name one number besides final-answer accuracy.

---

## 1. What chain-of-thought is

**Chain-of-thought (CoT)** is writing **steps** before the answer. A direct prompt is “What is 17 × 24?” A CoT prompt is “Show your work, then give the number.” Few-shot CoT puts worked examples in the context. Zero-shot CoT is often the sentence *Let’s think step by step.*

This is a **prompt / decoding** choice, not a new architecture and not a fine-tune (unless you later trained on traces). The model still predicts tokens. Extra tokens are extra **test-time compute**. The weights do not change.

Intermediate tokens can allocate compute: they store partial products, units, or a plan. That helps **multi-step** arithmetic, symbolic puzzles, and some school-science items. It does not magically add retrieval (Week 14) or tools. A longer string is not “thinking” in the everyday sense; it is extra decoding you can inspect.

Karpathy’s phrase is System 2 as more tokens. Same idea: each token is a fixed-size compute step, so a hard problem needs a longer tape.

Zero-shot vs few-shot is a method choice. Few-shot CoT is only as good as the traces you paste: same task, same answer format, same units. A mismatch is not “the model cannot reason”; it is a context that points at the wrong procedure.

---

## 2. Why we use it

Multi-hop arithmetic can use the tape. A four-hop word problem has intermediate quantities that need a place to sit. Direct decode might jump to a familiar number (400, 408, 428) with no check. CoT gives the model room to write \(10\times 24=240\), then \(7\times 24=168\), then add.

It can **hurt** on tasks that are a single lookup: extra steps are extra chances to wander. “Capital of France?” does not need hops. A CoT prompt can invent a story (“Lyon was the capital in…”) and then still say Paris—or wander to Lyon.

Longer traces cost latency and dollars. For a project, CoT is a **method knob**, not a personality. You still need a metric on the **answer**, and a separate look at the trace (note **13.3**). A correct box after a wrong derivation is not the same system as a correct derivation. Self-consistency (note **13.2**) is what you do when one chain is too noisy to trust.

---

## 3. Architecture

The architecture is the **same language model**. What changes is the prompt and the length of the generation. You parse a final boxed answer separately from the trace (note **13.3**). There is no new layer, no extra head, and no tool in this note.

![Scratch work, then a boxed answer](files/data-643/graphics/13.1-chain-of-thought/cot.png)

Freeze the instruction and the decoding settings (temperature, max tokens) when you report a number. Temperature 0 is one greedy chain, not a vote (note **13.2**). If you raise temperature to get diverse traces, you must still parse a final answer the same way every time.

Lab 13 grades traces as strings, with no API. The lab’s `23+19` items are the same algebra as the \(17\times 24\) cartoon with smaller numbers.

---

## 4. How it works, step by step

Take \(17\times 24\).

1. **Direct prompt.** “What is \(17\times 24\)?” Decode a short answer. The model may jump to a familiar number with no check.
2. **CoT prompt.** “Show your work, then the number,” or paste few-shot traces, or write *Let’s think step by step.*
3. **Generate** a longer string. The model still samples \(p(y_t\mid y_{<t},\text{prompt})\). The prompt asked for steps, so the string contains them.
4. **Parse** a final boxed answer separately from the trace. Gold for this item is 408. Lab 13’s `23+19` traces are the same idea.
5. **Score two things.** Answer accuracy on the box, and a trace check (note **13.3**). Do not claim the model “reasoned” unless you have a check on the steps.

A CoT string that actually computes \(17\times 24\) writes \(10\times 24=240\), \(7\times 24=168\), \(240+168=408\). Three intermediate lines hold partial products. That trace is also **faithful** (note **13.3**): the last computed value matches the box. A CoT-shaped line that computes \(17\times 20=340\) and then boxes 408 is the unfaithful cousin.

---

## 5. Mathematical formulas

The model is still next-token prediction. Let \(x\) be the CoT prompt (instruction, optional few-shot traces, and the question). The joint string of steps and answer is

\[
p_\theta(y\mid x)=\prod_{t}p_\theta(y_t\mid y_{<t},x).
\]

There are no new parameters. CoT changed \(x\) and the length of \(y\), not \(\theta\).

Temperature 0 is \(\arg\max\) at each step: one greedy chain. That is a baseline, not self-consistency.

---

## 6. Positive points and negative points

**Positive.**

- Extra tokens are extra test-time compute, which can hold partial products on multi-hop items.
- You can inspect the tape; Lab 13 grades traces as strings without an API.
- Zero-shot and few-shot are cheap knobs compared with training a new net.
- A correct, faithful trace (last computed value matches the box) is something you can show.

**Negative.**

- Extra steps can hurt one-hop lookup: more tokens are more chances to wander.
- Latency and cost scale with trace length.
- Fluent wrong algebra still looks like work; faithfulness is the next note.
- CoT is not retrieval and not tools. A longer string does not fetch a PDF or run a calculator.
- Few-shot traces from the wrong task point at the wrong procedure.

**When not to.** A single-hop fact lookup. A task that needs a document (Week 14 RAG) or an exact product (a calc tool), not more prose.

---

## 7. How to write it in a report

Say whether the prompt was zero-shot or few-shot, paste the exact instruction, and freeze decoding settings (temperature, max tokens). Do not claim the model “reasoned” unless you have a check on the steps. Temperature 0 is a single greedy chain: useful as a baseline, not as a vote (note **13.2**).

---

## 8. Teaching this note

About **30 minutes** at the board, then **~8 minutes** of video. First of three Week-13 notes; Lab 13 is constructed traces, not an API.

- **0–10 min.** Direct vs CoT prompt. Tokens as scratch paper.
- **10–20 min.** When CoT helps (multi-hop) vs hurts (lookup). Cost.
- **20–30 min.** Worked 17 × 24 on the board, then a one-hop counterexample.
- **Then** play Karpathy intro **35:00–38:02** (Thinking, System 1/2). Pause on “models need tokens to think.”

---

## 9. Worked example

Prompt: \(17\times 24\). Direct decode might jump to a familiar number (400, 408, 428) with no check.

A CoT string that actually computes:

1. \(10\times 24=240\)
2. \(7\times 24=168\)
3. \(240+168=408\)

Three intermediate tokens (here, three lines) hold partial products. The boxed answer is 408. Gold is 408. This trace is also **faithful** (note **13.3**): the last computed value matches the box.

![Partial products 240, 168, 408](files/data-643/graphics/13.1-chain-of-thought/cot-partial.png)

A one-hop item, “Capital of France?”, does not need hops. A CoT prompt can invent a story (“Lyon was the capital in…”) and then still say Paris—or wander to Lyon. Extra decode is extra risk. That is why you report **answer accuracy** and, separately, a trace check, not a vibe that the model “showed work.”

Lab 13’s `23+19` traces are the same algebra with smaller numbers.

---

## 10. Where students get stuck

- Calling CoT a fine-tune. It is a **prompt / decoding** choice unless you trained on traces.
- Scoring only the box. Wrong steps plus a lucky 408 will look like a win until note **13.3**.
- Pasting few-shot examples from a different task (math shots, then a policy question) and blaming the model.

---

## 11. Video

Watch [Andrej Karpathy, Intro to Large Language Models](https://www.youtube.com/watch?v=zjkBMFhNj_g), **35:00–38:02**.

Pause on System 1 vs System 2: the model gets more compute by emitting more tokens. That is extra test-time compute in classroom language. Optional nearby: **38:02–40:45** (self-improvement) is not required for this note. Notes **14.1–14.2** and **15.1** reuse this same URL at other minutes.

---

## 12. Practice

1. Why might CoT raise accuracy on a four-hop word problem and lower it on “What is the capital of France?”

2. Few-shot CoT puts examples in context. What goes wrong if those examples are a different task than the test item?

3. Name one number you would report besides final-answer accuracy if your project uses CoT.

4. Write a three-line CoT for \(17\times 24\) that ends in 408. Then write one line that is CoT-shaped but computes \(17\times 20=340\) and boxes 408. Which is unfaithful?

5. Direct prompt, temperature \(0\), one sample: accuracy \(0.62\). CoT, temperature \(0\), one sample: accuracy \(0.71\), mean tokens \(4\times\) longer. What two numbers belong in the table besides \(0.71\)?
