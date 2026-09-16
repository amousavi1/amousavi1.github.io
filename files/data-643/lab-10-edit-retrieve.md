Work in a **Jupyter** notebook with **Python** (stdlib is enough; `numpy` optional). Do notes **10.2–10.3** first. Optional file: [toy_facts.csv](files/data-643/toy_facts.csv).

```python
from pathlib import Path
```

---

## 1. A dict of facts, then one overwrite

Parametric memory as a key–value map.

```python
facts = {
    "paris": "capital of France",
    "berlin": "capital of Germany",
    "rome": "capital of Italy",
    "othello": "play by Shakespeare",
}
```

1. Print `facts["paris"]`. Then **edit the key**: `facts["paris"] = "capital of Germany"`. Print again. Unrelated keys must be unchanged. That is ROME’s *goal*, as a dictionary.

2. **Unlearn a set:** `del` every key whose value contains `"capital"`. What is left? Compare to (1): one assignment versus deleting a category.

3. If you load the CSV (`subject,relation,object` rows), build the dict from `subject`, then overwrite one subject. Print a retain list of subjects you did not touch.

---

## 2. Retrieve by token overlap

Non-parametric memory: a list of snippets, score by overlap with a query.

```python
snippets = [
    "Paris is the capital of France.",
    "Berlin is the capital of Germany.",
    "Rome is the capital of Italy.",
    "Othello is a tragedy by Shakespeare.",
    "The Seine flows through Paris.",
]

def toks(s):
    return set(s.lower().replace(".", "").split())

def retrieve(query, k=2):
    q = toks(query)
    scored = [(len(q & toks(s)), s) for s in snippets]
    scored.sort(reverse=True)
    return scored[:k]
```

1. Query `"capital of France"`. Is the Paris snippet first? Query `"Seine"`. Did geography beat Shakespeare?

2. After the dict overwrite in (1), retrieval still returns France for Paris if the **snippets** were not updated. Print both answers. That is parametric versus non-parametric drift.

3. Add a distractor snippet `"Paris is a city in Texas."` and query `"Paris capital"`. Report both top-2. A RAFT-style reader would have to ignore the Texas row; your overlap score will not.

---

## 3. Write-up

Four sentences: what overwriting a key did not do (paraphrases, other languages), why deleting a set is a different API than ROME, what token overlap misses that embeddings would catch, and why training with distractors (RAFT) is about the reader, not the index.
