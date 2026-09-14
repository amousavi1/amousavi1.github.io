These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

**Red-teaming** is organized probing: you try to elicit disallowed or unreliable behavior so you can **measure** it, then patch or refuse. It is an evaluation method, not a product feature. If your project claims “safe,” this week is how you would show your work.

---

## 1. Safety evaluation is a dataset of probes

A probe is a prompt (or a multi-turn script) aimed at a failure class: harmful instructions, privacy leakage, demographic stereotyping, over-refusal of benign medical questions, jailbreak-style roleplay that tries to undo the system prompt. You run a **fixed list**, plus a small exploratory budget. Success for the attacker is a policy violation; success for you is catching it.

![Probes in, model out, a logged failure](files/data-643/graphics/10.1-red-teaming/probe.png)

Score with a rubric or a judge model, then **spot-check the judge**. Automatic scores drift. Public benchmarks (XSTest, HarmBench-style sets, ToxiGen) are starting points; your domain needs its own rows.

---

## 2. Log the successful attacks

A failure that is not logged cannot be regressed against next week’s checkpoint. Store: prompt, output, category, severity, whether it was a known template, and the model hash. Do **not** publish a cookbook of working exploits on the open web as “extra credit.” The course artifact is a **count and a taxonomy** (e.g., 4/40 probes in category C), plus one anonymized example in the appendix if the instructor asks.

Iterated red-teaming: patch (SFT, DPO, a rule, a filter), then **rerun the same log**. New attacks will appear; that is expected. Coverage, not a one-time clean bill.

Threat model in the report: who is attacking (curious user versus a persistent adversary), what is in-bounds (the model’s text), and what is out of bounds (phishing real people, touching production keys). The probe list should match that model.

---

## 3. What red-teaming is not

It is not a substitute for access control, and it is not a promise that the model is aligned. Dual-use: the same skill that finds leaks can be misused. In this class you stay on toy models, public benchmarks, and instructor-specified categories. If a probe would cause real harm off-platform, you do not run it.

---

## 4. Practice

1. Why rerun an old successful probe after a DPO update?

2. A judge model labels 100 outputs “safe.” Why still read a sample by hand?

3. Name one benign prompt that should *not* be refused, so you can measure over-refusal.
