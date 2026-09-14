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
@page { size: letter landscape; margin: 0.42in; }
html, body { margin: 0; padding: 0; }
body {
  font-family: "Segoe UI", "Helvetica Neue", Helvetica, Arial, sans-serif;
  color: #1a1a1a;
}
.slide {
  page-break-after: always;
  height: 7.15in;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
}
.slide:last-child { page-break-after: auto; }
.kicker { margin: 0; color: #5f6368; font-size: 12pt; }
h1 {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 26pt;
  line-height: 1.2;
  margin: 0.12em 0 0.35em;
  color: #1f4e79;
}
ul { margin: 0.15em 0 0.4em; padding-left: 1.2em; font-size: 16pt; line-height: 1.35; }
li { margin: 0.18em 0; }
.fig {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 0;
}
.fig img {
  max-width: 100%;
  max-height: 4.55in;
  object-fit: contain;
}
"""

DECKS = [
    {
        "stem": "1.1-course-map",
        "title": "1.1 Course Map and the Semester Project",
        "slides": [
            {
                "title": "A self-contained LLM course",
                "bullets": [
                    "DATA 441/641 and 442/642 are not prerequisites.",
                    "Listed prereq: DATA 427/627.",
                    "Overlap with those courses is intentional: more people can take this.",
                    "The semester is a project. Lectures exist so that project has a backbone.",
                ],
                "image": "graphics/1.1-course-map/roadmap.png",
            },
            {
                "title": "A language model is a stack",
                "bullets": [
                    "Week 1 is the bottom: neurons, training, word vectors.",
                    "Week 3 puts attention on those vectors.",
                    "Later weeks align, retrieve, generate, and use tools.",
                ],
                "image": "graphics/1.1-course-map/stack.png",
            },
            {
                "title": "The project starts this week",
                "bullets": [
                    "A question you can measure, a public dataset, a baseline, one justified change.",
                    "Undergraduate: group report and talk. Graduate: main project plus a paper mini-project.",
                    "Lab 1 ends with a five-line topic seed. You may change it.",
                ],
            },
        ],
    },
    {
        "stem": "1.2-neurons-activations",
        "title": "1.2 Neurons, Activations, and Feedforward Nets",
        "slides": [
            {
                "title": "One neuron",
                "bullets": [
                    r"Pre-activation \(z = w^\top x + b\), then \(a = \sigma(z)\).",
                    r"\(w\) and \(b\) are the parameters you train.",
                    "ReLU in hidden layers; softmax when classes compete.",
                ],
                "image": "graphics/1.2-neurons-activations/neuron.png",
            },
            {
                "title": "The nonlinearity is the point",
                "bullets": [
                    "Two affine maps compose to one affine map.",
                    r"Without \(\sigma\), depth does not add power.",
                    "Sigmoid saturates. ReLU is cheap and sparse.",
                ],
                "image": "graphics/1.2-neurons-activations/activations.png",
            },
            {
                "title": "A feedforward net",
                "bullets": [
                    r"Layer \(\ell\): \(a^{(\ell)} = \sigma(W^{(\ell)} a^{(\ell-1)} + b^{(\ell)})\).",
                    r"\(a^{(0)} = x\). Every arrow is one weight.",
                ],
                "image": "graphics/1.2-neurons-activations/feedforward.png",
            },
            {
                "title": "XOR: why a hidden layer exists",
                "bullets": [
                    "One linear unit cannot separate XOR.",
                    "A small MLP can fold the space so the classes split.",
                    "Language models stack many such nonlinear maps.",
                ],
                "image": "graphics/1.2-neurons-activations/xor.png",
            },
        ],
    },
    {
        "stem": "1.3-gradient-descent",
        "title": "1.3 Gradient Descent",
        "slides": [
            {
                "title": "Training is walking downhill",
                "bullets": [
                    r"Pack weights into \(\theta\). Loss \(L(\theta)\) is a scalar.",
                    "The gradient points uphill. We step the other way.",
                ],
                "image": "graphics/1.3-gradient-descent/loss-surface.png",
            },
            {
                "title": "The update and the learning rate",
                "bullets": [
                    r"\(\theta \leftarrow \theta - \eta \nabla L(\theta)\).",
                    "Too small: crawl. Too large: overshoot.",
                    "SGD estimates the gradient on a minibatch.",
                ],
                "image": "graphics/1.3-gradient-descent/gd-1d.png",
            },
            {
                "title": "Forward, loss, backward, update",
                "bullets": [
                    "Keep activations: the backward pass needs them.",
                    "Backprop is the chain rule. PyTorch does it if the graph is differentiable.",
                    r"Pretraining and fine-tuning are this loop with different data and \(L\).",
                ],
                "image": "graphics/1.3-gradient-descent/train-loop.png",
            },
        ],
    },
    {
        "stem": "1.4-embeddings",
        "title": "1.4 Word Embeddings and Semantic Geometry",
        "slides": [
            {
                "title": "One-hot is a bad geometry",
                "bullets": [
                    "film and movie are orthogonal. New words have no coordinate.",
                    "Distributed = short, dense. Similar usage → similar vectors.",
                    "An embedding is the map from a token id into that space.",
                ],
                "image": "graphics/1.4-embeddings/onehot-vs-embed.png",
            },
            {
                "title": "Direction can mean something",
                "bullets": [
                    r"king − man + woman ≈ queen.",
                    "Cosine, not Euclidean length (length tracks frequency).",
                    "Nearest neighbors are a debug tool.",
                ],
                "image": "graphics/1.4-embeddings/semantic-geometry.png",
            },
            {
                "title": "Skip-gram learns the map",
                "bullets": [
                    "Fake task: from the center, predict each neighbor.",
                    "Keep the hidden weights. Throw away the softmax.",
                    "A transformer keeps transforming those vectors instead.",
                ],
                "image": "graphics/1.4-embeddings/skipgram-window.png",
            },
            {
                "title": "Intrinsic vs. extrinsic",
                "bullets": [
                    "Intrinsic: analogies, similarity, clustering of the space.",
                    "Extrinsic: does a downstream model improve?",
                    "They need not agree. Projects report extrinsic.",
                ],
                "image": "graphics/1.4-embeddings/intrinsic-extrinsic.png",
            },
            {
                "title": "Bias is also geometry",
                "bullets": [
                    "The same offsets can encode stereotypes.",
                    "Probe occupations along a she/he direction.",
                    "Lab 1 does this on a constructed 2-D space first.",
                ],
                "image": "graphics/1.4-embeddings/bias-geometry.png",
            },
        ],
    },
    {
        "stem": "2.1-sequence-rnns",
        "title": "2.1 Sequential Models and RNNs",
        "slides": [
            {
                "title": "A cell with memory",
                "bullets": [
                    r"Each step: \(x_t\) and \(h_{t-1}\) become \(h_t\).",
                    "The same weights at every token.",
                    "Reset the state between unrelated documents.",
                ],
                "image": "graphics/2.1-sequence-rnns/rnn-cell.png",
            },
            {
                "title": "Unrolled in time",
                "bullets": [
                    "The loop is a chain. That chain is the long-range path.",
                    "A CNN is parallel with a fixed window. An RNN is sequential with the whole past.",
                ],
                "image": "graphics/2.1-sequence-rnns/rnn-unroll.png",
            },
        ],
    },
    {
        "stem": "2.2-vanishing-gradients",
        "title": "2.2 Vanishing and Exploding Gradients",
        "slides": [
            {
                "title": "A product of many Jacobians",
                "bullets": [
                    r"\(\partial L / \partial h_1\) multiplies one factor per step.",
                    r"\(\tanh'\) is at most 1, and usually much smaller.",
                    "Gates keep a path whose multiplier can stay near 1.",
                ],
                "image": "graphics/2.2-vanishing-gradients/vanish.png",
            },
            {
                "title": "Two failure modes",
                "bullets": [
                    "Vanishing: early tokens do not train.",
                    "Exploding: NaNs. Clipping helps explosions, not vanishing.",
                ],
                "image": "graphics/2.2-vanishing-gradients/vanish-explode.png",
            },
        ],
    },
    {
        "stem": "2.3-lstm-gru",
        "title": "2.3 LSTMs and GRUs",
        "slides": [
            {
                "title": "LSTM: a highway plus three gates",
                "bullets": [
                    "Forget, input, output. The cell can copy.",
                    r"If \(f_t \approx 1\) and \(i_t \approx 0\), memory persists.",
                ],
                "image": "graphics/2.3-lstm-gru/lstm-gates.png",
            },
            {
                "title": "GRU: two gates",
                "bullets": [
                    "Reset and update. The hidden state is the memory.",
                    "Still a loop: better than vanilla, worse than attention at long range.",
                ],
                "image": "graphics/2.3-lstm-gru/gru-gates.png",
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
]


def _tex_to_html(text: str) -> str:
    out = []
    i = 0
    while i < len(text):
        if text.startswith("\\(", i):
            j = text.find("\\)", i + 2)
            if j == -1:
                out.append(html_lib.escape(text[i:]))
                break
            try:
                from latex2mathml.converter import convert

                out.append(convert(text[i + 2 : j].strip(), display="inline"))
            except Exception:
                out.append(html_lib.escape(text[i : j + 2]))
            i = j + 2
            continue
        nxt = text.find("\\(", i)
        chunk = text[i:] if nxt == -1 else text[i:nxt]
        out.append(html_lib.escape(chunk))
        if nxt == -1:
            break
        i = nxt
    return "".join(out)


def write_deck(deck: dict) -> pathlib.Path:
    WORK.mkdir(parents=True, exist_ok=True)
    slides_html = []
    for slide in deck["slides"]:
        bullets = "".join(f"<li>{_tex_to_html(b)}</li>" for b in slide.get("bullets") or [])
        fig = ""
        image = slide.get("image")
        if image:
            src = (FILES / image).resolve().as_uri()
            fig = f'<div class="fig"><img src="{src}" alt="" /></div>'
        slides_html.append(
            f"""<section class="slide">
  <p class="kicker">{COURSE} &middot; {html_lib.escape(deck["title"])}</p>
  <h1>{html_lib.escape(slide["title"])}</h1>
  <ul>{bullets}</ul>
  {fig}
</section>"""
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
