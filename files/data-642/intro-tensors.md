These notes walk through the lecture slides. The original deck is unchanged; use **(slides)** on the course hub if you want that PDF.

Figures and notes follow *Introduction to Tensor Decompositions and their Applications in Machine Learning*.

## 1. Brief history

**Tensors** generalize matrices to higher dimensions: multidimensional arrays.

They and their decompositions appear in 1927, then sit unused in computer science until late in the 20th century. Cheaper compute and better multilinear algebra — especially in the last decade — moved them into statistics, data science, and machine learning.

---

## 2. Tensor basics

A tensor is a multi-way collection of numbers, usually from \(\mathbb{R}\). The simplest high-dimensional case is a three-dimensional array: a **data cube**. The same notation extends to more modes.

![A three-way tensor as a data cube](files/data-642/graphics/8.1-intro-tensors/3d_tensor.png)

---

## 3. Tensor order

The **order** of a tensor is the number of dimensions.

| Object | Order | Notation |
| ------ | ----- | -------- |
| Scalar | 0 | \(x\in\mathbb{R}\) |
| Vector | 1 | \(\mathbf{x}\in\mathbb{R}^{I_1}\) |
| Matrix | 2 | \(\mathbf{X}\in\mathbb{R}^{I_1\times I_2}\) |
| Higher-order tensor | \(N\) | \(\mathcal{X}\in\mathbb{R}^{I_1\times I_2\times\cdots\times I_N}\) |

Each \(I\) is the length of that mode.

![Scalars, vectors, matrices, and a 3-way tensor](files/data-642/graphics/8.1-intro-tensors/tensors_examples.png)

---

## 4. Tensor indexing

Fix some indices to get a subarray.

- **Fibers:** fix every index but one.
- **Slices** (slabs): fix every index but two.

For a third-order tensor, fibers are \(x_{:jk}=x_{jk}\) (column), \(x_{i:k}\) (row), \(x_{ij:}\) (tube). Slices are \(\mathcal{X}_{::k}=\mathcal{X}_k\) (frontal), \(\mathcal{X}_{:j:}\) (lateral), \(\mathcal{X}_{i::}\) (horizontal).

![Fibers and slices of a 3-way tensor](files/data-642/graphics/8.1-intro-tensors/fibers.png)

---

## 5. Outer and inner product

The vector **outer product** is the product of the entries, written \(\circledcirc\). For two length-\(n\) vectors \(\mathbf{a}\) and \(\mathbf{b}\),

\[
\mathbf{X} = \mathbf{a}\circledcirc\mathbf{b} = \mathbf{a}\mathbf{b}^{\top}.
\]

For \(N\) vectors the same product is a tensor:

\[
\mathcal{X} = \mathbf{a}^{(1)}\circledcirc\mathbf{a}^{(2)}\circledcirc\cdots\circledcirc\mathbf{a}^{(N)},
\]

with \(x_{i_1 i_2\cdots i_N}=a^{(1)}_{i_1}a^{(2)}_{i_2}\cdots a^{(N)}_{i_N}\).

The **inner product** of two length-\(n\) vectors is a scalar:

\[
x = \langle\mathbf{a},\mathbf{b}\rangle = \mathbf{a}^{\top}\mathbf{b} = \sum_{i=1}^{n} a_i b_i.
\]

---

## 6. Rank-1 tensors

An \(N\)-way tensor is **rank-1** if it is exactly the outer product of \(N\) vectors. Adding a mode is a new scaling of a sub-tensor.

A rank-1 matrix: \(\mathbf{X}=\mathbf{a}\circledcirc\mathbf{b}\). A rank-1 3-way tensor: \(\mathcal{X}=\mathbf{a}\circledcirc\mathbf{b}\circledcirc\mathbf{c}\). The \(N\)-way form is the product above.

![Rank-1 tensor as an outer product of vectors](files/data-642/graphics/8.1-intro-tensors/mode.png)

---

## 7. Tensor rank

The **rank** \(\operatorname{rank}(\mathcal{X})=R\) is the smallest number of rank-1 tensors that sum to \(\mathcal{X}\):

\[
\mathcal{X}
=
\sum_{r=1}^{R}
\lambda_r\,
\mathbf{a}^{(1)}_r\circledcirc\mathbf{a}^{(2)}_r\circledcirc\cdots\circledcirc\mathbf{a}^{(N)}_r.
\]

The **factor matrices** \(\mathbf{A}\) store those vectors as columns:

\[
\mathbf{A} = \begin{bmatrix} \mathbf{a}_1 & \mathbf{a}_2 & \cdots & \mathbf{a}_R \end{bmatrix}.
\]

The weights \(\lambda_r\) (with \(\boldsymbol{\lambda}\in\mathbb{R}^R\)) often absorb column norms, typically so each column has squared length one.

---

## Practice

1. A matrix is a 2-way array. What is a tensor adding?

2. What is a **fiber**, and what is a **slice**?

3. What does \(\operatorname{rank}(\mathcal{X})=R\) mean in terms of rank-1 tensors?
