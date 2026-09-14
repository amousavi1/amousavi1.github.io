These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

This course is **self-contained**. DATA 441/641 and DATA 442/642 are **not** prerequisites. The listed prerequisite is DATA 427/627. Some ideas overlap those courses on purpose: embeddings, neural nets, and later transformers, so students who have not taken them can still finish an LLM project.

The main job of the semester is a **project**. Lectures and labs exist so that project has a backbone.

---

## 1. What the course is

DATA 443/643, *Advanced Concepts in Large Language Models*, is about how modern language systems are built, trained, adapted, and checked.

You will see:

- the architectures (feedforward nets, then sequence models, then transformers)
- how those models are scaled and aligned
- multimodal systems (vision, language, audio)
- generation, reasoning, retrieval, and tool use

Software: Python, PyTorch, Hugging Face, Jupyter. Canvas remains official for due dates.

![Four modules from nets to tools](files/data-643/graphics/1.1-course-map/roadmap.png)

---

## 2. A language model is a stack

An LLM is not one trick. It is layers of ideas. Week 1 is the bottom: a neuron, a training loop, and a vector for a word. Week 3 puts attention on those vectors. Later weeks align, retrieve, and ship.

![The LLM stack, with Week 1 at the base](files/data-643/graphics/1.1-course-map/stack.png)

If you already know MLPs and Word2Vec from another class, treat this week as a fast map into the rest of the syllabus. If you do not, this week is the on-ramp.

---

## 3. The project starts now

Undergraduate teams and graduate students (solo or a small team, as posted on Canvas) will pick a problem in language, multimodal AI, retrieval, or alignment.

Typical shape:

1. a question you can measure
2. a public dataset or a well-scoped corpus
3. a baseline, then one change that the course material justifies
4. an ablation and an honest failure case
5. a proposal, a talk, and an IEEE-style report

Graduate students also complete a **mini-project** on a recent paper (reproduce or extend one experiment). That is separate from the main project.

Do **not** wait until October to pick a topic. After Lab 1 you should be able to name a domain (news, clinical notes, code, speech, images+captions) even if the method is still “we will fine-tune something.”

---

## 4. What Week 1 is for

By Friday you should be able to:

- write the forward pass of one neuron and of a small MLP
- say what gradient descent is changing, and what it is minimizing
- explain why a dense embedding can represent similarity when a one-hot vector cannot
- tell intrinsic evaluation of embeddings from extrinsic evaluation
- name one way geometry can encode bias

Notes **1.2–1.4** and Lab 1 do that work.

---

## 5. Practice

1. Name one product you use that sits on the top of the stack in the figure. Which lower layer would you have to change to make it safer?

2. A classmate took DATA 641. Another did not. Why is Week 1 still required for both?

3. Write one sentence that could be a project question (not a method). Example: “Can retrieval cut hallucination on AU policy PDFs?” is a question. “Use LoRA” is not.
