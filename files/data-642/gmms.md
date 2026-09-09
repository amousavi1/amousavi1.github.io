These notes walk through the lecture slides. The original deck is unchanged; use **(slides)** on the course hub if you want that PDF.

Figures and notes follow Géron, *Hands-On Machine Learning*; Deisenroth, Faisal, and Ong, *Mathematics for Machine Learning*; and Theodoridis.

## 1. Gaussian mixture models

A **GMM** says each row was drawn from a mixture of Gaussians whose parameters you do not know.

One Gaussian → one cluster. Clusters look like **ellipsoids**. They may differ in shape, size, density, and orientation.

![Data from a mixture of Gaussians](files/data-642/graphics/11.1-gmms/EM_data.png)

You see an instance. You do not see which Gaussian wrote it, and you do not know the parameters.

---

## 2. The generative story

For each \(\boldsymbol{x}_i\), pick a cluster \(z_i\) among \(k\) clusters. The probability of cluster \(j\) is its **weight** \(\phi_j\):

\[
P(z_i=j)=\phi_j.
\]

If \(z_i=j\), draw the location from that Gaussian:

\[
\boldsymbol{x}_i\sim\mathcal{N}(\boldsymbol{\mu}_j,\mathbf{\Sigma}_j).
\]

So \(\mathbf{X}\) comes from \(k\) Gaussians, each with a weight \(\phi_j\), a mean \(\boldsymbol{\mu}_j\), and a covariance \(\mathbf{\Sigma}_j\). Collect those as \(\boldsymbol{\theta}\). **The job is to estimate \(\boldsymbol{\theta}\) from the observed \(\mathbf{X}\).**

---

## 3. Log-likelihood

The log-likelihood is the log probability of the data and the latent cluster ids under \(\boldsymbol{\theta}\):

\[
\log p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\theta})
=
\sum_{i=1}^n\log p(\boldsymbol{x}_i,z_i\mid\boldsymbol{\theta})
=
\sum_{i=1}^n\log\Bigl(\sum_{j=1}^k\phi_j\,\mathcal{N}(\boldsymbol{x}_i\mid\boldsymbol{\mu}_j,\mathbf{\Sigma}_j)\Bigr).
\]

Maximize this in \(\boldsymbol{\theta}\). **Expectation-maximization (EM)** does it by alternating an E-step and an M-step until the likelihood stops moving.

---

## 4. Expectation-maximization

**E-step.** Soft assignment: probability that point \(i\) came from cluster \(j\), given the current \(\boldsymbol{\theta}^{(t)}\):

\[
\gamma^{(t)}(z_{ij})
=
\frac{\phi_j^{(t)}\,\mathcal{N}(\boldsymbol{x}_i\mid\boldsymbol{\mu}_j^{(t)},\mathbf{\Sigma}_j^{(t)})}
{\sum_{j=1}^k\phi_j^{(t)}\,\mathcal{N}(\boldsymbol{x}_i\mid\boldsymbol{\mu}_j^{(t)},\mathbf{\Sigma}_j^{(t)})}.
\]

**M-step.** Update means, covariances, and weights to fit those responsibilities.

Means:

\[
\boldsymbol{\mu}_j^{(t+1)}
=
\frac{\sum_{i=1}^n\gamma^{(t)}(z_{ij})\,\boldsymbol{x}_i}
{\sum_{i=1}^n\gamma^{(t)}(z_{ij})}.
\]

Covariances:

\[
\mathbf{\Sigma}_j^{(t+1)}
=
\frac{\sum_{i=1}^n\gamma^{(t)}(z_{ij})(\boldsymbol{x}_i-\boldsymbol{\mu}_j^{(t+1)})(\boldsymbol{x}_i-\boldsymbol{\mu}_j^{(t+1)})^\top}
{\sum_{i=1}^n\gamma^{(t)}(z_{ij})}.
\]

Weights:

\[
\phi_j^{(t+1)}
=
\frac{\sum_{i=1}^n\gamma^{(t)}(z_{ij})}{n}.
\]

Repeat. Each pair of steps raises the likelihood a little. Stop when \(\boldsymbol{\theta}\) barely changes.

![EM iterating on a Gaussian mixture](files/data-642/graphics/11.1-gmms/EM_in_action.png)

---

## 5. Applications

**Image segmentation.** Color or texture. Soft membership helps on ambiguous pixels. Lighting and texture can vary; a mixture of Gaussians can still fit the intensities.

**Anomaly detection.** Model ordinary behavior as a mixture of Gaussians. Deviations are anomalies. Network traffic, transactions, sensors.

**Speech.** Model features such as Mel-frequency cepstral coefficients (MFCCs). The mixture captures how speech sounds vary; that is a classic acoustic model.

---

## 6. Practical notes

**Initialization.** Random, \(k\)-means then covariances, or hierarchical. Try more than one; the start matters.

**Singular covariances.** High dimension, or too few points per cluster. Add a small constant to the diagonal, or PCA the features first.

**How many components.** BIC or cross-validation. Score with log-likelihood, silhouette, or clustering purity, as appropriate.

**Speed.** Training is heavy on large or high-dimensional matrices. Use a solid implementation (scikit-learn, TensorFlow). Mini-batches or parallel work if the matrix is huge.

---

## Practice

1. A GMM is a soft clustering. What is being mixed?

2. In the E-step, what is \(\gamma^{(t)}(z_{ij})\)?

3. Why can two GMM fits on the same data disagree?
