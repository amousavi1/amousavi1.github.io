These notes walk through the lecture slides. The original deck is unchanged; use **(slides)** on the course hub if you want that PDF.

Figures and notes follow Géron, *Hands-On Machine Learning*; Deisenroth, Faisal, and Ong, *Mathematics for Machine Learning*; and Theodoridis.

## 1. Spectral clustering

Cluster by **similarity** of feature representations, not by Euclidean balls in the original space.

1. **Affinity matrix.** Pairwise similarities or distances. Points are vertices; edge weights are similarities.
2. **Graph Laplacian.** Turn the affinity matrix into a Laplacian. That matrix encodes connectivity.
3. **Eigendecomposition.** Eigenvectors of the Laplacian embed the points in a lower-dimensional space.
4. **Cluster the embedding.** Take the eigenvectors for the **smallest** eigenvalues. Run clustering (usually \(k\)-means) there.

Benefits: irregular shapes, non-convex clusters, nonlinear geometry. A flexible route on high-dimensional data.

Applications: image segmentation, social networks, gene expression, dimensionality reduction — anywhere the clumps are not round in the raw features.

---

## 2. The linear algebra

**Pairwise similarity or distance.** Euclidean distance of \(\boldsymbol{x}_i\) and \(\boldsymbol{x}_j\):

\[
d(\boldsymbol{x}_i,\boldsymbol{x}_j)=\sqrt{\sum_{k=1}^{n}(x_{ik}-x_{jk})^2}.
\]

Cosine similarity of \(\boldsymbol{u}\) and \(\boldsymbol{v}\):

\[
\frac{\boldsymbol{u}\cdot\boldsymbol{v}}{\|\boldsymbol{u}\|\,\|\boldsymbol{v}\|}.
\]

**Affinity matrix** \(A\): entry \(a_{ij}\) is the similarity (or distance) of \(\boldsymbol{x}_i\) and \(\boldsymbol{x}_j\).

**Graph Laplacian** \(L=D-A\), where \(D\) is diagonal with the **degree** of each vertex.

Then eigendecompose \(L\). Those eigenvectors are the embedding.

---

## 3. Computing eigenpairs

| Family | Idea |
| ------ | ---- |
| **Direct** | QR, Jacobi, bisection. Straightforward; expensive on large matrices. |
| **Iterative** | Power iteration, Lanczos. Better for large sparse \(L\). |
| **Matrix decompositions** | SVD or Cholesky, used indirectly. |
| **Graph partitioning** | Spectral partitioning or bisection: split the graph using eigenvectors, then work on the pieces. |
| **Sparse libraries** | ARPACK and friends: a few eigenpairs of a large sparse Laplacian. |

---

## Practice

1. Spectral clustering still runs \(k\)-means. In what space?

2. Write the graph Laplacian in terms of the affinity matrix \(A\).

3. Why might you build \(A\) from cosine similarity instead of Euclidean distance?
