These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

DATA 443/643, *Advanced Concepts in Large Language Models*, is a **self-contained** course on how language systems are built, trained, adapted, and checked. The listed prerequisite is DATA 427/627. DATA 441/641 and DATA 442/642 are **not** required: when this course uses a neural net or an embedding, it teaches it here. The semester job is a **measured project**. This note is the map for that job: four modules, one stack, the loss that trained the weights, and a project sentence that names one layer you will change.

---

## 1. What the course is

The semester is four modules, taught bottom-up:

- neural nets and embeddings, then sequence models, then transformers
- how those models are scaled and aligned
- multimodal systems (vision, language, and audio)
- generation, reasoning, retrieval, and tool use

That is one object, not four electives. Software: Python, PyTorch, Hugging Face, Jupyter. Canvas remains official for due dates.

![Four modules from nets to tools](files/data-643/graphics/1.1-course-map/roadmap.png)

---

## 2. A language model is a stack

The roadmap is the calendar. The stack is the same object as a deployed system.

Chat products sit at the **top**: decoding, tools, a UI. The weights you never see still came from next-token training at the **bottom**. Week 1 is that bottom: a neuron, a training loop, and a vector for a word. Week 3 puts attention on those vectors. Later weeks align, retrieve, and ship.

![The LLM stack, with Week 1 at the base](files/data-643/graphics/1.1-course-map/stack.png)

If you already know MLPs and Word2Vec, treat this week as a fast map into the rest of the course. If you do not, this week is the on-ramp. Either way, when a project “uses GPT,” name the layer you will actually change: data, a prompt, an adapter, a retriever, or an eval.

---

## 3. What those weights were trained to do

A language model is a distribution over tokens. For a sequence \(w_1,\ldots,w_T\),

\[
P(w_1,\ldots,w_T)=\prod_{t=1}^{T} P(w_t\mid w_{<t}).
\]

Each factor is a **softmax** over the vocabulary (note 1.2 writes the definition). Pretraining minimizes the **negative log-likelihood** of the observed tokens, also called the next-token cross-entropy:

\[
L=-\sum_{t=1}^{T}\log P(w_t\mid w_{<t}).
\]

Tiny numeric: suppose the model assigns \(P(\text{mat}\mid \text{the cat sat on the})=0.70\). The NLL of that one token is \(-\log 0.70\approx 0.357\). If it had assigned \(0.10\), the NLL would be \(\approx 2.30\). That scalar is what gradient descent (note 1.3) walks downhill on, at web scale.

You will not train a transformer this week. You will train the same kind of scalar on XOR and on a three-word skip-gram softmax.

Those trained numbers have to live somewhere. Karpathy’s running example is Llama 2 **70B**. Each parameter is stored as 2 bytes (float16), so the weights file is

\[
70 \times 10^{9} \times 2~\text{bytes} = 1.4 \times 10^{11}~\text{bytes} = 140~\text{GB}.
\]

Write two columns: **parameters file** vs **run file**. Running the model needs extra memory for activations; 140 GB is only the file of numbers. In that picture an LLM is two files: the weights and a little code that reads them.

---

## 4. The project names one layer

Walk a chat product down the stack you just drew: next-token pretraining (Weeks 1–3), post-training (Weeks 8–9), retrieval and tools (Week 14). Circle the one layer a student project can actually change. Then write a sentence that is a **question plus a metric**, not a method.

Bad: “Use LoRA on news.” Better: “Does a LoRA adapter on local news reduce entity hallucination vs. the base model, measured by exact-match on a 100-item holdout?”

The full contract is the [project overview](data-643-project-overview.html). The shape you need this week:

1. a question you can measure
2. a public dataset or a well-scoped corpus
3. a baseline, then one change the course material justifies
4. an ablation and an honest failure case
5. a proposal, a talk, and an IEEE-style report

Undergraduate teams; graduate students solo or a small team, as posted on Canvas. Graduate students also complete a **mini-project** on a recent paper (reproduce or extend one experiment). That is separate from the main project.

Do **not** wait until October. After Lab 1 you should be able to name a domain (news, clinical notes, code, speech, images+captions) even if the method is still “we will fine-tune something.”

---

## 5. What Week 1 is for

Notes **1.2–1.4** and Lab 1 *are* the base of the stack in the figure. By the end of this meeting you should be able to:

