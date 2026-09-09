These notes walk through the lecture slides. The original deck is unchanged; use **(slides)** on the course hub if you want that PDF.

Figures and notes follow Géron, *Hands-On Machine Learning*; Deisenroth, Faisal, and Ong, *Mathematics for Machine Learning*; and Theodoridis.

## 1. Central idea

**Clustering** groups similar instances. No labels.

- **Customer segmentation.** Split customers by behavior, purchases, or how they interact. Different groups, different products and messages.
- **Data analysis.** Find the clumps first. Then look at each clump, not at every row at once.
- **Dimensionality reduction.** Represent a cloud by its clusters instead of by every point. Useful when you want a picture of high-dimensional data.
- **Anomaly detection.** A point that fits no cluster is a candidate outlier: a defect, a fraud, odd behavior.
- **Semi-supervised learning.** A few labels, then copy each label onto the rest of its cluster.
- **Image segmentation.** Cluster pixels by color. Replace each pixel by the mean color of its cluster; fewer colors, easier objects to track.

---

## 2. \(k\)-means

Lloyd proposed it at Bell Labs in 1957 for pulse-code modulation; it left the company in 1982 as “Least square quantization in PCM.” Fast. Often a few iterations.

Write \(C_1,\dots,C_K\) for the index sets of the clusters. They **partition** the \(N\) observations:

1. \(C_1\cup C_2\cup\cdots\cup C_K=\{1,\dots,N\}\) — every row sits in some cluster.
2. \(C_i\cap C_j=\emptyset\) for \(i\neq j\) — clusters do not overlap.

A good clustering makes **within-cluster variation** small. Solve

\[
\min_{C_1,C_2,\dots,C_K}\sum_{k=1}^K W(C_k).
\]

Partition so the total within-cluster variation, summed over all \(K\) clusters, is as small as possible.

A typical \(W(C_k)\) is squared Euclidean distance:

\[
W(C_k)=\frac{1}{|C_k|}\sum_{i,i'\in C_k}\sum_{j=1}^P(x_{ij}-x_{i'j})^2,
\]

where \(|C_k|\) is the number of observations in cluster \(k\). All pairwise squared distances inside the cluster, divided by the cluster size.

---

## 3. Algorithm

1. **Initialization.** Pick \(K\) centroids. Random data points, or \(k\)-means++ (below).
2. **Assignment.** Each point goes to the nearest centroid. Euclidean distance is the usual metric; others are allowed. That step is the partition.
3. **Update.** Each centroid becomes the **mean** of the points assigned to it.
4. **Convergence.** Stop when centroids (or assignments) barely move.
5. Repeat steps 2–4. Each pass tries to cut total within-cluster variation.

---

## 4. Why two runs disagree

Random starts. Different initial centroids, different assignments and final centers.

![Different k-means solutions from different starts](files/data-642/graphics/10.1-clustering-kmeans/different_solutions.png)

The objective has **local optima**. A new start can land in a different hole. The stopping rule can also fire on a slightly different iterate.

**\(k\)-means++** (Arthur and Vassilvitskii, 2006) is a better start than uniform draws:

- Draw \(c_1\) uniformly from the data.
- Draw the next \(c_i\) as instance \(\boldsymbol{x}_i\) with probability

\[
\frac{D(\boldsymbol{x}_i)^2}{\sum_{j=1}^{m}D(\boldsymbol{x}_j)^2},
\]

where \(D(\boldsymbol{x}_i)\) is the distance from \(\boldsymbol{x}_i\) to the nearest centroid already chosen. Far points are more likely.
- Repeat until you have \(K\) centroids.

Then ordinary \(k\)-means. Suboptimal solutions become rarer, so you can cut `n_init`. In scikit-learn, `init="k-means++"` is the default.

**Elkan.** Skip many distance computations with the triangle inequality (\(AC\le AB+BC\)) and with lower and upper bounds on distances to centroids (Elkan, 2003). Set `algorithm="elkan"`. Dense data only. Sparse data uses the full algorithm.

---

## 5. Evaluation

| Tool | What it tells you |
| ---- | ----------------- |
| **Inertia** | Within-cluster sum of squares. Lower is tighter. |
| **Silhouette score** | Cohesion inside a cluster versus separation from others. Range \(-1\) to \(1\); higher is better. |
| **Elbow method** | Plot inertia against \(K\). The “elbow” is where the drop flattens — a candidate for \(K\). |
| **Adjusted Rand index (ARI)** | Agreement with another clustering. Range \(-1\) to \(1\). |
| **Visual inspection** | Scatter plots (or similar). Do the clumps look real? |
| **Cross-validation** | Holdout or \(k\)-fold, if you have a way to score unseen rows. |

---

## 6. Limits

\(k\)-means is a poor fit when clusters have **varying sizes**, **different densities**, or **non-spherical** shapes.

![k-means failing on size, density, and shape](files/data-642/graphics/10.1-clustering-kmeans/limitations.png)

---

## Practice

1. \(k\)-means assumes spherical clusters. Give a data set where that is wrong.

2. What do you do when \(k\) is not given?

3. Why can two runs on the same matrix return different partitions?
