These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

**Direct Preference Optimization (DPO)** (Rafailov et al., 2023) fits a policy to chosen/rejected pairs **without** training an RM and **without** PPO. The reward is written in closed form from the policy and a frozen reference, then the Bradley–Terry model becomes a classification loss on logits.

---

> **First time this method appears.** **DPO** fits a policy to the same preference pairs **without** an RM loop and **without** PPO.
>
> **What.** Under Bradley–Terry, the optimal reward is \(r=\beta\log(\pi/\pi_{\mathrm{ref}})+c(x)\). Plug into the logistic loss; \(r\) disappears. Train \(\pi_\theta\) offline.
> **Why.** RLHF’s PPO stage is heavy. DPO is a classification loss on logits of \(y_w\) and \(y_l\).
> **Architecture.** Policy + frozen reference. No critic, no sampling-in-the-loop required (you need logprobs of both completions).
> **How.** Lab 9: toy scalar logits. Start: \(\pi=\pi_{\mathrm{ref}}\) ⇒ loss \(\log 2\).
> **Formula.** \(\mathcal{L}_{\mathrm{DPO}}=-\log\sigma\big(\beta\log\frac{\pi_\theta(y_w\mid x)}{\pi_{\mathrm{ref}}(y_w\mid x)}-\beta\log\frac{\pi_\theta(y_l\mid x)}{\pi_{\mathrm{ref}}(y_l\mid x)}\big)\).
> **Tradeoffs.** + Offline, no RM. − Still needs pairs and a reference; can overfit; not magic if the pairs are noisy.
>
## 1. Skip the reward model

RLHF solves \(\max_\pi \mathbb{E}[r]-\beta\mathrm{KL}(\pi\|\pi_{\text{ref}})\). Under Bradley–Terry, the optimal \(r\) can be expressed as

\[
r(x,y)=\beta\log\frac{\pi(y\mid x)}{\pi_{\text{ref}}(y\mid x)}+\text{const}(x).
\]

Plug that into the RM logistic loss and the \(r\) parameters disappear. You train \(\pi_\theta\) directly.

The derived reward has a **partition \(Z(x)\)** that cancels because Bradley–Terry only sees a difference. KTO and IPO sit in the same family; this hour is DPO.

![DPO: pairs in, policy out, no RM loop](files/data-643/graphics/9.3-dpo/dpo.png)

---

## 2. The loss

\[
\mathcal{L}_{\text{DPO}}=-\log\sigma\Biggl(\beta\log\frac{\pi_\theta(y_w\mid x)}{\pi_{\text{ref}}(y_w\mid x)}-\beta\log\frac{\pi_\theta(y_l\mid x)}{\pi_{\text{ref}}(y_l\mid x)}\Biggr).
\]

In a batch you need log-probabilities of **both** completions under \(\pi_\theta\) and under \(\pi_{\text{ref}}\). The reference stays frozen (usually SFT). \(\beta\) is the same kind of leash as in RLHF: it scales how hard you push away from \(\pi_{\text{ref}}\).

Lab 9 will compute this on toy scalar logits, not on an LLM.

If \(\pi_\theta=\pi_{\text{ref}}\), both log-ratios are 0, the argument of \(\sigma\) is 0, and \(\sigma(0)=1/2\). Then \(\mathcal{L}_{\text{DPO}}=\log 2\approx 0.693\). That is the **start** of training, not a bug.

Write the argument of \(\sigma\) as \(\beta\bigl(\Delta\log\pi_\theta-\Delta\log\pi_{\mathrm{ref}}\bigr)\) if it helps: you want \(\pi_\theta\) to put relatively more mass on \(y_w\) than the reference did, compared with \(y_l\). Absolute log-prob can fall on both sequences; **relative** log-prob is what DPO scores.

---

## 3. When DPO is the right picture

You have pairs, a GPU, and no appetite for a PPO stack. Offline: the pair set is fixed, so you do not explore new \(y\) unless you collect more. If the SFT model never proposed good \(y_w\), DPO cannot invent them from nothing. Implicit reward can still overfit the pair set.

Report \(\beta\), the reference checkpoint, and a held-out preference accuracy (how often \(\pi_\theta\) assigns higher log-prob to \(y_w\) than to \(y_l\)). That number is not “the model is aligned”; it is “the model copied this rater.”

---

## 4. Teaching this note

About **35–40 minutes** at the board: write implicit \(r\), plug into \(\sigma\), compute \(\sigma(0)=1/2\). Play the Deep Dive **preference / RLHF** segment **2:48:26–3:09:39**. Lab 9 section 2 is the toy DPO scalar.

---

## 5. Worked example

Let \(\beta=1\). Suppose at init \(\pi_\theta=\pi_{\mathrm{ref}}\). Then

\[
\log\frac{\pi_\theta(y_w)}{\pi_{\mathrm{ref}}(y_w)}-\log\frac{\pi_\theta(y_l)}{\pi_{\mathrm{ref}}(y_l)}=0,
\]

so \(\mathcal{L}=-\log\sigma(0)=-\log(1/2)=\log 2\).

After a few steps, toy log-probs (sums over tokens): \(\log\pi_\theta(y_w)=-2.0\), \(\log\pi_{\mathrm{ref}}(y_w)=-2.5\), \(\log\pi_\theta(y_l)=-3.0\), \(\log\pi_{\mathrm{ref}}(y_l)=-2.0\). Log-ratio winner: \(-2.0-(-2.5)=0.5\). Log-ratio loser: \(-3.0-(-2.0)=-1.0\). Difference \(0.5-(-1.0)=1.5\). \(\sigma(1.5)\approx 0.818\), loss \(-\log 0.818\approx 0.201\).

The frozen reference is still there: without it, \(\pi_\theta\) can raise both log-probs or collapse. PPO can **sample new** \(y\) that were not in the pair file; offline DPO cannot.

![Init loss \(\log 2\), then a 1.5 logit gap](files/data-643/graphics/9.3-dpo/dpo-init.png)

---

## 6. Where students get stuck

- Forgetting \(\sigma(0)=1/2\) when \(\pi_\theta=\pi_{\mathrm{ref}}\) at step 0.
- Dropping \(\pi_{\mathrm{ref}}\) because “there is no RM.” The reference **is** the leash.
- Expecting DPO to invent replies the SFT model never wrote.

---

## 7. Video

[Karpathy — Deep Dive into LLMs like ChatGPT](https://www.youtube.com/watch?v=7xTGNNLPyMI). Play the **preference** segment **2:48:26–3:09:39** (RLHF). Pause on comparison data: DPO uses those same pairs, without the PPO loop. The closed-form loss is the board.

---

## 8. Practice

1. If \(\pi_\theta=\pi_{\text{ref}}\), what is \(\mathcal{L}_{\text{DPO}}\)? (Compute \(\sigma(0)\).)

2. Why do you still keep a frozen reference if there is no RM?

3. Name one thing PPO can do that offline DPO cannot, given a fixed pair file.

4. \(\beta=2\), winner log-ratio \(0.4\), loser log-ratio \(0.1\). What is the argument of \(\sigma\), and is the loss smaller or larger than \(\log 2\)?

5. Both completions have log-prob \(-10\) under \(\pi_\theta\) and under \(\pi_{\mathrm{ref}}\). What is the DPO loss, and what did the policy fail to learn yet?
