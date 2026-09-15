"""Pedagogical figures for DATA 443/643 Week 1."""

from __future__ import annotations

import pathlib

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "files" / "data-643" / "graphics"

NAVY = "#1f4e79"
TEAL = "#2a9d8f"
CORAL = "#c45c26"
GOLD = "#c9a227"
SLATE = "#44515c"
FILL = "#eef4f8"
FILL2 = "#e6f4f1"
FILL3 = "#f8eee8"


def _setup():
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 11,
            "axes.titlesize": 13,
            "axes.labelsize": 11,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.facecolor": "white",
            "axes.edgecolor": SLATE,
            "text.color": "#1a1a1a",
            "axes.labelcolor": "#1a1a1a",
            "xtick.color": SLATE,
            "ytick.color": SLATE,
        }
    )


def _save(fig, rel: str):
    path = OUT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180, bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)
    print(path.relative_to(ROOT))


def _box(ax, xy, w, h, text, facecolor=FILL, edge=NAVY, fontsize=10, weight="medium"):
    x, y = xy
    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.02,rounding_size=0.08",
            linewidth=1.6,
            edgecolor=edge,
            facecolor=facecolor,
        )
    )
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fontsize, color=NAVY, fontweight=weight)


def _arrow(ax, start, end, color=NAVY):
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=12,
            linewidth=1.5,
            color=color,
            shrinkA=1,
            shrinkB=1,
        )
    )


def roadmap():
    fig, ax = plt.subplots(figsize=(10.2, 3.4))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 3.2)
    ax.axis("off")
    modules = [
        (0.25, "Module 1\nWeeks 1–3\nNets, sequences,\nattention", FILL),
        (3.2, "Module 2\nWeeks 4–6\nVision, language,\naudio", FILL2),
        (6.15, "Module 3\nWeeks 7–10\nScale, align,\nadapt", FILL3),
        (9.1, "Module 4\nWeeks 11–14\nGenerate, reason,\nuse tools", "#f4f0e6"),
    ]
    for x, text, fill in modules:
        _box(ax, (x, 0.55), 2.55, 2.15, text, facecolor=fill, fontsize=10)
    for x in (2.85, 5.8, 8.75):
        _arrow(ax, (x, 1.6), (x + 0.3, 1.6))
    ax.set_title("Where Week 1 sits: foundations before transformers", loc="left", color=NAVY, pad=8)
    _save(fig, "1.1-course-map/roadmap.png")


