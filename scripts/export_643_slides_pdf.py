"""Build one-slide-per-page PDFs for DATA 443/643 Week 1."""

from __future__ import annotations

import html as html_lib
import pathlib
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
  justify-content: center;
  padding-left: 0.9in;
  padding-right: 0.9in;
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
ul {
  margin: 0.05em 0 0.15em;
  padding-left: 1.15em;
  font-size: 20pt;
  line-height: 1.38;
}
li { margin: 0.16em 0; }
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
                "takeaway": "Pedagogy drawn from Stanford CS224N (plan + one formula), CS231N (footer, one idea), MIT 6.S191 (diagram + numbers). Original slides; those courses are not copied.",
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
                "meta": "After MIT 6.S191 L1 and CS231N L4: one unit, then why depth needs a bend.",
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
                "caption": "MIT 6.S191 style: same example as a diagram and as a line. Ours uses ReLU, not sigmoid.",
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
                    "CS231N: you get a linear classifier again.",
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
                "meta": "After CS231N L3–L4 and Nielsen Ch. 1: walk downhill, then one computational graph.",
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
                "caption": "CS231N: each op is a gate. Local derivative times upstream.",
            },
            {
                "layout": "equation",
                "title": "The chain rule you must write",
                "equation": r"\frac{\partial L}{\partial w}=(a-y)\,\mathrm{ReLU}'(z)\,x",
                "notes": [
                    r"Squared error on one ReLU neuron.",
                    r"CMU 11-711 cousin: \(\partial L/\partial w=(p-y)x\).",
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
                "meta": "After Stanford CS224N Lecture 2: distributional meaning, skip-gram softmax, then evaluation.",
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
                "meta": "After Stanford CS224N W26 L4: any-length input, shared weights, then an RNN-LM.",
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
                "meta": "After CS231N L7 (BPTT, singular values) and CS224N L4 (near vs. long-term effects).",
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
                "meta": "After CMU 11-785 L14: a cell that can copy, plus input-dependent gates.",
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
                "title": "The bottleneck",
                "bullets": [
                    "An RNN compresses the past into one vector.",
                    "Attention: every token looks at every token in one step.",
                    r"Cost: \(O(T^2)\). Path length: 1.",
                ],
                "image": "graphics/3.1-attention-need/rnn-vs-attention.png",
            },
        ],
    },
    {
        "stem": "3.2-self-attention",
        "title": "3.2 Self-Attention (Q, K, V)",
        "slides": [
            {
                "title": "Query, key, value",
                "bullets": [
                    "Query asks. Key is asked. Value is mixed in.",
                    r"Weights: softmax of \(QK^\top / \sqrt{d}\).",
                ],
                "image": "graphics/3.2-self-attention/qkv.png",
            },
            {
                "title": "A row is a distribution",
                "bullets": [
                    "Large mass on a name: this pronoun just looked there.",
                    "Several heads in parallel, then concatenate.",
                ],
                "image": "graphics/3.2-self-attention/attn-heatmap.png",
            },
        ],
    },
    {
        "stem": "3.3-transformer-block",
        "title": "3.3 The Transformer Block",
        "slides": [
            {
                "title": "Attention has no order",
                "bullets": [
                    "Add sinusoidal or learned positions.",
                    "Later models use relative or rotary positions.",
                ],
                "image": "graphics/3.3-transformer-block/positional.png",
            },
            {
                "title": "One block",
                "bullets": [
                    "Attention mixes across positions. The MLP mixes across channels.",
                    "Residuals are the cousin of the LSTM highway.",
                ],
                "image": "graphics/3.3-transformer-block/block.png",
            },
        ],
    },
    {
        "stem": "3.4-gpt-bert",
        "title": "3.4 GPT and BERT",
        "slides": [
            {
                "title": "Same block, different mask",
                "bullets": [
                    "GPT: causal, next-token, generate.",
                    "BERT: bidirectional, masked tokens, encode.",
                    "Do not fine-tune BERT as if it were GPT.",
                ],
                "image": "graphics/3.4-gpt-bert/gpt-bert.png",
            },
        ],
    },
    {
        "stem": "4.1-multimodal-foundations",
        "title": "4.1 Multimodal Foundations",
        "slides": [
            {
                "title": "Joint versus coordinated",
                "bullets": [
                    "Joint: one fused vector. Missing a stream hurts.",
                    "Coordinated: two towers and a similarity. CLIP is this.",
                ],
                "image": "graphics/4.1-multimodal-foundations/joint-coord.png",
            },
        ],
    },
    {
        "stem": "4.2-vision-transformers",
        "title": "4.2 Vision Transformers",
        "slides": [
            {
                "title": "Patches as tokens",
                "bullets": [
                    "Flatten each patch, map to width d, add positions.",
                    "A 224 image with patch 16 is 196 tokens: a short paragraph.",
                ],
                "image": "graphics/4.2-vision-transformers/patches.png",
            },
            {
                "title": "The same stack as language",
                "bullets": [
                    "[CLS] + positions + transformer.",
                    "In this course, start from a pretrained ViT, not from scratch.",
                ],
                "image": "graphics/4.2-vision-transformers/vit.png",
            },
        ],
    },
    {
        "stem": "4.3-contrastive-zeroshot",
        "title": "4.3 Contrastive Learning and Zero-Shot Transfer",
        "slides": [
            {
                "title": "Matched pairs on the diagonal",
                "bullets": [
                    "InfoNCE wants image i with caption i.",
                    "Small batches mean easy negatives.",
                ],
                "image": "graphics/4.3-contrastive-zeroshot/contrastive.png",
            },
            {
                "title": "Zero-shot is nearest text",
                "bullets": [
                    "Class names are prompts, not a trained softmax.",
                    "Wording matters. Unseen phrases do not magically work.",
                ],
                "image": "graphics/4.3-contrastive-zeroshot/zeroshot.png",
            },
        ],
    },
    {
        "stem": "5.1-clip",
        "title": "5.1 CLIP",
        "slides": [
            {
                "title": "Two towers, one cosine",
                "bullets": [
                    "Image encoder and text encoder, web-scale pairs.",
                    "Good at retrieval and zero-shot. Not a captioner.",
                ],
                "image": "graphics/5.1-clip/clip-towers.png",
            },
        ],
    },
    {
        "stem": "5.2-blip",
        "title": "5.2 BLIP and Captioning",
        "slides": [
            {
                "title": "Clean, match, and write",
                "bullets": [
                    "Bootstrap captions, filter with image–text matching.",
                    "ITC + ITM + a language-model loss.",
                ],
                "image": "graphics/5.2-blip/blip-pipeline.png",
            },
        ],
    },
    {
        "stem": "5.3-retrieval-bias",
        "title": "5.3 Retrieval, Bias, and Robustness",
        "slides": [
            {
                "title": "Two retrieval directions",
                "bullets": [
                    "Text to image, and image to text.",
                    "Report recall@k and a few failure cases.",
                ],
                "image": "graphics/5.3-retrieval-bias/retrieval.png",
            },
            {
                "title": "Geometry encodes the web",
                "bullets": [
                    "Occupation and gender probes belong in the report.",
                    "High ImageNet zero-shot does not certify your domain.",
                ],
                "image": "graphics/5.3-retrieval-bias/vlm-bias.png",
            },
        ],
    },
    {
        "stem": "6.1-audio-spectrograms",
        "title": "6.1 Waveforms, Spectrograms, and Time–Frequency Tokens",
        "slides": [
            {
                "title": "A wave, then a picture",
                "bullets": [
                    "STFT windows the waveform and takes a DFT per frame.",
                    "The magnitude spectrogram is an image the Week 4 stack can read.",
                ],
                "image": "graphics/6.1-audio-spectrograms/wave-spec.png",
            },
            {
                "title": "Patches, as in ViT",
                "bullets": [
                    "Cut time–frequency tiles, flatten, embed, add positions.",
                    "Write sampling rate, window, hop, and mel versus linear STFT.",
                ],
                "image": "graphics/6.1-audio-spectrograms/spec-patches.png",
            },
        ],
    },
    {
        "stem": "6.2-audio-encoders",
        "title": "6.2 Audio Encoders and Speech Models",
        "slides": [
            {
                "title": "Whisper-style encoder–decoder",
                "bullets": [
                    "Log-mel in, transformer encoder, text decoder.",
                    "Same Week 3 block. New input. Transcript out.",
                ],
                "image": "graphics/6.2-audio-encoders/whisper.png",
            },
            {
                "title": "CLAP is CLIP for audio",
                "bullets": [
                    "Two towers, cosine, paired captions.",
                    "Retrieval and zero-shot tags, not a transcript.",
                ],
                "image": "graphics/6.2-audio-encoders/clap.png",
            },
        ],
    },
    {
        "stem": "6.3-fusion-scarcity",
        "title": "6.3 Fusion, Unified Embeddings, and Data Scarcity",
        "slides": [
            {
                "title": "Early, late, cross-attention",
                "bullets": [
                    "Early concat is simple and brittle if audio is missing.",
                    "Cross-attention lets text query audio keys and values.",
                ],
                "image": "graphics/6.3-fusion-scarcity/fusion.png",
            },
            {
                "title": "Labeled audio is scarce",
                "bullets": [
                    "Web text dwarfs image–text, which dwarfs transcribed audio.",
                    "Transfer from CLIP/Whisper is the usual project move.",
                ],
                "image": "graphics/6.3-fusion-scarcity/scarcity.png",
            },
        ],
    },
    {
        "stem": "7.1-scaling-laws",
        "title": "7.1 Scaling Laws",
        "slides": [
            {
                "title": "Loss versus compute",
                "bullets": [
                    "On a log–log plot, pretraining loss falls as a power of compute.",
                    "The curve bends when you starve data or parameters.",
                ],
                "image": "graphics/7.1-scaling-laws/compute-loss.png",
            },
            {
                "title": "Chinchilla: feed the model tokens",
                "bullets": [
                    "Bigger is not enough if tokens do not keep up.",
                    "A compute-optimal run balances parameters and data.",
                ],
                "image": "graphics/7.1-scaling-laws/chinchilla.png",
            },
        ],
    },
    {
        "stem": "7.2-mixture-of-experts",
        "title": "7.2 Mixture of Experts",
        "slides": [
            {
                "title": "A router, then a few experts",
                "bullets": [
                    "Each token activates a sparse subset of MLPs.",
                    "Capacity grows without dense FLOPs on every expert.",
                ],
                "image": "graphics/7.2-mixture-of-experts/moe.png",
            },
        ],
    },
    {
        "stem": "7.3-efficiency-deploy",
        "title": "7.3 Compression and Deployment",
        "slides": [
            {
                "title": "Prune, quantize, distill",
                "bullets": [
                    "Compression is a pipeline. Measure after each cut.",
                    "Int8 is not free: report quality, not only size.",
                ],
                "image": "graphics/7.3-efficiency-deploy/compress.png",
            },
            {
                "title": "Speculative decoding",
                "bullets": [
                    "A small model drafts a prefix. The large model verifies.",
                    "Accepted tokens must match the large model's distribution.",
                ],
                "image": "graphics/7.3-efficiency-deploy/speculative.png",
            },
        ],
    },
    {
        "stem": "8.1-sft-instructions",
        "title": "8.1 Supervised Fine-Tuning and Instruction Data",
        "slides": [
            {
                "title": "Pretrain, then SFT",
                "bullets": [
                    "Next-token on the web is not the same as following a request.",
                    "Instruction data is a distribution shift, not a new architecture.",
                ],
                "image": "graphics/8.1-sft-instructions/sft.png",
            },
            {
                "title": "One SFT row",
                "bullets": [
                    "A request and a completion you would actually want.",
                    "Prompt wording is part of the method. Write it down.",
                ],
                "image": "graphics/8.1-sft-instructions/pair.png",
            },
        ],
    },
    {
        "stem": "8.2-continual-forgetting",
        "title": "8.2 Continual Learning and Forgetting",
        "slides": [
            {
                "title": "Task B overwrites task A",
                "bullets": [
                    "Accuracy on the first task drops as you train the next.",
                    "That is catastrophic forgetting, not a mystery bug.",
                ],
                "image": "graphics/8.2-continual-forgetting/forget.png",
            },
            {
                "title": "Replay, freeze, or isolate",
                "bullets": [
                    "Mix old examples, freeze a backbone, or train a thin adapter.",
                    "Measure A after B, not only B after B.",
                ],
                "image": "graphics/8.2-continual-forgetting/replay.png",
            },
        ],
    },
    {
        "stem": "8.3-lora-adapters",
        "title": "8.3 LoRA, Adapters, and Federated Updates",
        "slides": [
            {
                "title": r"Train \(BA\), freeze \(W\)",
                "bullets": [
                    r"A low-rank pair updates \(W + BA\) without rewriting \(W\).",
                    r"Rank \(r\) is a knob: too small underfits, too large is full FT.",
                ],
                "image": "graphics/8.3-lora-adapters/lora.png",
            },
            {
                "title": "Ship adapters, not documents",
                "bullets": [
                    "Federated sketch: sites train LoRA locally, server averages.",
                    "Still not a privacy proof. It is a smaller delta.",
                ],
                "image": "graphics/8.3-lora-adapters/federated.png",
            },
        ],
    },
    {
        "stem": "9.1-preference-rewards",
        "title": "9.1 Preference Data and Reward Models",
        "slides": [
            {
                "title": "Chosen versus rejected",
                "bullets": [
                    "A pair is an order, not a score out of 100.",
                    r"Label: \(y_w \succ y_l\) given prompt \(x\).",
                ],
                "image": "graphics/9.1-preference-rewards/pair.png",
            },
            {
                "title": "A reward model scores completions",
                "bullets": [
                    "Trained as a classifier of the better completion.",
                    "Cheap to game if it is not the same as the human rater.",
                ],
                "image": "graphics/9.1-preference-rewards/reward.png",
            },
        ],
    },
    {
        "stem": "9.2-rlhf",
        "title": "9.2 RLHF",
        "slides": [
            {
                "title": "SFT, reward, then a policy update",
                "bullets": [
                    "Sample completions, score them, climb the reward.",
                    "A KL penalty keeps the policy near SFT.",
                ],
                "image": "graphics/9.2-rlhf/loop.png",
            },
        ],
    },
    {
        "stem": "9.3-dpo",
        "title": "9.3 Direct Preference Optimization",
        "slides": [
            {
                "title": "Same pairs, no PPO loop",
                "bullets": [
                    "The reward is written from the policy and a frozen reference.",
                    "Offline: DPO cannot invent completions that were never in the file.",
                ],
                "image": "graphics/9.3-dpo/dpo.png",
            },
        ],
    },
    {
        "stem": "10.1-red-teaming",
        "title": "10.1 Red-Teaming and Safety Evaluation",
        "slides": [
            {
                "title": "Try to break it on purpose",
                "bullets": [
                    "Safety is an evaluation, not a vibe.",
                    "Log the attacks that work. Report the ones that do not.",
                ],
                "image": "graphics/10.1-red-teaming/probe.png",
            },
        ],
    },
    {
        "stem": "10.2-editing-unlearning",
        "title": "10.2 Editing and Unlearning",
        "slides": [
            {
                "title": "Locate, then write",
                "bullets": [
                    "ROME finds an MLP association and overwrites the value.",
                    "One key. Not a new pretraining run.",
                ],
                "image": "graphics/10.2-editing-unlearning/rome.png",
            },
            {
                "title": "A set is not a key",
                "bullets": [
                    "Unlearning tries to forget documents while retaining the rest.",
                    "Editing Paris is not unlearning a behavior.",
                ],
                "image": "graphics/10.2-editing-unlearning/unlearn.png",
            },
        ],
    },
    {
        "stem": "10.3-raft-memory",
        "title": "10.3 RAFT and Memory-Augmented Models",
        "slides": [
            {
                "title": "Train with retrieved context",
                "bullets": [
                    "RAFT puts chunks in the prompt at train time, not only at demo time.",
                    "Include negatives so the model practices ignoring junk.",
                ],
                "image": "graphics/10.3-raft-memory/raft.png",
            },
            {
                "title": "Two stores",
                "bullets": [
                    "Weights are parametric. An index is not.",
                    "Editing one does not automatically fix the other.",
                ],
                "image": "graphics/10.3-raft-memory/memory.png",
            },
        ],
    },
    {
        "stem": "11.1-gan-idea",
        "title": "11.1 Generative Adversarial Nets",
        "slides": [
            {
                "title": "Generator versus discriminator",
                "bullets": [
                    r"\(G\) maps noise to fakes. \(D\) tries to tell fakes from data.",
                    "Neither player is a likelihood. Together they are a game.",
                ],
                "image": "graphics/11.1-gan-idea/players.png",
            },
        ],
    },
    {
        "stem": "11.2-gan-training",
        "title": "11.2 Training Dynamics",
        "slides": [
            {
                "title": "Keep the two losses in tension",
                "bullets": [
                    r"A 99% discriminator often means a dead generator.",
                    "If one player wins too early, the other stops learning.",
                ],
                "image": "graphics/11.2-gan-training/dynamics.png",
            },
        ],
    },
    {
        "stem": "11.3-mode-collapse",
        "title": "11.3 Mode Collapse and Evaluation",
        "slides": [
            {
                "title": "Sharp samples can still miss a mode",
                "bullets": [
                    "Look at coverage, not one pretty draw.",
                    "Two Gaussians: if every fake sits on one blob, you collapsed.",
                ],
                "image": "graphics/11.3-mode-collapse/collapse.png",
            },
        ],
    },
    {
        "stem": "12.1-diffusion-forward",
        "title": "12.1 The Forward Process",
        "slides": [
            {
                "title": "Data becomes noise",
                "bullets": [
                    r"Add a little Gaussian noise for \(T\) steps.",
                    r"\(x_T\) should look like the prior, not like the sample.",
                ],
                "image": "graphics/12.1-diffusion-forward/forward.png",
            },
        ],
    },
    {
        "stem": "12.2-diffusion-reverse",
        "title": "12.2 The Reverse Process",
        "slides": [
            {
                "title": "Learn to denoise",
                "bullets": [
                    r"The net typically predicts the noise (or \(x_0\)).",
                    "Each reverse step walks toward the data distribution.",
                ],
                "image": "graphics/12.2-diffusion-reverse/reverse.png",
            },
        ],
    },
    {
        "stem": "12.3-latent-conditioning",
        "title": "12.3 Latent Diffusion and Text Conditioning",
        "slides": [
            {
                "title": "Diffuse a cheap latent",
                "bullets": [
                    "VAE in, UNet in latent space, VAE out.",
                    "Text (often CLIP from Week 5) conditions the denoise step.",
                ],
                "image": "graphics/12.3-latent-conditioning/ldm.png",
            },
        ],
    },
    {
        "stem": "13.1-chain-of-thought",
        "title": "13.1 Chain-of-Thought",
        "slides": [
            {
                "title": "Steps before the answer",
                "bullets": [
                    "Intermediate tokens can carry scratch work.",
                    "Asking for steps is a prompt choice, not a new architecture.",
                ],
                "image": "graphics/13.1-chain-of-thought/cot.png",
            },
        ],
    },
    {
        "stem": "13.2-self-consistency-tot",
        "title": "13.2 Self-Consistency and Tree-of-Thoughts",
        "slides": [
            {
                "title": "Vote, or search a tree",
                "bullets": [
                    "Self-consistency: sample traces, majority on the answer.",
                    "Tree-of-Thoughts: expand partial steps when one path stalls.",
                ],
                "image": "graphics/13.2-self-consistency-tot/tree.png",
            },
        ],
    },
    {
        "stem": "13.3-faithfulness",
        "title": "13.3 Faithfulness of Explanations",
        "slides": [
            {
                "title": "Correct answer, invented steps",
                "bullets": [
                    "Process and outcome are different claims.",
                    "Do not put an unfaithful trace in a user-facing product.",
                ],
                "image": "graphics/13.3-faithfulness/unfaithful.png",
            },
        ],
    },
    {
        "stem": "14.1-rag-pipeline",
        "title": "14.1 Retrieval-Augmented Generation",
        "slides": [
            {
                "title": "Index, retrieve, generate",
                "bullets": [
                    "Non-parametric memory at inference.",
                    "Wrong chunks in the prompt become confident wrong answers.",
                ],
                "image": "graphics/14.1-rag-pipeline/rag.png",
            },
        ],
    },
    {
        "stem": "14.2-react-tools",
        "title": "14.2 ReAct and Tool Use",
        "slides": [
            {
                "title": "Thought, action, observation",
                "bullets": [
                    "Call a tool instead of guessing the lookup.",
                    "The observation is evidence. The next thought should use it.",
                ],
                "image": "graphics/14.2-react-tools/react.png",
            },
        ],
    },
    {
        "stem": "14.3-eval-presentations",
        "title": "14.3 Evaluating Applications and Giving the Talk",
        "slides": [
            {
                "title": "A talk is an evaluation story",
                "bullets": [
                    "Question, metric, baseline, ablation, failure case.",
                    "A demo GIF is not a substitute for a number.",
                ],
                "image": "graphics/14.3-eval-presentations/talk.png",
            },
        ],
    },
    {
        "stem": "15.1-exam-review",
        "title": "15.1 Exam Review",
        "slides": [
            {
                "title": "Four modules, one stack",
                "bullets": [
                    "The exam asks you to connect a method to a measurement.",
                    "Remaining talks: Canvas is official. Bring a failure case.",
                ],
                "image": "graphics/15.1-exam-review/map.png",
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
        return f"<h1>{title}</h1><p class='subtitle'>{sub}</p><p class='meta'>{meta}</p>"
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


def write_deck(deck: dict) -> pathlib.Path:
    WORK.mkdir(parents=True, exist_ok=True)
    n = len(deck["slides"])
    slides_html = []
    for i, slide in enumerate(deck["slides"], start=1):
        layout = _infer_layout(slide)
        klass = "slide title-slide" if layout == "title" else "slide"
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
