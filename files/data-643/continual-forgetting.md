These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

Train on task B after task A and **task A’s accuracy falls**. That drop is **catastrophic forgetting**. It is not a bug in one optimizer; it is what a single shared \(\boldsymbol{W}\) does when the new gradient points away from the old solution.

---

## 1. Why the old skill dies

The SFT (or pretrain) minimum for A is a point in weight space. Fine-tuning on B walks away from it. In an MLP, the same hidden units implemented both functions; XOR then AND in Lab 8 is the cartoon. In an LLM, new instruction data overwrites features that still mattered for coding, or for a language you are not currently sampling.

![Accuracy on A falling while B is trained](files/data-643/graphics/8.2-continual-forgetting/forget.png)

Measuring it is part of the method: keep a **held-out A set** and plot it every \(k\) steps of B. If you only report B, you did not look. Instruction SFT is a special case: the “old task” is everything the base model already did (code, languages, refusal style).

---

## 2. Replay and other patches

**Replay:** mix a buffer of A examples into the B batches so the gradient still has a component that preserves A. The buffer can be real stored rows or **pseudo-replay** (sample the old model). This is the idea you will implement in spirit: do not throw A away.

![Old examples mixed into the new stream](files/data-643/graphics/8.2-continual-forgetting/replay.png)

Other knobs: smaller learning rates, freeze early layers, **regularize toward \(\boldsymbol{W}_A\)** (EWC-style penalties), or attach a **task adapter** and leave \(\boldsymbol{W}\) frozen (note **8.3**). Adapters are often the cleaner LLM answer: you add B without moving A’s weights.

---

## 3. Continual setups you will actually run

Instruction collections arrive in waves (new tool, new hospital, new semester). A legal design is: freeze the base, train LoRA on B, keep the A LoRA. Merging adapters is a separate, lossy step. If you must update one set of weights, replay A on purpose.

---

## 4. Practice

1. You fine-tune only on AND after XOR. What should happen to XOR accuracy if the hidden layer is tiny and shared?

2. Why is sampling the *old* model a form of replay even when you cannot store the old dataset?

3. Name one reason LoRA (next note) can avoid forgetting that replay cannot: the base \(\boldsymbol{W}\) never moves.