def stack():
    fig, ax = plt.subplots(figsize=(9.4, 4.6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.2)
    ax.axis("off")
    layers = [
        ("Applications: RAG, tools, multimodal products", GOLD, 5.15),
        ("Alignment and adaptation: SFT, RLHF, LoRA, retrieval", CORAL, 4.05),
        ("Transformer: self-attention over token embeddings", TEAL, 2.95),
        ("Token embeddings: distributed word (and later patch) vectors", NAVY, 1.85),
        ("This week: neurons, activations, gradient descent", SLATE, 0.55),
    ]
    for text, edge, y in layers:
        _box(ax, (0.4, y), 9.2, 0.95, text, facecolor="white", edge=edge, fontsize=11)
    ax.set_title("A language model is a stack. Week 1 is the bottom two layers.", loc="left", color=NAVY, pad=6)
    _save(fig, "1.1-course-map/stack.png")


def neuron():
    fig, ax = plt.subplots(figsize=(9.6, 4.2))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis("off")
    inputs = [(1.2, 4.7, r"$x_1$"), (1.2, 3.0, r"$x_2$"), (1.2, 1.3, r"$x_3$")]
    for x, y, lab in inputs:
        ax.add_patch(Circle((x, y), 0.38, facecolor=FILL, edgecolor=NAVY, linewidth=1.6))
        ax.text(x, y, lab, ha="center", va="center", fontsize=12, color=NAVY)
    ax.add_patch(Circle((6.2, 3.0), 0.72, facecolor=FILL2, edgecolor=TEAL, linewidth=1.8))
    ax.text(6.2, 3.0, r"$\sum$", ha="center", va="center", fontsize=16, color=TEAL)
    ax.add_patch(
        FancyBboxPatch((8.35, 2.35), 2.4, 1.3, boxstyle="round,pad=0.03,rounding_size=0.1", facecolor=FILL3, edgecolor=CORAL, linewidth=1.6)
    )
    ax.text(9.55, 3.0, r"$\sigma(\cdot)$", ha="center", va="center", fontsize=14, color=CORAL)
    for x, y, _ in inputs:
        _arrow(ax, (x + 0.42, y), (5.5, 3.0), color=NAVY)
    _arrow(ax, (6.95, 3.0), (8.3, 3.0), color=TEAL)
    ax.add_patch(Circle((11.35, 3.0), 0.38, facecolor=FILL, edgecolor=NAVY, linewidth=1.6))
    ax.text(11.35, 3.0, r"$a$", ha="center", va="center", fontsize=12, color=NAVY)
    _arrow(ax, (10.78, 3.0), (10.95, 3.0), color=CORAL)
    ax.text(3.55, 4.55, r"$w_1$", color=NAVY, fontsize=11)
    ax.text(3.7, 3.35, r"$w_2$", color=NAVY, fontsize=11)
    ax.text(3.55, 1.55, r"$w_3$", color=NAVY, fontsize=11)
    ax.text(7.35, 3.55, r"$z$", color=TEAL, fontsize=11)
    ax.text(6.2, 1.55, r"$z = w^\top x + b$", ha="center", fontsize=12, color=SLATE)
    ax.set_title("One neuron: weighted sum, then a nonlinearity", loc="left", color=NAVY)
    _save(fig, "1.2-neurons-activations/neuron.png")


def activations():
    x = np.linspace(-4.5, 4.5, 400)
    fig, axes = plt.subplots(1, 2, figsize=(9.8, 3.7))
    axes[0].plot(x, 1 / (1 + np.exp(-x)), color=TEAL, lw=2.2, label="sigmoid")
    axes[0].plot(x, np.tanh(x), color=NAVY, lw=2.2, label="tanh")
    axes[0].plot(x, np.maximum(0, x), color=CORAL, lw=2.2, label="ReLU")
    axes[0].axhline(0, color="#ccc", lw=0.8)
    axes[0].axvline(0, color="#ccc", lw=0.8)
    axes[0].set_title("Activation")
    axes[0].legend(frameon=False, loc="upper left")
    axes[0].set_ylim(-1.3, 4.2)
    sig = 1 / (1 + np.exp(-x))
    axes[1].plot(x, sig * (1 - sig), color=TEAL, lw=2.2, label="sigmoid'")
    axes[1].plot(x, 1 - np.tanh(x) ** 2, color=NAVY, lw=2.2, label="tanh'")
    axes[1].plot(x, (x > 0).astype(float), color=CORAL, lw=2.2, label="ReLU'")
    axes[1].axhline(0, color="#ccc", lw=0.8)
    axes[1].axvline(0, color="#ccc", lw=0.8)
    axes[1].set_title("Derivative")
    axes[1].legend(frameon=False, loc="upper right")
    axes[1].set_ylim(-0.15, 1.25)
    for ax in axes:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    fig.suptitle("Without a nonlinearity, stacked layers collapse to one linear map", color=NAVY, y=1.02)
    fig.tight_layout()
    _save(fig, "1.2-neurons-activations/activations.png")


def feedforward():
    fig, ax = plt.subplots(figsize=(9.8, 4.6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.4)
    ax.axis("off")
    cols = [
        (1.3, [1.2, 2.4, 3.6, 4.8], "input\n$x$"),
        (4.3, [1.8, 3.2, 4.6], "hidden\n$a^{(1)}$"),
        (7.3, [1.8, 3.2, 4.6], "hidden\n$a^{(2)}$"),
        (10.3, [2.5, 3.9], "output\n$\\hat{y}$"),
    ]
    nodes = []
    for x, ys, label in cols:
        col_nodes = []
        for y in ys:
            ax.add_patch(Circle((x, y), 0.32, facecolor=FILL, edgecolor=NAVY, linewidth=1.5))
            col_nodes.append((x, y))
        ax.text(x, 0.55, label, ha="center", va="center", fontsize=10, color=SLATE)
        nodes.append(col_nodes)
    for i in range(len(nodes) - 1):
        for a in nodes[i]:
            for b in nodes[i + 1]:
                ax.plot([a[0] + 0.32, b[0] - 0.32], [a[1], b[1]], color="#9bb4c9", lw=0.7, zorder=0)
    ax.set_title("A feedforward net: each layer is $a^{\\ell}=\\sigma(W^{\\ell}a^{\\ell-1}+b^{\\ell})$", loc="left", color=NAVY)
    _save(fig, "1.2-neurons-activations/feedforward.png")


def xor_sep():
    rng = np.random.default_rng(3)
    fig, axes = plt.subplots(1, 2, figsize=(9.4, 3.8))
    pts = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
    labs = np.array([0, 1, 1, 0])
    jitter = rng.normal(0, 0.04, pts.shape)
    p = pts + jitter
    axes[0].scatter(p[labs == 0, 0], p[labs == 0, 1], c=NAVY, s=70, label="class 0")
    axes[0].scatter(p[labs == 1, 0], p[labs == 1, 1], c=CORAL, s=70, label="class 1")
    axes[0].plot([-0.2, 1.2], [0.15, 0.85], color=TEAL, lw=1.6, ls="--")
    axes[0].set_title("One linear cut cannot do XOR")
    axes[0].legend(frameon=False, loc="upper right")
    axes[1].scatter(p[labs == 0, 0], p[labs == 0, 1], c=NAVY, s=70)
    axes[1].scatter(p[labs == 1, 0], p[labs == 1, 1], c=CORAL, s=70)
    t = np.linspace(-0.2, 1.2, 200)
    axes[1].plot(t, 0.5 + 0.42 * np.sin(2 * np.pi * t), color=TEAL, lw=1.8)
    axes[1].set_title("A hidden layer can bend the boundary")
    for ax in axes:
        ax.set_xlim(-0.25, 1.25)
        ax.set_ylim(-0.25, 1.25)
        ax.set_aspect("equal")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1])
    fig.tight_layout()
    _save(fig, "1.2-neurons-activations/xor.png")


