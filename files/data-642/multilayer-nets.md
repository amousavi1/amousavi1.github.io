These notes walk through the lecture slides. The original deck is unchanged; use **(slides)** on the course hub if you want that PDF.

Figures and notes follow Géron, *Hands-On Machine Learning*; Deisenroth, Faisal, and Ong, *Mathematics for Machine Learning*; Theodoridis; and 3blue1brown.

## 1. A multi-layer net

A **multi-layer perceptron** stacks dense layers. Below: pixels of a digit flatten to an input vector, then hidden layers, then class scores.

![Feed-forward net for a handwritten digit](files/data-642/graphics/12.2-multilayer-nets/neural_net_Perceptron.png)

---

## 2. What the layers are doing

Think of a deep net as **multistage distillation**: each layer filters the previous representation; what remains is more useful for the task.

![Successive layers as a distillation pipeline](files/data-642/graphics/12.2-multilayer-nets/deep2.png)

---

## 3. Linear-algebra notation

Weights, activations, and the next layer line up as matrix–vector products. The picture is the notation you will write.

![Matrix notation for a layer](files/data-642/graphics/12.2-multilayer-nets/notation1.png)

---

## 4. Mathematics of a layer

**Linear map.** Neuron \(l\) does not see raw \(\boldsymbol{x}\) after the first layer. It sees the previous activations \(\boldsymbol{a}^{(l-1)}\):

\[
\boldsymbol{z}^{(l)} = \boldsymbol{W}^{(l)}\boldsymbol{a}^{(l-1)} + \boldsymbol{b}^{(l)},
\]

where \(\boldsymbol{z}^{(l)}\) is the pre-activation, \(\boldsymbol{W}^{(l)}\) the weight matrix, \(\boldsymbol{b}^{(l)}\) the bias.

**Activation.** Elementwise nonlinearity:

\[
\boldsymbol{a}^{(l)} = \sigma\bigl(\boldsymbol{z}^{(l)}\bigr).
\]

Without \(\sigma\), stacked layers collapse to one linear map. The nonlinearity is what a hidden layer is for.

---

## 5. Activation functions

Common choices: **sigmoid**, **tanh**, **ReLU**, **softmax**. Applied elementwise after the linear map (softmax on the output for mutually exclusive classes).

![Common activation functions](files/data-642/graphics/12.2-multilayer-nets/activation_functions.png)

---

## Practice

1. Write the forward pass of a two-layer net in one line of matrix products.

2. If you drop \(\sigma\) from every hidden layer, what class of functions can the net represent?

3. In \(\boldsymbol{z}^{(l)}=\boldsymbol{W}^{(l)}\boldsymbol{a}^{(l-1)}+\boldsymbol{b}^{(l)}\), what is \(\boldsymbol{a}^{(0)}\)?