- write the forward pass of one neuron and of a small MLP, including sigmoid, ReLU, \(\operatorname{ReLU}'\), and softmax
- take two gradient-descent steps by hand, and write one ReLU unit’s chain rule
- explain skip-gram’s softmax over a tiny vocabulary, and why Word2Vec keeps the lookup table
- tell intrinsic evaluation of embeddings from extrinsic evaluation
- name one way geometry can encode bias, with the signed-projection probe from Lab 1

This week does **not** include attention, LoRA, GloVe, or a history-of-NLP lecture. Those wait.

---

## 6. Teaching this note

**~26 minutes**, including a short Karpathy clip. Draw the four-module roadmap, then the stack, then the next-token product and the 140 GB file. Spend the remaining minutes turning “I want to use an LLM” into a measurable project sentence. Play **0:00–8:00** of Karpathy in class (two files, then next-token compression). Stop before the post-training tour.

The rest of the two-hour meeting: 1.2 neuron / XOR (~16 min) → 1.3 gradient descent (~18 min) → 1.4 skip-gram and bias (~18 min) → Lab 1 start (~32 min). Remaining videos are homework, not in-class playback.

---

## 7. Worked example

Put Llama 2 70B and a chat box on the same board.

1. Parameters file: \(70\times 10^{9}\times 2\) bytes \(=140\) GB. The run file is larger.
2. Walk the chat box down the stack. Circle one layer a project can change.
3. Rewrite the topic. “Use LoRA on news” becomes the better sentence in section 4.

---

## 8. Where students get stuck

- Treating the course as “how to prompt ChatGPT” instead of a stack you can measure.
- Picking a method first (“we will fine-tune”) before a question and a dataset.
- Assuming DATA 641/642 is required, then tuning out of Week 1.
- Confusing the 140 GB **weights file** with the extra memory needed to **run** the model.

---

## 9. Video

In class: [Karpathy: Intro to Large Language Models](https://www.youtube.com/watch?v=zjkBMFhNj_g), **0:00–8:00** (two files, then next-token compression).

Homework: finish **0:00–20:00**. Pause at **0:20** (an LLM is two files: weights + a little code), **4:17** (pretraining as next-token compression of the internet), **8:58** (“dreams” / fluent but ungrounded text), and **14:14** (fine-tuning into an assistant). Stop at the **17:52** summary. The rest of the hour is optional.

Also after class, not in the meeting: [Intro to deep learning: perceptron through gradient descent](https://www.youtube.com/watch?v=ErnWZxJovaM) from the perceptron (~17:20) through loss and gradient descent (~44:22). That is the homework-video twin of notes 1.2–1.3.

---

## 10. Sources

Karpathy’s intro talk is this note’s video. For the rest of Week 1, read rather than skim-cite:

- Goodfellow, Bengio, Courville, *Deep Learning*, Chapter 6 opening and **§6.1 XOR**: [deeplearningbook.org/contents/mlp.html](https://www.deeplearningbook.org/contents/mlp.html)
- Nielsen, *Neural Networks and Deep Learning*, Chapter 1 on gradient descent (stop before the long MNIST writeup): [neuralnetworksanddeeplearning.com/chap1.html](http://neuralnetworksanddeeplearning.com/chap1.html)
- Jurafsky & Martin, *Speech and Language Processing* (draft of 19 August 2026), **Chapter 5 Embeddings**: [web.stanford.edu/~jurafsky/slp3/5.pdf](https://web.stanford.edu/~jurafsky/slp3/5.pdf). The live draft moved vector semantics here; do not follow an older “Chapter 6 = embeddings” label.
- Mikolov et al. (2013a), *Efficient estimation of word representations*, §§1–3: [arXiv:1301.3781](https://arxiv.org/abs/1301.3781)

Cite, do not assign: Rumelhart, Hinton, Williams (1986) on backpropagation; Mikolov et al. (2013b) on negative sampling.

Related university courses appear once on the title slide and under **Extra materials** on the hub. They are not homework.

---

## 11. Practice

1. Name one product you use that sits on the top of the stack in the figure. Which lower layer would you have to change to make it safer?

2. A classmate took DATA 641. Another did not. Why is Week 1 still required for both?

3. Write one sentence that could be a project question (not a method). Example: “Can retrieval cut hallucination on AU policy PDFs?” is a question. “Use LoRA” is not.

4. Llama 2 70B stores each parameter as 2 bytes. Compute the weights-file size in GB. If you instead stored the same 70 billion parameters as 1-byte integers, what would the file size be?

5. A model assigns \(P(\text{cat}\mid \text{the})=0.40\) and \(P(\text{sat}\mid \text{the cat})=0.25\). What is the NLL of the two-token continuation “cat sat”? (Natural log is fine; leave it as \(-\log 0.40-\log 0.25\).)
