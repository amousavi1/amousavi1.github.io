These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

A trace can be **wrong** and the boxed answer **right**. That is **unfaithful** chain-of-thought: the steps you read are not a reliable account of why the answer appeared. By the end you should be able to flag Lab 13’s 52-then-42 row, write the faithful-among-wins rate, and say why a majority vote of 42 is not a faithfulness check.

---

## 1. What faithfulness is

**Faithfulness** asks whether the **steps caused** the answer, not whether the box is lucky. A lucky win: last step says 52, box says 42, gold is 42. Accuracy can pass while the trace is a lie.

Chen et al. (2025) document a related product failure: models can **use a hint** without writing it in the CoT. This course’s classroom version is Lab 13: last integer 52, box 42. Lightman et al. (*Let’s Verify Step by Step*) distinguish a **process** reward, which scores the steps, from an **outcome** reward, which scores only the box. We do not train a process RM here. We run a checker on constructed traces.

**Faithful** here is a check you can run: do the written steps compute the stated answer, and are those steps valid for the problem? It is not a claim about inner states. We do not read the residual stream in this course. Fluency of the prose is not the check. A tidy paragraph can still fail the algebra.

The decoder can jump to a familiar number, then invent arithmetic that pretends to justify it. Or it can compute 52 in the scratch work and still emit 42 because 42 was in the few-shot pattern. Final-answer accuracy will score both as wins. You should not.

---

## 2. Why we use it

CoT and self-consistency can look careful and still be unfaithful. A project that “shows work” must check the work. Majority vote (note **13.2**) does not repair it: many traces can share the lucky box. Three unfaithful traces can still vote 42.

Related failure: **post-hoc** explanations in RAG (Week 14). Citing a chunk you never used is the same shape of bug.

You need two columns because they move separately. A lucky win increments accuracy and fails faithfulness. An honest miss (wrong box, steps that match that wrong box) is a different story from theater that happens to box the gold.

---

## 3. Architecture

There is no new net. There is a **checker**: parse intermediates versus the box. Optional later machinery is a process reward model that scores steps, versus outcome-only training. This lab does not train either.

On constructed traces (Lab 13) you can parse the last computed value from the steps and compare it to the answer field. Mismatch \(\Rightarrow\) unfaithful. On free-form LM output you need a checker: unit tests, a calculator, a second model, or a human rubric.

![Steps that do not support the boxed answer](files/data-643/graphics/13.3-faithfulness/unfaithful.png)

Lab 13’s last `p1` trace: steps compute 52, box is 42. Last `p2` trace: steps compute 48, box is 47. Those are lucky wins if the box matches gold.

Do not call the checker rate “reasoning accuracy.” Call it a **checker pass rate**. Inner states are out of scope.

---

## 4. How it works, step by step

Take Lab 13’s last `p1` row, gold \(42\).

1. Read the steps as strings: `"23 + 10 = 33"`, `"33 + 9 = 52"`.
2. Parse the last integer in the steps: \(52\).
3. Compare that integer to the `answer` field. Here `answer` is \(42\), so \(52\neq 42\): **unfaithful**.
4. Compare `answer` to gold. \(42=42\): **correct box**, therefore a **lucky win**. Accuracy +1, faithfulness 0 on this row.
5. Report two rates on the set: answer accuracy, and **faithful-among-wins** (below). Do not drop unfaithful traces only when the box is wrong. Lucky wins are the ones that hide.

A checker for `23+19` traces stored as lists of strings is `last_int(" ".join(steps))` versus `answer`. Fluency of `"so 42"` in the prose would not pass this check if the last computed integer was 52.

---

## 5. Mathematical formulas

Accuracy is the fraction of items whose box matches gold. Faithfulness among wins is a different fraction:

\[
F=\frac{\#\{\text{correct box and steps match box}\}}{\#\{\text{correct box}\}}.
\]

If 10 items have the right box and 4 of those have matching steps, \(F=0.4\). Accuracy can be \(0.90\) while \(F=0.40\). Those two numbers are the point.

A cartoon one-row check is \(\mathrm{last\_int}(\text{steps})=\text{answer}\) for faithfulness of that trace, and \(\text{answer}=\text{gold}\) for a correct box. Lucky win means the second holds and the first fails.

---

## 6. Positive points and negative points

**Positive.**

- A last-integer checker catches theater on constructed traces without training a process RM.
- Faithful-among-wins is a number you can put next to accuracy, instead of a vibe that the model showed work.
- The same bug class shows up in RAG citations (used `[d1]`, wrote `[d2]`), so the habit transfers.
- Lab 13 already stores steps as lists of strings, so the parser is a few lines.

**Negative.**

- Checkers can be wrong: a regex can miss a later correction, or a second model can rubber-stamp fluent nonsense.
- Humans are slow; a rubric does not scale to every project run.
- Process rewards are extra training, and we do not train one here.
- Majority vote of a lucky box is still unfaithful. SC does not substitute for a checker.
- Scoring fluency (“the steps read nicely”) is a weak metric and will pass theater.

**When not to.** Do not advertise “the model shows its work” with only box accuracy. Do not treat a process RM paper as this lab.

---

## 7. What belongs in a project

If you advertise “the model shows its work,” add a faithfulness number: fraction of traces whose checked steps match the answer, among items with a correct box. Report a failure case where the box is right and the algebra is not. That is more useful than another leaderboard screenshot.

Do not call that number “reasoning accuracy.” Call it a **checker pass rate**. Inner states are out of scope.

---

## 8. Teaching this note

About **30 minutes** at the board, then **~12 minutes** of video. Then start Lab 13 if the vote note is already done.

- **0–10 min.** Define unfaithful: last step value \(\neq\) box, or steps invalid.
- **10–20 min.** Lucky win vs honest miss. Why accuracy is not enough.
- **20–30 min.** Worked Lab 13 row: 52 in the steps, 42 in the box. Design the parser.
- **Then** play Karpathy Deep Dive **1:20:32–1:41:46** (hallucinations, tool use, working memory). Pause on confident wrong answers; name that **unfaithful** when it happens *inside* a CoT trace, not only in a final sentence.

---

## 9. Worked example

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

## 10. Where students get stuck

- Scoring fluency (“the steps read nicely”) as faithfulness.
- Dropping unfaithful traces only when the box is **wrong**. Lucky wins are the ones that hide.
- Assuming a majority vote of 42 is faithful. Three unfaithful traces can still vote 42.

---

## 11. Video

Watch [Andrej Karpathy, Deep Dive into LLMs like ChatGPT](https://www.youtube.com/watch?v=7xTGNNLPyMI), **1:20:32–1:41:46**.

Pause on hallucinations and on tools as working memory: a calculator observation is a check the trace can ignore (Week 14) or use. Same URL as note **13.2**; different chapter. Do not treat this segment as a jailbreak lesson.

---

## 12. Practice

1. Accuracy is 90% and 40% of those wins have invalid steps. What is the faithfulness problem in one sentence?

2. Why is “the steps look fluent” a weak faithfulness metric?

3. Design a tiny checker for `23+19` traces stored as lists of strings. What would you parse?

4. Steps last-integer \(52\), box \(42\), gold \(42\). Fill in: faithful? correct box? lucky win?

5. Four traces, boxes \(42,42,32,42\). Two of the \(42\)s are unfaithful. Majority vote on boxes? Faithful-only majority if you drop unfaithful traces first?
