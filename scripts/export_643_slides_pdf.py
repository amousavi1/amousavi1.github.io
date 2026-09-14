"""Build one-slide-per-page PDFs for DATA 443/643 Week 1."""

from __future__ import annotations

import html as html_lib
import pathlib
import subprocess

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
    for deck in DECKS:
        html_path = write_deck(deck)
        pdf_path = OUT / f"{deck['stem']}.pdf"
        print_pdf(html_path, pdf_path)
        print(f"Wrote {pdf_path.relative_to(ROOT)} ({pdf_path.stat().st_size} bytes)")
    print("done")


if __name__ == "__main__":
    main()
