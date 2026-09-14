These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

**RAG** is retrieve, then generate. The language model does not have to store every fact in its weights. You give it **chunks** at request time and ask it to answer from those chunks.

---

## 1. Three stages

1. **Index.** Split documents, embed each chunk, store vectors plus the raw text and an id.
2. **Retrieve.** Embed the query, take top-\(k\) by cosine (or a hybrid with keywords).
3. **Generate.** Stuff the chunks into a prompt: answer the question, cite ids, say when the context is missing.

![Index documents, retrieve chunks, then generate with citations](files/data-643/graphics/14.1-rag-pipeline/rag.png)

The generator is still a next-token model. RAG changes its **conditioning**, not its architecture. A wrong index cannot be saved by a prettier prompt. Dense embeddings (Week 1, Week 5) are one index; keyword overlap is another. Lab 14 uses counts so the ranking is something you can print.

---

## 2. What can fail

Retrieval misses the supporting chunk (recall@k). Retrieval returns a near-miss that the model then over-trusts. The model **ignores** a good chunk and hallucinates. Citations that do not match the used sentences are the RAG version of unfaithful CoT (note **13.3**).

Chunk size, overlap, embedding choice, and \(k\) are method. Lab 14 uses bag-of-words cosine so you can see the ranking without a GPU. ReAct (note **14.2**) can treat retrieve as one action among others, including a calculator.

---

## 3. Measurement

Report retrieval recall@k on a labeled set of (question, gold chunk ids), then answer accuracy with an attribution check: does the cited id actually contain the claim? Always include a no-retrieval baseline. “We used RAG” is not a result.

---

## 4. Practice

1. Why can raising \(k\) hurt the answer even if it raises recall?

2. You retrieve the right chunk and the answer is still wrong. Name two different bugs.

3. What belongs in the index besides the embedding vector?
