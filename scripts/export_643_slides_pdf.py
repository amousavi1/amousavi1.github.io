"""Build one-slide-per-page PDFs for DATA 443/643 Week 1."""

from __future__ import annotations

import html as html_lib
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
FILES = ROOT / "files" / "data-643"
OUT = FILES / "slides"
WORK = FILES / "_slide-work"
EDGE = pathlib.Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")

COURSE = "DATA 443/643"

SLIDE_CSS = """
@page { size: 13.333in 7.5in; margin: 0; }
html, body { margin: 0; padding: 0; background: #fff; }
body {
  font-family: "Segoe UI", "Helvetica Neue", Helvetica, Arial, sans-serif;
  color: #1c1c1c;
}
.slide {
  page-break-after: always;
  width: 13.333in;
  height: 7.5in;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  background: #fff;
}
.slide:last-child { page-break-after: auto; }
.slide-body {
  flex: 1;
  min-height: 0;
  padding: 0.38in 0.58in 0.22in;
  display: flex;
  flex-direction: column;
}
.slide.title-slide .slide-body {
  justify-content: flex-start;
  padding-left: 0.9in;
  padding-right: 0.9in;
  padding-bottom: 0.12in;
}
.title-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.kicker {
  margin: 0 0 0.12in;
  color: #5f6b73;
  font-size: 12.5pt;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}
h1 {
  font-family: "Segoe UI", "Helvetica Neue", Helvetica, Arial, sans-serif;
  font-size: 32pt;
  font-weight: 650;
  line-height: 1.15;
  margin: 0 0 0.22in;
  color: #0b6e99;
}
.title-slide h1 {
  font-size: 44pt;
  color: #0b6e99;
  margin-bottom: 0.18in;
}
.title-slide .subtitle {
  font-size: 20pt;
  color: #333;
  margin: 0 0 0.45in;
}
.title-slide .meta {
  font-size: 16pt;
  color: #5f6b73;
  line-height: 1.45;
}
.credit {
  margin: 0;
  font-size: 11.5pt;
  color: #5f6b73;
  line-height: 1.35;
  max-width: 92%;
}
ul {
  margin: 0.05em 0 0.15em;
  padding-left: 1.15em;
  font-size: 20pt;
  line-height: 1.38;
}
li { margin: 0.16em 0; }
.slide.first-look ul {
  font-size: 16.5pt;
  line-height: 1.32;
}
.slide.first-look li { margin: 0.1em 0; }
.split {
  flex: 1;
  display: grid;
  grid-template-columns: 0.42fr 0.58fr;
  gap: 0.38in;
  min-height: 0;
  align-items: center;
}
.split.wide-text { grid-template-columns: 0.5fr 0.5fr; }
.split .copy { min-width: 0; }
.fig {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 0;
}
.fig img {
  max-width: 100%;
  max-height: 5.55in;
  object-fit: contain;
}
.split .fig img { max-height: 5.35in; }
.eq {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  min-height: 0;
}
.eq math {
  font-size: 1.85em;
}
.eq-notes {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.22in;
  margin-top: 0.32in;
  width: 100%;
}
.eq-notes div, .callout {
  background: #f4f8fb;
  border-left: 5px solid #0b6e99;
  padding: 0.16in 0.18in;
  font-size: 14.5pt;
  line-height: 1.3;
  color: #24343c;
  text-align: left;
}
.agenda { list-style: none; padding: 0; margin: 0.1in 0 0; }
.agenda li {
  display: grid;
  grid-template-columns: 0.5in 1fr;
  gap: 0.18in;
  align-items: center;
  padding: 0.16in 0;
  border-bottom: 1px solid #e4eaee;
  font-size: 22pt;
}
.agenda .n {
  color: #0b6e99;
  font-weight: 700;
}
.cards {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.28in;
  align-content: center;
}
.cards.three { grid-template-columns: repeat(3, 1fr); }
.card {
  background: #f7fafc;
  border: 1px solid #d7e2ea;
  border-radius: 10px;
  padding: 0.22in 0.24in;
  min-height: 2.2in;
}
.card h2 {
  margin: 0 0 0.12in;
  font-size: 18pt;
  color: #0b6e99;
}
.card p { font-size: 15.5pt; line-height: 1.35; margin: 0.08em 0; }
.compare {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.3in;
  align-items: stretch;
}
.compare .col {
  border-radius: 10px;
  padding: 0.24in;
}
.compare .bad { background: #f8eee8; border: 1px solid #e7c7b4; }
.compare .good { background: #e6f4f1; border: 1px solid #b7ddd6; }
.compare h2 { margin: 0 0 0.14in; font-size: 18pt; }
.compare p { font-size: 16pt; line-height: 1.4; margin: 0; }
.takeaway {
  margin-top: auto;
  background: #fff7e8;
  border-left: 6px solid #c9a227;
  padding: 0.16in 0.22in;
  font-size: 16.5pt;
  line-height: 1.35;
}
.caption { margin: 0.08in 0 0; color: #5f6b73; font-size: 13.5pt; }
.bar {
  height: 0.42in;
  background: #8c1515;
  color: #fff;
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  padding: 0 0.45in;
  font-size: 11.5pt;
  letter-spacing: 0.01em;
}
.bar .left { justify-self: start; }
.bar .mid { justify-self: center; }
.bar .right { justify-self: end; }
.title-slide .bar { background: #1f4e79; }
.rule { height: 4px; background: #c9a227; }
"""

