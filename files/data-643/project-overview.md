These notes are the project contract for DATA 443/643. Canvas dates win if they disagree. The course is built around this project: lectures and labs exist so the report has methods you can defend.

---

## 1. What you are building

A **measured** system in language, multimodal AI, retrieval, alignment, or a close neighbor from the syllabus. Not a literature survey, and not a demo with no numbers.

Minimum shape:

1. a question
2. data with a license you can cite
3. a baseline
4. one change the course justifies (architecture, objective, retrieval, alignment, or efficiency)
5. an ablation or error analysis
6. a limitation you actually looked for (bias, hallucination, compute, leakage)

Undergraduate: group project, 10-page IEEE-style report, talk. Graduate: independent (or a smaller team if Canvas allows), same report shape, plus a **mini-project** on a recent paper.

---

## 2. Timeline (Fall 2026; exact days on Canvas)

| Milestone | Typical window |
| --------- | -------------- |
| Topic seed (Lab 1, ungraded) | Week 1 |
| Project proposal | October |
| Graduate mini-project proposal | October |
| Talks | December |
| Report | December |

Start reading data docs in Weeks 2–3. Do not wait for transformers (Week 3) to pick a domain.

---

## 3. Proposal

Two to three pages. Include:

- question and why it is not already solved by calling an API with the default prompt
- dataset, split, and label definition
- baseline and the one change
- compute budget (laptop GPU, Colab, AU, or CPU-only)
- success metric and a failure case you will inspect
- ethics: whose text, whose faces, what the ranking does to people

Graduate mini-project: name the paper (2024–2026), the experiment you will rerun or extend, and the resource you will use (open weights, not a closed API as the only method).

---

## 4. Report and talk

Report: IEEE-style, about 10 pages (mini-project: about 3). Figures of the system and of errors beat screenshots of a notebook.

Talk: undergraduate group and graduate main project as posted; graduate mini-project about 10 minutes plus questions.

Code: a notebook or repo that reruns the tables from a seed. If a closed model is involved, still include an open baseline.

---

## 5. Topic seeds (not a closed list)

- Retrieval-augmented answering over a documented corpus (policies, papers, manuals), with a hallucination check
- Instruction tuning or LoRA on a small open model for a narrow task, versus the base model
- CLIP-style retrieval or captioning, with a bias probe on occupations or geography
- Safety: a red-team set and a refusal metric you can compute
- Knowledge editing or unlearning on a factual slice, with a side-effect check
- Diffusion or GAN *conditioning on text* only if you already have GPU time; language-only projects are enough

If you took 641 or 642, do not resubmit that project. Reuse data only if the **question** is new (for example, the 641 classifier becomes a retrieval or alignment study).