def loss_surface():
    u = np.linspace(-2.2, 2.2, 200)
    v = np.linspace(-2.2, 2.2, 200)
    U, V = np.meshgrid(u, v)
    Z = 0.55 * U**2 + 1.6 * V**2
    fig, ax = plt.subplots(figsize=(6.6, 4.8))
    cs = ax.contour(U, V, Z, levels=12, colors=NAVY, linewidths=0.9, alpha=0.7)
    ax.clabel(cs, inline=True, fontsize=7, fmt="%.1f")
    path_x = [-1.85, -1.2, -0.75, -0.42, -0.22, -0.1, -0.04]
    path_y = [1.7, 0.85, 0.4, 0.18, 0.08, 0.03, 0.01]
    ax.plot(path_x, path_y, color=CORAL, lw=2.2, marker="o", ms=5)
    ax.scatter([0], [0], c=TEAL, s=80, zorder=5)
    ax.text(0.08, -0.28, "min", color=TEAL, fontsize=11)
    ax.set_xlabel(r"$w_1$")
    ax.set_ylabel(r"$w_2$")
    ax.set_title("Gradient descent walks downhill on the loss")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    _save(fig, "1.3-gradient-descent/loss-surface.png")


def gd_1d():
    x = np.linspace(-3.2, 3.2, 400)
    f = 0.35 * x**2 + 0.15 * np.sin(3 * x) + 0.4
    fig, ax = plt.subplots(figsize=(8.4, 3.8))
    ax.plot(x, f, color=NAVY, lw=2.2)
    xs = [2.5, 1.55, 0.85, 0.35, 0.08]
    ys = [0.35 * t**2 + 0.15 * np.sin(3 * t) + 0.4 for t in xs]
    ax.plot(xs, ys, color=CORAL, marker="o", lw=1.8, ms=7)
    ax.annotate("too large a step\ncan overshoot", xy=(xs[0], ys[0]), xytext=(1.6, 3.1),
                arrowprops=dict(arrowstyle="->", color=SLATE), color=SLATE, fontsize=9)
    ax.set_xlabel(r"$w$")
    ax.set_ylabel(r"$L(w)$")
    ax.set_title(r"Update: $w \leftarrow w - \eta\nabla L(w)$")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    _save(fig, "1.3-gradient-descent/gd-1d.png")