DECKS = [
    {
        "stem": "1.1-course-map",
        "title": "1.1 Course Map and the Semester Project",
        "slides": [
            {
                "layout": "title",
                "title": "Course Map and the Semester Project",
                "subtitle": "DATA 443/643  ·  Advanced Concepts in Large Language Models",
                "meta": "Week 1  ·  American University  ·  Ahmad Mousavi",
                "credit": "Ideas and 16:9 layout from Stanford CS224N, CS231N, and MIT 6.S191. Original slides; those courses are not copied.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan",
                "agenda": [
                    ("1", "Where this course sits, and why it is self-contained"),
                    ("2", "An LLM is a stack; Week 1 is the base"),
                    ("3", "What pretraining actually minimizes"),
                    ("4", "The 140 GB weights file"),
                    ("5", "Turn a method into a project question"),
                ],
                "takeaway": "Key goal: leave with a stack picture, a next-token loss, and one measurable project sentence.",
            },
            {
                "layout": "split",
                "title": "A self-contained LLM course",
                "bullets": [
                    "Listed prereq: DATA 427/627.",
                    "DATA 641 and 642 are not required.",
                    "Overlap is intentional so more people can finish a project.",
                ],
                "image": "graphics/1.1-course-map/roadmap.png",
            },
            {
                "layout": "split",
                "title": "A language model is a stack",
                "bullets": [
                    "Chat products sit at the top.",
                    "The weights still came from next-token training.",
                    "Name the layer you will change: data, prompt, adapter, retriever, or eval.",
                ],
                "image": "graphics/1.1-course-map/stack.png",
            },
            {
                "layout": "equation",
                "title": "Pretraining minimizes next-token NLL",
                "equation": r"P(w_1,\ldots,w_T)=\prod_{t=1}^{T} P(w_t\mid w_{1:t-1})",
                "notes": [
                    "Each factor is a softmax over the vocabulary.",
                    "The training loss is the negative log of those probabilities.",
                    "If the model assigns 0.70, NLL is about 0.36. If 0.10, NLL is about 2.30.",
                ],
            },
            {
                "layout": "equation",
                "title": "Llama 2 70B is a 140 GB file",
                "equation": r"70\times 10^{9}\times 2~\mathrm{bytes}=140~\mathrm{GB}",
                "notes": [
                    "Each parameter stored as float16 (2 bytes).",
                    "Parameters file vs run file: running needs extra memory.",
                    "Karpathy: an LLM is weights plus a little code.",
                ],
            },
            {
                "layout": "compare",
                "title": "The project starts with a question",
                "left_title": "Not a project",
                "left": "Use LoRA on news.",
                "right_title": "A project",
                "right": "Does a LoRA adapter on local news reduce entity hallucination vs. the base model, measured by exact-match on a 100-item holdout?",
            },
            {
                "layout": "cards",
                "title": "Today’s two-hour meeting",
                "cards": [
                    ("1.1 Course map", "Stack, next-token NLL, 140 GB, project sentence. Short Karpathy clip."),
                    ("1.2–1.4 Board notes", "Neuron and XOR, then gradient descent, then skip-gram and bias."),
                    ("Lab 1", "Linear vs MLP on XOR, then the constructed 2-D embedding probe."),
                ],
                "takeaway": "Key goal: one timed meeting, one stack picture, one project sentence.",
            },
        ],
    },
    {
        "stem": "1.2-neurons-activations",
        "title": "1.2 Neurons, Activations, and Feedforward Nets",
        "slides": [
            {
                "layout": "title",
                "title": "Neurons, Activations, and Feedforward Nets",
                "subtitle": "DATA 443/643  ·  Week 1, note 1.2",
                "meta": "Week 1  ·  American University  ·  Ahmad Mousavi",
                "credit": "Ideas from MIT 6.S191 L1 and CS231N L4. Original slides; those courses are not copied.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan",
                "agenda": [
                    ("1", "One neuron: z, then a"),
                    ("2", "Four formulas you will write"),
                    ("3", "Why two linear layers collapse"),
                    ("4", "XOR, Goodfellow’s table, 3 vs 33"),
                ],
            },
            {
                "layout": "split",
                "title": "One neuron",
                "bullets": [
                    r"Pre-activation \(z=w^\top x+b\).",
                    r"Activation \(a=\sigma(z)\).",
                    r"If you skip \(z\), you cannot take derivatives next note.",
                ],
                "image": "graphics/1.2-neurons-activations/neuron.png",
            },
            {
                "layout": "figure",
                "title": "The perceptron: plug in the numbers",
                "image": "graphics/1.2-neurons-activations/perceptron-numeric.png",
                "caption": "Same example as a diagram and as a line. Ours uses ReLU, not sigmoid.",
            },
            {
                "layout": "equation",
                "title": "Four formulas. No Jacobian today.",
                "equation": r"\sigma(z)=\frac{1}{1+e^{-z}}\qquad \mathrm{ReLU}(z)=\max(0,z)",
                "notes": [
                    r"\(\mathrm{ReLU}'(z)=\mathbf{1}_{z>0}\). At 0, PyTorch uses 0.",
                    r"\(\mathrm{softmax}(z)_i=e^{z_i}/\sum_j e^{z_j}\).",
                    "ReLU in hidden layers. Softmax when classes compete.",
                ],
            },
            {
                "layout": "split",
                "title": "The nonlinearity is the point",
                "bullets": [
                    "Two affine maps compose to one affine map.",
                    "Without a bend, depth adds no power.",
                    "Without a nonlinearity you get a linear classifier again.",
                ],
                "image": "graphics/1.2-neurons-activations/activations.png",
                "takeaway": r"\(W_2(W_1 x+b_1)+b_2=(W_2 W_1)x+(W_2 b_1+b_2)\).",
            },
            {
                "layout": "split",
                "title": "A feedforward net",
                "bullets": [
                    r"Layer \(\ell\): \(a^{(\ell)}=\sigma(W^{(\ell)}a^{(\ell-1)}+b^{(\ell)})\).",
                    r"\(a^{(0)}=x\). Every arrow is one weight.",
                    "A transformer block still contains this MLP.",
                ],
                "image": "graphics/1.2-neurons-activations/feedforward.png",
            },
            {
                "layout": "split",
                "title": "XOR: why a hidden layer exists",
                "bullets": [
                    "One linear unit cannot separate XOR.",
                    "A hidden layer folds the square.",
                    "Language models stack many such maps.",
                ],
                "image": "graphics/1.2-neurons-activations/xor.png",
            },
            {
                "layout": "figure",
                "title": "Goodfellow §6.1: an explicit XOR net",
                "image": "graphics/1.2-neurons-activations/xor-table.png",
                "takeaway": r"Lab 1 MLP is 33 parameters, not this hand-chosen net. Linear(2,1) is 3 parameters and cannot do this table.",
            },
        ],
    },
    {
        "stem": "1.3-gradient-descent",
        "title": "1.3 Gradient Descent",
        "slides": [
            {
                "layout": "title",
                "title": "Gradient Descent",
                "subtitle": "DATA 443/643  ·  Week 1, note 1.3",
                "meta": "Week 1  ·  American University  ·  Ahmad Mousavi",
                "credit": "Ideas from CS231N L3–L4 and Nielsen Ch. 1. Original slides; those sources are not copied.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan",
                "agenda": [
                    ("1", "Loss as a surface"),
                    ("2", "The update, two steps, overshoot"),
                    ("3", "Forward, loss, backward, update"),
                    ("4", "One ReLU unit as gates"),
                ],
            },
            {
                "layout": "split",
                "title": "Training is walking downhill",
                "bullets": [
                    r"Pack weights into \(\theta\). \(L(\theta)\) is a scalar.",
                    "Loss = cost = empirical risk.",
                    "The gradient points uphill. Step the other way.",
                ],
                "image": "graphics/1.3-gradient-descent/loss-surface.png",
            },
            {
                "layout": "equation",
                "title": "The update",
                "equation": r"\theta \leftarrow \theta - \eta \nabla L(\theta)",
                "notes": [
                    r"\(\eta\) too small: crawl. Too large: overshoot.",
                    "SGD estimates the gradient on a minibatch.",
                    "Adam waits. Nielsen Ch. 1 is enough for today.",
                ],
            },
            {
                "layout": "split",
                "title": "Two steps, then overshoot",
                "bullets": [
                    r"\(L(\theta)=(\theta-3)^2\), \(\theta_0=0\), \(\eta=0.25\).",
                    r"\(\theta_1=1.5\), \(\theta_2=2.25\). Minimum at 3.",
                    r"\(\eta=2\) sends \(\theta_1=12\): overshoot.",
                ],
                "image": "graphics/1.3-gradient-descent/gd-1d.png",
            },
            {
                "layout": "split",
                "title": "Forward, loss, backward, update",
                "bullets": [
                    "Keep activations. Backward needs them.",
                    "Autograd is backprop: the chain rule.",
                    r"Forget `zero_grad()`: gradients accumulate.",
                ],
                "image": "graphics/1.3-gradient-descent/train-loop.png",
            },
            {
                "layout": "figure",
                "title": "One ReLU unit as a computational graph",
                "image": "graphics/1.3-gradient-descent/one-unit-backprop.png",
                "caption": "Each op is a gate. Local derivative times upstream.",
            },
            {
                "layout": "equation",
                "title": "The chain rule you must write",
                "equation": r"\frac{\partial L}{\partial w}=(a-y)\,\mathrm{ReLU}'(z)\,x",
                "notes": [
                    r"Squared error on one ReLU neuron.",
                    r"Softmax/CE cousin: \(\partial L/\partial w=(p-y)x\).",
                    r"\(x=2,w=0.5,y=0\): gradient \(2\), then \(w\leftarrow 0.3\) at \(\eta=0.1\).",
                ],
            },
            {
                "layout": "compare",
                "title": "Lab 1 loss takes logits",
                "left_title": "Wrong",
                "left": "sigmoid(z), then BCEWithLogitsLoss. You squash twice.",
                "right_title": "Right",
                "right": "Pass z into BCEWithLogitsLoss. The sigmoid is inside the loss.",
                "takeaway": "Next-token NLL is this same loop at vocabulary scale.",
            },
        ],
    },
    {
        "stem": "1.4-embeddings",
        "title": "1.4 Word Embeddings and Semantic Geometry",
        "slides": [
            {
                "layout": "title",
                "title": "Word Embeddings and Semantic Geometry",
                "subtitle": "DATA 443/643  ·  Week 1, note 1.4",
                "meta": "Week 1  ·  American University  ·  Ahmad Mousavi",
                "credit": "Ideas from Stanford CS224N Lecture 2 (distributional meaning, skip-gram). Original slides; that course is not copied.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan",
                "agenda": [
                    ("1", "One-hot is a bad geometry"),
                    ("2", "How a corpus becomes a distributional vector"),
                    ("3", "Skip-gram softmax, then what you keep"),
                    ("4", "Analogies, evaluation, and bias as geometry"),
                ],
                "takeaway": "Key goal: a word can be a dense vector learned from its neighbors; you can write P(o given c); projects report extrinsic numbers.",
            },
            {
                "layout": "split",
                "title": "Problem with words as discrete symbols",
                "bullets": [
                    "film and movie are orthogonal.",
                    "No natural similarity for one-hot vectors.",
                    "A new word has no coordinate.",
                ],
                "image": "graphics/1.4-embeddings/onehot-vs-embed.png",
            },
            {
                "layout": "cards",
                "title": "Three words that are not synonyms",
                "cards": [
                    ("Distributional", "Similar contexts, similar meaning. Harris; Firth; Jurafsky Ch. 5."),
                    ("Distributed", "The code is a dense vector, not a one-hot."),
                    ("Embedding", "The lookup: nn.Embedding, a row of a V by d table."),
                ],
            },
            {
                "layout": "figure",
                "title": "How a distributional embedding is obtained",
                "image": "graphics/1.4-embeddings/how-obtained.png",
                "caption": "Corpus, then a window, then a fake prediction task. Words that shared neighbors sit nearby. Those rows are the embeddings.",
                "takeaway": "Firth: you shall know a word by the company it keeps. Word2Vec is one algorithm for that. A thesaurus is not.",
            },
            {
                "layout": "split",
                "title": "Skip-gram: from the center, predict a neighbor",
                "bullets": [
                    "Fake task on a window.",
                    "CBOW: from neighbors, predict the center.",
                    r"Logits \(z_w=u_w^\top v_c\).",
                ],
                "image": "graphics/1.4-embeddings/skipgram-window.png",
            },
            {
                "layout": "equation",
                "title": "Word2Vec prediction function",
                "equation": r"P(w_o\mid w_c)=\frac{\exp(u_o^{\top} v_c)}{\sum_{w}\exp(u_w^{\top} v_c)}",
                "notes": [
                    "1. Dot product scores similarity of o and c.",
                    "2. Exp makes every score positive.",
                    "3. Normalize over the vocabulary. That is softmax.",
                ],
            },
            {
                "layout": "figure",
                "title": "Skip-gram is a table, a product, then a softmax",
                "image": "graphics/1.4-embeddings/skipgram-uv.png",
                "caption": "Keep V (center rows). Throw away the softmax. A transformer keeps transforming those vectors.",
            },
            {
                "layout": "split",
                "title": "A three-word softmax you can finish by hand",
                "bullets": [
                    r"Scores \((1, 0.5, 0)\) for cat, mat, sat.",
                    r"\(p\approx(0.51, 0.31, 0.19)\).",
                    "Mikolov 2013a §§1–3. Negative sampling is cited, not derived.",
                ],
                "image": "graphics/1.4-embeddings/skipgram-softmax.png",
            },
            {
                "layout": "compare",
                "title": "Counting vs. predicting",
                "left_title": "Count",
                "left": "Build a co-occurrence matrix, then factor it (LSA / GloVe). Classical vector semantics can start here.",
                "right_title": "Predict",
                "right": "Skip-gram predicts context. Same distributional idea; same training loop as an LLM. No SVD homework this week.",
            },
            {
                "layout": "split",
                "title": "Direction can mean something",
                "bullets": [
                    r"king − man + woman ≈ queen.",
                    r"Cosine: \(u^\top v/(\|u\|\|v\|)\). Length tracks frequency.",
                    "Nearest neighbors debug. They are not a project metric.",
                ],
                "image": "graphics/1.4-embeddings/semantic-geometry.png",
            },
            {
                "layout": "split",
                "title": "How to evaluate word vectors",
                "bullets": [
                    "Intrinsic: analogies, similarity, clustering.",
                    "Extrinsic: does a downstream model improve?",
                    "They need not agree. Projects report extrinsic.",
                ],
                "image": "graphics/1.4-embeddings/intrinsic-extrinsic.png",
            },
            {
                "layout": "split",
                "title": "Bias is also geometry",
                "bullets": [
                    r"Offset \(o=\overrightarrow{\mathrm{he}}-\overrightarrow{\mathrm{she}}\).",
                    r"Score \(v^{\top}o/\|o\|\). Larger sits closer to he.",
                    "Lab 1: constructed 2-D first, then the same probe on a real model later.",
                ],
                "image": "graphics/1.4-embeddings/bias-geometry.png",
            },
            {
                "layout": "cards",
                "title": "What to take from this lecture",
                "cards": [
                    ("Write it", "Skip-gram softmax from the center vector. Keep those rows; throw the classifier."),
                    ("Report it", "Intrinsic numbers debug the space. Extrinsic numbers go in the project."),
                    ("Probe it", "The same geometry can encode a stereotype. Lab 1 measures that on purpose."),
                ],
            },
        ],
    },
    {
        "stem": "2.1-sequence-rnns",
        "title": "2.1 Sequential Models and RNNs",
        "slides": [
            {
                "layout": "title",
                "title": "Sequential Models and RNNs",
                "subtitle": "DATA 443/643  ·  Week 2, note 2.1",
                "meta": "Week 2  ·  American University  ·  Ahmad Mousavi",
                "credit": "Ideas from Stanford CS224N W26 L4 (language models and RNNs). Original slides; that course is not copied.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan",
                "agenda": [
                    ("1", "Why a fixed window is not enough"),
                    ("2", "The cell, then the unroll"),
                    ("3", "Many-to-one versus many-to-many"),
                    ("4", "An RNN language model is next-token NLL"),
                    ("5", "A two-step numeric table"),
                ],
                "takeaway": "Key goal: leave with a shared cell and a next-token loss that sits on a hidden state.",
            },
            {
                "layout": "compare",
                "title": "A window cannot grow with the sentence",
                "left_title": "n-gram / fixed MLP",
                "left": "Last k words only. Raise k and the table is sparse, or the concat layer gets a new weight per position.",
                "right_title": "Recurrent cell",
                "right": "Any length. Same W_h at every step. In principle the first token can still sit in h_T.",
            },
            {
                "layout": "split",
                "title": "The cell",
                "bullets": [
                    r"Each step: \(x_t\) and \(h_{t-1}\) become \(h_t\).",
                    "The same weights at every token.",
                    r"Reset \(h_0=0\) between unrelated documents.",
                ],
                "image": "graphics/2.1-sequence-rnns/rnn-cell.png",
            },
            {
                "layout": "equation",
                "title": "Vanilla recurrence",
                "equation": r"h_t=\tanh(W_h h_{t-1}+W_x x_t+b)",
                "notes": [
                    "Copies of W_h, not a new matrix per step.",
                    "tanh is the usual vanilla default.",
                    "That overwrite is why long-range gradients die in 2.2.",
                ],
            },
            {
                "layout": "split",
                "title": "Unrolled in time",
                "bullets": [
                    "The loop is a chain. That chain is the long-range path.",
                    "A CNN is parallel with a fixed window.",
                    "An RNN is sequential with the whole past.",
                ],
                "image": "graphics/2.1-sequence-rnns/rnn-unroll.png",
            },
            {
                "layout": "figure",
                "title": "The same cell, different wiring",
                "image": "graphics/2.1-sequence-rnns/arch-zoo.png",
                "caption": "Lab 2 is many-to-one. Language modeling is many-to-many. Encoder-decoder waits for Week 3.",
            },
            {
                "layout": "split",
                "title": "An RNN language model",
                "bullets": [
                    r"Softmax over the vocabulary from \(h_t\).",
                    r"Loss at \(t\): \(-\log P(x_{t+1}\mid h_t)\).",
                    "Teacher forcing: the true previous token, not a sample.",
                ],
                "image": "graphics/2.1-sequence-rnns/rnn-lm.png",
            },
            {
                "layout": "split",
                "title": r"Two steps, same \(W_h=0.5 I\)",
                "bullets": [
                    r"\(h_0=0\), \(x_1=[1,0]\), \(x_2=[0,1]\).",
                    r"\(h_1\approx[0.76,0]\). Then \(h_2\approx[0.36,0.76]\).",
                    r"Token 1 shrinks in \(h_2\). That is the teaser for 2.2.",
                ],
                "image": "graphics/2.1-sequence-rnns/rnn-numeric.png",
            },
            {
                "layout": "cards",
                "title": "What to take from this lecture",
                "cards": [
                    ("Share it", "One W_h along the sentence. Reset between documents."),
                    ("Score it", "Next-token NLL from h_t. Same loss as Week 1, new state."),
                    ("Watch it", "If the first token has already shrunk, Lab 2 will fail at long T."),
                ],
            },
        ],
    },
    {
        "stem": "2.2-vanishing-gradients",
        "title": "2.2 Vanishing and Exploding Gradients",
        "slides": [
            {
                "layout": "title",
                "title": "Vanishing and Exploding Gradients",
                "subtitle": "DATA 443/643  ·  Week 2, note 2.2",
                "meta": "Week 2  ·  American University  ·  Ahmad Mousavi",
                "credit": "Ideas from CS231N L7 and CS224N L4 (BPTT, singular values). Original slides; those courses are not copied.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan",
                "agenda": [
                    ("1", "BPTT: the shared matrix gets a sum"),
                    ("2", "A product of Jacobians"),
                    ("3", "Largest |eigenvalue| of W_h"),
                    ("4", "Clipping helps explosions, not vanishing"),
                    ("5", "What that does to a language model"),
                ],
            },
            {
                "layout": "split",
                "title": "Backprop through time",
                "bullets": [
                    "A repeated weight gets every copy's gradient.",
                    "That sum is BPTT.",
                    "Truncation is for memory. It does not fix vanishing.",
                ],
                "image": "graphics/2.2-vanishing-gradients/bptt.png",
            },
            {
                "layout": "equation",
                "title": "A product along the chain",
                "equation": r"\frac{\partial L}{\partial h_1}=\frac{\partial L}{\partial h_T}\frac{\partial h_T}{\partial h_{T-1}}\cdots\frac{\partial h_2}{\partial h_1}",
                "notes": [
                    r"Each factor contains \(W_h\) and \(\tanh'\).",
                    r"\(|\tanh'|\le 1\), and usually much smaller.",
                    r"Twenty factors of \(0.5\) is already \(10^{-6}\).",
                ],
            },
            {
                "layout": "split",
                "title": "The early token's learning signal dies",
                "bullets": [
                    "Forward state can still hold a faint trace.",
                    "The gradient does not come back.",
                    "Gates (2.3) keep a path near 1.",
                ],
                "image": "graphics/2.2-vanishing-gradients/vanish.png",
            },
            {
                "layout": "split",
                "title": "Linear recurrence is an eigenvalue story",
                "bullets": [
                    r"Scale like \(|\lambda_{\max}|^t\).",
                    r"Below 1: vanish. Above 1: explode.",
                    "Vanilla nets do not learn a unitary W_h.",
                ],
                "image": "graphics/2.2-vanishing-gradients/eigen-scale.png",
            },
            {
                "layout": "split",
                "title": "Two failure modes",
                "bullets": [
                    "Vanishing: early tokens do not train.",
                    "Exploding: NaNs, then you restart.",
                    "Same product, opposite disaster.",
                ],
                "image": "graphics/2.2-vanishing-gradients/vanish-explode.png",
            },
            {
                "layout": "split",
                "title": "Clipping is a shorter step, not a resurrection",
                "bullets": [
                    r"If \(\|g\|>c\), replace \(g\) by \(c\,g/\|g\|\).",
                    "Same direction, smaller step.",
                    "A vanished vector is already near 0.",
                ],
                "image": "graphics/2.2-vanishing-gradients/clipping.png",
            },
            {
                "layout": "compare",
                "title": "What the product does to next-token training",
                "left_title": "Near effects",
                "left": "The last few words still move the weights. The model learns local fluency.",
                "right_title": "Long-term effects",
                "right": "Tickets at step 7 never trains the last-word NLL. At test time the net cannot use that binding.",
            },
            {
                "layout": "cards",
                "title": "What to take from this lecture",
                "cards": [
                    ("Sum copies", "BPTT is the chain rule on a shared W_h."),
                    ("Clip explosions", "Pascanu: rescale a huge g. Do not claim it fixes vanishing."),
                    ("Measure Lab 2", "If T=40 is chance, the product is the bug, not PyTorch."),
                ],
            },
        ],
    },
    {
        "stem": "2.3-lstm-gru",
        "title": "2.3 LSTMs and GRUs",
        "slides": [
            {
                "layout": "title",
                "title": "LSTMs and GRUs",
                "subtitle": "DATA 443/643  ·  Week 2, note 2.3",
                "meta": "Week 2  ·  American University  ·  Ahmad Mousavi",
                "credit": "Ideas from CMU 11-785 L14 (stability, LSTM as a copy path). Original slides; that course is not copied.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan",
                "agenda": [
                    ("1", "Why a tanh overwrite cannot remember"),
                    ("2", "Three LSTM gates and the cell highway"),
                    ("3", "Copy regime: forget open, input closed"),
                    ("4", "GRU: two gates, hidden state is memory"),
                    ("5", "Bidirectional is illegal for next-token LMs"),
                ],
            },
            {
                "layout": "compare",
                "title": "The hidden state is constantly rewritten",
                "left_title": "Vanilla RNN",
                "left": "Every step: tanh of a new mix. Memory length is an eigenvalue accident.",
                "right_title": "Gated cell",
                "right": "A wire that can copy, plus learned switches that say when to write or erase.",
            },
            {
                "layout": "split",
                "title": "LSTM: a highway plus three gates",
                "bullets": [
                    "Forget, input, output. Each in (0, 1).",
                    "The cell is mostly multiply and add.",
                    "Hochreiter and Schmidhuber 1997; forget gate Gers 2000.",
                ],
                "image": "graphics/2.3-lstm-gru/lstm-gates.png",
            },
            {
                "layout": "equation",
                "title": "The cell update you will write",
                "equation": r"c_t=f_t\odot c_{t-1}+i_t\odot\tilde{c}_t",
                "notes": [
                    r"Then \(h_t=o_t\odot\tanh(c_t)\).",
                    r"If \(f_t\approx 1\) and \(i_t\approx 0\), the cell copies.",
                    r"Along that path, \(\partial c_t/\partial c_{t-1}=f_t\).",
                ],
            },
            {
                "layout": "split",
                "title": "Copy regime",
                "bullets": [
                    r"\(c_{t-1}=2\), \(f=1\), \(i=0\) gives \(c_t=2\).",
                    r"Ten copies: gradient \(1^{10}=1\).",
                    "Learnable, not guaranteed. About 100 steps, not infinity.",
                ],
                "image": "graphics/2.3-lstm-gru/copy-regime.png",
            },
            {
                "layout": "split",
                "title": "GRU: two gates, no extra cell",
                "bullets": [
                    "Reset and update. The hidden state is the memory.",
                    r"\(z\approx 0\) copies. \(z\approx 1\) replaces.",
                    "Fewer parameters. Still a loop.",
                ],
                "image": "graphics/2.3-lstm-gru/gru-gates.png",
            },
            {
                "layout": "compare",
                "title": "When you would still pick a gate",
                "left_title": "LSTM / GRU",
                "left": "Speech, time series, a small sequential baseline. Lab 2.",
                "right_title": "Transformer (Week 3)",
                "right": "Long text, GPU parallelism, path length one. The default for this course's projects.",
            },
            {
                "layout": "cards",
                "title": "What to take from this lecture",
                "cards": [
                    ("Write it", "c_t = forget * old + input * new."),
                    ("Copy it", "f=1, i=0 is a wire. Bidirectional peeks at the future."),
                    ("Next week", "Attention stops using this chain. Lab 2 is why."),
                ],
            },
        ],
    },
    {
        "stem": "3.1-attention-need",
        "title": "3.1 From Recurrence to Attention",
        "slides": [
            {
                "layout": "title",
                "title": "From Recurrence to Attention",
                "subtitle": "DATA 443/643  ·  Week 3, note 3.1",
                "meta": "Week 3  ·  American University  ·  Ahmad Mousavi",
                "credit": "Ideas from Stanford CS224N W26 L5 (attention as a direct look). Original slides; that course is not copied.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan",
                "agenda": [
                    ("1", "The seq2seq bottleneck"),
                    ("2", "Bahdanau rereads; Vaswani drops the loop"),
                    ("3", "Path length 1 is not cost 1"),
                    ("4", "Why a GPU likes attention"),
                ],
                "takeaway": "Key goal: leave with RNN path T, attention path 1, attention cost T squared.",
            },
            {
                "layout": "split",
                "title": "One vector is not a memory",
                "bullets": [
                    "An encoder–decoder RNN packs the source into h_T.",
                    "Long source, same-size bottle.",
                    "Attention is a direct look at the encoder states.",
                ],
                "image": "graphics/3.1-attention-need/bottleneck.png",
            },
            {
                "layout": "split",
                "title": "A chain versus all-pairs",
                "bullets": [
                    "RNN: token 1 reaches token 40 through 39 overwrites.",
                    "Attention: one score in a T by T map.",
                    "Week 2's Jacobian product is no longer the story.",
                ],
                "image": "graphics/3.1-attention-need/rnn-vs-attention.png",
            },
            {
                "layout": "compare",
                "title": "Two different inventions",
                "left_title": "Bahdanau 2015",
                "left": "Attention on an RNN. Queries from the decoder; keys from the encoder.",
                "right_title": "Vaswani 2017",
                "right": "Attention instead of an RNN. Self-attention: Q, K, V from the same sequence.",
            },
            {
                "layout": "split",
                "title": "Path length 1, cost T squared",
                "bullets": [
                    "The short path is why we left recurrence.",
                    "The quadratic bill is why Week 7 exists.",
                    "Full attention is this course's default.",
                ],
                "image": "graphics/3.1-attention-need/path-cost.png",
            },
            {
                "layout": "equation",
                "title": "A 4k-token PDF",
                "equation": r"T=4096,\quad T^{2}\approx 1.68\times 10^{7}",
                "notes": [
                    "Scores per head per layer, before batching.",
                    "Four bytes each is about 67 MB for one map.",
                    "FlashAttention is an implementation, not a new model.",
                ],
            },
            {
                "layout": "cards",
                "title": "What to take from this lecture",
                "cards": [
                    ("Reread", "Do not pack the source into one vector."),
                    ("Path 1", "Token 1 can touch token T in one hop."),
                    ("Pay T squared", "Lab 3 is T=4. A project PDF is not."),
                ],
            },
        ],
    },
    {
        "stem": "3.2-self-attention",
        "title": "3.2 Self-Attention (Q, K, V)",
        "slides": [
            {
                "layout": "title",
                "title": "Self-Attention (Q, K, V)",
                "subtitle": "DATA 443/643  ·  Week 3, note 3.2",
                "meta": "Week 3  ·  American University  ·  Ahmad Mousavi",
                "credit": "Ideas from CMU 11-711 (scaled dots, multi-head, causal mask). Original slides; that course is not copied.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan",
                "agenda": [
                    ("1", "Query asks, key is asked, value is mixed"),
                    ("2", "Scale by sqrt of d_k, then softmax"),
                    ("3", "Multi-head: concat, then W_O"),
                    ("4", "Causal mask: minus infinity, not zero"),
                ],
            },
            {
                "layout": "split",
                "title": "Query, key, value",
                "bullets": [
                    "Q, K, V are three linear maps of X.",
                    "A row of QK transpose: how much this token wants each position.",
                    "Then mix values. Mixing keys is the lab bug.",
                ],
                "image": "graphics/3.2-self-attention/qkv.png",
            },
            {
                "layout": "equation",
                "title": "Scaled dot-product attention",
                "equation": r"A=\mathrm{softmax}\bigl(QK^{\top}/\sqrt{d_k}\bigr),\quad \mathrm{out}=AV",
                "notes": [
                    "Variance of a dot product grows with d_k.",
                    "The scale keeps softmax from becoming one-hot.",
                    "Softmax over keys (last dim), not over queries.",
                ],
            },
            {
                "layout": "split",
                "title": "A 2 by 2 you will write",
                "bullets": [
                    r"S = diag(2, 2), d_k = 2.",
                    r"Row 1 softmax is about [0.80, 0.20].",
                    r"If V = I, the output is A.",
                ],
                "image": "graphics/3.2-self-attention/qkv-numeric.png",
            },
            {
                "layout": "split",
                "title": "A row is a distribution",
                "bullets": [
                    "Large mass on a name: this pronoun just looked there.",
                    "Equal keys split mass equally.",
                    "Lab 3 heatmaps this for T = 4.",
                ],
                "image": "graphics/3.2-self-attention/attn-heatmap.png",
            },
            {
                "layout": "split",
                "title": "Multi-head",
                "bullets": [
                    "Several small attentions in parallel.",
                    "Concatenate, then one linear W_O.",
                    "Heads can specialize. You still compute one by hand.",
                ],
                "image": "graphics/3.2-self-attention/multihead.png",
            },
            {
                "layout": "split",
                "title": "Causal mask",
                "bullets": [
                    "Illegal future scores become minus infinity.",
                    "Softmax of a zero is not probability zero.",
                    "This mask is GPT. BERT hides tokens instead.",
                ],
                "image": "graphics/3.2-self-attention/causal-mask.png",
            },
            {
                "layout": "cards",
                "title": "What to take from this lecture",
                "cards": [
                    ("Write it", "A = softmax(QK^T / sqrt(d_k)), then A V."),
                    ("Scale it", "Skip the square root and the row becomes too peaked."),
                    ("Mask it", "Lab 3: first bidirectional, then GPT-style."),
                ],
            },
        ],
    },
    {
        "stem": "3.3-transformer-block",
        "title": "3.3 The Transformer Block",
        "slides": [
            {
                "layout": "title",
                "title": "The Transformer Block",
                "subtitle": "DATA 443/643  ·  Week 3, note 3.3",
                "meta": "Week 3  ·  American University  ·  Ahmad Mousavi",
                "credit": "Ideas from Princeton COS 484 L8–L9 (positions, residual, MLP). Original slides; that course is not copied.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan",
                "agenda": [
                    ("1", "Attention is a set; language is ordered"),
                    ("2", "Add the residual; do not replace x"),
                    ("3", "The MLP holds most of the weights"),
                    ("4", "Encoder two sublayers; decoder three"),
                ],
            },
            {
                "layout": "split",
                "title": "Positions have to be added",
                "bullets": [
                    "Permute the tokens, attention permutes with them.",
                    "Sinusoids or learned vectors, added to embeddings.",
                    "Without them, dog bites man equals man bites dog.",
                ],
                "image": "graphics/3.3-transformer-block/positional.png",
            },
            {
                "layout": "split",
                "title": "One block",
                "bullets": [
                    "Attention mixes across positions.",
                    "The MLP mixes across channels at one position.",
                    "Layer-norm one token at a time.",
                ],
                "image": "graphics/3.3-transformer-block/block.png",
            },
            {
                "layout": "split",
                "title": "Residual: add, do not replace",
                "bullets": [
                    r"x becomes x + sublayer(x).",
                    "Cousin of the LSTM highway in Week 2.",
                    "A dead head still passes x through.",
                ],
                "image": "graphics/3.3-transformer-block/residual.png",
            },
            {
                "layout": "equation",
                "title": "Most weights are not attention",
                "equation": r"4d^{2}\ \text{(attention)} \quad\text{vs}\quad 8d^{2}\ \text{(MLP)}",
                "notes": [
                    r"W_Q, W_K, W_V, W_O versus d to 4d and back.",
                    r"GPT-2 small: N=12, d=768.",
                    "Pre-norm is the modern default; post-norm is 2017.",
                ],
            },
            {
                "layout": "split",
                "title": "Encoder versus decoder",
                "bullets": [
                    "BERT: encoder only, bidirectional.",
                    "GPT: decoder only, no cross-attention.",
                    "T5 / BART keep both. Captioning will too.",
                ],
                "image": "graphics/3.3-transformer-block/enc-dec.png",
            },
            {
                "layout": "cards",
                "title": "What to take from this lecture",
                "cards": [
                    ("Order it", "Positions are not optional for language."),
                    ("Add it", "Residual is x plus the sublayer, like a gated cell."),
                    ("Count it", "If you only plot attention heads, you missed the MLP."),
                ],
            },
        ],
    },
    {
        "stem": "3.4-gpt-bert",
        "title": "3.4 GPT and BERT",
        "slides": [
            {
                "layout": "title",
                "title": "GPT and BERT",
                "subtitle": "DATA 443/643  ·  Week 3, note 3.4",
                "meta": "Week 3  ·  American University  ·  Ahmad Mousavi",
                "credit": "Ideas from Princeton COS 484 L10 and CS224N pretraining (GPT vs BERT). Original slides; those courses are not copied.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan",
                "agenda": [
                    ("1", "Static table versus contextual vector"),
                    ("2", "Causal next-token versus masked tokens"),
                    ("3", "Same width, different mask and loss"),
                    ("4", "What a project is allowed to stream"),
                ],
            },
            {
                "layout": "split",
                "title": "The same type, two vectors",
                "bullets": [
                    "Week 1: bank is one row.",
                    "A transformer: river bank is not money bank.",
                    "Pretrain once, fine-tune many times.",
                ],
                "image": "graphics/3.4-gpt-bert/contextual.png",
            },
            {
                "layout": "split",
                "title": "Same block, different mask",
                "bullets": [
                    "GPT: look left, predict the next token.",
                    "BERT: look both ways, fill [MASK].",
                    "Those are two different uses of the word mask.",
                ],
                "image": "graphics/3.4-gpt-bert/gpt-bert.png",
            },
            {
                "layout": "split",
                "title": "Two objectives",
                "bullets": [
                    r"GPT: \(p(x_t\mid x_{1:t-1})\).",
                    "BERT: p(masked token given the rest).",
                    "Do not fine-tune BERT as if it were GPT.",
                ],
                "image": "graphics/3.4-gpt-bert/mlm-clm.png",
            },
            {
                "layout": "compare",
                "title": "What you can ship",
                "left_title": "Decoder (GPT-style)",
                "left": "Generate, chat, RAG, tools. The default stack for this course.",
                "right_title": "Encoder (BERT-style)",
                "right": "Classify, tag, embed a span. Cannot stream a paragraph.",
            },
            {
                "layout": "equation",
                "title": "A causal 2 by 2",
                "equation": r"S_{\mathrm{GPT}}=\begin{bmatrix}1&-\infty\\3&4\end{bmatrix}",
                "notes": [
                    "Row 1 softmax is [1, 0]. Token 1 cannot see token 2.",
                    r"Row 2 is softmax([3, 4]) about [0.27, 0.73].",
                    "BERT softmaxes the unmasked S. Token 1 does look ahead.",
                ],
            },
            {
                "layout": "cards",
                "title": "What to take from this lecture",
                "cards": [
                    ("Context", "Embeddings are now a function of the sentence."),
                    ("Fork", "Causal LM versus MLM. Same d, different job."),
                    ("Project", "If it must stream tokens, it is not BERT."),
                ],
            },
        ],
    },
    {
        "stem": "4.1-multimodal-foundations",
        "title": "4.1 Multimodal Foundations",
        "slides": [
            {
                "layout": "title",
                "title": "Multimodal Foundations",
                "subtitle": "DATA 443/643  ·  Week 4, note 4.1",
                "meta": "Week 4  ·  American University  ·  Ahmad Mousavi",
                "credit": "Ideas from CMU 11-777 (five jobs; joint vs coordinated). Original slides; that course is not copied.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan",
                "agenda": [
                    ("1", "Why more than one stream"),
                    ("2", "Five jobs: represent, align, fuse, translate, co-learn"),
                    ("3", "Joint concat versus two towers and a cosine"),
                    ("4", "A 2-D retrieval numeric"),
                ],
                "takeaway": "Key goal: leave knowing CLIP scores pairs; it does not fuse pixels with token ids.",
            },
            {
                "layout": "split",
                "title": "Five jobs, not one architecture",
                "bullets": [
                    "Represent: one vector, or two towers?",
                    "Align, fuse, translate, co-learn are different verbs.",
                    "Captioning maps. CLIP scores.",
                ],
                "image": "graphics/4.1-multimodal-foundations/five-challenges.png",
            },
            {
                "layout": "split",
                "title": "Joint versus coordinated",
                "bullets": [
                    "Joint: mash streams into one vector.",
                    "Coordinated: a tower each, then a similarity.",
                    "Missing a stream hurts the joint model.",
                ],
                "image": "graphics/4.1-multimodal-foundations/joint-coord.png",
            },
            {
                "layout": "compare",
                "title": "What your demo is allowed to do",
                "left_title": "Typed search over photos",
                "left": "Coordinated. Embed the query alone. Rank by cosine.",
                "right_title": "Must output a sentence",
                "right": "Translation. You need a decoder (BLIP, an LLM). Cosine is not a caption.",
            },
            {
                "layout": "split",
                "title": "Rank by cosine",
                "bullets": [
                    r"Match \(v=[1,0]\), \(t=[0.8,0.2]\) is about 0.97.",
                    "Mismatch with [0, 1] is 0.",
                    "Concat of those two vectors is 4-D and needs both.",
                ],
                "image": "graphics/4.1-multimodal-foundations/cosine-numeric.png",
            },
            {
                "layout": "cards",
                "title": "What to take from this lecture",
                "cards": [
                    ("Do not concat and call it CLIP", "CLIP never concatenates pixels with token ids in pretraining."),
                    ("Name the job", "Search, caption, or detect a region? Different boxes on the five-job strip."),
                    ("Week 4.3", "The coordination loss is InfoNCE. Zero-shot is a text prompt."),
                ],
            },
        ],
    },
    {
        "stem": "4.2-vision-transformers",
        "title": "4.2 Vision Transformers",
        "slides": [
            {
                "layout": "title",
                "title": "Vision Transformers",
                "subtitle": "DATA 443/643  ·  Week 4, note 4.2",
                "meta": "Week 4  ·  American University  ·  Ahmad Mousavi",
                "credit": "Ideas from Stanford CS231N 2025 L8 (ViT patches). Original slides; that course is not copied.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan",
                "agenda": [
                    ("1", "Tile the image; do not use overlapping windows"),
                    ("2", "Flatten, then a linear map to width d"),
                    ("3", "Add positions; every patch may look"),
                    ("4", "Start from a pretrained tower"),
                ],
            },
            {
                "layout": "split",
                "title": "Patches as tokens",
                "bullets": [
                    r"\(N = HW / P^{2}\) non-overlapping tiles.",
                    r"A 16 by 16 RGB patch is 768 numbers.",
                    "That linear map is a conv with kernel P, stride P.",
                ],
                "image": "graphics/4.2-vision-transformers/patches.png",
            },
            {
                "layout": "split",
                "title": "Flatten one tile",
                "bullets": [
                    r"A 2 by 2 of 1,2,3,4 becomes [1, 2, 3, 4].",
                    "Then W maps to width d.",
                    "Lab 4 does this on a 32 by 32 RGB crop.",
                ],
                "image": "graphics/4.2-vision-transformers/patch-numeric.png",
            },
            {
                "layout": "split",
                "title": "A 224 image is a short paragraph",
                "bullets": [
                    r"P = 16 gives N = 196, plus [CLS] is 197.",
                    r"Attention map: \(197^{2}\) scores per head.",
                    "No GPT mask: there is no future patch.",
                ],
                "image": "graphics/4.2-vision-transformers/vit-count.png",
            },
            {
                "layout": "split",
                "title": "The same stack as language",
                "bullets": [
                    "Positions are not optional. Top is not bottom.",
                    "[CLS] or mean-pool, then a head.",
                    "From scratch on 800 scans is the wrong default.",
                ],
                "image": "graphics/4.2-vision-transformers/vit.png",
            },
            {
                "layout": "cards",
                "title": "What to take from this lecture",
                "cards": [
                    ("Count it", "N = HW / P squared. Tiles, not CNN windows."),
                    ("Reuse Week 3", "Transformer block, bidirectional, add positions."),
                    ("Freeze a tower", "CLIP's image encoder is often this ViT, already trained."),
                ],
            },
        ],
    },
    {
        "stem": "4.3-contrastive-zeroshot",
        "title": "4.3 Contrastive Learning and Zero-Shot Transfer",
        "slides": [
            {
                "layout": "title",
                "title": "Contrastive Learning and Zero-Shot Transfer",
                "subtitle": "DATA 443/643  ·  Week 4, note 4.3",
                "meta": "Week 4  ·  American University  ·  Ahmad Mousavi",
                "credit": "Ideas from Stanford CS231N 2025 L16 (InfoNCE, zero-shot prompts). Original slides; that course is not copied.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan",
                "agenda": [
                    ("1", "An N by N grid; the diagonal is the match"),
                    ("2", "InfoNCE; the rest of the batch are negatives"),
                    ("3", "Zero-shot: nearest prompt, not a C-way softmax"),
                    ("4", "Linear probe versus zero-shot"),
                ],
            },
            {
                "layout": "split",
                "title": "Matched pairs on the diagonal",
                "bullets": [
                    "Encode N images and N captions.",
                    "Image i should sit with caption i.",
                    "This is 4.1's coordinated space, with a loss.",
                ],
                "image": "graphics/4.3-contrastive-zeroshot/contrastive.png",
            },
            {
                "layout": "equation",
                "title": "InfoNCE, one row",
                "equation": r"-\log\frac{\exp(\mathrm{sim}(v_i,t_i)/\tau)}{\sum_j\exp(\mathrm{sim}(v_i,t_j)/\tau)}",
                "notes": [
                    "CLIP trains this both ways: image-to-text and text-to-image.",
                    "Small tau sharpens. Argmax of a row does not flip.",
                    "N=4 in lab is to see the matrix, not to match ImageNet.",
                ],
            },
            {
                "layout": "split",
                "title": "A 2 by 2 you will write",
                "bullets": [
                    r"Scores [0.9, 0.1], tau = 1, gives about [0.69, 0.31].",
                    r"Loss is -log 0.69 about 0.37.",
                    "Identical captions: uniform softmax, no learning.",
                ],
                "image": "graphics/4.3-contrastive-zeroshot/infonce-numeric.png",
            },
            {
                "layout": "split",
                "title": "Zero-shot is nearest text",
                "bullets": [
                    'Encode "a photo of a dog", not the token dog.',
                    "New classes are new strings.",
                    "Unseen phrases do not magically work.",
                ],
                "image": "graphics/4.3-contrastive-zeroshot/zeroshot.png",
            },
            {
                "layout": "split",
                "title": "Two ways to transfer",
                "bullets": [
                    "Linear probe: freeze the image tower, train C classes.",
                    "Zero-shot: the classifier is the text tower.",
                    "Captioning and LLaVA wait. This week is the score.",
                ],
                "image": "graphics/4.3-contrastive-zeroshot/probe-vs-zeroshot.png",
            },
            {
                "layout": "cards",
                "title": "What to take from this lecture",
                "cards": [
                    ("Off-diagonal is a negative", "Not a don't-care. Shuffle in Lab 4 and the loss should rise."),
                    ("Prompt it", "A photo of beats the raw label. Ensemble is optional."),
                    ("Week 5", "CLIP's data, retrieval, and the bias that comes with the geometry."),
                ],
            },
        ],
    },
    {
        "stem": "5.1-clip",
        "title": "5.1 CLIP",
        "slides": [
            {
                "layout": "title",
                "title": "CLIP",
                "subtitle": "DATA 443/643  ·  Week 5, note 5.1",
                "meta": "Week 5  ·  American University  ·  Ahmad Mousavi",
                "credit": "Ideas from Stanford CS231N 2025 L16 (two towers, a cosine, not a captioner). Original slides; that course is not copied.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan",
                "agenda": [
                    ("1", "Two towers; keep both after training"),
                    ("2", "A similarity score, not a sentence"),
                    ("3", "A 2 by 2 cosine matrix"),
                    ("4", "Temperature and batch size"),
                ],
                "takeaway": "Key goal: leave able to write encode_image, encode_text, cosine — and to refuse generate.",
            },
            {
                "layout": "split",
                "title": "Two towers, one cosine",
                "bullets": [
                    "ViT or ResNet for the image. A transformer for the text.",
                    "InfoNCE on the batch (note 4.3).",
                    "After training you keep the towers, not a fused head.",
                ],
                "image": "graphics/5.1-clip/clip-towers.png",
            },
            {
                "layout": "compare",
                "title": "What the API is allowed to do",
                "left_title": "CLIP",
                "left": "Score a pair. Retrieve. Zero-shot by nearest prompt. Freeze the image tower later.",
                "right_title": "Not CLIP",
                "right": "Decode a caption. Draw boxes. Guarantee the photo is true. That is BLIP, a detector, or a human.",
            },
            {
                "layout": "split",
                "title": "A batch of 2 you will write",
                "bullets": [
                    r"Unit vectors. \(S_{11}=1.0\), \(S_{12}=0.6\), \(S_{21}=0\), \(S_{22}=0.8\).",
                    "The diagonal should win each row.",
                    "One negative is not CLIP scale. It is the algebra.",
                ],
                "image": "graphics/5.1-clip/clip-numeric.png",
            },
            {
                "layout": "equation",
                "title": "InfoNCE on row 1",
                "equation": r"-\log\frac{\exp(S_{11}/\tau)}{\exp(S_{11}/\tau)+\exp(S_{12}/\tau)}",
                "notes": [
                    r"\(\tau=1\): softmax about [0.60, 0.40], NLL about 0.51.",
                    r"\(\tau=0.07\): match probability about 0.997.",
                    "Huge batches exist so you have many negatives.",
                ],
            },
            {
                "layout": "split",
                "title": "Small tau, large batch",
                "bullets": [
                    r"Learned \(\tau\) is often near 0.07.",
                    "A batch of 8 has 7 negatives. A batch of 1024 has 1023.",
                    "Fine-grained word order still needs hard negatives later.",
                ],
                "image": "graphics/5.1-clip/clip-tau.png",
            },
            {
                "layout": "cards",
                "title": "What to take from this lecture",
                "cards": [
                    ("Three calls", "encode_image, encode_text, cosine. No generate."),
                    ("Temperature", "Same scores, different softmax. Check unit length first."),
                    ("Next", "If you must write a sentence, that is 5.2."),
                ],
            },
        ],
    },
    {
        "stem": "5.2-blip",
        "title": "5.2 BLIP and Captioning",
        "slides": [
            {
                "layout": "title",
                "title": "BLIP and Captioning",
                "subtitle": "DATA 443/643  ·  Week 5, note 5.2",
                "meta": "Week 5  ·  American University  ·  Ahmad Mousavi",
                "credit": "Ideas from Stanford CS231N 2025 L16 (CoCa: add a decoder) and the BLIP paper (ITC, ITM, LM, bootstrap). Original slides; those sources are not copied.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan",
                "agenda": [
                    ("1", "Retrieve versus write"),
                    ("2", "Filter noisy web pairs"),
                    ("3", "Three losses: ITC, ITM, LM"),
                    ("4", "One ITM numeric"),
                ],
                "takeaway": "Key goal: CLIP scores; BLIP can decode; the filter is why web alt-text is not the training text.",
            },
            {
                "layout": "compare",
                "title": "Two jobs that look similar in a demo",
                "left_title": "Retrieval (CLIP)",
                "left": "Return a string that already lives in the gallery. Metric: recall@k.",
                "right_title": "Captioning (BLIP)",
                "right": "Generate a new string. Metric: CIDEr, CLIP-score, and a human check. Hallucinated objects are the failure.",
            },
            {
                "layout": "split",
                "title": "Bootstrap, then train",
                "bullets": [
                    "Alt-text is often a filename or a SKU.",
                    "Generate a caption, keep it if ITM still matches.",
                    "CoCa adds a decoder. BLIP also cleans the pairs.",
                ],
                "image": "graphics/5.2-blip/blip-pipeline.png",
            },
            {
                "layout": "split",
                "title": "Three losses, one backbone",
                "bullets": [
                    "ITC: CLIP-style softmax over the batch.",
                    "ITM: yes/no on one pair, often a hard negative.",
                    "LM: next-token, cross-attend to ViT patches.",
                ],
                "image": "graphics/5.2-blip/blip-losses.png",
            },
            {
                "layout": "equation",
                "title": "ITM is a sigmoid, not a batch softmax",
                "equation": r"\sigma(s)=\frac{1}{1+e^{-s}}",
                "notes": [
                    r"Matched \(s=2\): \(\sigma\approx 0.88\), CE \(\approx 0.13\).",
                    r"Mismatch \(s=-1\): \(\sigma\approx 0.27\), CE \(\approx 0.31\).",
                    "ITC needs a batch. ITM can score one pair.",
                ],
            },
            {
                "layout": "split",
                "title": "Write the ITM table",
                "bullets": [
                    "True caption: a red mug on a desk.",
                    "False caption: a blue bicycle.",
                    "If you only retrieve, stop at ITC. If you write, you need LM.",
                ],
                "image": "graphics/5.2-blip/blip-itm-numeric.png",
            },
            {
                "layout": "cards",
                "title": "What to take from this lecture",
                "cards": [
                    ("Filter", "Do not train LM on DSC0001.jpg."),
                    ("Three verbs", "Align, match, decode. Different losses."),
                    ("Whisper clip", "Encoder–decoder analog. Whisper has no ITC+ITM."),
                ],
            },
        ],
    },
    {
        "stem": "5.3-retrieval-bias",
        "title": "5.3 Retrieval, Bias, and Robustness",
        "slides": [
            {
                "layout": "title",
                "title": "Retrieval, Bias, and Robustness",
                "subtitle": "DATA 443/643  ·  Week 5, note 5.3",
                "meta": "Week 5  ·  American University  ·  Ahmad Mousavi",
                "credit": "Ideas from Stanford CS231N 2025 L16 (prompt sensitivity, distribution shift) and the CLIP paper’s broader-impact discussion. Original slides; those sources are not copied.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan",
                "agenda": [
                    ("1", "Two retrieval directions"),
                    ("2", "recall@k needs k and a gallery size"),
                    ("3", "An occupation probe with numbers"),
                    ("4", "Typographic attacks"),
                ],
                "takeaway": "Key goal: a cosine that finds cats also ranks stereotypes. Measure both.",
            },
            {
                "layout": "split",
                "title": "One space, two queries",
                "bullets": [
                    "Text to image: type a string, rank photos.",
                    "Image to text: a photo, rank captions.",
                    "Throw away a tower and one direction dies.",
                ],
                "image": "graphics/5.3-retrieval-bias/retrieval.png",
            },
            {
                "layout": "split",
                "title": "Always write k",
                "bullets": [
                    r"Gold in the top \(k\) scores 1 for that query.",
                    "Average over queries. State gallery size.",
                    r"On 100k images, recall@1 can look like zero while recall@10 is usable.",
                ],
                "image": "graphics/5.3-retrieval-bias/recall-numeric.png",
            },
            {
                "layout": "split",
                "title": "Occupation probe",
                "bullets": [
                    r"Query woman: nurse, then ceo, then cat.",
                    r"Query man: ceo tied with cat; nurse last.",
                    "Lab 5 runs this on toy_clip.csv. A résumé ranker needs the same table.",
                ],
                "image": "graphics/5.3-retrieval-bias/occupation-numeric.png",
            },
            {
                "layout": "split",
                "title": "The web is in the geometry",
                "bullets": [
                    "Prompts move the query along Week 1’s axes.",
                    "High ImageNet zero-shot does not certify medical photos.",
                    "A probe is a fixed list plus a rule for a bad hit.",
                ],
                "image": "graphics/5.3-retrieval-bias/vlm-bias.png",
            },
            {
                "layout": "split",
                "title": "Typographic attack",
                "bullets": [
                    "An apple with iPod printed on it.",
                    "CLIP often reads the overlay first.",
                    "Same cosine. Different harm than occupations.",
                ],
                "image": "graphics/5.3-retrieval-bias/typographic.png",
            },
            {
                "layout": "cards",
                "title": "What to take from this lecture",
                "cards": [
                    ("Two numbers", "recall@k and a failure case."),
                    ("Probe", "Document prompts. Do not claim you debiased by deleting an axis."),
                    ("Lab 5", "nurse / ceo versus man / woman is this lecture in 2-D."),
                ],
            },
        ],
    },
    {
        "stem": "6.1-audio-spectrograms",
        "title": "6.1 Waveforms, Spectrograms, and Time–Frequency Tokens",
        "slides": [
            {
                "layout": "title",
                "title": "Spectrograms as Tokens",
                "subtitle": "DATA 443/643  ·  Week 6, note 6.1",
                "meta": "Week 6  ·  American University  ·  Ahmad Mousavi",
                "credit": "Ideas from Stanford CS224S 2025 L2 (spectrogram as spectrum + time) and L5 (why not a raw waveform). Original slides; that course is not copied.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan",
                "agenda": [
                    ("1", "A 1-D wave, then an STFT"),
                    ("2", "Count frames, not samples"),
                    ("3", "Patch the picture as in ViT"),
                    ("4", "Whisper’s 25 ms / 10 ms numbers"),
                ],
                "takeaway": "Key goal: leave able to compute T from L, N, H, and to refuse a 16 kHz transformer.",
            },
            {
                "layout": "split",
                "title": "A wave, then a picture",
                "bullets": [
                    r"Pressure \(x[n]\) at sampling rate \(f_s\).",
                    r"STFT: window length \(N\), hop \(H\), then a DFT.",
                    "Plot magnitudes. Most encoders drop phase.",
                ],
                "image": "graphics/6.1-audio-spectrograms/wave-spec.png",
            },
            {
                "layout": "equation",
                "title": "How many frames?",
                "equation": r"T=1+\operatorname{floor}\bigl((L-N)/H\bigr)",
                "notes": [
                    r"One second at 16 kHz: \(L=16000\).",
                    r"\(N=400\), \(H=160\) gives \(T=98\).",
                    "Double the hop: about half as many frames. Frequency bins do not move.",
                ],
            },
            {
                "layout": "split",
                "title": "Slide the window",
                "bullets": [
                    r"Window \(N/f_s=25\) ms, hop \(10\) ms: Whisper’s default.",
                    "Frames last long enough to see a phoneme.",
                    "A raw 16 kHz wave is 16,000 tokens per second.",
                ],
                "image": "graphics/6.1-audio-spectrograms/stft-frames.png",
            },
            {
                "layout": "split",
                "title": "Then patch, as in ViT",
                "bullets": [
                    r"An \(80\times 400\) mel grid, \(16\times 16\) tiles: 125 tokens.",
                    "Time is not quite space. Name which axis is frequency.",
                    "Lab 6 crops remainders. Do not drop a formant band silently.",
                ],
                "image": "graphics/6.1-audio-spectrograms/spec-patches.png",
            },
            {
                "layout": "cards",
                "title": "What to take from this lecture",
                "cards": [
                    ("Write the front end", "fs, N, hop, mel versus linear."),
                    ("Bin k", r"Near \(k\cdot f_s/N\) hertz. Check Lab 6’s 440 and 880."),
                    ("Not a transcript", "Tasks sit on top of the tokens. That is 6.2."),
                ],
            },
        ],
    },
    {
        "stem": "6.2-audio-encoders",
        "title": "6.2 Audio Encoders and Speech Models",
        "slides": [
            {
                "layout": "title",
                "title": "Audio Encoders and Speech Models",
                "subtitle": "DATA 443/643  ·  Week 6, note 6.2",
                "meta": "Week 6  ·  American University  ·  Ahmad Mousavi",
                "credit": "Ideas from Stanford CS224S 2025 L11 (Whisper: log-mel, two convs, GPT-style decoder, 30 s, no CTC). Original slides; that course is not copied.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan",
                "agenda": [
                    ("1", "Whisper: encoder then a causal decoder"),
                    ("2", "30 seconds is 3000 frames, not 480k samples"),
                    ("3", "Special tokens: language, task, time"),
                    ("4", "CLAP: CLIP for audio"),
                ],
                "takeaway": "Key goal: pick Whisper vs CLAP by the head, not by the spectrogram.",
            },
            {
                "layout": "split",
                "title": "Whisper is translation, with a spectrogram",
                "bullets": [
                    "Log-mel in. Two convs. Transformer encoder.",
                    "Decoder is GPT-style and causal. No CTC.",
                    "Cross-attention into encoder states. Same as note 3.3.",
                ],
                "image": "graphics/6.2-audio-encoders/whisper.png",
            },
            {
                "layout": "equation",
                "title": "Why the spectrogram exists",
                "equation": r"30\,\mathrm{s}\times 16\,\mathrm{kHz}=480{,}000 \quad\text{vs}\quad 30/0.010=3000",
                "notes": [
                    "3000 mel frames, 80 bands, then a stride-2 stem.",
                    "About 1500 encoder steps, not a 480k-token transformer.",
                    "Long audio: 30 s windows. Timestamp tokens shift the window.",
                ],
            },
            {
                "layout": "split",
                "title": "Thirty seconds, then tokens",
                "bullets": [
                    r"Special tokens: language, <|transcribe|>, timestamps.",
                    "The loss is next-token on the text, conditioned on audio.",
                    "Timestamps are vocabulary, not a second model.",
                ],
                "image": "graphics/6.2-audio-encoders/whisper-chunk.png",
            },
            {
                "layout": "split",
                "title": "CLAP is CLIP for sound",
                "bullets": [
                    "Audio tower and text tower. InfoNCE on captions.",
                    "Rank clips by cosine. Do not decode a transcript.",
                    "The text tower may be bidirectional. Whisper’s decoder may not.",
                ],
                "image": "graphics/6.2-audio-encoders/clap.png",
            },
            {
                "layout": "split",
                "title": "Rank, then stop",
                "bullets": [
                    "Cosines 0.11, 0.72, 0.40. Rank is clip 2, 3, 1.",
                    "If you needed the words in clip 2, call Whisper on the wave.",
                    "Same spectrogram tokens. Different head.",
                ],
                "image": "graphics/6.2-audio-encoders/clap-rank.png",
            },
            {
                "layout": "cards",
                "title": "What to take from this lecture",
                "cards": [
                    ("Transcript", "Whisper. Subtitles and timestamps."),
                    ("Search", "CLAP. Zero-shot tags. Dual retrieval."),
                    ("Project", "Do not concat Whisper states into CLIP without naming the rates."),
                ],
            },
        ],
    },
    {
        "stem": "6.3-fusion-scarcity",
        "title": "6.3 Fusion, Unified Embeddings, and Data Scarcity",
        "slides": [
            {
                "layout": "title",
                "title": "Fusion, Unified Embeddings, and Data Scarcity",
                "subtitle": "DATA 443/643  ·  Week 6, note 6.3",
                "meta": "Week 6  ·  American University  ·  Ahmad Mousavi",
                "credit": "Ideas from CMU 11-777 (early / late / cross-attention fusion) and note 4.1’s coordinated baseline. Original slides; that course is not copied.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan",
                "agenda": [
                    ("1", "Early, late, cross-attention"),
                    ("2", "Concat grows width; add needs a shared axis"),
                    ("3", "The data pyramid"),
                    ("4", "What to write in a report"),
                ],
                "takeaway": "Key goal: name the fusion and the missing-modality plan. Cosine is not cross-attention.",
            },
            {
                "layout": "split",
                "title": "Three places to fuse",
                "bullets": [
                    "Early: concat features, one backbone. Brittle if audio is missing.",
                    "Late: a model each, then combine scores.",
                    "Cross-attention: queries from one stream, K and V from the other.",
                ],
                "image": "graphics/6.3-fusion-scarcity/fusion.png",
            },
            {
                "layout": "split",
                "title": "Concat versus add",
                "bullets": [
                    r"\([a;v]\in\mathbb{R}^{256}\) if each is 128-D.",
                    r"Add is illegal if widths differ. Map first: \(W_v\in\mathbb{R}^{128\times 256}\).",
                    "CLIP two-towers never concat pixels with token ids.",
                ],
                "image": "graphics/6.3-fusion-scarcity/concat-add.png",
            },
            {
                "layout": "equation",
                "title": "A missing microphone",
                "equation": r"[a;v]\in\mathbb{R}^{256}\quad\text{needs both streams}",
                "notes": [
                    "Early concat with no dropout assumes audio is there.",
                    "Late towers can skip a cosine if the mic dies.",
                    "Cross-attention can mask a whole key set.",
                ],
            },
            {
                "layout": "split",
                "title": "Pretrain where the data is thick",
                "bullets": [
                    "Web text, then image–text, then transcribed audio, then labeled tasks.",
                    "Freeze Whisper or CLIP. Train a small head on 400 rows.",
                    "Do not train a joint stack from scratch on 400 clips.",
                ],
                "image": "graphics/6.3-fusion-scarcity/scarcity.png",
            },
            {
                "layout": "cards",
                "title": "What to take from this lecture",
                "cards": [
                    ("Name it", "Early, late, or cross-attention. Which loss sees both streams?"),
                    ("Count it", "Unpaired hours, paired hours, labeled rows."),
                    ("Lab 6", "Concat versus add in 4-D is this slide in miniature."),
                ],
            },
        ],
    },
    {
        "stem": "7.1-scaling-laws",
        "title": "7.1 Scaling Laws",
        "slides": [
            {
                "layout": "title",
                "title": "Scaling Laws",
                "subtitle": "DATA 443/643  ·  Week 7, note 7.1",
                "meta": "Week 7  ·  American University  ·  Ahmad Mousavi",
                "credit": "Ideas from Stanford CS224N 2025 L9 (Kaplan curves; GPT-3 tokens vs Chinchilla). Original slides; that course is not copied.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan",
                "agenda": [
                    ("1", "Loss as a power of compute"),
                    ("2", "A numeric on L(C)"),
                    ("3", "Chinchilla: tokens with parameters"),
                    ("4", "What a law does not tell you"),
                ],
                "takeaway": "Key goal: write N and D, not only 7B. L is pretraining CE, not chat quality.",
            },
            {
                "layout": "split",
                "title": "A smoother log–log curve",
                "bullets": [
                    r"\(L(C)\approx a C^{-b}+L_\infty\).",
                    "Extra FLOPs still buy loss, with diminishing returns.",
                    "Lab 7 fits a, b, c on toy points. The paper’s range is many decades.",
                ],
                "image": "graphics/7.1-scaling-laws/compute-loss.png",
            },
            {
                "layout": "equation",
                "title": "One hundred times the compute",
                "equation": r"L=2\,C^{-0.15}+1.4",
                "notes": [
                    r"\(C=10^4\): \(L\approx 1.90\).",
                    r"\(C=10^6\): \(L\approx 1.65\). A 100× jump bought 0.25 nats.",
                    r"If you already sit on \(L_\infty\), extra FLOPs buy almost nothing.",
                ],
            },
            {
                "layout": "split",
                "title": "GPT-3 was underfed",
                "bullets": [
                    "GPT-3: 175B parameters, 300B tokens.",
                    r"That is about 1.7 tokens per parameter, not 20.",
                    "A 70B trained with enough tokens beat larger starved nets.",
                ],
                "image": "graphics/7.1-scaling-laws/gpt3-tokens.png",
            },
            {
                "layout": "split",
                "title": "Same FLOPs, different (N, D)",
                "bullets": [
                    r"Training FLOPs scale like \(6ND\).",
                    r"A: \(4N_0\) params, \(D_0/4\) tokens. B: \(N_0\), \(D_0\).",
                    "Chinchilla picks the balanced pair, not the wide starved net.",
                ],
                "image": "graphics/7.1-scaling-laws/chinchilla.png",
            },
            {
                "layout": "cards",
                "title": "What to take from this lecture",
                "cards": [
                    ("Write D", "7B × 20 tokens/param wants 140B tokens."),
                    ("L is not chat", "Alignment, mixture, and eval sit off the curve."),
                    ("Lab 7", "Fit a, b, c. Four noisy points are not a law."),
                ],
            },
        ],
    },
    {
        "stem": "7.2-mixture-of-experts",
        "title": "7.2 Mixture of Experts",
        "slides": [
            {
                "layout": "title",
                "title": "Mixture of Experts",
                "subtitle": "DATA 443/643  ·  Week 7, note 7.2",
                "meta": "Week 7  ·  American University  ·  Ahmad Mousavi",
                "credit": "Ideas from Stanford CS336 2025 L4 (Mixtral: 8 routed, top-2 active). Original slides; that course is not copied.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan",
                "agenda": [
                    ("1", "Router, then k experts"),
                    ("2", "Stored weights versus active FLOPs"),
                    ("3", "Load collapse"),
                    ("4", "When a dense 7B is the better project"),
                ],
                "takeaway": "Key goal: 8 MLPs on disk, 2 in the FLOP count. Say that out loud.",
            },
            {
                "layout": "split",
                "title": "Sparse where the parameters already live",
                "bullets": [
                    "Attention can stay dense. The MLP is the MoE.",
                    "Mixtral is 8 experts, k=2. Switch used k=1.",
                    "DeepSeek’s 256-expert nets wait. This hour is the picture.",
                ],
                "image": "graphics/7.2-mixture-of-experts/moe.png",
            },
            {
                "layout": "equation",
                "title": "Top-k mix",
                "equation": r"y=\sum_{i\in\mathcal{T}(x)} g_i(x)\,E_i(x)",
                "notes": [
                    r"\(\mathcal{T}\) is the k selected experts.",
                    "Renormalize the two gates so they sum to 1.",
                    "If every token has the same logits, you trained two MLPs.",
                ],
            },
            {
                "layout": "split",
                "title": "Collapse is a dense net in disguise",
                "bullets": [
                    "32 tokens, k=2: 64 slots. Uniform load is 8 per expert.",
                    "If two experts eat 43 slots, six experts are cold.",
                    "Load-balancing tries to stop that. Token drop is the other knob.",
                ],
                "image": "graphics/7.2-mixture-of-experts/moe-collapse.png",
            },
            {
                "layout": "compare",
                "title": "What you actually ship",
                "left_title": "Dense 7B",
                "left": "One weight file, a dense GEMM, simple batching.",
                "right_title": "Mixtral-style 8×",
                "right": "Eight MLP shards in RAM even if two run. Tokens in one sequence may disagree on the expert.",
            },
            {
                "layout": "cards",
                "title": "What to take from this lecture",
                "cards": [
                    ("Stored ≠ active", "8× MLP weights, ~2× MLP FLOPs."),
                    ("Router", "If it always picks expert 2, you trained one expert."),
                    ("Lab 7", "Scaling fit and INT8, not an MoE train."),
                ],
            },
        ],
    },
    {
        "stem": "7.3-efficiency-deploy",
        "title": "7.3 Compression and Deployment",
        "slides": [
            {
                "layout": "title",
                "title": "Compression and Deployment",
                "subtitle": "DATA 443/643  ·  Week 7, note 7.3",
                "meta": "Week 7  ·  American University  ·  Ahmad Mousavi",
                "credit": "Ideas from Stanford CS224N 2025 L11 (prune / PEFT as deploy moves). Original slides; that course is not copied.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan",
                "agenda": [
                    ("1", "Prune, quantize, distill"),
                    ("2", "Affine INT8 with a zero-point"),
                    ("3", "Speculative decoding"),
                    ("4", "What to report"),
                ],
                "takeaway": "Key goal: bits and tokens/s versus fp16, on the same eval, not only perplexity.",
            },
            {
                "layout": "bullets",
                "title": "First time: four deployment methods",
                "bullets": [
                    "What. Prune zeros weights. Quantize uses fewer bits. Distill trains a smaller student. Speculate drafts then verifies.",
                    r"Why. 7B in fp16 is \(\approx 14\) GB. Serving is memory and tokens/s, not only loss.",
                    r"How. Affine INT8: \(x\approx s(q-z)\). Speculative accept if \(p_{\mathrm{target}}(x)\ge p_{\mathrm{draft}}(x)\).",
                    "Tradeoffs. + Fits RAM, faster decode. − Outliers blow the scale; a rejected draft wasted the small model.",
                ],
            },
            {
                "layout": "split",
                "title": "A pipeline, not a slogan",
                "bullets": [
                    "Prune: zeros or dropped heads. Needs recovery training.",
                    "Quantize: fewer bits. Distill: a smaller student.",
                    "LoRA is a small Δ, not pruning. Algebra is note 8.3.",
                ],
                "image": "graphics/7.3-efficiency-deploy/compress.png",
            },
            {
                "layout": "equation",
                "title": "Scale and zero-point",
                "equation": r"x\approx s\,(q-z),\quad q\in\{0,\ldots,2^b-1\}",
                "notes": [
                    r"On \([-1,1]\), \(b=8\): \(s=2/255\), \(z=128\).",
                    "Drop z and you cannot represent negatives.",
                    "One activation outlier blows the scale. Lab 7 shows the MSE jump.",
                ],
            },
            {
                "layout": "split",
                "title": "Write the INT8 table",
                "bullets": [
                    r"\(q=128\mapsto 0\). \(q=255\mapsto\approx 0.996\).",
                    "7B fp16 is about 14 GB. INT4 weights about 3.5 GB plus overhead.",
                    "Same architecture. Different bits.",
                ],
                "image": "graphics/7.3-efficiency-deploy/int8-numeric.png",
            },
            {
                "layout": "split",
                "title": "Draft, then verify",
                "bullets": [
                    "A cheap model proposes several tokens.",
                    "The target checks them in one parallel pass.",
                    "Reject at the first mismatch; resample from the target. The distribution does not change.",
                ],
                "image": "graphics/7.3-efficiency-deploy/speculative.png",
            },
            {
                "layout": "cards",
                "title": "What to take from this lecture",
                "cards": [
                    ("Need z", "Centered maps still go negative."),
                    ("Speculate ≠ distill", "Extra small forwards to save large ones."),
                    ("Report", "Bits, layers, tokens/s, and the same downstream number."),
                ],
            },
        ],
    },
    {
        "stem": "8.1-sft-instructions",
        "title": "8.1 Supervised Fine-Tuning and Instruction Data",
        "slides": [
            {
                "layout": "title",
                "title": "Supervised Fine-Tuning",
                "subtitle": "DATA 443/643  ·  Week 8, note 8.1",
                "meta": "Week 8  ·  American University  ·  Ahmad Mousavi",
                "credit": "Ideas from Stanford CS224N 2025 L10 (instruction finetuning as InstructGPT stage 1). Original slides; that course is not copied.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan",
                "agenda": [
                    ("1", "Pretrain next-token, then follow a request"),
                    ("2", "Mask the prompt"),
                    ("3", "Quality beats noisy volume"),
                    ("4", "The template is part of the method"),
                ],
                "takeaway": "Key goal: SFT copies answers. Preferences are Week 9.",
            },
            {
                "layout": "split",
                "title": "Same transformer, different data",
                "bullets": [
                    "The base model already scores every continuation.",
                    "Instruction fine-tuning is the first InstructGPT stage.",
                    "Alpaca and Vicuna are this stage with public pairs.",
                ],
                "image": "graphics/8.1-sft-instructions/sft.png",
            },
            {
                "layout": "split",
                "title": "A row you would imitate",
                "bullets": [
                    "Not a Wikipedia paragraph.",
                    "A task plus an answer you would accept.",
                    "System prompts and schemas live in the prompt, not a new net.",
                ],
                "image": "graphics/8.1-sft-instructions/pair.png",
            },
            {
                "layout": "split",
                "title": "Zeros on the user",
                "bullets": [
                    "Forward the prompt. Zero those positions in the loss.",
                    "Otherwise the model spends gradient on imitating the user.",
                    "Ten-token answers and 400-token answers are different datasets.",
                ],
                "image": "graphics/8.1-sft-instructions/sft-mask.png",
            },
            {
                "layout": "compare",
                "title": "What should dominate the first run",
                "left_title": "80 clean medical pairs",
                "left": "Lead. Every response token is a label you want.",
                "right_title": "80,000 noisy threads",
                "right": "Token average lets the forum win 10:1. Filter or down-weight.",
            },
            {
                "layout": "cards",
                "title": "What to take from this lecture",
                "cards": [
                    ("Mask", "Loss on Tr response tokens, not Tp + Tr."),
                    ("Template", "Train and eval with the same roles."),
                    ("Not RLHF", "SFT copies. Chosen-versus-rejected is Week 9."),
                ],
            },
        ],
    },
    {
        "stem": "8.2-continual-forgetting",
        "title": "8.2 Continual Learning and Forgetting",
        "slides": [
            {
                "layout": "title",
                "title": "Continual Learning and Forgetting",
                "subtitle": "DATA 443/643  ·  Week 8, note 8.2",
                "meta": "Week 8  ·  American University  ·  Ahmad Mousavi",
                "credit": "Ideas from Stanford CS224N 2025 L11 (a full Δ is another copy of W) plus the XOR-then-AND lab. Original slides; that course is not copied.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan",
                "agenda": [
                    ("1", "Task B walks off task A"),
                    ("2", "Measure A while you train B"),
                    ("3", "Replay still moves W"),
                    ("4", "Freeze W, train an adapter"),
                ],
                "takeaway": "Key goal: forgetting is A vs B, not train vs test on one task.",
            },
            {
                "layout": "split",
                "title": "A shared W cannot sit at two minima",
                "bullets": [
                    "XOR then AND on the same hidden layer is Lab 8.",
                    "In an LLM the old task is code, languages, refusal style.",
                    "If you only report B, you did not look.",
                ],
                "image": "graphics/8.2-continual-forgetting/forget.png",
            },
            {
                "layout": "split",
                "title": "Replay keeps a component of A",
                "bullets": [
                    "Mix A rows into B batches, or sample the old model.",
                    "50/50 is the simplest buffer.",
                    "Replay still updates W. That is not LoRA.",
                ],
                "image": "graphics/8.2-continual-forgetting/replay.png",
            },
            {
                "layout": "compare",
                "title": "Does W move?",
                "left_title": "Replay / EWC",
                "left": "Yes. You still need A data (or a Fisher sketch).",
                "right_title": "Frozen LoRA",
                "right": "No. XOR accuracy on the frozen net cannot move. That is why PEFT exists.",
            },
            {
                "layout": "cards",
                "title": "What to take from this lecture",
                "cards": [
                    ("Plot A", "Held-out A every k steps of B."),
                    ("Name it", "Overfitting is one task. Forgetting is two."),
                    ("Lab 8", "XOR collapses toward AND unless you replay or freeze."),
                ],
            },
        ],
    },
    {
        "stem": "8.3-lora-adapters",
        "title": "8.3 LoRA, Adapters, and Federated Updates",
        "slides": [
            {
                "layout": "title",
                "title": "LoRA and Adapters",
                "subtitle": "DATA 443/643  ·  Week 8, note 8.3",
                "meta": "Week 8  ·  American University  ·  Ahmad Mousavi",
                "credit": "Ideas from Stanford CS224N 2025 L11 (LoRA: BA, merge, swap, no extra decode latency). Original slides; that course is not copied.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan",
                "agenda": [
                    ("1", "W + (α/r) BA"),
                    ("2", "r(d+k) versus dk"),
                    ("3", "Init B = 0, then merge or swap"),
                    ("4", "Ship adapters, not documents"),
                ],
                "takeaway": "Key goal: one adapter per skill so XOR never has to move.",
            },
            {
                "layout": "split",
                "title": "Freeze W, train a thin pair",
                "bullets": [
                    r"\(A\in\mathbb{R}^{r\times k}\), \(B\in\mathbb{R}^{d\times r}\), \(r\ll\min(d,k)\).",
                    "Usual inserts: attention projections and MLP maps.",
                    "QLoRA quantizes W to 4-bit and still trains float adapters.",
                ],
                "image": "graphics/8.3-lora-adapters/lora.png",
            },
            {
                "layout": "equation",
                "title": "The forward map",
                "equation": r"h=Wx+\frac{\alpha}{r}BAx",
                "notes": [
                    r"Init \(B=0\) so step 0 is the base model.",
                    "Gaussian A, zero B: the first step can still move.",
                    r"Trainable count is \(r(d+k)\), not \(r^2\).",
                ],
            },
            {
                "layout": "split",
                "title": "A 4096 map, rank 8",
                "bullets": [
                    r"Full W: \(4096^2\approx 16.8\) million.",
                    r"LoRA: \(8\times 8192=65{,}536\) (about 0.39%).",
                    "A full GPT-3 copy is 175B extra per task.",
                ],
                "image": "graphics/8.3-lora-adapters/lora-count.png",
            },
            {
                "layout": "split",
                "title": "Merge or keep a file",
                "bullets": [
                    r"Merge \(W\leftarrow W+(\alpha/r)BA\): no extra decode latency.",
                    "Swap: subtract one BA, add another.",
                    "Federated sketch: sites send A,B. Not a privacy proof.",
                ],
                "image": "graphics/8.3-lora-adapters/federated.png",
            },
            {
                "layout": "cards",
                "title": "What to take from this lecture",
                "cards": [
                    ("Count", "r(d+k) per adapted matrix."),
                    ("Init", "Zero B. Both factors zero is a deadlock."),
                    ("Lab 8", "4×4 printout, then XOR-then-AND without moving W."),
                ],
            },
        ],
    },
    {
        "stem": "9.1-preference-rewards",
        "title": "9.1 Preference Data and Reward Models",
        "slides": [
            {
                "layout": "title",
                "title": "Preferences and Reward Models",
                "subtitle": "DATA 443/643  ·  Week 9, note 9.1",
                "meta": "Week 9  ·  American University  ·  Ahmad Mousavi",
                "credit": "Ideas from Stanford CS224N 2025 L10 (Bradley–Terry RM; best-of-n is a baseline). Original slides; that course is not copied.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan",
                "agenda": [
                    ("1", "A pair is an order, not a grade"),
                    ("2", "Logistic loss on the difference"),
                    ("3", "Chance is log 2"),
                    ("4", "Best-of-n uses the RM without PPO"),
                ],
                "takeaway": "Key goal: only Δ enters. r_φ is a fit to your raters, not “helpfulness.”",
            },
            {
                "layout": "split",
                "title": "Chosen versus rejected",
                "bullets": [
                    r"Label: \(y_w \succ y_l\) given prompt \(x\).",
                    "Both can be fluent. One is better for the rater.",
                    "If both are wrong, the RM still learns a relative order.",
                ],
                "image": "graphics/9.1-preference-rewards/pair.png",
            },
            {
                "layout": "equation",
                "title": "Bradley–Terry on a pair",
                "equation": r"\mathcal{L}=-\log\,\sigma(r_w-r_l)",
                "notes": [
                    r"\(\sigma(0)=1/2\), so chance is \(\log 2\approx 0.693\).",
                    r"Only \(\Delta=r_w-r_l\) enters. Absolute “7/10” does not.",
                    "Initialize the RM from SFT so it already speaks assistant.",
                ],
            },
            {
                "layout": "split",
                "title": "Write the three losses",
                "bullets": [
                    r"\(\Delta=2\): \(\sigma\approx 0.881\), loss \(\approx 0.127\).",
                    r"\(\Delta=-2\): the RM is wrong; loss \(\approx 2.13\).",
                    "Lab 9 should print both the easy pair and a flip.",
                ],
                "image": "graphics/9.1-preference-rewards/rm-numeric.png",
            },
            {
                "layout": "compare",
                "title": "The RM is already useful",
                "left_title": "Best-of-n",
                "left": "Sample n from SFT, return the RM’s favorite. AlpacaFarm: a strong baseline. Extra cost is n forwards, not a PPO loop.",
                "right_title": "PPO (next note)",
                "right": "Trains a new π_θ. Needs on-policy samples. Same RM. Different job.",
            },
            {
                "layout": "cards",
                "title": "What to take from this lecture",
                "cards": [
                    ("Pairs", "An order, not a score out of 100."),
                    ("Held-out", "How often r_w > r_l on pairs the RM did not train on."),
                    ("Not RLHF", "Best-of-n uses the RM. It does not train a policy."),
                ],
            },
        ],
    },
    {
        "stem": "9.2-rlhf",
        "title": "9.2 RLHF",
        "slides": [
            {
                "layout": "title",
                "title": "RLHF",
                "subtitle": "DATA 443/643  ·  Week 9, note 9.2",
                "meta": "Week 9  ·  American University  ·  Ahmad Mousavi",
                "credit": "Ideas from Stanford CS224N 2025 L10 (InstructGPT: SFT, RM, then KL-leashed RL). Original slides; that course is not copied.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan",
                "agenda": [
                    ("1", "Three stages; only the last is RL"),
                    ("2", "A KL leash to SFT"),
                    ("3", "A two-word KL cartoon"),
                    ("4", "Why people look past PPO"),
                ],
                "takeaway": "Key goal: β=0 hacks the RM. π_ref is the SFT model, not the base LM.",
            },
            {
                "layout": "split",
                "title": "SFT, then RM, then a policy update",
                "bullets": [
                    "Stages 1–2 use a fixed dataset.",
                    "Stage 3 needs fresh samples from the current π_θ.",
                    "InstructGPT scaled this stack.",
                ],
                "image": "graphics/9.2-rlhf/loop.png",
            },
            {
                "layout": "equation",
                "title": "Climb reward, stay near SFT",
                "equation": r"J=r_\phi(x,y)-\beta\operatorname{KL}(\pi_\theta\|\pi_{\mathrm{ref}})",
                "notes": [
                    r"\(\pi_{\mathrm{ref}}=\pi_{\mathrm{SFT}}\), frozen.",
                    r"Large \(\beta\) stays near SFT. \(\beta=0\) is no leash.",
                    "You do not derive PPO here. You write the leash.",
                ],
            },
            {
                "layout": "split",
                "title": "A two-word vocab",
                "bullets": [
                    r"\(\pi_{\mathrm{ref}}=(0.7,0.3)\), \(\pi_\theta=(0.99,0.01)\).",
                    r"\(\operatorname{KL}\approx 0.31\).",
                    r"\(\beta=0.1\) subtracts 0.031. \(\beta=0\) subtracts nothing.",
                ],
                "image": "graphics/9.2-rlhf/kl-numeric.png",
            },
            {
                "layout": "compare",
                "title": "Who wins the objective",
                "left_title": "β = 0",
                "left": "Reward rises. KL explodes. Text becomes a caricature of the raters.",
                "right_title": "Large β",
                "right": "The policy barely leaves SFT. You paid for PPO and bought almost nothing.",
            },
            {
                "layout": "cards",
                "title": "What to take from this lecture",
                "cards": [
                    ("On-policy", "Last week’s samples are stale once π_θ moved."),
                    ("Leash", "π_ref is SFT, because the RM was trained on SFT-style answers."),
                    ("Project", "Best-of-n or DPO. Full PPO on an LLM is usually out of scope."),
                ],
            },
        ],
    },
    {
        "stem": "9.3-dpo",
        "title": "9.3 Direct Preference Optimization",
        "slides": [
            {
                "layout": "title",
                "title": "Direct Preference Optimization",
                "subtitle": "DATA 443/643  ·  Week 9, note 9.3",
                "meta": "Week 9  ·  American University  ·  Ahmad Mousavi",
                "credit": "Ideas from Stanford CS224N 2025 L10 (DPO: write r from π; Z(x) cancels). Original slides; that course is not copied.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan",
                "agenda": [
                    ("1", "Skip the RM and the PPO loop"),
                    ("2", "Closed-form r from the policy"),
                    ("3", "Init loss is still log 2"),
                    ("4", "Offline: no new y unless you collect them"),
                ],
                "takeaway": "Key goal: the frozen reference is the leash. Dropping it is not DPO.",
            },
            {
                "layout": "split",
                "title": "Same pairs, shorter stack",
                "bullets": [
                    "The optimal r is a log-ratio plus Z(x).",
                    "Z(x) cancels in a pairwise difference.",
                    "KTO and IPO exist. This hour is DPO.",
                ],
                "image": "graphics/9.3-dpo/dpo.png",
            },
            {
                "layout": "equation",
                "title": "The implicit reward",
                "equation": r"r(x,y)=\beta\,\log\frac{\pi(y\mid x)}{\pi_{\mathrm{ref}}(y\mid x)}",
                "notes": [
                    r"Plug into Bradley–Terry. The \(r\) head disappears.",
                    r"If \(\pi_\theta=\pi_{\mathrm{ref}}\), the argument of \(\sigma\) is 0.",
                    r"Trainable object is \(\pi_\theta\). The reference stays frozen.",
                ],
            },
            {
                "layout": "split",
                "title": "A toy step",
                "bullets": [
                    r"Init: \(\mathcal{L}=\log 2\approx 0.693\).",
                    "Winner log-ratio 0.5, loser −1.0, gap 1.5.",
                    r"\(\sigma(1.5)\approx 0.818\), loss \(\approx 0.201\).",
                ],
                "image": "graphics/9.3-dpo/dpo-init.png",
            },
            {
                "layout": "compare",
                "title": "What the pair file cannot do",
                "left_title": "PPO",
                "left": "Samples new y from the current policy. Can explore replies that were never labeled.",
                "right_title": "Offline DPO",
                "right": "Fixed pairs. If SFT never wrote a good y_w, DPO cannot invent it.",
            },
            {
                "layout": "cards",
                "title": "What to take from this lecture",
                "cards": [
                    ("Init", "σ(0)=1/2 is the start, not a bug."),
                    ("Report", "β, the reference checkpoint, held-out preference accuracy."),
                    ("Lab 9", "Toy logits. Not an LLM PPO run."),
                ],
            },
        ],
    },
    {
        "stem": "10.1-red-teaming",
        "title": "10.1 Red-Teaming and Safety Evaluation",
        "slides": [
            {
                "layout": "title",
                "title": "Safety as a Rate",
                "subtitle": "DATA 443/643  ·  Week 10, note 10.1",
                "meta": "Week 10  ·  American University  ·  Ahmad Mousavi",
                "credit": "Ideas from Stanford CS336 2025 L12 (HarmBench / HELM safety as rates). Original slides; that course is not copied.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan",
                "agenda": [
                    ("1", "A fixed probe list, then a fraction"),
                    ("2", "Split harm from over-refusal"),
                    ("3", "Rerun after the patch"),
                    ("4", "A judge is not a substitute for a sample"),
                ],
                "takeaway": "Key goal: 4/40 is a number you can rerun. A vibe is not.",
            },
            {
                "layout": "split",
                "title": "Probes in, a log out",
                "bullets": [
                    "HarmBench is 510 labeled behaviors.",
                    "AIR-Bench: 314 categories, 5694 prompts. HELM hosts suites.",
                    "In class you use a short public list and instructor categories.",
                ],
                "image": "graphics/10.1-red-teaming/probe.png",
            },
            {
                "layout": "split",
                "title": "Four cells, one rate",
                "bullets": [
                    "10 + 10 + 10 + 10 probes. Fails 0, 1, 2, 1.",
                    r"Overall \(4/40=10\%\). Log the four ids.",
                    "Do not publish working attack strings on the open site.",
                ],
                "image": "graphics/10.1-red-teaming/probe-rates.png",
            },
            {
                "layout": "compare",
                "title": "Two different failures",
                "left_title": "True safety hit",
                "left": "A disallowed or leaky completion. Count it in the harm cell.",
                "right_title": "Over-refusal",
                "right": "“What is ibuprofen used for?” should not refuse. Mixing this into “unsafe %” hides a model that tightened too far.",
            },
            {
                "layout": "compare",
                "title": "Capability versus propensity",
                "left_title": "API model",
                "left": "Refusal rate (propensity) is the number you ship. The user cannot fine-tune the weights.",
                "right_title": "Open-weight",
                "right": "A refusal is not a capability bound. Fine-tuning can move the propensity. Report both.",
            },
            {
                "layout": "cards",
                "title": "What to take from this lecture",
                "cards": [
                    ("Rerun", "Same 40 after DPO. One cell moved is not “done.”"),
                    ("Judge", "Spot-check a 10% sample. Look at the outputs."),
                    ("Not a recipe", "Measurement. No jailbreak how-to in this course."),
                ],
            },
        ],
    },
    {
        "stem": "10.2-editing-unlearning",
        "title": "10.2 Editing and Unlearning",
        "slides": [
            {
                "layout": "title",
                "title": "Editing and Unlearning",
                "subtitle": "DATA 443/643  ·  Week 10, note 10.2",
                "meta": "Week 10  ·  American University  ·  Ahmad Mousavi",
                "credit": "Ideas from CS224N 2025 interpretability and ROME (locate, then write). Original slides; those sources are not copied.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan",
                "agenda": [
                    ("1", "Causal locate, then a rank-one write"),
                    ("2", "Three probes: edit, neighbor, paraphrase"),
                    ("3", "A set is not a key"),
                    ("4", "Retain is the utility cost"),
                ],
                "takeaway": "Key goal: flipping one prompt is not an isolated fact.",
            },
            {
                "layout": "bullets",
                "title": "First time: editing versus unlearning",
                "bullets": [
                    "What. Edit: rewrite one fact. Unlearn: lower a set of behaviors. They are not the same experiment.",
                    "Why. Retraining from scratch is too expensive. Serving a wrong object is a product bug.",
                    r"How. Locate the MLP, then \(W\leftarrow W+uv^{\top}\) so \(W'k_*=v_*\). Unlearn: continue train + retain set.",
                    "Tradeoffs. + Cheap write. − Neighbors leak; paraphrases miss. Retain accuracy is the cost of unlearning.",
                ],
            },
            {
                "layout": "split",
                "title": "Locate, then write",
                "bullets": [
                    "If a component stores the fact, intervening on it should change the object.",
                    "ROME: mid-layer MLP on the last subject token.",
                    "MEMIT spreads the write across several layers.",
                ],
                "image": "graphics/10.2-editing-unlearning/rome.png",
            },
            {
                "layout": "equation",
                "title": "One outer product",
                "equation": r"W'=W+uv^{\top}",
                "notes": [
                    r"Choose \(u,v\) so \(W'k_*=v_*\) and old keys barely move.",
                    "That is one fact, not a topic delete.",
                    r"Toy \(d=4\): a rank-one write is \(d+4d=20\) numbers, not a full fine-tune.",
                ],
            },
            {
                "layout": "split",
                "title": "CounterFact-style columns",
                "bullets": [
                    "Edit 8/10 looks like success.",
                    "Neighbor 2/10: Italy moved. The write leaked.",
                    "Retain 9/10: unrelated facts mostly sat still.",
                ],
                "image": "graphics/10.2-editing-unlearning/edit-probes.png",
            },
            {
                "layout": "compare",
                "title": "A key versus a set",
                "left_title": "Edit",
                "left": "One association. Lab 10: facts[\"paris\"] = \"capital of Germany\". Neighbors must stay.",
                "right_title": "Unlearn",
                "right": "A corpus. Forget-QA 90%→20% is not success if retain-QA 88%→21%.",
            },
            {
                "layout": "cards",
                "title": "What to take from this lecture",
                "cards": [
                    ("Three probes", "Edit, neighbor, paraphrase. One prompt is not a method."),
                    ("Not legal delete", "Verbatim drop can hide latent knowledge."),
                    ("Lab 10", "A dict overwrite is the cartoon, not ROME."),
                ],
            },
        ],
    },
    {
        "stem": "10.3-raft-memory",
        "title": "10.3 RAFT and Memory-Augmented Models",
        "slides": [
            {
                "layout": "title",
                "title": "RAFT and Two Memories",
                "subtitle": "DATA 443/643  ·  Week 10, note 10.3",
                "meta": "Week 10  ·  American University  ·  Ahmad Mousavi",
                "credit": "Ideas from Stanford CS224N 2025 L13 (parametric vs open-book). RAFT is the training twist. Original slides; that course is not copied.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan",
                "agenda": [
                    ("1", "What RAG is, in one page"),
                    ("2", "Train the reader on the test stack"),
                    ("3", "Gold plus distractors"),
                    ("4", "Weights versus an index"),
                ],
                "takeaway": "Key goal: if gold is in the prompt and the answer is still the old salary, that is a reader bug.",
            },
            {
                "layout": "split",
                "title": "What RAG is  (you need this before RAFT)",
                "bullets": [
                    "Look up passages from a collection you control, put them in the prompt, generate from them.",
                    "The generator is usually frozen. Edit a PDF and re-index; do not retrain.",
                    "Week 14.1 is the full first-time lecture. This hour trains the reader.",
                ],
                "image": "graphics/14.1-rag-pipeline/rag.png",
            },
            {
                "layout": "split",
                "title": "SFT on the bundle",
                "bullets": [
                    "Parametric recall versus open-book.",
                    "RAFT: question + snippets + an answer that cites or ignores.",
                    "Still SFT. The labels are answers given the bundle.",
                ],
                "image": "graphics/10.3-raft-memory/raft.png",
            },
            {
                "layout": "split",
                "title": "A late-policy question",
                "bullets": [
                    "Overlap 5, 1, 1, 4. Top-3: gold, old, exam.",
                    "Target: cite snippet 1, skip snippet 4.",
                    "If you only ever trained with gold alone, junk wins.",
                ],
                "image": "graphics/10.3-raft-memory/overlap-retrieve.png",
            },
            {
                "layout": "compare",
                "title": "Two stores",
                "left_title": "Parametric",
                "left": "Weights. Fast, always on, hard to update. ROME and SFT live here.",
                "right_title": "Non-parametric",
                "right": "A PDF you can edit, then re-index. Prefer this if the number moves every month.",
            },
            {
                "layout": "compare",
                "title": "Whose bug was that",
                "left_title": "Retrieval",
                "left": "Gold ranked 3rd and k=2. The reader never saw it. Raise k or fix chunking.",
                "right_title": "Reader",
                "right": "Gold is in the prompt; the model recites the pretrain snapshot. That is RAFT’s job. Week 14 is the full stack.",
            },
            {
                "layout": "cards",
                "title": "What to take from this lecture",
                "cards": [
                    ("Distractors", "Gold-only training never practices skip."),
                    ("Two writes", "A salary in a PDF is not a ROME write."),
                    ("Lab 10", "Token-overlap retrieve, then overwrite one dict key."),
                ],
            },
        ],
    },
    {
        "stem": "11.1-gan-idea",
        "title": "11.1 Generative Adversarial Nets",
        "slides": [
            {
                "layout": "title",
                "title": "Generative Adversarial Nets",
                "subtitle": "DATA 443/643  ·  Week 11, note 11.1",
                "meta": "Week 11  ·  American University  ·  Ahmad Mousavi",
                "credit": "Ideas from Stanford CS231N 2025 L13 (give up on p(x); sample in one pass). Original slides; that course is not copied.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan",
                "agenda": [
                    ("1", "G maps z to a fake. D scores real vs fake."),
                    ("2", "No likelihood, only a sampler"),
                    ("3", "Bayes D when G parks on one spike"),
                    ("4", "One pretty sample is not a trained G"),
                ],
                "takeaway": "Key goal: G is a distribution. D is a moving classifier.",
            },
            {
                "layout": "split",
                "title": "Two players, one sample",
                "bullets": [
                    r"\(z\sim\mathcal{N}(0,I)\). \(x=G(z)\).",
                    "D never sees z. G never sees a real x on its own update.",
                    "Implicit density, direct sample.",
                ],
                "image": "graphics/11.1-gan-idea/players.png",
            },
            {
                "layout": "equation",
                "title": "The optimal discriminator",
                "equation": r"D^*(x)=\frac{p_r(x)}{p_r(x)+p_g(x)}",
                "notes": [
                    r"If \(p_g=p_r\), \(D^*=1/2\) on every \(x\).",
                    "If G never visits a mode, D is 1 there and G never hears about it.",
                    "You cannot read p(x) off a trained GAN.",
                ],
            },
            {
                "layout": "split",
                "title": "Two spikes, G parked on +2",
                "bullets": [
                    r"Reals: half at \(-2\), half at \(+2\).",
                    r"Bayes \(D(+2)=0.5\). \(D(-2)=1\).",
                    "A coin flip at +2 is not coverage of the mixture.",
                ],
                "image": "graphics/11.1-gan-idea/d-bayes.png",
            },
            {
                "layout": "compare",
                "title": "What you can and cannot do",
                "left_title": "A GAN",
                "left": "Draw a fake in one forward pass. No p(x), no p(z|x), no test log-likelihood.",
                "right_title": "Week 12 diffusion",
                "right": "An explicit noise schedule. T reverse steps. You still sample; you also have a regression loss.",
            },
            {
                "layout": "cards",
                "title": "What to take from this lecture",
                "cards": [
                    ("Sampler", "G is not an autoencoder. The only teacher is D’s scalar."),
                    ("Moving D", "Yesterday’s perfect D scores a different G today."),
                    ("Lab 11", "8-D noise → 2-D point. Two Gaussians, not faces."),
                ],
            },
        ],
    },
    {
        "stem": "11.2-gan-training",
        "title": "11.2 Training Dynamics",
        "slides": [
            {
                "layout": "title",
                "title": "The Min-Max Loop",
                "subtitle": "DATA 443/643  ·  Week 11, note 11.2",
                "meta": "Week 11  ·  American University  ·  Ahmad Mousavi",
                "credit": "Ideas from Stanford CS231N 2025 L13 (minimax; alternate D then G). Original slides; that course is not copied.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan",
                "agenda": [
                    ("1", "Write J. Circle that G is only in the fake term."),
                    ("2", "One D step, one G step"),
                    ("3", "Non-saturating −log D(G(z))"),
                    ("4", "A falling G loss is not better pictures"),
                ],
                "takeaway": "Key goal: a 99% D is often a dead G.",
            },
            {
                "layout": "split",
                "title": "Keep the two losses in tension",
                "bullets": [
                    "Train D on reals=1 and fakes=0. Freeze G.",
                    "Train G with labels=1. Freeze D. You want D wrong.",
                    "Detach fakes on the D step. One shared backward is a bug.",
                ],
                "image": "graphics/11.2-gan-training/dynamics.png",
            },
            {
                "layout": "equation",
                "title": "Who wants J large",
                "equation": r"J=\mathbb{E}[\log D(x)]+\mathbb{E}[\log(1-D(G(z)))]",
                "notes": [
                    "D maximizes J. G minimizes J.",
                    "G does not appear in the real term.",
                    r"Nash hope: \(p_g=p_r\) and \(D=1/2\). Training does not promise it.",
                ],
            },
            {
                "layout": "split",
                "title": "One real, one fake",
                "bullets": [
                    r"\(D(x)=0.9\), \(D(G(z))=0.2\): \(J\approx -0.328\).",
                    r"At \(D(G)=0.01\), \(\log(1-D)\approx -0.010\) is flat.",
                    r"\(-\log D\approx 4.605\) still has slope. Lab 11 feeds ones into BCE.",
                ],
                "image": "graphics/11.2-gan-training/j-numeric.png",
            },
            {
                "layout": "compare",
                "title": "Two generator losses",
                "left_title": "Saturating",
                "left": "Minimize log(1−D(G(z))). Early on, D is sharp and the slope dies.",
                "right_title": "Non-saturating",
                "right": "Maximize log D(G(z)). Same game, usable gradient. That is the lab default.",
            },
            {
                "layout": "cards",
                "title": "What to take from this lecture",
                "cards": [
                    ("Two phases", "Only θ_d, then only θ_g. Not one joint backward."),
                    ("Do not rank", "A small G loss can mean D collapsed."),
                    ("Lab 11", "400 steps. Print both losses. Then look at the scatter."),
                ],
            },
        ],
    },
    {
        "stem": "11.3-mode-collapse",
        "title": "11.3 Mode Collapse and Evaluation",
        "slides": [
            {
                "layout": "title",
                "title": "Coverage, Not One Fake",
                "subtitle": "DATA 443/643  ·  Week 11, note 11.3",
                "meta": "Week 11  ·  American University  ·  Ahmad Mousavi",
                "credit": "Ideas from Stanford CS231N 2025 L13 (implicit samples; you still need coverage). Original slides; that course is not copied.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan",
                "agenda": [
                    ("1", "D only fights the support of G"),
                    ("2", "Fidelity versus coverage"),
                    ("3", "92/8 is collapse; 47/53 is covered"),
                    ("4", "Write the check before you train"),
                ],
                "takeaway": "Key goal: sharp and identical is collapse, not success.",
            },
            {
                "layout": "split",
                "title": "One mode is enough to fool D",
                "bullets": [
                    "G parks on cluster A. D learns B is real.",
                    "G may jump to B, or never leave A.",
                    "Modes G never visits do not appear in G’s loss.",
                ],
                "image": "graphics/11.3-mode-collapse/collapse.png",
            },
            {
                "layout": "split",
                "title": "Two seeds, same architecture",
                "bullets": [
                    "100 fakes. Nearest-mean bins.",
                    "92 / 8: the 8% bin is under 10%. Collapse.",
                    "47 / 53: write covered. Report both fractions.",
                ],
                "image": "graphics/11.3-mode-collapse/coverage-bins.png",
            },
            {
                "layout": "compare",
                "title": "Two questions",
                "left_title": "Fidelity",
                "left": "Does this fake look real? A grid of images. Precision.",
                "right_title": "Coverage",
                "right": "Did we hit the real support? Recall. FID is a proxy with a large sample.",
            },
            {
                "layout": "compare",
                "title": "Why text-to-image moved",
                "left_title": "GAN",
                "left": "One forward pass. Fast. Collapse is the usual failure.",
                "right_title": "Diffusion (Week 12)",
                "right": "T reverse steps. Slower. Usually covers better. The coverage lesson does not move.",
            },
            {
                "layout": "cards",
                "title": "What to take from this lecture",
                "cards": [
                    ("Bin rule", "Either mode under 10% of 100 fakes: collapse."),
                    ("Loss is silent", "G’s loss has no term for a missing cluster."),
                    ("Lab 11", "Print the two percentages, not only lossG."),
                ],
            },
        ],
    },
    {
        "stem": "12.1-diffusion-forward",
        "title": "12.1 The Forward Process",
        "slides": [
            {
                "layout": "title",
                "title": "The Forward Process",
                "subtitle": "DATA 443/643  ·  Week 12, note 12.1",
                "meta": "Week 12  ·  American University  ·  Ahmad Mousavi",
                "credit": "Ideas from Stanford CS231N 2025 L14 (corrupt x; jump to x_t in one shot). Original slides; that course is not copied.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan",
                "agenda": [
                    ("1", "A fixed kernel. No discriminator."),
                    ("2", "α_t and α-bar_t"),
                    ("3", "The one-line reparameterization"),
                    ("4", "Print α-bar at 1, T/2, T"),
                ],
                "takeaway": "Key goal: training samples t and jumps. You do not walk 1…t.",
            },
            {
                "layout": "split",
                "title": "Destroy the sample on purpose",
                "bullets": [
                    r"\(\alpha_t=1-\beta_t\), \(\bar{\alpha}_t=\prod_{s=1}^t \alpha_s\).",
                    r"Markov: \(q(x_t\mid x_{t-1})=\mathcal{N}(\sqrt{\alpha_t}\,x_{t-1},\beta_t I)\).",
                    "The forward process is not learned.",
                ],
                "image": "graphics/12.1-diffusion-forward/forward.png",
            },
            {
                "layout": "equation",
                "title": "Closed form, one Gaussian",
                "equation": r"x_t=\sqrt{\bar{\alpha}_t}\,x_0+\sqrt{1-\bar{\alpha}_t}\,\varepsilon",
                "notes": [
                    r"\(\varepsilon\sim\mathcal{N}(0,I)\).",
                    r"\(\bar{\alpha}_t=1\) keeps \(x_0\). Zero keeps \(\varepsilon\).",
                    "That one-liner is the whole point of this note.",
                ],
            },
            {
                "layout": "split",
                "title": "A scalar path",
                "bullets": [
                    r"\(x_0=1\), \(\varepsilon=2\).",
                    r"At \(\bar{\alpha}=0.64\), \(x_t=2.0\): more noise than signal.",
                    "Lab 12: same square roots on a 2-D vector.",
                ],
                "image": "graphics/12.1-diffusion-forward/alphabar.png",
            },
            {
                "layout": "compare",
                "title": "Do not simulate the chain at train time",
                "left_title": "Markov loop",
                "left": "Walk t hops of q(x_s | x_{s-1}). Slow, and unnecessary for the loss.",
                "right_title": "Jump",
                "right": "Sample t, draw ε, form x_t. Noise levels, then learn to undo a bit.",
            },
            {
                "layout": "cards",
                "title": "What to take from this lecture",
                "cards": [
                    ("Three names", "β_t, α_t, α-bar_t. Write them every time."),
                    ("Too fast", "Every β=0.9: early t is already junk."),
                    ("Lab 12", "Print α-bar at 1, T/2, T. They should fall."),
                ],
            },
        ],
    },
    {
        "stem": "12.2-diffusion-reverse",
        "title": "12.2 The Reverse Process",
        "slides": [
            {
                "layout": "title",
                "title": "Learn to Denoise",
                "subtitle": "DATA 443/643  ·  Week 12, note 12.2",
                "meta": "Week 12  ·  American University  ·  Ahmad Mousavi",
                "credit": "Ideas from Stanford CS231N 2025 L14 (predict the noise; T reverse steps). Original slides; that course is not copied.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan",
                "agenda": [
                    ("1", "MSE on ε, not an adversary"),
                    ("2", "One reverse-step mean"),
                    ("3", "Oracle: true ε peels back to x_0"),
                    ("4", "T net calls versus one GAN pass"),
                ],
                "takeaway": "Key goal: the net predicts the noise you added in 12.1.",
            },
            {
                "layout": "split",
                "title": "Ordinary regression",
                "bullets": [
                    r"Sample t, form \(x_t\), guess \(\varepsilon\).",
                    r"Predicting \(\varepsilon\) is equivalent (up to scale) to \(x_0\) or the score.",
                    "t is an input. The same x_t is a different problem at t=10 and t=900.",
                ],
                "image": "graphics/12.2-diffusion-reverse/reverse.png",
            },
            {
                "layout": "equation",
                "title": "DDPM training loss",
                "equation": r"\mathcal{L}=\|\varepsilon-\varepsilon_\theta(x_t,t)\|^2",
                "notes": [
                    "No discriminator. A known target.",
                    "Sampling still walks t = T … 1.",
                    "Lab 12 uses the true posterior mean. You know x_0.",
                ],
            },
            {
                "layout": "split",
                "title": "Reuse x_t = 2.0 from 12.1",
                "bullets": [
                    r"\(\alpha_t=\bar{\alpha}_t=0.64\), \(\varepsilon_\theta=2\).",
                    "The reverse mean lands on x_0 = 1.0.",
                    r"If \(\varepsilon_\theta=0\), you mostly rescale \(x_t\). Not a sample.",
                ],
                "image": "graphics/12.2-diffusion-reverse/reverse-mean.png",
            },
            {
                "layout": "compare",
                "title": "The trade",
                "left_title": "GAN (Week 11)",
                "left": "One forward pass. Min-max. Collapse is the usual failure.",
                "right_title": "DDPM",
                "right": "T network calls (or fewer with DDIM). Report the sampler next to the metric.",
            },
            {
                "layout": "cards",
                "title": "What to take from this lecture",
                "cards": [
                    ("Oracle", "Lab 12 does not train a U-Net. It uses the known x_0."),
                    ("Noise on the way down", "Drop σ_t z and every sample looks the same."),
                    ("Report T", "Changing T at test time is part of the method."),
                ],
            },
        ],
    },
    {
        "stem": "12.3-latent-conditioning",
        "title": "12.3 Latent Diffusion and Text Conditioning",
        "slides": [
            {
                "layout": "title",
                "title": "Latents and Text",
                "subtitle": "DATA 443/643  ·  Week 12, note 12.3",
                "meta": "Week 12  ·  American University  ·  Ahmad Mousavi",
                "credit": "Ideas from Stanford CS231N 2025 L14 (LDM D=8, C=16; CFG). Original slides; that course is not copied.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan",
                "agenda": [
                    ("1", "Denoise a VAE latent, not pixels"),
                    ("2", "CLIP’s text tower as c"),
                    ("3", "Classifier-free guidance"),
                    ("4", "s=1 is still conditional"),
                ],
                "takeaway": "Key goal: report s, a prompt-alignment score, and a failure case.",
            },
            {
                "layout": "split",
                "title": "Compress, denoise, decode",
                "bullets": [
                    "Encoder frozen. UNet on z. Decoder back to pixels.",
                    "A modern LDM stacks VAE + GAN + diffusion.",
                    "DiT exists. This hour is the VAE latent picture.",
                ],
                "image": "graphics/12.3-latent-conditioning/ldm.png",
            },
            {
                "layout": "split",
                "title": "Count the cells",
                "bullets": [
                    r"\(256\times 256\times 3\) vs \(32\times 32\times 16\) (\(D=8\), \(C=16\)).",
                    "About 12× fewer numbers per reverse step.",
                    r"Stable Diffusion’s public recipe is \(64\times 64\times 4\) on \(512^2\): about \(48\times\) fewer.",
                ],
                "image": "graphics/12.3-latent-conditioning/latent-count.png",
            },
            {
                "layout": "equation",
                "title": "Classifier-free guidance",
                "equation": r"\hat{\varepsilon}=\varepsilon_u+s(\varepsilon_c-\varepsilon_u)",
                "notes": [
                    "Train by randomly dropping the text. One net, two calls.",
                    r"\(s=1\) is the conditional prediction. Not “no text.”",
                    r"\(s>1\) extrapolates. Variety usually drops.",
                ],
            },
            {
                "layout": "split",
                "title": "A scalar CFG",
                "bullets": [
                    r"\(\varepsilon_u=0.8\), \(\varepsilon_c=0.2\).",
                    r"\(s=1\to 0.2\). \(s=3\to -1.0\). \(s=7.5\to -3.7\).",
                    "CLIP’s image tower scores pairs. Sampling needs the text tower.",
                ],
                "image": "graphics/12.3-latent-conditioning/cfg-scale.png",
            },
            {
                "layout": "cards",
                "title": "What to take from this lecture",
                "cards": [
                    ("Two calls", "Empty prompt and text. Then mix with s."),
                    ("Measure", "CLIP cosine vs the prompt, plus a wrong-count failure."),
                    ("Lab 12", "Still 2-D denoising. No U-Net."),
                ],
            },
        ],
    },
    {
        "stem": "13.1-chain-of-thought",
        "title": "13.1 Chain-of-Thought",
        "slides": [
            {
                "layout": "title",
                "title": "Steps Before the Answer",
                "subtitle": "DATA 443/643  ·  Week 13, note 13.1",
                "meta": "Week 13  ·  American University  ·  Ahmad Mousavi",
                "credit": "Ideas from Stanford CS224N 2026 L12 (CoT is extra tokens). Original slides; that course is not copied.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan",
                "agenda": [
                    ("1", "A prompt, not a new architecture"),
                    ("2", "Tokens as scratch paper"),
                    ("3", "17 × 24 in three lines"),
                    ("4", "When extra decode hurts"),
                ],
                "takeaway": "Key goal: CoT is a decoding choice. Report the prompt and the box.",
            },
            {
                "layout": "split",
                "title": "Ask for work, then the number",
                "bullets": [
                    "Direct: “What is 17 × 24?” CoT: “Show your work.”",
                    "The weights do not change. The tape gets longer.",
                    "Few-shot traces must match the test task.",
                ],
                "image": "graphics/13.1-chain-of-thought/cot.png",
            },
            {
                "layout": "equation",
                "title": "Partial products on the tape",
                "equation": r"17\times 24=10\times 24+7\times 24=240+168=408",
                "notes": [
                    "Three lines hold 240, 168, then 408.",
                    "Direct decode has no place to put the 240.",
                    "Lab 13 uses the same algebra on 23+19.",
                ],
            },
            {
                "layout": "split",
                "title": "A tape you can inspect",
                "bullets": [
                    "Gold is 408. This trace is also faithful (13.3).",
                    "A one-hop lookup does not need hops. Extra steps wander.",
                    "Freeze temperature and max tokens in the report.",
                ],
                "image": "graphics/13.1-chain-of-thought/cot-partial.png",
            },
            {
                "layout": "compare",
                "title": "When the extra tokens help",
                "left_title": "Single lookup",
                "left": "Capital of France. A story about Lyon is extra risk, not extra reasoning.",
                "right_title": "Multi-hop",
                "right": "Dependent arithmetic, a plan, then a box. Intermediate tokens store the hops.",
            },
            {
                "layout": "cards",
                "title": "What to take from this lecture",
                "cards": [
                    ("Not a fine-tune", "Unless you trained on traces, CoT is a prompt."),
                    ("Two numbers", "Answer accuracy, and a trace check in 13.3."),
                    ("Lab 13", "Constructed strings. No LLM API."),
                ],
            },
        ],
    },
    {
        "stem": "13.2-self-consistency-tot",
        "title": "13.2 Self-Consistency and Tree-of-Thoughts",
        "slides": [
            {
                "layout": "title",
                "title": "Vote, or Search a Tree",
                "subtitle": "DATA 443/643  ·  Week 13, note 13.2",
                "meta": "Week 13  ·  American University  ·  Ahmad Mousavi",
                "credit": "Ideas from Stanford CS224N 2026 L12 (SC +17.9 pp GSM8K). Original slides; that course is not copied.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan",
                "agenda": [
                    ("1", "k traces, majority on the parsed answer"),
                    ("2", "Wang et al.: +17.9 pp on GSM8K"),
                    ("3", "ToT scores partial nodes"),
                    ("4", "A shared bug still wins the vote"),
                ],
                "takeaway": "Key goal: vote on answers. k=1 is greedy CoT.",
            },
            {
                "layout": "split",
                "title": "Test-time compute as k forwards",
                "bullets": [
                    r"Temperature \(>0\). Parse each box. Majority.",
                    "Extra tokens are extra compute. SC spends k of them.",
                    "Do not assign DeepSeek-R1 / GRPO as homework.",
                ],
                "image": "graphics/13.2-self-consistency-tot/tree.png",
            },
            {
                "layout": "equation",
                "title": "Majority on the parsed answer",
                "equation": r"\hat{a}=\operatorname{argmax}_{a}\,|\{i:\operatorname{parse}(y_i)=a\}|",
                "notes": [
                    "Vote on the number, not on the wording of the steps.",
                    r"Tie-break is a method choice. Write it down.",
                    r"Temperature 0 makes all \(k\) traces the same.",
                ],
            },
            {
                "layout": "split",
                "title": "Lab 13 numbers, then GSM8K",
                "bullets": [
                    "23+19: answers 42, 32, 42. Majority 42.",
                    r"\(k=1\) on B scores 32 and misses.",
                    "Wang et al.: +17.9 pp vs greedy CoT.",
                ],
                "image": "graphics/13.2-self-consistency-tot/sc-vote.png",
            },
            {
                "layout": "compare",
                "title": "Two ways to spend the budget",
                "left_title": "Self-consistency",
                "left": "i.i.d. full traces. Vote. Shared formula bugs survive.",
                "right_title": "Tree-of-Thoughts",
                "right": "Expand partial thoughts, score, prune. ReAct (Week 14) calls a tool instead.",
            },
            {
                "layout": "cards",
                "title": "What to take from this lecture",
                "cards": [
                    ("Plot k", "Accuracy vs k, plus greedy CoT at k=1."),
                    ("GSM8K punch", "+17.9 pp is a lift, not a proof of faithful steps."),
                    ("Lab 13", "Vote on constructed answers. Then flag 13.3."),
                ],
            },
        ],
    },
    {
        "stem": "13.3-faithfulness",
        "title": "13.3 Faithfulness of Explanations",
        "slides": [
            {
                "layout": "title",
                "title": "Correct Box, Invented Steps",
                "subtitle": "DATA 443/643  ·  Week 13, note 13.3",
                "meta": "Week 13  ·  American University  ·  Ahmad Mousavi",
                "credit": "Ideas from CS224N 2026 L12–L13 (unfaithful CoT; process vs outcome). Original slides; that course is not copied.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan",
                "agenda": [
                    ("1", "Process vs outcome"),
                    ("2", "Chen et al.: CoT need not match the hint used"),
                    ("3", "52 in the steps, 42 in the box"),
                    ("4", "Checker pass rate among wins"),
                ],
                "takeaway": "Key goal: accuracy +1 can still be faithfulness 0.",
            },
            {
                "layout": "split",
                "title": "Two different claims",
                "bullets": [
                    "Outcome: the box matches gold.",
                    "Process: the written steps compute that box, validly.",
                    "Lightman et al.: a process reward scores steps, not only the box.",
                ],
                "image": "graphics/13.3-faithfulness/unfaithful.png",
            },
            {
                "layout": "equation",
                "title": "Faithfulness among correct boxes",
                "equation": r"F=\frac{n_{m}}{n_{w}}",
                "notes": [
                    r"\(n_{w}\): right box. \(n_{m}\): steps also match the box.",
                    "Not a claim about inner states. We do not read residuals.",
                    "A majority of 42 can still be three lucky wins.",
                ],
            },
            {
                "layout": "split",
                "title": "Lab 13’s lucky win",
                "bullets": [
                    r"Steps: \(23+10=33\), \(33+9=52\). Box: 42. Gold: 42.",
                    "Last integer in steps is 52. Unfaithful. Lucky win.",
                    "Chen et al. 2025: models can use a hint they never write.",
                ],
                "image": "graphics/13.3-faithfulness/lucky-win.png",
            },
            {
                "layout": "compare",
                "title": "What the number is not",
                "left_title": "Answer accuracy",
                "left": "Did the box match gold? Lucky 42 still scores.",
                "right_title": "Checker pass rate",
                "right": "Among those wins, did the steps match the box? Put that in the report.",
            },
            {
                "layout": "cards",
                "title": "What to take from this lecture",
                "cards": [
                    ("Parse", "Last integer in the steps vs the answer field."),
                    ("Product", "Do not ship an unfaithful trace as “showing work.”"),
                    ("Lab 13", "Flag the 52→42 row. Fluency is not the check."),
                ],
            },
        ],
    },
    {
        "stem": "14.1-rag-pipeline",
        "title": "14.1 Retrieval-Augmented Generation",
        "slides": [
            {
                "layout": "title",
                "title": "What RAG is, and how it works",
                "subtitle": "DATA 443/643  ·  Week 14, note 14.1",
                "meta": "Week 14  ·  American University  ·  Ahmad Mousavi",
                "credit": "Ideas from Stanford CS224N 2026 L10 and Lewis et al. 2020. Original slides; those sources are not copied.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan  (first time seeing RAG)",
                "agenda": [
                    ("1", "What it is, and why weights are not enough"),
                    ("2", "Architecture: index, retrieve, generate"),
                    ("3", "Formulas: cosine, top-k, next-token, Lewis’s sum"),
                    ("4", "Pros, cons, and four failure modes"),
                    ("5", "Worked ranking: cosine 1 / 0.707 / 0"),
                ],
                "takeaway": "Key goal: define RAG, draw the boxes, write the formulas, and name one failure retrieval cannot fix.",
            },
            {
                "layout": "split",
                "title": "What RAG is",
                "bullets": [
                    "A frozen LLM answers from weights. Those weights are a snapshot.",
                    "RAG: look up passages from a collection you control, then generate from them.",
                    "Retrieval finds text. Augmented means it goes in the prompt. Generation is still next-token.",
                ],
                "image": "graphics/14.1-rag-pipeline/rag.png",
            },
            {
                "layout": "compare",
                "title": "Why bother",
                "left_title": "Closed book (weights only)",
                "left": "Fast. Stale. No chunk id to cite. Fluent guesses when the fact is missing.",
                "right_title": "RAG (index + generator)",
                "right": "Edit a PDF and re-index. Cite [d1]. Keep a modest LLM plus a large library.",
            },
            {
                "layout": "figure",
                "title": "Three ways to give a model new facts",
                "image": "graphics/14.1-rag-pipeline/tradeoffs.png",
                "caption": "Fine-tune changes weights. Long context pastes everything. RAG retrieves a few chunks.",
            },
            {
                "layout": "figure",
                "title": "Architecture: the transformer does not change",
                "image": "graphics/14.1-rag-pipeline/architecture.png",
                "caption": "Offline: chunk, embed, store vector+text+id. Online: embed the query, top-k, stuff, generate.",
            },
            {
                "layout": "split",
                "title": "How a question runs",
                "bullets": [
                    "Embed the query with the same map as the chunks.",
                    "Keep the k nearest passages. Stuff them with ids into a prompt.",
                    "Instruct: answer from the passages, cite, or say the context is missing.",
                ],
                "image": "graphics/14.1-rag-pipeline/architecture.png",
            },
            {
                "layout": "equation",
                "title": "Retrieve by cosine",
                "equation": r"\cos(e(q),e(z))=\frac{e(q)^{\top}e(z)}{\|e(q)\|\,\|e(z)\|}",
                "notes": [
                    r"\(\hat{z}_{1:k}=\operatorname{TopK}_z \cos(e(q),e(z))\).",
                    "Lab 14: e is bag-of-words counts. A product uses a neural embedding.",
                    "Same embedder for questions and chunks. Mixing maps breaks ranking.",
                ],
            },
            {
                "layout": "equation",
                "title": "Generate from the stuffed prompt",
                "equation": r"p_\theta(y\mid q,\hat{z}_{1:k})=\prod_t p_\theta(y_t\mid y_{<t},x)",
                "notes": [
                    r"\(x=\operatorname{Prompt}(q,\hat{z}_{1:k})\). RAG changed \(x\), not the net.",
                    r"Lewis et al.: \(p(y\mid q)=\sum_z p_\eta(z\mid q)\,p_\theta(y\mid q,z)\).",
                    "The lab does hard top-k stuffing, not the full sum.",
                ],
            },
            {
                "layout": "compare",
                "title": "What it is good and bad at",
                "left_title": "Positive",
                "left": "Update facts by editing the index. Cite ids. Frozen generator. Private PDFs stay out of the weights.",
                "right_title": "Negative",
                "right": "A miss cannot be fixed by a prettier prompt. Latency. Chunking and k are method. Lost in the middle. Unfaithful citations.",
            },
            {
                "layout": "cards",
                "title": "Four failures to name",
                "cards": [
                    ("Miss", "Gold never entered top-k. Measure recall@k."),
                    ("Near-miss", "Related junk ranks high; the model over-trusts it."),
                    ("Ignore", "Gold is in the prompt; weights still win. RAFT’s job."),
                    ("Bad cite", "Used [d1], wrote [d2]. Unfaithful, like CoT."),
                ],
            },
            {
                "layout": "split",
                "title": "k is a method knob",
                "bullets": [
                    "k=1 stuffs d1 (the close-time chunk).",
                    "k=2 also stuffs d3 (hours). Recall can rise; the near-miss can mislead.",
                    "Lost in the middle: gold in a long context is often ignored.",
                ],
                "image": "graphics/14.1-rag-pipeline/cosine-rank.png",
            },
            {
                "layout": "equation",
                "title": "Worked cosine on three toy docs",
                "equation": r"\cos(q,d1)=1,\quad \cos(q,d3)=1/\sqrt{2},\quad \cos(q,d2)=0",
                "notes": [
                    r"\(q=d1=(1,1,0)\). \(d3=(1,0,0)\). \(d2=(0,0,1)\).",
                    "Rank: d1, d3, d2. Lab 14 prints this ranking. No GPU.",
                    r"Recall@k needs gold ids. Attribution needs the cited id to contain the claim.",
                ],
            },
            {
                "layout": "compare",
                "title": "Two weeks, two jobs",
                "left_title": "10.3 RAFT",
                "left": "A training recipe: learn to use retrieved docs, distractors included. Weights change.",
                "right_title": "14.1 this hour",
                "right": "The inference stack, taught from scratch: what, why, boxes, formulas, then the ranking.",
            },
            {
                "layout": "cards",
                "title": "What to take from this lecture",
                "cards": [
                    ("Definition", "Retrieve passages, stuff them, generate. Not a new net."),
                    ("Two metrics", "Retrieval recall@k, then answer + attribution."),
                    ("Cite ids", "Vectors without raw text cannot be cited."),
                    ("Lab 14", "Five AU-toy snippets. Cosine, then a citation."),
                ],
            },
        ],
    },
    {
        "stem": "14.2-react-tools",
        "title": "14.2 ReAct and Tool Use",
        "slides": [
            {
                "layout": "title",
                "title": "What ReAct is, and how a tool call works",
                "subtitle": "DATA 443/643  ·  Week 14, note 14.2",
                "meta": "Week 14  ·  American University  ·  Ahmad Mousavi",
                "credit": "Ideas from Stanford CS224N 2026 L10 and Yao et al. Original slides; those sources are not copied.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan  (first time seeing ReAct)",
                "agenda": [
                    ("1", "What it is, and why CoT is not enough"),
                    ("2", "Architecture: policy, parser, tools"),
                    ("3", "Formulas: sample, Tool(a), append"),
                    ("4", "Pros, cons, unfaithful next-thought"),
                    ("5", "Worked calc[17*24] → 408"),
                ],
                "takeaway": "Key goal: define ReAct, write the five-line log, and say why the observation must be in the next context.",
            },
            {
                "layout": "split",
                "title": "What ReAct is",
                "bullets": [
                    "Thought: scratch in language. Action: a structured tool call. Observation: a string the model did not write.",
                    "CoT can invent 17×24. ReAct is supposed to wait for calc.",
                    "RAG retrieve is one tool. calc is another. Same loop.",
                ],
                "image": "graphics/14.2-react-tools/react.png",
            },
            {
                "layout": "compare",
                "title": "Why a tool, not more thought tokens",
                "left_title": "Chain of thought",
                "left": "Extra tokens before the answer. Still guesses. Fluency is not a check.",
                "right_title": "ReAct",
                "right": "The next thought can depend on a real observation: arithmetic, search, or a retrieved chunk.",
            },
            {
                "layout": "split",
                "title": "Architecture",
                "bullets": [
                    "Policy: the LLM samples the next line.",
                    "Parser: action → tool name and arguments. Failures return ERR.",
                    "Tools: functions. Lab 14 calc only matches digits and +*/.",
                ],
                "image": "graphics/14.2-react-tools/react.png",
            },
            {
                "layout": "equation",
                "title": "The loop is a decoding protocol",
                "equation": r"o_t=\mathrm{Tool}(a_t),\quad c_{t+1}=c_t\oplus\tau_t\oplus a_t\oplus o_t",
                "notes": [
                    r"\((\tau_t,a_t)\sim p_\theta(\cdot\mid c_t)\). No new trained module today.",
                    "Stop at Answer, or at a step cap.",
                    "Stuffed RAG is one retrieve then one generate. ReAct can call again.",
                ],
            },
            {
                "layout": "compare",
                "title": "What it is good and bad at",
                "left_title": "Positive",
                "left": "Delegate exact ops. Mix retrieve and calc. The transcript is an audit log.",
                "right_title": "Negative",
                "right": "Bad parses, wrong tool, ignored obs, loops, latency. Free Python eval is out of bounds in this class.",
            },
            {
                "layout": "split",
                "title": "Do not multiply in the thought",
                "bullets": [
                    "Action calc[17*24]. Observation 408. Answer 408.",
                    "If the next thought says 428, the loop is unfaithful.",
                    "Lab 14: calc[23*60] → 1380, plus a citation [d1].",
                ],
                "image": "graphics/14.2-react-tools/react.png",
            },
            {
                "layout": "compare",
                "title": "Three control loops",
                "left_title": "CoT / SC / ToT",
                "left": "Text only, or search among thoughts. No observation from the world unless you add one.",
                "right_title": "ReAct",
                "right": "Interleave thoughts with tool results. Missing a line in the log means you ran CoT.",
            },
            {
                "layout": "cards",
                "title": "What to take from this lecture",
                "cards": [
                    ("Definition", "Think, call a tool, read, continue."),
                    ("Five-line log", "Thought, Action, Observation, Thought, Answer."),
                    ("Dummy calc", "Lab 14 is not python_eval."),
                    ("Cap", "Looping calc[1+1] is a missing step limit."),
                ],
            },
        ],
    },
    {
        "stem": "14.3-eval-presentations",
        "title": "14.3 Evaluating Applications and Giving the Talk",
        "slides": [
            {
                "layout": "title",
                "title": "A Talk Is an Evaluation Story",
                "subtitle": "DATA 443/643  ·  Week 14, note 14.3",
                "meta": "Week 14  ·  American University  ·  Ahmad Mousavi",
                "credit": "Talk craft from Peyton Jones; numbers from this course. Original slides.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan",
                "agenda": [
                    ("1", "A metric that could change your mind"),
                    ("2", "Baseline, split, n, seeds"),
                    ("3", "+2 pp vs 4 pp of seed noise"),
                    ("4", "One failure case with ids"),
                ],
                "takeaway": "Key goal: question, table, ablation, failure. Not a notebook tour.",
            },
            {
                "layout": "split",
                "title": "Write a falsifiable sentence",
                "bullets": [
                    "Name the knob, the split, and n.",
                    "A demo GIF is not a substitute for a number.",
                    "If a closed API is in the loop, still show an open baseline.",
                ],
                "image": "graphics/14.3-eval-presentations/talk.png",
            },
            {
                "layout": "split",
                "title": "Do not lead with a 2-point bump",
                "bullets": [
                    "RAG 0.82 and 0.78 (mean 0.80). Baseline 0.80 and 0.76 (mean 0.78).",
                    "Lift 0.02. Seed spread 0.04. n=50.",
                    "Say that out loud. Then show a failure RAG actually changed.",
                ],
                "image": "graphics/14.3-eval-presentations/seed-spread.png",
            },
            {
                "layout": "compare",
                "title": "Ablation vs theater",
                "left_title": "Fake ablation",
                "left": "You claimed LoRA; you turned off dropout. That was not the claim.",
                "right_title": "Real ablation",
                "right": "Turn off the claimed knob (no retrieval, k=1, no CoT) and show the metric move.",
            },
            {
                "layout": "compare",
                "title": "If one minute remains",
                "left_title": "Drop this",
                "left": "A second architecture diagram the back row cannot read.",
                "right_title": "Keep this",
                "right": "The failure: query, retrieved ids, what broke.",
            },
            {
                "layout": "cards",
                "title": "What to take from this lecture",
                "cards": [
                    ("Spine", "30 s question, 1 min picture, 1 min table, 1 min failure."),
                    ("Canvas", "Slot and upload are official. Week 15 leftover talks too."),
                    ("Peyton Jones", "Start with the problem. Mechanism later."),
                ],
            },
        ],
    },
    {
        "stem": "15.1-exam-review",
        "title": "15.1 Exam Review",
        "slides": [
            {
                "layout": "title",
                "title": "Method, Then Measurement",
                "subtitle": "DATA 443/643  ·  Week 15, note 15.1",
                "meta": "Week 15  ·  American University  ·  Ahmad Mousavi",
                "credit": "A recap of DATA 443/643. Method then measurement. Original slides.",
            },
            {
                "layout": "agenda",
                "title": "Lecture plan",
                "agenda": [
                    ("1", "Four modules, one stack"),
                    ("2", "A formula sheet you can write"),
                    ("3", "Failure → the number that catches it"),
                    ("4", "Remaining talks: Canvas + a failure case"),
                ],
                "takeaway": "Key goal: name the method, then the measurement. Trivia is not the exam.",
            },
            {
                "layout": "split",
                "title": "What sits on the exam",
                "bullets": [
                    "M1 nets → transformers. M2 vision, audio, CLIP.",
                    "M3 scale, SFT, RLHF. M4 GAN, diffusion, CoT, RAG.",
                    "Draw the picture. Attach one number.",
                ],
                "image": "graphics/15.1-exam-review/map.png",
            },
            {
                "layout": "cards",
                "title": "Write these, then say what you would plot",
                "cards": [
                    ("Attention / GAN", r"\(\operatorname{softmax}(QK^{\top}/\sqrt{d})V\). \(D^{*}=p_{r}/(p_{r}+p_{g})\)."),
                    ("Diffusion / CFG", r"\(x_{t}=\sqrt{\bar{\alpha}_{t}}\,x_{0}+\sqrt{1-\bar{\alpha}_{t}}\,\varepsilon\). \(\hat{\varepsilon}=\varepsilon_{u}+s(\varepsilon_{c}-\varepsilon_{u})\)."),
                    ("DPO / cosine", r"\(\sigma(0)=1/2\). \(\cos(a,b)=a^{\top}b/(\|a\|\|b\|)\)."),
                ],
            },
            {
                "layout": "split",
                "title": "The exam shape",
                "bullets": [
                    "Same face, low lossG → mode bins, not lossG.",
                    "Right box, last step 52 → F among wins.",
                    "Cite [d5], fact in [d1] → attribution + recall@k.",
                ],
                "image": "graphics/15.1-exam-review/fail-metric.png",
            },
            {
                "layout": "compare",
                "title": "Pairs the exam likes",
                "left_title": "Architecture choice",
                "left": "GPT vs BERT. CLIP vs BLIP. GAN vs diffusion. CoT vs ReAct. Justify with the task.",
                "right_title": "The metric",
                "right": "Then say what you would plot. Labs 11–14 are the Module 4 shortcuts.",
            },
            {
                "layout": "cards",
                "title": "What to take from this lecture",
                "cards": [
                    ("Labs on paper", "11 bins, 12 oracle reverse, 13 last-int vs box, 14 cosine + calc."),
                    ("Talks", "Canvas is official. Bring a failure, not only the best run."),
                    ("Karpathy", "Recap of the LLM stack. Not a substitute for Weeks 11–12."),
                ],
            },
        ],
    },
]


