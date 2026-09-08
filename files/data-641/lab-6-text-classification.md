Work in a **Jupyter** notebook. Number the exercises. Do notes **6.1** and **6.2** first. You will need `pandas` and `scikit-learn`.

Download [covid19_tweets.csv](files/data-641/covid19_tweets.csv) into the same folder as the notebook. You already vectorized these tweets in Lab 4. This week you put a **classifier** on the end.

When you are done: **File → Download as → HTML**, then upload the HTML on Canvas. Save the notebook before you export.

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report, confusion_matrix
```

---

## 1. Load and split (1 point)

1. Read `covid19_tweets.csv`. Use `Tweet` as `X` and `Is_Unreliable` as `y`. Drop empty tweets.

2. Print the class counts. Say whether the problem is balanced.

3. Split **70% train / 30% test**, stratified on `y`. Print the train and test sizes and the class mix in each.

Fit the vectorizer **only** on the training text.

---

## 2. TF–IDF features (1 point)

Build a `TfidfVectorizer` (unigrams, or unigrams plus bigrams). Fit on the training tweets. Transform train and test.

Print the vocabulary size and the shape of the two document-term matrices. If you cap `max_features` or drop stop words, say so.

---

## 3. \(k\)-NN (1 point)

Train `KNeighborsClassifier` on the TF–IDF train matrix. Cosine distance is the usual choice on these vectors (`metric="cosine"`). Pick a `k` and say why.

Print a classification report on the test set (accuracy, precision, recall, F1).

---

## 4. Linear SVM (1 point)

Train `LinearSVC` on the same train matrix. Print the test classification report.

In a comment: which model wins on F1 (or on the class you care about), and is the gap large enough to matter?

---

## 5. Errors the average hid (1 point)

Print a confusion matrix for the **better** of the two models. Then do **one** of these:

- read three false positives and three false negatives (print the tweet text)
- or list the tokens with the largest SVM coefficients if you used `LinearSVC`

Write two or three sentences: what the model is using, and one failure a single F1 number hid.
