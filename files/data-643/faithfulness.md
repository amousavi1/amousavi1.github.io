These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

A trace can be **wrong** and the boxed answer **right**. That is **unfaithful** chain-of-thought: the steps you read are not a reliable account of why the answer appeared.

Stanford **CS224N 2026 L12** points at Chen et al. (2025): models can **use a hint** without writing it in the CoT. This course’s classroom version is Lab 13: last integer 52, box 42. **CS224N L13** / Lightman et al. (*Let’s Verify Step by Step*): a **process** reward scores the steps; an **outcome** reward scores only the box. We do not train a process RM here. We run a checker on constructed traces.

---

> **First time this evaluation appears.** **Faithfulness** asks whether the **steps caused** the answer, not whether the box is lucky.
>
> **What.** Lucky win: last step says 52, box says 42, gold is 42. Accuracy can pass while the trace is a lie. Process vs outcome (CS224N L13).
> **Why.** CoT and SC can look careful and still be unfaithful. A project that “shows work” must check the work.
> **Architecture.** No new net. A checker: parse intermediates vs the box. Optional process reward (score steps), vs outcome-only.
> **How.** Lab 13 flags the 52→42 row. Report accuracy **and** faithful-among-wins.
> **Formula.** Cartoon: \(\mathrm{F}=\#\{\text{wins with consistent trace}\}/\#\{\text{wins}\}\). Accuracy alone is not \(F\).
> **Tradeoffs.** + Catches theater. − Checkers can be wrong; humans are slow; process rewards are extra training (not this lab).
>
## 1. Lucky answers

The decoder can jump to a familiar number, then invent arithmetic that pretends to justify it. Or it can compute 52 in the scratch work and still emit 42 because 42 was in the few-shot pattern. Final-answer accuracy will score both as wins. You should not.

![Steps that do not support the boxed answer](files/data-643/graphics/13.3-faithfulness/unfaithful.png)

**Faithful** here is a check you can run: do the written steps compute the stated answer, and are those steps valid for the problem? It is not a claim about inner states. We do not read the residual stream in this course. Fluency of the prose is not the check. A tidy paragraph can still fail the algebra.

Lab 13’s last `p1` trace: steps compute 52, box is 42. Last `p2` trace: steps compute 48, box is 47. Those are lucky wins if the box matches gold.

---

## 2. How to flag it

On constructed traces (Lab 13) you can parse the last computed value from the steps and compare it to the answer field. Mismatch \(\Rightarrow\) unfaithful. On free-form LM output you need a checker: unit tests, a calculator, a second model, or a human rubric. CoT plus self-consistency can still vote up an unfaithful majority if the lucky answer is popular.

Related failure: **post-hoc** explanations in RAG (Week 14). Citing a chunk you never used is the same shape of bug. Majority vote (note **13.2**) does not repair it: many traces can share the lucky box.

---

## 3. What belongs in a project

If you advertise “the model shows its work,” add a faithfulness number: fraction of traces whose checked steps match the answer, among items with a correct box. Report a failure case where the box is right and the algebra is not. That is more useful than another leaderboard screenshot.

Do not call that number “reasoning accuracy.” Call it a **checker pass rate**. Inner states are out of scope.

---

## 4. Teaching this note

About **30 minutes** at the board, then **~12 minutes** of video. Then start Lab 13 if the vote note is already done. Lecture ideas follow **CS224N 2026 L12–L13** (unfaithful CoT; process vs outcome).

- **0–10 min.** Define unfaithful: last step value \(\neq\) box, or steps invalid.
- **10–20 min.** Lucky win vs honest miss. Why accuracy is not enough.
- **20–30 min.** Worked Lab 13 row: 52 in the steps, 42 in the box. Design the parser.
- **Then** play Karpathy Deep Dive **1:20:32–1:41:46** (hallucinations, tool use, working memory). Pause on confident wrong answers; name that **unfaithful** when it happens *inside* a CoT trace, not only in a final sentence.

---

## 5. Worked example

Trace (Lab 13, `p1` last row):

- steps: `"23 + 10 = 33"`, `"33 + 9 = 52"`
- `answer`: \(42\)
- gold: \(42\)

Parse the last integer in the steps: \(52\). Compare to `answer`: \(52\neq 42\). **Unfaithful.** Compare `answer` to gold: \(42=42\). **Lucky win.** Accuracy +1, faithfulness 0 on this row.

![52 in the steps, 42 in the box](files/data-643/graphics/13.3-faithfulness/lucky-win.png)

Faithfulness rate in a report, among correct boxes:

\[
\frac{\#\{\text{correct box and steps match box}\}}{\#\{\text{correct box}\}}.
\]

If 10 items have the right box and 4 of those have matching steps, the rate is \(0.4\). Say that. Do not say “the model reasoned on 90% of items” because accuracy was 90%.

A checker for `23+19` traces stored as lists of strings: `last_int(" ".join(steps))` vs `answer`. That is Lab 13. Fluency of `"so 42"` in the prose would not pass this check if the last computed integer was 52.

---

## 6. Where students get stuck

- Scoring fluency (“the steps read nicely”) as faithfulness.
- Dropping unfaithful traces only when the box is **wrong**. Lucky wins are the ones that hide.
- Assuming a majority vote of 42 is faithful. Three unfaithful traces can still vote 42.

---

## 7. Video

Watch [Andrej Karpathy, Deep Dive into LLMs like ChatGPT](https://www.youtube.com/watch?v=7xTGNNLPyMI), **1:20:32–1:41:46**.

Pause on hallucinations and on tools as working memory: a calculator observation is a check the trace can ignore (Week 14) or use. Same URL as note **13.2**; different chapter. Do not treat this segment as a jailbreak lesson.

---

## 8. Practice

1. Accuracy is 90% and 40% of those wins have invalid steps. What is the faithfulness problem in one sentence?

2. Why is “the steps look fluent” a weak faithfulness metric?

3. Design a tiny checker for `23+19` traces stored as lists of strings. What would you parse?

4. Steps last-integer \(52\), box \(42\), gold \(42\). Fill in: faithful? correct box? lucky win?

5. Four traces, boxes \(42,42,32,42\). Two of the \(42\)s are unfaithful. Majority vote on boxes? Faithful-only majority if you drop unfaithful traces first?
