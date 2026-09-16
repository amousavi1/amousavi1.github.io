These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

Weights store facts as distributed circuitry. **Editing** tries to change **one** association. **Unlearning** tries to remove a **set** of examples or a topic so they are no longer easy to recover. Both are approximate; neither is a legal delete button.

---

## 1. ROME: locate, then write

Meng et al., **ROME** (Rank-One Model Editing). Empirically, many “subject \(\to\) attribute” facts (Paris, capital of, France) concentrate in a mid-layer MLP on the last token of the subject. **Locate** that layer with causal traces; **write** a rank-one update so the same key maps to a new value.

![Locate a fact in an MLP, write a new value](files/data-643/graphics/10.2-editing-unlearning/rome.png)

**MEMIT** extends the write across several layers for many facts at once. The algebra is a constrained least-squares update of the MLP down-projection, not a full fine-tune. Side effects: neighborhood facts can move; paraphrases may still leak the old value.

A rank-one write is one outer product, \(uv^{\top}\), added into an MLP weight. That is enough to redirect **one** key. It is not a delete of a topic.

Stanford CS224N 2025’s interpretability lecture: if a component stores the association, **intervening** on it should change the predicted object. ROME is that slogan as an edit: locate the mid-layer MLP at the last subject token, then write. **CounterFact**-style grading needs three columns: edit success, neighborhood (specificity), paraphrase (generalization).

Causal tracing (the locate step) is an ablation: run the fact prompt, patch hidden states from a clean run into a corrupted run, see which layer restores the object. You will not implement traces in Lab 10; you need the slogan **locate, then write**.

---

## 2. Unlearn a set versus edit a key

**Edit a key:** one prompt, one new completion (`The capital of France is Berlin` as a toy). Success is that prompt (and close paraphrases) flipping, while unrelated geography stays put.

**Unlearn a set:** a corpus you want gone (a book, personal data, a toxic cluster). Methods: gradient ascent on those rows, influence-style downweighting, relabel-and-SFT, or extra DPO against the bad completions. You must check **utility** on a retain set, not only forget accuracy. Models memorize by many routes; one loss spike does not erase a concept.

![Forgetting a set while keeping a retain set](files/data-643/graphics/10.2-editing-unlearning/unlearn.png)

Lab 10 will overwrite a dictionary key—that is editing as data structure, not as ROME. The analogy: a key–value store is parametric memory you can assign; an LLM is not.

---

## 3. What to report

Specificity (did neighbors survive?), generalization (paraphrase, multilingual), and a retain metric. If your project needs “remove this,” say which operational definition you used (extractive QA accuracy, membership inference, verbatim string match). Verbatim drop can hide latent knowledge.

Hallucination in the Deep Dive clip is the model guessing from parametric memory when it should look something up. Editing tries to rewrite that memory. Unlearning tries to make a set hard to guess. Neither replaces a datastore (note **10.3**).

---

## 4. Teaching this note

About **35 minutes** at the board: one key rewrite vs a 200-document forget set, then three numbers (edit success, neighbor, retain). Play Deep Dive **1:20:32–1:41:46** (hallucination, knowledge / working memory). Lab 10’s dict overwrite is the cartoon, not ROME.

Write the three probes (edit, neighbor, paraphrase) as a grading rubric. A report with only the edit prompt fails the rubric even if that prompt flipped.

---

## 5. Worked example

Edit: `Paris` \(\to\) `capital of Germany` (toy). Probe A: “The capital of France is” should now prefer Berlin. Probe B (neighbor): “The capital of Italy is” should still be Rome. Probe C (paraphrase): “France’s capital city is” may still say Paris if the write sat on one surface form. That is why paraphrase is a required column.

![Edit 8/10 is not isolated if neighbors move](files/data-643/graphics/10.2-editing-unlearning/edit-probes.png)

Unlearn: 200 forget documents, 200 retain documents. After ascent on the forget set, forget-QA accuracy 90% \(\to\) 20% looks like success **until** retain-QA 88% \(\to\) 21%. You did not unlearn a topic; you damaged the model. Report both.

ROME is one rank-one bump. Unlearning “all EU capitals” is a set. Do not expect the single write to wipe the set. Lab 10: `facts["paris"]="..."` vs `del` every value containing `"capital"`.

Count parameters in the cartoon write: if the MLP down-projection is \(d\times 4d\) with \(d=4\) in a toy, a rank-one \(uv^{\top}\) is \(4+16=20\) numbers, not a full fine-tune. Scale is different in an LLM; the **rank** is the point.

---

## 6. Where students get stuck

- Measuring only the edited prompt. Neighbors and paraphrases are the method.
- Treating verbatim-string drop as “the fact is gone.”
- Using one ROME write for a whole category. That is unlearning, a different job.

---

## 7. Video

[Karpathy — Deep Dive into LLMs like ChatGPT](https://www.youtube.com/watch?v=7xTGNNLPyMI). Play **1:20:32–1:41:46** (hallucinations, tool use, **knowledge / working memory**). Pause on facts living in weights versus being looked up: editing fights the first; RAFT (next note) trains the second. ROME’s rank-one write is the board.

---

## 8. Practice

1. ROME writes a rank-one bump in one MLP. Why might a paraphrase still produce the old fact?

2. You unlearn a 200-document set and only measure those 200 prompts. What did you fail to measure?

3. Editing `Paris → Berlin` is a key rewrite. Unlearning “all EU capitals” is a set. Which one should you *not* expect ROME’s single write to do well?

4. Edit success 8/10, neighbor success 2/10, retain 9/10. In one sentence, did the write isolate the fact? What would you try next: another layer, or a smaller step size?

5. Forget set 100 items (30 still recalled), retain set 100 items (10 now wrong). Write forget-failure and retain-failure rates. Which rate is the utility cost?