def train_loop():
    fig, ax = plt.subplots(figsize=(10.0, 3.6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 3.4)
    ax.axis("off")
    boxes = [
        (0.25, "Forward\ncompute $\\hat{y}$", FILL),
        (3.2, "Loss\n$L(\\hat{y}, y)$", FILL2),
        (6.15, "Backward\n$\\nabla_w L$", FILL3),
        (9.1, "Update\n$w \\leftarrow w-\\eta\\nabla L$", "#f4f0e6"),
    ]
    for x, text, fill in boxes:
        _box(ax, (x, 0.85), 2.55, 1.7, text, facecolor=fill, fontsize=11)
    for x in (2.85, 5.8, 8.75):
        _arrow(ax, (x, 1.7), (x + 0.3, 1.7))
    ax.annotate(
        "repeat over batches / epochs",
        xy=(10.35, 0.7),
        xytext=(0.4, 0.25),
        arrowprops=dict(arrowstyle="->", color=SLATE, connectionstyle="arc3,rad=0.18"),
        color=SLATE,
        fontsize=10,
    )
    ax.set_title("Training a net is this loop. Backprop is just the chain rule.", loc="left", color=NAVY)
    _save(fig, "1.3-gradient-descent/train-loop.png")


def onehot_vs_embed():
    fig, axes = plt.subplots(1, 2, figsize=(9.8, 3.9))
    vocab = ["cat", "dog", "king", "movie", "film"]
    onehot = np.eye(len(vocab))
    axes[0].imshow(onehot, cmap="Blues", vmin=0, vmax=1)
    axes[0].set_xticks(range(5))
    axes[0].set_xticklabels(vocab, rotation=30, ha="right")
    axes[0].set_yticks(range(5))
    axes[0].set_yticklabels(vocab)
    axes[0].set_title("One-hot: orthogonal, sparse")
    embed = np.array(
        [
            [0.82, 0.11, -0.05, 0.20],
            [0.77, 0.18, -0.02, 0.14],
            [-0.12, 0.74, 0.41, -0.10],
            [0.08, -0.15, 0.71, 0.52],
            [0.10, -0.12, 0.68, 0.49],
        ]
    )
    im = axes[1].imshow(embed, cmap="coolwarm", vmin=-1, vmax=1)
    axes[1].set_xticks(range(4))
    axes[1].set_xticklabels([f"d{i+1}" for i in range(4)])
    axes[1].set_yticks(range(5))
    axes[1].set_yticklabels(vocab)
    axes[1].set_title("Embedding: dense, similar rows sit nearby")
    fig.colorbar(im, ax=axes[1], fraction=0.046, pad=0.04)
    fig.tight_layout()
    _save(fig, "1.4-embeddings/onehot-vs-embed.png")


def semantic_geometry():
    fig, ax = plt.subplots(figsize=(6.8, 5.2))
    pts = {
        "man": (0.4, 3.2),
        "woman": (0.55, 1.15),
        "king": (2.55, 3.35),
        "queen": (2.7, 1.3),
    }
    ax.scatter(*zip(*pts.values()), c=[NAVY, CORAL, NAVY, CORAL], s=90, zorder=3)
    for name, (x, y) in pts.items():
        ax.text(x + 0.08, y + 0.12, name, fontsize=12, color=NAVY)
    ax.annotate("", xy=pts["king"], xytext=pts["man"], arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.8))
    ax.annotate("", xy=pts["queen"], xytext=pts["woman"], arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.8))
    ax.annotate("", xy=pts["woman"], xytext=pts["man"], arrowprops=dict(arrowstyle="->", color=CORAL, lw=1.6, ls="--"))
    ax.annotate("", xy=pts["queen"], xytext=pts["king"], arrowprops=dict(arrowstyle="->", color=CORAL, lw=1.6, ls="--"))
    ax.text(1.35, 3.55, "royal", color=TEAL, fontsize=11)
    ax.text(-0.05, 2.15, "gender", color=CORAL, fontsize=11)
    ax.set_xlim(-0.4, 3.5)
    ax.set_ylim(0.6, 4.0)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(r"king $-$ man $+$ woman $\approx$ queen")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    _save(fig, "1.4-embeddings/semantic-geometry.png")


