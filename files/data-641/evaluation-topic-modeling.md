## 1. Why bother measuring topics

A topic model always returns \(k\) word lists. That does not mean the lists are themes.

Evaluation is how you:

- reject a bad run (or a bad \(k\))
- compare SVD, NMF, and LDA on **this** corpus
- tune priors, iterations, and preprocessing
- check that a human in the domain can name the topics
- feed the next experiment (the feedback loop)

Likelihood on the training matrix is not enough. A model can fit counts and still produce a topic that is *the, of, said* plus one noun.

![Evaluating topic models](files/data-641/graphics/topic-eval.png)

---

## 2. Automatic metrics

These do not replace reading the words. They let you discard hopeless settings before you read.

| Metric | Question it asks | Watch for |
| ------ | ---------------- | --------- |
| **Perplexity** | How well does the model predict held-out documents? | Lower is better. Can disagree with human quality |
| **Coherence** (PMI, NPMI, \(C_V\)) | Do the top words in a topic actually co-occur? | `gensim.CoherenceModel` is the usual tool |
| **Topic diversity** | Do topics share too many top words? | High diversity can also mean fragmented junk |
| **Silhouette** | If you treat \(\theta\) as a clustering, do documents sit in tight groups? | Needs a hard assignment; LDA is a mix |
| **Stability** | Do the same topics reappear across random seeds or subsamples? | Unstable topics are not ready to ship |

Perplexity is a language-model number. Deep-learning stacks expose it; classical LDA libraries expose a bound or a held-out likelihood. Use it to compare **the same family** of models, not to declare LDA "better" than NMF.

Coherence is the metric you will actually plot against \(k\). If \(C_V\) peaks at 12 and the word lists at 12 are namable, stop there.

---

## 3. Human and downstream checks

**Topic intrusion.** Show a person the top words of a topic plus one **intruder** word from another topic. If they cannot spot the intruder, the topic is a mess. There is no standard library; you can run this on a form or on Mechanical Turk.

**Document clustering.** If you have gold categories (section labels, product lines), treat the model's hard topic or a clustering of \(\theta\) as a partition. Then use ARI, NMI, or Fowlkes–Mallows (`sklearn.metrics`). This measures agreement with a known cut, not "beauty" of the words.

**Use the topics.** If the model is a recommender or a browsing UI, measure clicks, not NPMI. Note **recommender-systems** takes that view.

---

## 4. How to run an evaluation, practically

1. Freeze preprocessing (stops, min count, n-grams). Then sweep \(k\).
2. For each \(k\), record coherence, diversity, and a quick read of the worst topic.
3. Rerun the winner with three seeds. If the names change, do not write a report yet.
4. Only then look at perplexity or a clustering score.

A number without a word list is not a result. A word list without a number is a vibe. You want both.

LDA, NMF, and LSA are not ranked by one universal winner. They are ranked on your documents, your \(k\), and whether a person can use the output.

---

## 5. A short scorecard you can reuse

Write this down for every run:

- corpus and preprocessing hash (or a one-line description)
- method and \(k\), seed, iterations
- mean coherence and the worst topic's top 10 words
- a yes/no: could you name every topic in five minutes?

If the last box is no, the numbers do not matter yet. Note **14.1** and **14.2** are the models. This note is how you refuse a pretty but useless factorization. Week 15 (summarization, MT, recommenders) will reuse topics only if they pass this bar.

---

## 6. Practice

1. Coherence is high and every topic's top words include *company*, *said*, *year*. What is broken, the metric or the preprocessing?

2. Why might the \(k\) that minimizes perplexity be different from the \(k\) a journalist can name?

3. You rerun LDA twice with \(k=20\). Half the topics shuffle. What do you report to a stakeholder, and what do you try next?

Report the instability. Do not average two incompatible name lists and call that the model.