def _math(src: str, display: str = "inline") -> str:
    try:
        from latex2mathml.converter import convert

        return convert(src.strip(), display=display)
    except Exception:
        return html_lib.escape(src)


def _tex_to_html(text: str) -> str:
    out = []
    i = 0
    n = len(text)
    while i < n:
        if text.startswith("\\[", i):
            j = text.find("\\]", i + 2)
            if j == -1:
                out.append(html_lib.escape(text[i:]))
                break
            out.append(_math(text[i + 2 : j], display="block"))
            i = j + 2
            continue
        if text.startswith("\\(", i):
            j = text.find("\\)", i + 2)
            if j == -1:
                out.append(html_lib.escape(text[i:]))
                break
            out.append(_math(text[i + 2 : j], display="inline"))
            i = j + 2
            continue
        nxt_inline = text.find("\\(", i)
        nxt_disp = text.find("\\[", i)
        nxt = min([x for x in (nxt_inline, nxt_disp) if x != -1], default=-1)
        chunk = text[i:] if nxt == -1 else text[i:nxt]
        out.append(html_lib.escape(chunk))
        if nxt == -1:
            break
        i = nxt
    return "".join(out)


def _img(rel: str) -> str:
    src = (FILES / rel).resolve().as_uri()
    return f'<div class="fig"><img src="{src}" alt="" /></div>'