def skipgram():
    fig, ax = plt.subplots(figsize=(10.2, 3.2))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 3.3)
    ax.axis("off")
    words = ["The", "cat", "sat", "on", "the", "mat"]
    xs = np.linspace(0.85, 11.1, len(words))
    ax.add_patch(
        FancyBboxPatch(
            (xs[0] - 0.82, 1.18),
            (xs[4] - xs[0]) + 1.64,
            1.32,
            boxstyle="round,pad=0.02,rounding_size=0.08",
            linewidth=0,
            facecolor=FILL2,
            zorder=0,
        )
    )
    for i, (x, w) in enumerate(zip(xs, words)):
        face = FILL3 if w == "sat" else "white"
        edge = CORAL if w == "sat" else (TEAL if abs(i - 2) <= 2 else NAVY)
        _box(ax, (x - 0.7, 1.35), 1.4, 0.95, w, facecolor=face, edge=edge, fontsize=12)
    ax.annotate(
        "center",
        xy=(xs[2], 2.4),
        xytext=(xs[2], 2.95),
        ha="center",
        color=CORAL,
        fontsize=11,
        arrowprops=dict(arrowstyle="->", color=CORAL),
    )
    ax.text((xs[0] + xs[4]) / 2, 0.55, "context window (size 2)", ha="center", color=TEAL, fontsize=11)
    ax.set_title("Skip-gram: predict each neighbor from the center word", loc="left", color=NAVY)
    _save(fig, "1.4-embeddings/skipgram-window.png")


