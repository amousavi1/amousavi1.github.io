These notes walk through the lecture slides. The original deck is unchanged; use **(slides)** on the course hub if you want that PDF.

Figures and notes follow Géron, *Hands-On Machine Learning*; Deisenroth, Faisal, and Ong, *Mathematics for Machine Learning*; and Theodoridis.

## 1. Anomaly detection

Find rows that do not look like the rest. Those are **anomalies** (outliers). The bulk are **inliers**.

- **Fraud.** Odd transactions or activity.
- **Manufacturing.** Defects, failing machines.
- **Preprocessing.** Drop junk before you train, so the model is less pushed around by noise.

---

## 2. GMMs as the density

**Normal behavior.** Fit a mixture of Gaussians to ordinary data. Points that do not fit are anomalies.

**Flexible.** Network traffic, money, sensors — one tool, many shapes of “normal.”

**Density.** Low-density regions are the anomalies. Set the threshold from domain knowledge, or from a known defect rate. Example: 4% defective in a factory → flag the 4% lowest-density points. Stars in the figure are the anomalies.

![Low-density GMM regions marked as anomalies](files/data-642/graphics/11.2-gmms-anomaly/fig.png)

---

## 3. Limits

| Issue | What goes wrong |
| ----- | --------------- |
| **Gaussian assumption** | If “normal” is not a mixture of ellipsoids, the density is a bad map. |
| **Initialization** | Bad starts → local optima, or a poor picture of normal. |
| **Nonlinear structure** | The model is a sum of Gaussians, not a nonlinear manifold. |
| **High dimension** | Many parameters; curse of dimensionality; overfitting or slowness. |
| **Bias from outliers** | The mixture tries to fit **everything**, including the junk. Too many outliers, and some of them start to look “normal.” |

---

## 4. Tips

**Features.** Choose them. PCA if the ambient dimension is large.

**Evaluation.** Precision, recall, F1. Cross-validation or a holdout.

**Hyperparameters.** Number of components, covariance type, regularization.

---

## Practice

1. How would you turn a GMM density into an anomaly score?

2. Why can too many outliers bias a GMM’s picture of “normal”?

3. Name one reason a GMM can fail as an anomaly detector even when you set the density threshold carefully.
