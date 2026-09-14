These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

**RLHF** (InstructGPT / ChatGPT-style) is a three-stage stack: SFT, a reward model, then a **policy** optimized with RL (usually **PPO**) so sampled replies score high under the RM without wandering too far from SFT.

---

## 1. The loop

1. **SFT** on instruction pairs (note **8.1**). Call this \(\pi_{\text{SFT}}\).
2. **RM** \(r_\phi\) on chosen/rejected pairs (note **9.1**).
3. **PPO:** sample \(y\sim\pi_\theta(\cdot\mid x)\), score with \(r_\phi\), update \(\pi_\theta\).

![SFT, reward model, PPO policy](files/data-643/graphics/9.2-rlhf/loop.png)

PPO is on-policy: you need fresh rollouts from the current \(\pi_\theta\). That is expensive (generate, reward, critic). The **critic** (value head) estimates advantages so the policy gradient has lower variance. You do not need to derive PPO in this course; you need the picture and the KL term.

---

## 2. The KL penalty

Without a constraint, \(\pi_\theta\) **hacks** \(r_\phi\): long, flattering, or degenerate text that the RM likes. The usual objective looks like

\[
\mathbb{E}_{x,y\sim\pi_\theta}\bigl[r_\phi(x,y)-\beta\,\mathrm{KL}\bigl(\pi_\theta(\cdot\mid x)\,\|\,\pi_{\text{ref}}(\cdot\mid x)\bigr)\bigr],
\]

with \(\pi_{\text{ref}}=\pi_{\text{SFT}}\) frozen. \(\beta\) is the knob: large \(\beta\) stays near SFT; small \(\beta\) chases reward. In code this is often a per-token penalty \(\beta\log\pi_\theta-\beta\log\pi_{\text{ref}}\).

---

## 3. Why people look past PPO

It works at company scale and is finicky in a seminar: sampling, KL, reward scale, and a moving policy. **DPO** (next note) skips the RM and the loop. RLHF is still the conceptual parent: preferences \(\to\) a scalar of “better” \(\to\) a policy that maximizes it with a leash.

For a project, running full PPO on an LLM is usually out of scope. Best-of-\(n\) with a tiny RM, or DPO on a small classifier, is enough to show you understood the stack.

---

## 4. Practice

1. Which of the three stages needs *samples from the current policy*, not a fixed dataset?

2. If \(\beta=0\), what failure mode should you expect?

3. Why is \(\pi_{\text{ref}}\) the SFT model rather than the raw pretrained LM?
