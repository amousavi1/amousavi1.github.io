These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

Weights store facts as distributed circuitry. **Editing** tries to change **one** association. **Unlearning** tries to remove a **set** of examples or a topic so they are no longer easy to recover. Both are approximate; neither is a legal delete button.

---

## 1. ROME: locate, then write

Meng et al., **ROME** (Rank-One Model Editing). Empirically, many “subject \(\to\) attribute” facts (Paris, capital of, France) concentrate in a mid-layer MLP on the last token of the subject. **Locate** that layer with causal traces; **write** a rank-one update so the same key maps to a new value.

![Locate a fact in an MLP, write a new value](files/data-643/graphics/10.2-editing-unlearning/rome.png)

**MEMIT** extends the write across several layers for many facts at once. The algebra is a constrained least-squares update of the MLP down-projection, not a full fine-tune. Side effects: neighborhood facts can move; paraphrases may still leak the old value.

---

## 2. Unlearn a set versus edit a key

**Edit a key:** one prompt, one new completion (`The capital of France is Berlin` as a toy). Success is that prompt (and close paraphrases) flipping, while unrelated geography stays put.

**Unlearn a set:** a corpus you want gone (a book, personal data, a toxic cluster). Methods: gradient ascent on those rows, influence-style downweighting, relabel-and-SFT, or extra DPO against the bad completions. You must check **utility** on a retain set, not only forget accuracy. Models memorize by many routes; one loss spike does not erase a concept.

![Forgetting a set while keeping a retain set](files/data-643/graphics/10.2-editing-unlearning/unlearn.png)

Lab 10 will overwrite a dictionary key—that is editing as data structure, not as ROME. The analogy: a key–value store is parametric memory you can assign; an LLM is not.

---

## 3. What to report

Specificity (did neighbors survive?), generalization (paraphrase, multilingual), and a retain metric. If your project needs “remove this,” say which operational definition you used (extractive QA accuracy, membership inference, verbatim string match). Verbatim drop can hide latent knowledge.

---

## 4. Practice

1. ROME writes a rank-one bump in one MLP. Why might a paraphrase still produce the old fact?

2. You unlearn a 200-document set and only measure those 200 prompts. What did you fail to measure?

3. Editing `Paris → Berlin` is a key rewrite. Unlearning “all EU capitals” is a set. Which one should you *not* expect ROME’s single write to do well?
