These notes walk through the lecture slides. The original deck is unchanged; use **(slides)** on the course hub if you want that PDF.

Figures and notes follow Géron, *Hands-On Machine Learning*; Deisenroth, Faisal, and Ong, *Mathematics for Machine Learning*; and Theodoridis.

## 1. Selecting the number of clusters

Inertia and silhouette assume **spherical** clusters. A GMM’s ellipsoids are not that. Use an information criterion instead: **BIC** or **AIC**.

\[
\mathrm{BIC}=\log(N)\,p-2\log(\hat{L}),
\]

\[
\mathrm{AIC}=2p-2\log(\hat{L}).
\]

- \(N\) is the number of instances.
- \(p\) is the number of parameters the model learned.
- \(\hat{L}\) is the maximized likelihood — the probability of the observed \(\mathbf{X}\) given the fitted model.

Both **penalize** extra parameters (more clusters) and **reward** a high likelihood. That is the trade.

---

## 2. Other algorithms for anomaly detection

**Fast-MCD (minimum covariance determinant).** Cleanup and outlier detection. Ordinary points come from **one** Gaussian; the set is contaminated. Estimate that Gaussian while ignoring likely outliers. A better elliptic envelope, cleaner flags.

**Isolation Forest.** Fast, especially in high dimension. A random forest where each tree picks random features and thresholds to isolate points. Anomalies sit far away, so they isolate in **fewer** splits than ordinary points.

**Local outlier factor (LOF).** Compare a point’s density to the density around its neighbors. Anomalies are more isolated than those neighbors.

**One-class SVM.** Novelty detection. Separate the cloud from the origin in a high-dimensional space; find a small region that holds the training points. A new point outside is novel. SVM hyperparameters, plus a margin for the chance of calling a new point novel by mistake. Fine in high dimension; does **not** scale to huge matrices the way some other SVMs do.

---

## Practice

1. Why are inertia and silhouette the wrong tools for choosing the number of GMM components?

2. What do BIC and AIC penalize, and what do they reward?

3. Isolation Forest versus one-class SVM: which one is aimed at novelty on high-dimensional data that is **not** huge?
