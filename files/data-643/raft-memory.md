These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

Facts can live in **weights** (parametric) or in an **external store** you look up (non-parametric). **RAFT** here is **retrieval-augmented fine-tuning**: you train the model *with* retrieved documents in context so it learns to use them, not only to recite the pretrain snapshot.

---

## 1. RAFT: train the reader, not only the index

A vanilla RAG pipeline (Week 14) retrieves at test time and hopes the frozen LLM attends. Domain RAFT (Zhang et al. and related recipes) builds training rows that look like the test stack: question, a set of snippets (some relevant, some **distractors**), and an answer that must cite or ignore on purpose. The loss is SFT on that answer. The model learns “read this, skip that.”

![Retrieve, then fine-tune the reader on the bundle](files/data-643/graphics/10.3-raft-memory/raft.png)

If every training snippet is gold, the model never practices rejecting junk. Include negatives. If you never train with retrieval, editing the index will not fix a model that ignores the index. RAFT is still SFT: the labels are answers *given the bundle*, not a new architecture.

---

## 2. Parametric versus non-parametric memory

**Parametric:** the MLP and attention weights. Fast, always on, hard to update (ROME, SFT, forgetting). **Non-parametric:** a datastore, BM25, embeddings, a kNN over hidden states (kNN-LM, RETRO, memorizing transformers). You update a fact by writing a snippet, not by locating a layer.

![Weights versus an external memory](files/data-643/graphics/10.3-raft-memory/memory.png)

Hybrids are the product default: parametric priors plus retrieved evidence. Lab 10’s token-overlap retriever is a non-parametric cartoon. Overwriting a dict key is a parametric cartoon.

---

## 3. What to choose

Need daily-changing policy PDFs? Non-parametric plus a RAFT-style reader. Need style and instruction following? Parametric SFT/LoRA. Need to correct one biography? Try an edit **and** a datastore row; measure both. Hallucination often means the parametric prior won over the snippet. RAFT is how you train that fight.

---

## 4. Practice

1. Why add distractor snippets to RAFT training rows?

2. You can fix a wrong salary in a PDF. Which memory did you update?

3. Name one failure that retrieval cannot fix if the reader was never trained to look at the context.
