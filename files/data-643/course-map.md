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

A two-hour weekly meeting is not four independent mini-classes. You will usually get **one 30–40 minute board note**, a short video clip, discussion, and lab time. The other notes that week are homework or the second board block.

---

## 2. A language model is a stack

An LLM is not one trick. It is layers of ideas. Week 1 is the bottom: a neuron, a training loop, and a vector for a word. Week 3 puts attention on those vectors. Later weeks align, retrieve, and ship.

![The LLM stack, with Week 1 at the base](files/data-643/graphics/1.1-course-map/stack.png)

If you already know MLPs and Word2Vec from another class, treat this week as a fast map into the rest of the syllabus. If you do not, this week is the on-ramp.

When you use a chat product you are standing on the **top** of that stack (decoding, tools, a UI). The weights you never see still came from next-token training. If your project “uses GPT,” name the layer you will actually change: data, a prompt, an adapter, a retriever, or an eval.

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

## 5. Teaching this note

This is a **30–40 minute** first-day board block. Draw the four-module roadmap, then the stack, then spend the rest of the time turning a vague “I want to use an LLM” into a measurable project sentence. Play **0:00–20:00** of the Karpathy talk (pause at the two-file Llama picture and at the pretrain vs. assistant split). Lab 1 can wait until notes 1.2–1.4.

---

## 6. Worked example

Karpathy’s running example is Llama 2 **70B**. Each parameter is stored as 2 bytes (float16), so the weights file is

\[
70 \times 10^{9} \times 2~\text{bytes} = 1.4 \times 10^{11}~\text{bytes} = 140~\text{GB}.
\]

Write two columns on the board: **parameters file** vs **run file**. Then walk ChatGPT down the stack: next-token pretraining (Week 1–3), post-training (Weeks 8–9), retrieval/tools (Week 14). Circle the one layer a student project can actually change.

Now rewrite a bad topic. Bad: “Use LoRA on news.” Better: “Does a LoRA adapter on local news reduce entity hallucination vs. the base model, measured by exact-match on a 100-item holdout?”

---

## 7. Where students get stuck

- Treating the course as “how to prompt ChatGPT” instead of a stack you can measure.
- Picking a method first (“we will fine-tune”) before a question and a dataset.
- Assuming DATA 641/642 is required, then tuning out of Week 1.

---

## 8. Video

Watch [Karpathy: Intro to Large Language Models](https://www.youtube.com/watch?v=zjkBMFhNj_g), **0:00–20:00**.

Pause at **0:20** (an LLM is two files: weights + a little code), **4:17** (pretraining as next-token compression of the internet), **8:58** (“dreams” / fluent but ungrounded text), and **14:14** (fine-tuning into an assistant). Stop at the **17:52** summary. The rest of the hour is optional homework.

---

## 9. Practice

1. Name one product you use that sits on the top of the stack in the figure. Which lower layer would you have to change to make it safer?

2. A classmate took DATA 641. Another did not. Why is Week 1 still required for both?

3. Write one sentence that could be a project question (not a method). Example: “Can retrieval cut hallucination on AU policy PDFs?” is a question. “Use LoRA” is not.

4. Llama 2 70B stores each parameter as 2 bytes. Compute the weights-file size in GB. If you instead stored the same 70 billion parameters as 1-byte integers, what would the file size be?

5. A two-hour meeting uses 20 minutes of video and 25 minutes to start Lab 1. The remaining time is split equally across notes 1.2, 1.3, and 1.4. How many minutes does each of those notes get?
