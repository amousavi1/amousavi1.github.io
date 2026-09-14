These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

A trace can be **wrong** and the boxed answer **right**. That is **unfaithful** chain-of-thought: the steps you read are not a reliable account of why the answer appeared.

---

## 1. Lucky answers

The decoder can jump to a familiar number, then invent arithmetic that pretends to justify it. Or it can compute 52 in the scratch work and still emit 42 because 42 was in the few-shot pattern. Final-answer accuracy will score both as wins. You should not.

![Steps that do not support the boxed answer](files/data-643/graphics/13.3-faithfulness/unfaithful.png)

**Faithful** here is a check you can run: do the written steps compute the stated answer, and are those steps valid for the problem? It is not a claim about inner states. We do not read the residual stream in this course. Fluency of the prose is not the check. A tidy paragraph can still fail the algebra.

---

## 2. How to flag it

On constructed traces (Lab 13) you can parse the last computed value from the steps and compare it to the answer field. Mismatch \(\Rightarrow\) unfaithful. On free-form LM output you need a checker: unit tests, a calculator, a second model, or a human rubric. CoT plus self-consistency can still vote up an unfaithful majority if the lucky answer is popular.

Related failure: **post-hoc** explanations in RAG (Week 14). Citing a chunk you never used is the same shape of bug. Majority vote (note **13.2**) does not repair it: many traces can share the lucky box.

---

## 3. What belongs in a project

If you advertise “the model shows its work,” add a faithfulness number: fraction of traces whose checked steps match the answer, among items with a correct box. Report a failure case where the box is right and the algebra is not. That is more useful than another leaderboard screenshot.

---

## 4. Practice

1. Accuracy is 90% and 40% of those wins have invalid steps. What is the faithfulness problem in one sentence?

2. Why is “the steps look fluent” a weak faithfulness metric?

3. Design a tiny checker for `23+19` traces stored as lists of strings. What would you parse?
