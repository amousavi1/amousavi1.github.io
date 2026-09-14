These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

Pretraining teaches **next token on the web**. **Supervised fine-tuning (SFT)** teaches a model to follow **instructions**: a user message, a demonstration of a good reply. Same transformer, different data.

---

## 1. Pretrain, then SFT

The pretrained decoder already assigns probability to every continuation. It does not, by default, answer as an assistant, refuse a harmful ask, or stay in a JSON schema. SFT continues maximum-likelihood training, but now each example is a **prompt \(\to\) response** pair and you typically supervise only the response tokens (mask the prompt in the loss).

![Pretraining then instruction SFT](files/data-643/graphics/8.1-sft-instructions/sft.png)

InstructGPT’s first stage, Alpaca, Vicuna, and most “chat” checkpoints start here. Preference methods (Week 9) sit **on top of** an SFT policy; they are not a substitute for a coherent instruction distribution.

If the concatenated string has \(T_p\) prompt tokens and \(T_r\) response tokens, the SFT loss averages over \(T_r\) positions, not \(T_p+T_r\). Otherwise the model spends gradient on imitating the user.

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

Token accounting: if you report “2,000 SFT rows” without \(T_r\), you have not said how much supervision you ran. Ten-token answers and 400-token answers are different datasets. Masking the prompt is also a compute choice: you still **forward** the prompt (the model must condition on it); you just zero those positions in the loss.

---

## 4. Teaching this note

About **30–35 minutes** at the board: pretrain vs SFT on one toy string, mask the prompt, then a good pair vs a noisy scrape. Play Karpathy **14:14–21:05** (finetuning into an assistant, ~7 min). Lab 8 is LoRA/forgetting, not an instruction dump.

Chalk the mask as a 0/1 vector under the tokens. If nobody can say why the zeros sit on the user side, replay that minute before the video.

---

## 5. Worked example

Token ids, cartoon: prompt `[user] List two colors.` is 6 tokens; response ` red blue` is 3 tokens (including a leading space, say). The causal LM still predicts every next token, but the **loss mask** is \(0,0,0,0,0,0,1,1,1\). Gradient hits only the three response positions.

Batch of two: one 80-token medical pair (all response tokens clean), one 800-token forum thread with a junk target. Uniform average over tokens \(\Rightarrow\) the forum dominates 10:1. That is why 80 perfect pairs should lead the first SFT run, and the 80,000 threads should be filtered or down-weighted.

A pair must include a **prompt that looks like test time** and a **demonstration you would accept**. A pretraining document has neither role.

If you include chain-of-thought in SFT, the demonstration **is** the trace plus the answer. At eval you must ask for the same format or you are measuring a different target. That is prompt design as method, not a style footnote.

---

## 6. Where students get stuck

- Training on the whole concat equally, so the model learns to mimic the user.
- Equating “more rows” with “better SFT” when most rows are noisy.
- Thinking SFT is RLHF. SFT copies answers; preferences come in Week 9.

---

## 7. Video

[Karpathy — Intro to Large Language Models](https://www.youtube.com/watch?v=zjkBMFhNj_g). Play the **post-training / assistant** section **14:14–21:05**. Pause when he contrasts the base model with the assistant: that is SFT. RLHF in the appendix (**21:05+**) waits for Week 9.

---

## 8. Practice

1. Why mask the prompt tokens in the SFT loss instead of training next-token on the whole concatenated string equally?

2. You have 80 perfect medical instruction pairs and 80,000 noisy forum threads. Which set should dominate the first SFT run, and why?

3. Name one thing a good SFT pair must include that a pretraining document does not.

4. Prompt length 40, response length 10, batch 4 sequences (all the same lengths). How many token positions enter the SFT mean? What fraction of the concat is that?

5. You SFT with the template `### Instruction:` but eval with ChatML roles. Why can the loss look fine while the demo fails?
