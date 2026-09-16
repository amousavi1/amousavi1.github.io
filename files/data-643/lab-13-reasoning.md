Work in a **Jupyter** notebook with **Python** (NumPy optional). Do notes **13.1–13.3** first. **No LLM API.** The traces are lists of strings we constructed.

**First time you implement this.** The lecture notes this week already answered what the method is, why it exists, the architecture, the formula, and the tradeoffs. Read that first-time block before these exercises. This lab is the first time you **compute** it, not the first definition.

```python
PROBLEMS = [
    {
        "id": "p1",
        "q": "23 + 19",
        "gold": 42,
        "traces": [
            {"steps": ["20 + 19 = 39", "39 + 3 = 42"], "answer": 42},
            {"steps": ["23 + 19 = 32"], "answer": 32},
            {"steps": ["3 + 9 = 12, write 2 carry 1", "2 + 1 + 1 = 4, so 42"], "answer": 42},
            {"steps": ["23 + 10 = 33", "33 + 9 = 52"], "answer": 42},
        ],
    },
    {
        "id": "p2",
        "q": "6 * 7 + 5",
        "gold": 47,
        "traces": [
            {"steps": ["6 * 7 = 42", "42 + 5 = 47"], "answer": 47},
            {"steps": ["6 * 7 = 42", "42 + 5 = 47"], "answer": 47},
            {"steps": ["6 + 7 = 13", "13 * 5 = 65"], "answer": 65},
            {"steps": ["6 * 7 = 42", "42 + 5 = 48"], "answer": 47},
        ],
    },
]
```

Trace `p1` last row: steps compute 52, boxed answer is 42. Trace `p2` last row: steps compute 48, box is 47. Those are **unfaithful**.

---

## 1. Parse and vote

```python
import re

def last_int(text):
    nums = [int(x) for x in re.findall(r"-?\d+", text)]
    return nums[-1] if nums else None

def step_result(trace):
    return last_int(" ".join(trace["steps"]))
```

1. For each problem, print every `answer` and `step_result`.

2. Majority vote on `answer` (break ties by first-seen winner). Compare the vote to `gold`.

3. Does voting beat the first trace alone on `p1`? On `p2`?

---

## 2. Flag unfaithful traces

A trace is unfaithful if `step_result != answer`. (If steps contain several integers, you are using the last one on purpose.)

1. Print a table: problem id, trace index, faithful?, answer correct?.

2. Count **lucky wins**: `answer == gold` and unfaithful.

3. Accuracy of the majority vote versus **faithful-only** majority (drop unfaithful traces before voting). If the faithful set is empty, write `None`.

---

## 3. Write-up

Four sentences: what self-consistency voted for on each problem, how many lucky wins you found, why a correct box is not a faithful chain, and one extra check you would add if the steps were free English (not just integers).
