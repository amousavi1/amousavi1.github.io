These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

Pretraining teaches **next token on the web**. **Supervised fine-tuning (SFT)** teaches a model to follow **instructions**: a user message, a demonstration of a good reply. Same transformer, different data.

---

## 1. Pretrain, then SFT

The pretrained decoder already assigns probability to every continuation. It does not, by default, answer as an assistant, refuse a harmful ask, or stay in a JSON schema. SFT continues maximum-likelihood training, but now each example is a **prompt \(\to\) response** pair and you typically supervise only the response tokens (mask the prompt in the loss).

![Pretraining then instruction SFT](files/data-643/graphics/8.1-sft-instructions/sft.png)

InstructGPT’s first stage, Alpaca, Vicuna, and most “chat” checkpoints start here. Preference methods (Week 9) sit **on top of** an SFT policy; they are not a substitute for a coherent instruction distribution.

---

## 2. What an instruction pair looks like

A row is not a Wikipedia paragraph. It is a task plus an answer you are willing to imitate:

- user: “Summarize this abstract in two sentences.”
- assistant: the two sentences.

System prompts, few-shot exemplars, and tool schemas are part of the **prompt design**, not a separate model. Wording changes the SFT target: “be brief” and “write a memo” are different labels.

![An instruction paired with a demonstration](files/data-643/graphics/8.1-sft-instructions/pair.png)

Quality beats volume once you have a few thousand clean pairs. Noisy scraped “instructions” teach the noise. If you mix many tasks, you still risk **forgetting** the pretrain distribution (note **8.2**).

---

## 3. Prompt design, as method

Write the template you used (roles, delimiters, whether you included chain-of-thought). Evaluate with the same template. A project that “just fine-tuned LLaMA” without showing the instruction mix is incomplete. SFT can overfit to a style; it cannot invent a reward for “humans prefer B over A.” That is Week 9.

---

## 4. Practice

1. Why mask the prompt tokens in the SFT loss instead of training next-token on the whole concatenated string equally?

2. You have 80 perfect medical instruction pairs and 80,000 noisy forum threads. Which set should dominate the first SFT run, and why?

3. Name one thing a good SFT pair must include that a pretraining document does not.
