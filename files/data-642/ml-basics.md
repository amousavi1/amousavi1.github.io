These notes walk through the lecture slides. The original deck is unchanged; use **(slides)** on the course hub if you want that PDF.

The figures follow Géron, *Hands-On Machine Learning*, Ch. 1. *Mathematics for Machine Learning* is the math source for the rest of Module 1.

## 1. Types of machine learning systems

The algorithms in this course change. The **setup** usually does not.

**Supervised.** The training rows come with answers (labels).

- **Classification** puts a row in a bucket (spam / ham).
- **Regression** predicts a number (price of a car).

Methods you already know still apply: \(k\)-NN, linear and logistic regression, SVMs, trees, forests, neural nets. Weeks 5 and 12–15 pick these up again with more math.

**Unsupervised.** No labels.

| Family | Examples in this course |
| ------ | ----------------------- |
| Clustering | \(k\)-means, hierarchical |
| Anomaly / novelty | one-class SVM; later GMMs |
| Latent variables | PCA, kernel PCA, ICA, tensors |
| Association rules | Apriori, Eclat (know the names) |

**Semi-supervised.** A little labeled data, a lot of unlabeled. A photo app clusters faces, then asks you to name each cluster. One label per person names everyone in the album.

![Semi-supervised face clustering](files/data-642/graphics/ml-semi-supervised.png)

**Reinforcement.** An **agent** takes actions, sees a reward (or a penalty), and updates a **policy**. We will not live here. Know the words.

![Reinforcement learning loop](files/data-642/graphics/ml-reinforcement.png)

---

## 2. Batch versus online

Another cut: can the system learn from a **stream**, or must it see the whole matrix at once?

**Batch (offline).** Train on all available data, then freeze the model. You can still adapt: collect new data, retrain from scratch, ship a new version. Simple. Slow if the matrix is huge. Fine when the world changes on a daily or weekly clock. Bad for a phone, a rover, or a stock ticker.

**Online.** Update as points arrive.

![Online learning](files/data-642/graphics/ml-online.png)

The **learning rate** is how fast you forget the past.

- High: you track a changing stream, and you also chase noise.
- Low: you are stable, and you are late.

Online learning does not need the whole dataset in RAM. It can also be order-sensitive and poisoned by outliers. A live system that trains online can be wrecked by one bad sensor or by someone stuffing a search ranking. Monitor the inputs. Be ready to switch learning off and roll back.

---

## 3. Why models fail

| Problem | What it looks like | What you do |
| ------- | ------------------ | ----------- |
| Too little data | High variance, lucky splits | More data, or a simpler model. Medium data is still the usual case here — do not abandon the math. |
| Non-representative data | Sampling noise or sampling **bias**; the test world is not the train world | Fix how you sample |
| Poor quality | Errors, outliers, sensor junk | Clean before you model |
| Irrelevant features | The signal is not in the columns | Select, extract, or collect better ones |
| Underfitting | Train and test both bad | Richer model, better features, less regularization |
| Overfitting | Train great, test poor | Simpler model, more data, less noise |

![Underfitting versus overfitting](files/data-642/graphics/ml-over-under.png)

---

## 4. Practice

1. Name one supervised and one unsupervised method this course will treat later, and what label each one does or does not see.

2. A spam filter is retrained every night on the last 30 days of mail. Is that batch or online? What breaks if the stream is attacked for one afternoon?

3. Why can a very large training set still fail to represent the world you care about?