def _ul(items: list[str]) -> str:
    if not items:
        return ""
    return "<ul>" + "".join(f"<li>{_tex_to_html(b)}</li>" for b in items) + "</ul>"


def _takeaway(slide: dict) -> str:
    text = slide.get("takeaway")
    if not text:
        return ""
    return f'<div class="takeaway">{_tex_to_html(text)}</div>'


def _infer_layout(slide: dict) -> str:
    if slide.get("layout"):
        return slide["layout"]
    if slide.get("agenda"):
        return "agenda"
    if slide.get("equation"):
        return "equation"
    if slide.get("cards"):
        return "cards"
    if slide.get("left") or slide.get("compare"):
        return "compare"
    if slide.get("image") and slide.get("bullets"):
        return "split"
    if slide.get("image"):
        return "figure"
    return "bullets"


def _body(slide: dict) -> str:
    layout = _infer_layout(slide)
    title = html_lib.escape(slide.get("title") or "")
    heading = f"<h1>{title}</h1>" if title else ""
    if layout == "title":
        sub = html_lib.escape(slide.get("subtitle") or "")
        meta = html_lib.escape(slide.get("meta") or "").replace("  ·  ", "<br/>")
        credit = html_lib.escape(slide.get("credit") or "")
        credit_html = f"<p class='credit'>{credit}</p>" if credit else ""
        return (
            f"<div class='title-main'><h1>{title}</h1>"
            f"<p class='subtitle'>{sub}</p><p class='meta'>{meta}</p></div>"
            f"{credit_html}"
        )
    if layout == "agenda":
        rows = []
        for row in slide.get("agenda") or []:
            n, text = row[0], row[1]
            rows.append(
                f"<li><span class='n'>{html_lib.escape(str(n))}</span>"
                f"<span>{_tex_to_html(text)}</span></li>"
            )
        return heading + f"<ol class='agenda'>{''.join(rows)}</ol>" + _takeaway(slide)
    if layout == "equation":
        notes = slide.get("notes") or []
        note_html = ""
        if notes:
            cols = "".join(f"<div>{_tex_to_html(n)}</div>" for n in notes)
            note_html = f"<div class='eq-notes'>{cols}</div>"
        return (
            heading
            + f"<div class='eq'>{_math(slide.get('equation') or '', display='block')}{note_html}</div>"
            + _takeaway(slide)
        )
    if layout == "cards":
        cards = []
        for ht, body in slide.get("cards") or []:
            cards.append(f"<div class='card'><h2>{html_lib.escape(ht)}</h2><p>{_tex_to_html(body)}</p></div>")
        klass = "cards three" if len(slide.get("cards") or []) == 3 else "cards"
        return heading + f"<div class='{klass}'>{''.join(cards)}</div>" + _takeaway(slide)
    if layout == "compare":
        left_t = html_lib.escape(slide.get("left_title") or "Before")
        right_t = html_lib.escape(slide.get("right_title") or "After")
        return (
            heading
            + "<div class='compare'>"
            + f"<div class='col bad'><h2>{left_t}</h2><p>{_tex_to_html(slide.get('left') or '')}</p></div>"
            + f"<div class='col good'><h2>{right_t}</h2><p>{_tex_to_html(slide.get('right') or '')}</p></div>"
            + "</div>"
            + _takeaway(slide)
        )
    if layout == "figure":
        cap = slide.get("caption")
        cap_html = f"<p class='caption'>{_tex_to_html(cap)}</p>" if cap else ""
        return heading + _img(slide["image"]) + cap_html + _takeaway(slide)
    if layout == "split":
        return (
            heading
            + "<div class='split'>"
            + f"<div class='copy'>{_ul(slide.get('bullets') or [])}{_takeaway(slide)}</div>"
            + _img(slide["image"])
            + "</div>"
        )
    fig = _img(slide["image"]) if slide.get("image") else ""
    return heading + _ul(slide.get("bullets") or []) + fig + _takeaway(slide)


