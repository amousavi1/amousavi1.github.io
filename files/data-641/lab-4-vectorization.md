Work in a **Jupyter** notebook. Number the exercises. Do notes **4.1** through **4.5** first. You will need `pandas` and `scikit-learn`.

Download [covid19_tweets.csv](files/data-641/covid19_tweets.csv) into the same folder as the notebook (or use a relative path). Columns are `Tweet` (text) and `Is_Unreliable` (label). `Category` is optional this week.

When you are done: **File → Download as → HTML**, then upload the HTML on Canvas. Save the notebook before you export.

```python
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
```

`MultiLabelBinarizer` is one way to build a one-hot matrix over a vocabulary. `CountVectorizer` and `TfidfVectorizer` are the usual sklearn versions of bag-of-words, n-grams, and TF–IDF.

---

## 1. Load the tweets (1 point)

1. Read `covid19_tweets.csv` with pandas.

2. Print `shape`, column names, the label counts for `Is_Unreliable`, and two sample tweets.

3. Drop rows with empty `Tweet` text. Work from a list (or a Series) of the remaining tweets for the rest of the lab.

You are vectorizing this week, not classifying. You do not need a train/test split.

---

## 2. One-hot encoding (1 point)

Turn each tweet into a one-hot vector over the corpus vocabulary: a token is `1` if it appears in that tweet, `0` otherwise.

Print:

- the vocabulary size
- the shape of the document-term matrix
- the vector for **one** tweet, and the tokens that are on in that vector

A binary `CountVectorizer(binary=True)` or a `MultiLabelBinarizer` on tokenized tweets is enough. Say which you used.

---

## 3. Bag-of-words (1 point)

Same tweets, now with **counts**. Print the shape and the bag-of-words vector for the same tweet you used in Exercise 2, plus the tokens with nonzero counts.

If a tweet repeats a word, the count should be greater than 1. That is the difference from one-hot.

---

## 4. Bag of n-grams (1 point)

Use `CountVectorizer` with an n-gram range that includes more than unigrams (for example `ngram_range=(1, 2)` or `(2, 2)`). Print the n-gram vocabulary size, a few feature names, and the vector for the same tweet.

In a comment: which n-grams in that tweet would a unigram bag have missed?

---

## 5. TF–IDF (1 point)

Transform the same tweets with `TfidfVectorizer`. Print the shape and the TF–IDF vector for the same tweet.

In a short comment: name one token that looks more important under TF–IDF than under raw counts (or the reverse), and why that happened.