def eval_two_ways():
    fig, ax = plt.subplots(figsize=(9.8, 3.8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4.2)
    ax.axis("off")
    _box(ax, (0.3, 1.5), 2.6, 1.4, "Embedding\nspace", FILL, fontsize=11)
    _box(ax, (4.3, 2.45), 3.3, 1.35, "Intrinsic\nanalogy, similarity, clustering", FILL2, fontsize=11)
    _box(ax, (4.3, 0.45), 3.3, 1.35, "Extrinsic\ndoes a downstream model improve?", FILL3, fontsize=11)
    _box(ax, (8.6, 1.5), 3.0, 1.4, "A number\nyou can report", "#f4f0e6", fontsize=11)
    _arrow(ax, (2.95, 2.2), (4.25, 3.05), TEAL)
    _arrow(ax, (2.95, 2.2), (4.25, 1.15), CORAL)
    _arrow(ax, (7.65, 3.1), (8.55, 2.35), TEAL)
    _arrow(ax, (7.65, 1.15), (8.55, 2.05), CORAL)
    ax.set_title("Two ways to score embeddings. They need not agree.", loc="left", color=NAVY)
    _save(fig, "1.4-embeddings/intrinsic-extrinsic.png")


def bias_offset():
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    jobs = {
        "nurse": (0.7, 0.9),
        "receptionist": (1.1, 1.35),
        "engineer": (3.1, 3.15),
        "physicist": (3.5, 3.55),
    }
    ax.scatter(*zip(*jobs.values()), c=NAVY, s=70, zorder=3)
    for name, (x, y) in jobs.items():
        ax.text(x + 0.08, y + 0.08, name, fontsize=11, color=NAVY)
    ax.annotate("", xy=(2.4, 2.4), xytext=(1.2, 1.2), arrowprops=dict(arrowstyle="->", color=CORAL, lw=2))
    ax.text(1.55, 2.15, "she  →  he\noffset", color=CORAL, fontsize=10)
    ax.set_xlim(0.2, 4.2)
    ax.set_ylim(0.4, 4.0)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Geometry can encode stereotypes as well as meaning")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    _save(fig, "1.4-embeddings/bias-geometry.png")


def xor_table():
    fig, ax = plt.subplots(figsize=(8.4, 3.4))
    ax.axis("off")
    cols = [r"$(x_1,x_2)$", r"$a_1=\mathrm{ReLU}(x_1+x_2)$", r"$a_2=\mathrm{ReLU}(x_1+x_2-1)$", r"$\hat{y}=a_1-2a_2$"]
    rows = [
        ["(0, 0)", "0", "0", "0"],
        ["(0, 1)", "1", "0", "1"],
        ["(1, 0)", "1", "0", "1"],
        ["(1, 1)", "2", "1", "0"],
    ]
    table = ax.table(cellText=rows, colLabels=cols, loc="center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1.15, 1.7)
    for (r, c), cell in table.get_celld().items():
        cell.set_edgecolor(SLATE)
        if r == 0:
            cell.set_facecolor(FILL)
            cell.get_text().set_color(NAVY)
        elif c == 3:
            cell.set_facecolor(FILL2)
    ax.set_title("XOR with two ReLUs: OR, AND, then subtract (Goodfellow 6.1)", loc="left", color=NAVY)
    _save(fig, "1.2-neurons-activations/xor-table.png")


def softmax_bars():
    z = np.array([1.0, 0.5, 0.0])
    p = np.exp(z) / np.exp(z).sum()
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    names = ["cat", "mat", "sat"]
    ax.bar(names, p, color=[TEAL, GOLD, CORAL], edgecolor=NAVY, linewidth=1.2)
    ax.set_ylim(0, 0.65)
    ax.set_ylabel("softmax probability")
    for i, v in enumerate(p):
        ax.text(i, v + 0.02, f"{v:.2f}", ha="center", color=NAVY)
    ax.set_title(r"Skip-gram toy: $P(w\mid v_c)$ for $V=3$, scores $u^\top v_c=(1,0.5,0)$", loc="left", color=NAVY)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    _save(fig, "1.4-embeddings/skipgram-softmax.png")


def backprop_gates():
    fig, ax = plt.subplots(figsize=(10.2, 3.2))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 3.4)
    ax.axis("off")
    _box(ax, (0.2, 1.1), 2.0, 1.2, r"$x$", FILL3, fontsize=13)
    _box(ax, (2.8, 1.1), 2.2, 1.2, r"$z=w^\top x+b$", FILL, fontsize=11)
    _box(ax, (5.6, 1.1), 2.2, 1.2, r"$a=\mathrm{ReLU}(z)$", FILL2, fontsize=11)
    _box(ax, (8.4, 1.1), 3.2, 1.2, r"$L=\frac{1}{2}(a-y)^2$", FILL, fontsize=12)
    _arrow(ax, (2.25, 1.7), (2.75, 1.7), CORAL)
    _arrow(ax, (5.05, 1.7), (5.55, 1.7), TEAL)
    _arrow(ax, (7.85, 1.7), (8.35, 1.7), NAVY)
    ax.text(6.0, 0.35, r"backward: $(a-y)\cdot 1_{z>0}\cdot x$  (CS231N: local $\times$ upstream)", fontsize=11, color=SLATE)
    ax.set_title("One ReLU unit: cache $x$ and $z$; autograd is this chain", loc="left", color=NAVY)
    _save(fig, "1.3-gradient-descent/one-unit-backprop.png")


def main():
    _setup()
    roadmap()
    stack()
    neuron()
    activations()
    feedforward()
    xor_sep()
    xor_table()
    loss_surface()
    gd_1d()
    train_loop()
    backprop_gates()
    onehot_vs_embed()
    semantic_geometry()
    skipgram()
    softmax_bars()
    eval_two_ways()
    bias_offset()
    print("done")


if __name__ == "__main__":
    main()
