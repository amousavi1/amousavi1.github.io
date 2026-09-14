These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

The last week of content is also how you **show** the project. A talk is not a tour of notebooks. It is a question, a method, a number, an ablation, and a failure you actually inspected.

---

## 1. One metric that matches the question

Pick the number that would change your mind. Retrieval: recall@k plus an answer score. Generation: a task metric plus a human or checklist on a slice. Alignment: a refusal or preference rate you can recompute. Do not lead with loss curves.

![A talk slide: metric, ablation, one failure](files/data-643/graphics/14.3-eval-presentations/talk.png)

State the split, the baseline, and the seed. If a closed API is in the loop, still report an open baseline (project note). Uncertainty belongs next to the number: a range over seeds, or at least “\(n=\) this many test items.”

---

## 2. Ablation and a failure case

An ablation turns one knob off (no retrieval, no CoT, no LoRA, \(k=1\) vs \(k=5\)) and shows the metric move. If it does not move, say so.

A **failure case** is a real input: the retrieved chunks, the trace, the image, the unsafe completion. Explain the bug class (missed mode, unfaithful steps, ignored observation, stereotype in CLIP space). This is the same honesty rule as Weeks 11–13: coverage, faithfulness, citations.

---

## 3. The talk

Time is short. Suggested spine: question (30 s), system picture (1 min), main table (1 min), ablation (30 s), failure case (1 min), limit and next step (30 s). Graduate mini-project: one experiment from the paper, what you reran, what differed.

Slides: few words, readable axes, ids on chunks if you do RAG. Canvas holds the slot and the upload. Week 15’s remaining talks follow that same spine. Practice the failure-case minute; that is usually what people remember.

---

## 4. Practice

1. Your accuracy rose 2 points and the variance across seeds is 3 points. What do you say in the talk?

2. Name an ablation that would be fake (does not match your method claim).

3. You have one minute left. Which is more useful: another architecture diagram, or one failure with the retrieved ids?
