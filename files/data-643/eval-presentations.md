These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

The last week of content is also how you **show** the project. A talk is not a tour of notebooks. It is a question, a method, a number, an ablation, and a failure you actually inspected.

---

## 1. One metric that matches the question

Pick the number that would change your mind. Retrieval: recall@k plus an answer score. Generation: a task metric plus a human or checklist on a slice. Alignment: a refusal or preference rate you can recompute. Do not lead with loss curves.

![A talk slide: metric, ablation, one failure](files/data-643/graphics/14.3-eval-presentations/talk.png)

State the split, the baseline, and the seed. If a closed API is in the loop, still report an open baseline (project note). Uncertainty belongs next to the number: a range over seeds, or at least “\(n=\) this many test items.”

Write the claim as a sentence a skeptic could falsify: “RAG raises exact-match on weekday hours by more than seed noise, with \(k=2\), bag-of-words cosine, \(n=50\).” If you cannot say the knob, you do not have a result yet.

---

## 2. Ablation and a failure case

An ablation turns one knob off (no retrieval, no CoT, no LoRA, \(k=1\) vs \(k=5\)) and shows the metric move. If it does not move, say so.

A **failure case** is a real input: the retrieved chunks, the trace, the image, the unsafe completion. Explain the bug class (missed mode, unfaithful steps, ignored observation, stereotype in CLIP space). This is the same honesty rule as Weeks 11–13: coverage, faithfulness, citations.

---

## 3. The talk

Time is short. Suggested spine: question (30 s), system picture (1 min), main table (1 min), ablation (30 s), failure case (1 min), limit and next step (30 s). Graduate mini-project: one experiment from the paper, what you reran, what differed.

Slides: few words, readable axes, ids on chunks if you do RAG. Canvas holds the slot and the upload. Week 15’s remaining talks follow that same spine. Practice the failure-case minute; that is usually what people remember.

What not to do: a twelve-slide architecture tour, a live notebook that might fail, or a metric you cannot recompute from the appendix. If the number is from a closed API, still show an open baseline on the same split. Graduate mini-project: name the paper experiment, what you reran, and one way your number differed—without a story about a venue.

---

## 4. Teaching this note

About **30 minutes** at the board (and a dry-run of one failure-case minute), then **20 minutes** of video.

- **0–10 min.** Metric matches the question. Baseline, split, \(n\), uncertainty.
- **10–20 min.** Ablation that could falsify the claim. Fake ablations.
- **20–30 min.** Worked 2-point “gain” that is smaller than seed noise. Talk spine on the board.
- **Then** play Peyton Jones **0:00–20:00**. Pause on “start with the problem” and on not drowning the audience in mechanism.

If the class still has remaining talks, use the last 30 minutes of the two-hour block for them, not for extra architecture slides. The note is done when every team can name their metric, ablation, and failure in one breath.

---

## 5. Worked example

You ran two seeds. Accuracy with RAG: \(0.82\) and \(0.78\) (mean \(0.80\)). No-retrieval baseline: \(0.80\) and \(0.76\) (mean \(0.78\)). Test set \(n=50\).

The mean lift is \(0.02\). The spread across seeds is \(0.04\). A 2-point gain with 3–4 points of seed jitter and \(n=50\) is **not** a result you lead with. In the talk you say: “point estimate +2 points; seeds move by about that much; \(n=50\).” Then you show a **failure case** that RAG actually changed: e.g. query about library hours, baseline hallucinated 21:00, RAG cited `[d1]` with 23:00—or RAG retrieved `[d2]` and the model ignored `[d1]`.

![Lift 0.02 versus seed spread 0.04](files/data-643/graphics/14.3-eval-presentations/seed-spread.png)

Fake ablation: you claim “LoRA on attention is why we beat the baseline,” but the ablation turns off dropout instead of the adapter. That knob was not the claim.

Time budget for a 5-minute slot: 30 s question, 1 min picture, 1 min table, 30 s ablation, 1 min failure, 30 s limit. If you have one minute left, drop a second architecture slide, not the failure.

Checklist before you upload slides: one question on slide 1, one table with a baseline, one ablation that matches the claim, one failure with ids or a trace, font large enough for the back row, no unreadable notebook dump.

---

## 6. Where students get stuck

- Leading with architecture diagrams and loss curves. The audience cannot grade those.
- Calling a 2-point bump a win when seed std is 3 points.
- Demoing only a cherry-picked success. The failure case is the scientific slide.

---

## 7. Video

Watch [Simon Peyton Jones, How to give a great research talk](https://www.youtube.com/watch?v=sT_-owjKIbA), **0:00–20:00**.

Pause when he insists on motivation before mechanism, and on slides the back row can read. The rest of that talk is optional after class. This is the presentation craft for Week 14–15; it is not a methods paper.

---

## 8. Practice

1. Your accuracy rose 2 points and the variance across seeds is 3 points. What do you say in the talk?

2. Name an ablation that would be fake (does not match your method claim).

3. You have one minute left. Which is more useful: another architecture diagram, or one failure with the retrieved ids?

4. Baseline \(0.70\), method \(0.74\), three seeds of the method \(0.71,0.74,0.77\), \(n=40\). Write one spoken sentence that is honest.

5. You claim RAG helps closing-time questions. What ablation belongs on the slide, and what one row would you show as a failure if retrieval returned the shuttle chunk?