_FIRST_LOOK_KEYS = ("What", "Why", "Architecture", "How", "Formula", "Tradeoffs")
_FIRST_LOOK_LINE = re.compile(
    r"^>?\s*\*\*(What|Why|Architecture|How|Formula|Tradeoffs)\.\*\*\s*(.+)$"
)


def _first_look_slide(stem: str) -> dict | None:
    slug = stem.split("-", 1)[-1]
    path = FILES / f"{slug}.md"
    if not path.exists():
        return None
    found: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        m = _FIRST_LOOK_LINE.match(raw.strip())
        if m and m.group(1) not in found:
            found[m.group(1)] = m.group(2).strip()
    if any(k not in found for k in _FIRST_LOOK_KEYS):
        return None
    def _plain(s: str) -> str:
        return s.replace("**", "")

    return {
        "layout": "bullets",
        "title": "First time: what / why / formula",
        "bullets": [
            _plain(f"What / why. {found['What']} {found['Why']}"),
            _plain(f"Architecture. {found['Architecture']}"),
            _plain(f"Formula. {found['Formula']}"),
            _plain(f"Tradeoffs. {found['Tradeoffs']}"),
        ],
        "takeaway": _plain(f"How. {found['How']}"),
    }


def _slides_with_first_look(deck: dict) -> list[dict]:
    slides = list(deck["slides"])
    if any(str(s.get("title") or "").startswith("First time") for s in slides):
        return slides
    extra = _first_look_slide(deck["stem"])
    if extra is None:
        return slides
    idx = 1
    for i, slide in enumerate(slides):
        if slide.get("layout") == "agenda":
            idx = i + 1
    slides.insert(idx, extra)
    return slides


