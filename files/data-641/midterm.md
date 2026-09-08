## 1. What this week is

The midterm covers **Weeks 1–8**. It is a check that you can run the applied stack from raw text to a classifier, including the neural models from Weeks 7 and 8.

There are no new lecture topics this week. Use the time to close gaps, not to skim Week 10.

Canvas is the official source for time, place, and allowed materials. This note is only a study map.

---

## 2. What is in scope

| Block | Weeks | You should be able to |
| ----- | ----- | --------------------- |
| Map of NLP and Python | 1 | Name core tasks; say what is ML vs rules; write small Python (lists, dicts, files) |
| NLP pipeline | 2–3 | Acquisition, cleanup, preprocessing, features, modeling, evaluation, deployment |
| Representations | 4–5 | One-hot, bag of words, TF–IDF, distributed vectors, Word2Vec (CBOW / skip-gram) |
| Classification | 6 | A text-classification pipeline; classical models and how you evaluate them |
| CNNs for text | 7 | Why a convolution helps on n-grams; how a CNN classifier is wired |
| RNNs for text | 8 | Why recurrence fits sequences; how an RNN classifier uses hidden state |

"Be able to" means: define the piece, say when you would use it, and work a short example or diagram. It does not mean memorize API flags.

Labs and homework through this block are fair practice. If a fact lived only in a footnote of a later module, it is out.

---

## 3. How to prepare

**Re-read your own notes and labs.** Redo a pipeline on a tiny file: clean, tokenize, vectorize, fit, score. If you cannot do that without the solution notebook, start there.

**Build a one-page crib of definitions** (for study, not for the room unless the instructor allows it): precision / recall / F1, TF–IDF, embedding, filter / feature map, hidden state. Write one sentence in your own words for each.

**Compare representations.** Same sentence as one-hot, as BoW counts, as TF–IDF, as a Word2Vec average. Know what is lost at each step.

**Trace a CNN and an RNN on a short sequence.** What is shared across positions? What is the input to the next step? You do not need to derive every gradient.

**Work old mistakes.** Midterms repeat the ideas people missed on homework, not the same numbers.

---

## 4. What this exam is not

It is not Weeks 10–15 (IE, chatbots, topic models, summarization, MT). Those come after.

It is not a trivia quiz about paper titles or library version numbers.

It will not be described further here. If you want the format or a sample, ask in class or read the Canvas announcement—not this page.

---

## 5. Practice

1. List the pipeline stages from acquisition to monitoring. For a spam filter, which stage is your current bottleneck?

2. In one sentence each, contrast bag of words with a skip-gram embedding.

3. Why would you pick a CNN rather than a bag-of-words logistic model for a phrase-sensitive task, and when is the logistic model enough?
