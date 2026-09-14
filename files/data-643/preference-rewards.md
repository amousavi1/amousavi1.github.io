These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

SFT copies demonstrations. **Preferences** say which of two replies is better when both are fluent. A **reward model (RM)** is a classifier of that comparison. Week 9.2 will use the RM inside RL; Week 9.3 will skip it.

---

## 1. Chosen versus rejected

A human (or a strong teacher model) sees a prompt \(x\) and two completions \(y_w\) (**chosen**, winner) and \(y_l\) (**rejected**, loser). The label is a pairwise order, not a numeric grade. Ties and multi-way ranks exist; this course uses pairs.

![A prompt with a chosen and a rejected completion](files/data-643/graphics/9.1-preference-rewards/pair.png)

Collection is the bottleneck: instructions must be clear, raters disagree, and the pair set can encode rater bias. If both \(y_w\) and \(y_l\) are wrong, the RM still learns a relative order among mistakes.

---

## 2. The reward model

Initialize from the SFT policy (or its encoder). Score a pair with a scalar head \(r_\phi(x,y)\). Bradley–Terry / logistic loss:

\[
\mathcal{L}_{\text{RM}} = -\log \sigma\bigl(r_\phi(x,y_w)-r_\phi(x,y_l)\bigr).
\]

The RM wants a higher number on the chosen reply. Lab 9 will fit this on toy scores. At test time you can rank \(n\) samples from the policy by \(r_\phi\) (**best-of-\(n\)**) without any RL.

![A scalar reward head on a completion](files/data-643/graphics/9.1-preference-rewards/reward.png)

---

## 3. What the number is not

\(r_\phi\) is not truth, safety, or “helpfulness” in the abstract. It is a fit to the raters you hired, on the prompts you wrote. Reward hacking: the policy learns to please \(r_\phi\) with verbose, sycophantic, or empty-safe text. That is why RLHF adds a KL penalty to the SFT model (next note), and why you keep a held-out preference set.

---

## 4. Practice

1. If \(r(x,y_w)=r(x,y_l)\) always, what is \(\mathcal{L}_{\text{RM}}\)?

2. Why initialize the RM from SFT instead of from a raw pretrained LM?

3. Best-of-\(n\) uses the RM without PPO. What extra cost did you pay at inference?
