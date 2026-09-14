These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

A transformer is a large neural net. Before attention, you need one unit, a nonlinearity, and a stack of layers. That is this note.

---

## 1. One neuron

A neuron takes a vector \(\boldsymbol{x}\), forms a weighted sum plus a bias, then applies a scalar nonlinearity \(\sigma\):

\[
z = \boldsymbol{w}^{\top}\boldsymbol{x} + b, \qquad a = \sigma(z).
\]

\(z\) is the **pre-activation**. \(a\) is the **activation**. \(\boldsymbol{w}\) and \(b\) are the parameters you will train.

![One neuron: weighted sum, then a nonlinearity](files/data-643/graphics/1.2-neurons-activations/neuron.png)

If \(\sigma\) is a step function, this is a 1950s perceptron. If \(\sigma\) is a sigmoid, it is logistic regression in one unit. Modern nets mostly use **ReLU** in hidden layers, **tanh** or GELU in some transformer blocks, and **softmax** on mutually exclusive class scores.

---

## 2. Why the nonlinearity is not optional

A layer without \(\sigma\) is an affine map. Two affine maps compose to one affine map:

\[
W_2(W_1\boldsymbol{x}+\boldsymbol{b}_1)+\boldsymbol{b}_2 = (W_2 W_1)\boldsymbol{x} + (W_2\boldsymbol{b}_1+\boldsymbol{b}_2).
\]

Stack as many linear layers as you want: you still have a linear classifier. The bend is the point of the hidden layer.

![Common activations and their derivatives](files/data-643/graphics/1.2-neurons-activations/activations.png)

ReLU is cheap and sparse (negative pre-activations become 0). Sigmoid saturates: its derivative is near 0 for large \(|z|\), which will matter when we talk about vanishing gradients in Week 2.

---

## 3. A feedforward net

A **multi-layer perceptron (MLP)** is a stack of dense layers. Layer \(\ell\) sees the previous activations, not the raw input (except \(\ell=1\)):

\[
\boldsymbol{z}^{(\ell)} = W^{(\ell)}\boldsymbol{a}^{(\ell-1)} + \boldsymbol{b}^{(\ell)}, \qquad
\boldsymbol{a}^{(\ell)} = \sigma\bigl(\boldsymbol{z}^{(\ell)}\bigr), \qquad
\boldsymbol{a}^{(0)}=\boldsymbol{x}.
\]

![A small feedforward net](files/data-643/graphics/1.2-neurons-activations/feedforward.png)

Every arrow in that picture is one entry of some \(W^{(\ell)}\). A “fully connected” layer means every unit in layer \(\ell-1\) talks to every unit in layer \(\ell\).

---

## 4. What a hidden layer buys you

A single linear unit cannot separate XOR: the positive class is not on one side of a line. Two hidden units, then a linear output, can fold the space so the classes become linearly separable.

![XOR needs a nonlinear hidden layer](files/data-643/graphics/1.2-neurons-activations/xor.png)

That is the whole argument for depth, in miniature. Language models stack many such nonlinear maps (and, from Week 3, attention) so that “cat sat on the mat” and “the mat sat on the cat” do not look like the same vector.

---

## 5. Practice

1. Write \(a^{(2)}\) for a two-hidden-layer net as a nested formula in \(W^{(1)},W^{(2)},W^{(3)}\) and \(\sigma\).

2. Drop every \(\sigma\). What class of functions remains?

3. Why is ReLU’s derivative 0 on the negative half-line a feature *and* a failure mode?
