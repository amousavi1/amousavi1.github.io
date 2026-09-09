## 1. Four learning setups

This course is advanced machine learning. The algorithms change. The **setup** usually does not.

**Supervised.** The training rows come with answers (labels). Classification puts a row in a bucket (spam / ham). Regression predicts a number (price of a car). Methods you already know still apply: \(k\)-NN, linear and logistic regression, SVMs, trees, forests, neural nets. Weeks 5 and 12–15 pick these up again with more math.

**Unsupervised.** No labels. Clustering (\(k\)-means, hierarchical), anomaly detection (one-class SVM, later GMMs), and latent-variable models (PCA, kernel PCA, ICA, tensors) are the second half of the semester.

**Semi-supervised.** A little labeled data, a lot of unlabeled. A photo app that clusters faces and then asks you to name each cluster is the usual picture.

**Reinforcement.** An agent takes actions, sees a reward, and updates a policy. We will not live here. Know the words.

The Géron book is the informal source for this lecture. *Mathematics for Machine Learning* is the math source for the rest of Module 1.

---

## 2. Batch versus online

**Batch (offline).** Fit on the whole training set, then freeze the model. Simple. Expensive if you retrain from scratch every night on a huge matrix. Fine when the world is slow.

**Online.** Update as points arrive. The **learning rate** is how fast you forget the past. High: you track a changing stream and you also chase noise. Low: you are stable and you are late.

A live system that trains online can be poisoned by one bad sensor. Monitor the inputs. Be ready to switch learning off.

---

## 3. Why models fail

| Problem | What it looks like | What you do |
| ------- | ------------------ | ----------- |
| Too little data | High variance, lucky splits | More data, or a simpler model |
| Non-representative data | Sampling bias; the test world is not the train world | Fix how you sample |
| Poor quality | Errors, outliers, sensor junk | Clean before you model |
| Irrelevant features | The signal is not in the columns | Select, extract, or collect better ones |
| Underfitting | Train and test both bad | Richer model, better features, less regularization |
| Overfitting | Train great, test poor | Simpler model, more data, less noise |

Data can beat a clever algorithm on a large problem. Medium data is still the usual case in this course. Do not abandon the math.