def write_deck(deck: dict) -> pathlib.Path:
    WORK.mkdir(parents=True, exist_ok=True)
    slides = _slides_with_first_look(deck)
    n = len(slides)
    slides_html = []
    for i, slide in enumerate(slides, start=1):
        layout = _infer_layout(slide)
        klass = "slide title-slide" if layout == "title" else "slide"
        if str(slide.get("title") or "").startswith("First time"):
            klass += " first-look"
        kicker = ""
        if layout not in {"title"}:
            kicker = f"<p class='kicker'>{html_lib.escape(COURSE)} · lecture {html_lib.escape(deck['stem'].split('-', 1)[0])}</p>"
        bar = (
            "<div class='rule'></div>"
            f"<footer class='bar'><span class='left'>Ahmad Mousavi</span>"
            f"<span class='mid'>{html_lib.escape(deck['title'])}</span>"
            f"<span class='right'>{i} / {n}</span></footer>"
        )
        slides_html.append(
            f"<section class='{klass}'><div class='slide-body'>{kicker}{_body(slide)}</div>{bar}</section>"
        )
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>{html_lib.escape(deck["title"])}</title>
  <style>{SLIDE_CSS}</style>
</head>
<body>
{chr(10).join(slides_html)}
</body>
</html>
"""
    path = WORK / f"{deck['stem']}.html"
    path.write_text(html.replace("\r\n", "\n"), encoding="utf-8", newline="\n")
    return path


def print_pdf(html_path: pathlib.Path, pdf_path: pathlib.Path) -> None:
    if not EDGE.exists():
        raise FileNotFoundError(f"Edge not found: {EDGE}")
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        str(EDGE),
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        html_path.resolve().as_uri(),
    ]
    subprocess.run(cmd, check=True)


def main() -> None:
    weeks = {int(a) for a in sys.argv[1:] if a.isdigit()}
    for deck in DECKS:
        week = int(deck["stem"].split(".", 1)[0])
        if weeks and week not in weeks:
            continue
        html_path = write_deck(deck)
        pdf_path = OUT / f"{deck['stem']}.pdf"
        print_pdf(html_path, pdf_path)
        print(f"Wrote {pdf_path.relative_to(ROOT)} ({pdf_path.stat().st_size} bytes)")
    print("done")


if __name__ == "__main__":
    main()
