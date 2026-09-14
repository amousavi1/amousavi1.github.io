These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

**Direct Preference Optimization (DPO)** (Rafailov et al., 2023) fits a policy to chosen/rejected pairs **without** training an RM and **without** PPO. The reward is written in closed form from the policy and a frozen reference, then the Bradley–Terry model becomes a classification loss on logits.

---

## 1. Skip the reward model

RLHF solves \(\max_\pi \mathbb{E}[r]-\beta\mathrm{KL}(\pi\|\pi_{\text{ref}})\). Under Bradley–Terry, the optimal \(r\) can be expressed as

\[
r(x,y)=\beta\log\frac{\pi(y\mid x)}{\pi_{\text{ref}}(y\mid x)}+\text{const}(x).
\]

Plug that into the RM logistic loss and the \(r\) parameters disappear. You train \(\pi_\theta\) directly.

![DPO: pairs in, policy out, no RM loop](files/data-643/graphics/9.3-dpo/dpo.png)

---

## 2. The loss

\[
\mathcal{L}_{\text{DPO}}=-\log\sigma\Biggl(\beta\log\frac{\pi_\theta(y_w\mid x)}{\pi_{\text{ref}}(y_w\mid x)}-\beta\log\frac{\pi_\theta(y_l\mid x)}{\pi_{\text{ref}}(y_l\mid x)}\Biggr).
\]

In a batch you need log-probabilities of **both** completions under \(\pi_\theta\) and under \(\pi_{\text{ref}}\). The reference stays frozen (usually SFT). \(\beta\) is the same kind of leash as in RLHF: it scales how hard you push away from \(\pi_{\text{ref}}\).

Lab 9 will compute this on toy scalar logits, not on an LLM.

---

## 3. When DPO is the right picture

You have pairs, a GPU, and no appetite for a PPO stack. Offline: the pair set is fixed, so you do not explore new \(y\) unless you collect more. If the SFT model never proposed good \(y_w\), DPO cannot invent them from nothing. Implicit reward can still overfit the pair set.

Report \(\beta\), the reference checkpoint, and a held-out preference accuracy (how often \(\pi_\theta\) assigns higher log-prob to \(y_w\) than to \(y_l\)). That number is not “the model is aligned”; it is “the model copied this rater.”

---

## 4. Practice

1. If \(\pi_\theta=\pi_{\text{ref}}\), what is \(\mathcal{L}_{\text{DPO}}\)? (Compute \(\sigma(0)\).)

2. Why do you still keep a frozen reference if there is no RM?

3. Name one thing PPO can do that offline DPO cannot, given a fixed pair file.
