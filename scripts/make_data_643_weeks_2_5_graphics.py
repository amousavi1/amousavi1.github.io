"""Pedagogical figures for DATA 443/643 Weeks 2–5."""

from __future__ import annotations

import pathlib

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

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
FILL4 = "#f4f0e6"


def _setup():
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 11,
            "axes.titlesize": 13,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.facecolor": "white",
            "axes.edgecolor": SLATE,
            "text.color": "#1a1a1a",
        }
    )


def _save(fig, rel: str):
    path = OUT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180, bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)
    print(path.relative_to(ROOT))


def _box(ax, xy, w, h, text, facecolor=FILL, edge=NAVY, fontsize=10):
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
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fontsize, color=NAVY)


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


def rnn_cell():
    fig, ax = plt.subplots(figsize=(8.8, 4.2))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 5)
    ax.axis("off")
    _box(ax, (0.4, 2.05), 2.1, 1.1, r"$h_{t-1}$", FILL, NAVY, 13)
    _box(ax, (4.0, 2.0), 2.6, 1.2, "RNN cell", FILL2, TEAL, 13)
    _box(ax, (8.3, 2.05), 2.1, 1.1, r"$h_t$", FILL, NAVY, 13)
    _box(ax, (4.25, 0.35), 2.1, 0.95, r"$x_t$", FILL3, CORAL, 13)
    _arrow(ax, (2.55, 2.6), (3.95, 2.6))
    _arrow(ax, (6.65, 2.6), (8.25, 2.6), TEAL)
    _arrow(ax, (5.3, 1.35), (5.3, 1.95), CORAL)
    ax.set_title("Same weights at every step: input plus previous state", loc="left", color=NAVY)
    _save(fig, "2.1-sequence-rnns/rnn-cell.png")


def rnn_unroll():
    fig, ax = plt.subplots(figsize=(10.4, 3.8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4.2)
    ax.axis("off")
    xs = [0.4, 3.5, 6.6, 9.7]
    labs = [r"$x_1$", r"$x_2$", r"$x_3$", r"$x_4$"]
    hs = [r"$h_1$", r"$h_2$", r"$h_3$", r"$h_4$"]
    for i, x in enumerate(xs):
        _box(ax, (x, 0.35), 1.7, 0.85, labs[i], FILL3, CORAL, 12)
        _box(ax, (x, 1.7), 1.7, 1.0, "cell", FILL2, TEAL, 11)
        _box(ax, (x, 3.1), 1.7, 0.75, hs[i], FILL, NAVY, 12)
        _arrow(ax, (x + 0.85, 1.2), (x + 0.85, 1.65), CORAL)
        _arrow(ax, (x + 0.85, 2.75), (x + 0.85, 3.05), TEAL)
        if i < 3:
            _arrow(ax, (x + 1.75, 2.2), (xs[i + 1], 2.2))
    ax.set_title("Unrolled in time. The chain is why long-range gradients struggle.", loc="left", color=NAVY)
    _save(fig, "2.1-sequence-rnns/rnn-unroll.png")


def vanishing():
    t = np.arange(1, 31)
    tanh_prod = 0.6 ** t
    gate_prod = 0.97 ** t
    fig, ax = plt.subplots(figsize=(8.2, 3.8))
    ax.semilogy(t, tanh_prod, color=CORAL, lw=2.2, label=r"vanilla RNN ($\approx 0.6^t$)")
    ax.semilogy(t, gate_prod, color=TEAL, lw=2.2, label=r"gated path ($\approx 0.97^t$)")
    ax.set_xlabel("steps back in time")
    ax.set_ylabel("gradient scale (log)")
    ax.legend(frameon=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_title("A product of many small derivatives kills the early-token signal")
    _save(fig, "2.2-vanishing-gradients/vanish.png")


def explode_vs_vanish():
    fig, axes = plt.subplots(1, 2, figsize=(9.4, 3.5))
    t = np.linspace(0, 8, 200)
    axes[0].plot(t, np.exp(-0.55 * t), color=CORAL, lw=2.2)
    axes[0].set_title("Vanishing")
    axes[0].set_ylabel("signal")
    axes[1].plot(t, np.exp(0.45 * t), color=NAVY, lw=2.2)
    axes[1].set_title("Exploding")
    for ax in axes:
        ax.set_xlabel("depth / time")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    fig.tight_layout()
    _save(fig, "2.2-vanishing-gradients/vanish-explode.png")


def lstm_gates():
    fig, ax = plt.subplots(figsize=(10.2, 4.4))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5)
    ax.axis("off")
    _box(ax, (0.3, 2.1), 1.7, 0.9, r"$x_t, h_{t-1}$", FILL, NAVY, 10)
    _box(ax, (2.6, 3.55), 2.1, 0.85, "forget $f_t$", FILL3, CORAL, 11)
    _box(ax, (2.6, 2.15), 2.1, 0.85, "input $i_t$", FILL2, TEAL, 11)
    _box(ax, (2.6, 0.75), 2.1, 0.85, "output $o_t$", FILL4, GOLD, 11)
    _box(ax, (5.5, 1.85), 2.6, 1.4, r"cell $c_t$" + "\n(highway)", FILL, NAVY, 12)
    _box(ax, (8.9, 2.1), 2.5, 0.9, r"$h_t = o_t \cdot \tanh(c_t)$", FILL2, TEAL, 10)
    _arrow(ax, (2.05, 2.55), (2.55, 3.9), CORAL)
    _arrow(ax, (2.05, 2.55), (2.55, 2.55), TEAL)
    _arrow(ax, (2.05, 2.55), (2.55, 1.15), GOLD)
    _arrow(ax, (4.75, 3.95), (6.4, 3.25), CORAL)
    _arrow(ax, (4.75, 2.55), (5.45, 2.55), TEAL)
    _arrow(ax, (8.15, 2.55), (8.85, 2.55))
    ax.set_title("LSTM: a cell highway plus learned gates", loc="left", color=NAVY)
    _save(fig, "2.3-lstm-gru/lstm-gates.png")


def gru_gates():
    fig, ax = plt.subplots(figsize=(9.6, 3.6))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 3.6)
    ax.axis("off")
    _box(ax, (0.35, 1.25), 2.3, 1.1, r"$x_t, h_{t-1}$", FILL, NAVY, 12)
    _box(ax, (3.4, 2.15), 2.4, 0.95, "reset $r_t$", FILL3, CORAL, 12)
    _box(ax, (3.4, 0.55), 2.4, 0.95, "update $z_t$", FILL2, TEAL, 12)
    _box(ax, (6.7, 1.2), 3.7, 1.2, r"$h_t=(1-z)\cdot h_{t-1}+z\cdot\tilde{h}$", FILL4, GOLD, 10)
    _arrow(ax, (2.7, 1.8), (3.35, 2.55), CORAL)
    _arrow(ax, (2.7, 1.8), (3.35, 1.0), TEAL)
    _arrow(ax, (5.85, 2.6), (6.65, 1.95), CORAL)
    _arrow(ax, (5.85, 1.0), (6.65, 1.6), TEAL)
    ax.set_title("GRU: two gates, no separate cell state", loc="left", color=NAVY)
    _save(fig, "2.3-lstm-gru/gru-gates.png")


def arch_zoo():
    fig, axes = plt.subplots(1, 3, figsize=(11.2, 3.4))
    titles = [
        "Many-to-one\n(sentiment)",
        "Many-to-many\n(tagging / LM)",
        "Encoder then decode\n(leave for Week 3)",
    ]
    for ax, title in zip(axes, titles):
        ax.set_xlim(0, 6.2)
        ax.set_ylim(0, 4.2)
        ax.axis("off")
        ax.set_title(title, color=NAVY, fontsize=11, pad=2)
        xs = [0.55, 1.85, 3.15, 4.45]
        for i, x in enumerate(xs):
            _box(ax, (x, 0.35), 0.95, 0.7, rf"$x_{i+1}$", FILL3, CORAL, 10)
            _box(ax, (x, 1.55), 0.95, 0.75, "cell", FILL2, TEAL, 9)
            _arrow(ax, (x + 0.48, 1.08), (x + 0.48, 1.5), CORAL)
            if i < 3:
                _arrow(ax, (x + 1.0, 1.92), (xs[i + 1], 1.92))
        if title.startswith("Many-to-one"):
            _box(ax, (4.35, 2.85), 1.15, 0.7, r"$\hat y$", FILL, NAVY, 11)
            _arrow(ax, (4.92, 2.35), (4.92, 2.8), TEAL)
        elif title.startswith("Many-to-many"):
            for i, x in enumerate(xs):
                _box(ax, (x, 2.85), 0.95, 0.7, rf"$y_{i+1}$", FILL, NAVY, 10)
                _arrow(ax, (x + 0.48, 2.35), (x + 0.48, 2.8), TEAL)
        else:
            _box(ax, (4.25, 2.85), 1.35, 0.7, "bottleneck", FILL4, GOLD, 9)
            _arrow(ax, (4.92, 2.35), (4.92, 2.8), GOLD)
    fig.tight_layout()
    _save(fig, "2.1-sequence-rnns/arch-zoo.png")


def rnn_lm():
    fig, ax = plt.subplots(figsize=(10.6, 3.7))
    ax.set_xlim(0, 12.2)
    ax.set_ylim(0, 4.0)
    ax.axis("off")
    steps = [
        (0.25, r"$x_t$" + "\nid", FILL3, CORAL),
        (2.55, "lookup\nembed", FILL, NAVY),
        (4.85, r"cell" + "\n" + r"$h_t$", FILL2, TEAL),
        (7.15, "linear", FILL4, GOLD),
        (9.45, "softmax\nnext token", FILL, NAVY),
    ]
    for x, text, fill, edge in steps:
        _box(ax, (x, 1.25), 2.05, 1.55, text, fill, edge, 11)
    for x in (2.3, 4.6, 6.9, 9.2):
        _arrow(ax, (x, 2.0), (x + 0.25, 2.0))
    ax.text(5.85, 3.35, r"same $W_h, W_x$ at every $t$", ha="center", color=SLATE, fontsize=11)
    ax.text(5.85, 0.45, r"loss at $t$: $-\log P(x_{t+1}\mid h_t)$", ha="center", color=NAVY, fontsize=12)
    ax.set_title("An RNN language model is next-token softmax from the hidden state", loc="left", color=NAVY)
    _save(fig, "2.1-sequence-rnns/rnn-lm.png")


def rnn_numeric():
    fig, ax = plt.subplots(figsize=(9.6, 3.6))
    ax.axis("off")
    cols = [r"step", r"$x_t$", r"$W_h h_{t-1}+W_x x_t$", r"$h_t=\tanh(\cdot)$"]
    rows = [
        [r"$t=1$", r"$[1,0]$", r"$[1,0]$", r"$[0.76, 0]$"],
        [r"$t=2$", r"$[0,1]$", r"$[0.38, 1]$", r"$[0.36, 0.76]$"],
    ]
    table = ax.table(cellText=rows, colLabels=cols, loc="center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 1.85)
    for (r, c), cell in table.get_celld().items():
        cell.set_edgecolor(SLATE)
        if r == 0:
            cell.set_facecolor(FILL)
            cell.set_text_props(color=NAVY, fontweight="medium")
        else:
            cell.set_facecolor("white")
    ax.set_title(r"$W_h=0.5 I$, $W_x=I$, $h_0=0$. Token 1 shrinks in $h_2$.", loc="left", color=NAVY, pad=12)
    _save(fig, "2.1-sequence-rnns/rnn-numeric.png")


def bptt():
    fig, ax = plt.subplots(figsize=(10.4, 3.9))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4.3)
    ax.axis("off")
    xs = [0.5, 3.4, 6.3]
    for i, x in enumerate(xs):
        _box(ax, (x, 2.35), 2.0, 0.95, rf"copy of $W_h$" + "\n" + rf"at $t={i+1}$", FILL2, TEAL, 10)
        _box(ax, (x, 0.45), 2.0, 0.8, rf"$L_{i+1}$", FILL3, CORAL, 11)
        _arrow(ax, (x + 1.0, 1.3), (x + 1.0, 2.3), CORAL)
        if i < 2:
            _arrow(ax, (x + 2.05, 2.8), (xs[i + 1], 2.8))
    _box(ax, (9.15, 2.25), 2.45, 1.15, r"one $W_h$" + "\n" + r"$\nabla=$ sum", FILL, NAVY, 11)
    _arrow(ax, (8.35, 2.85), (9.1, 2.85), GOLD)
    ax.text(6.0, 3.95, "BPTT: the shared matrix gets every copy's gradient", ha="center", color=NAVY, fontsize=12)
    _save(fig, "2.2-vanishing-gradients/bptt.png")


def eigen_scale():
    t = np.arange(0, 21)
    fig, ax = plt.subplots(figsize=(8.4, 3.8))
    ax.semilogy(t, 0.9 ** t, color=CORAL, lw=2.2, label=r"$|\lambda_{\max}|=0.9$  (vanishes)")
    ax.semilogy(t, 1.1 ** t, color=NAVY, lw=2.2, label=r"$|\lambda_{\max}|=1.1$  (explodes)")
    ax.axhline(1.0, color=SLATE, lw=0.8, ls="--")
    ax.set_xlabel("steps $t$")
    ax.set_ylabel(r"$|\lambda_{\max}|^t$  (log)")
    ax.legend(frameon=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_title("Linear recurrence: long-run scale is the largest |eigenvalue| of $W_h$")
    _save(fig, "2.2-vanishing-gradients/eigen-scale.png")


def clipping():
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.5))
    axes[0].annotate("", xy=(3.2, 0.9), xytext=(0.3, 0.3),
                     arrowprops=dict(arrowstyle="-|>", color=CORAL, lw=2.4, mutation_scale=16))
    axes[0].annotate("", xy=(1.55, 0.55), xytext=(0.3, 0.3),
                     arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=2.6, mutation_scale=16))
    axes[0].text(2.15, 1.15, r"$\|g\|=10$", color=CORAL, fontsize=12)
    axes[0].text(1.65, 0.15, r"clip to $c=5$", color=TEAL, fontsize=12)
    axes[0].set_title("Exploding: same direction, shorter step")
    axes[1].annotate("", xy=(0.55, 0.38), xytext=(0.3, 0.3),
                     arrowprops=dict(arrowstyle="-|>", color=CORAL, lw=2.0, mutation_scale=10))
    axes[1].text(0.75, 0.55, r"$\|g\|=10^{-6}$", color=CORAL, fontsize=12)
    axes[1].text(0.75, 0.15, "clipping leaves it dead", color=SLATE, fontsize=11)
    axes[1].set_title("Vanishing: there is nothing to rescale")
    for ax in axes:
        ax.set_xlim(0, 3.6)
        ax.set_ylim(0, 1.6)
        ax.axis("off")
    fig.tight_layout()
    _save(fig, "2.2-vanishing-gradients/clipping.png")


def copy_regime():
    fig, ax = plt.subplots(figsize=(10.0, 3.6))
    ax.set_xlim(0, 11.5)
    ax.set_ylim(0, 4.0)
    ax.axis("off")
    _box(ax, (0.3, 1.35), 2.2, 1.3, r"$c_{t-1}=2$", FILL, NAVY, 13)
    _box(ax, (3.2, 2.45), 2.3, 0.9, r"$f_t=1$", FILL2, TEAL, 12)
    _box(ax, (3.2, 0.65), 2.3, 0.9, r"$i_t=0$", FILL3, CORAL, 12)
    _box(ax, (6.3, 1.35), 2.4, 1.3, r"$c_t=2$", FILL, NAVY, 13)
    _box(ax, (9.15, 1.35), 2.05, 1.3, r"$\partial c_t/\partial c_{t-1}=1$", FILL4, GOLD, 10)
    _arrow(ax, (2.55, 2.0), (3.15, 2.85), TEAL)
    _arrow(ax, (2.55, 2.0), (3.15, 1.1), CORAL)
    _arrow(ax, (5.55, 2.0), (6.25, 2.0))
    _arrow(ax, (8.75, 2.0), (9.1, 2.0), GOLD)
    ax.set_title("Copy regime: forget open, input closed. The cell is a wire.", loc="left", color=NAVY)
    _save(fig, "2.3-lstm-gru/copy-regime.png")


def rnn_vs_attention():
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 3.8))
    for ax in axes:
        ax.set_xlim(0, 6)
        ax.set_ylim(0, 4)
        ax.axis("off")
    xs = np.linspace(0.7, 5.3, 5)
    for i, x in enumerate(xs):
        axes[0].add_patch(Circle((x, 0.8), 0.28, facecolor=FILL3, edgecolor=CORAL, lw=1.4))
        axes[0].add_patch(Circle((x, 2.9), 0.28, facecolor=FILL, edgecolor=NAVY, lw=1.4))
        if i:
            axes[0].annotate("", xy=(xs[i] - 0.3, 2.9), xytext=(xs[i - 1] + 0.3, 2.9),
                             arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.3))
        axes[0].annotate("", xy=(x, 2.55), xytext=(x, 1.15),
                         arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.1))
    axes[0].set_title("RNN: each state sees the past through a chain")
    for i, x in enumerate(xs):
        axes[1].add_patch(Circle((x, 0.8), 0.28, facecolor=FILL3, edgecolor=CORAL, lw=1.4))
        axes[1].add_patch(Circle((x, 2.9), 0.28, facecolor=FILL, edgecolor=NAVY, lw=1.4))
        for j, y in enumerate(xs):
            axes[1].plot([x, y], [1.1, 2.55], color="#9bb4c9", lw=0.5, zorder=0)
    axes[1].set_title("Attention: every token can look at every token")
    fig.tight_layout()
    _save(fig, "3.1-attention-need/rnn-vs-attention.png")


def qkv():
    fig, ax = plt.subplots(figsize=(10.0, 3.8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4)
    ax.axis("off")
    _box(ax, (0.3, 1.4), 2.2, 1.2, r"token $x$", FILL, NAVY, 12)
    _box(ax, (3.3, 2.55), 1.9, 0.9, r"$Q = xW_Q$", FILL2, TEAL, 11)
    _box(ax, (3.3, 1.45), 1.9, 0.9, r"$K = xW_K$", FILL3, CORAL, 11)
    _box(ax, (3.3, 0.35), 1.9, 0.9, r"$V = xW_V$", FILL4, GOLD, 11)
    _box(ax, (6.2, 1.35), 2.6, 1.3, "softmax of\n" + r"$QK^{\top}/\sqrt{d}$", FILL, NAVY, 11)
    _box(ax, (9.4, 1.45), 2.2, 1.1, r"$A\,V$", FILL2, TEAL, 13)
    _arrow(ax, (2.55, 2.0), (3.25, 2.95), TEAL)
    _arrow(ax, (2.55, 2.0), (3.25, 1.9), CORAL)
    _arrow(ax, (2.55, 2.0), (3.25, 0.8), GOLD)
    _arrow(ax, (5.25, 2.95), (6.15, 2.3), TEAL)
    _arrow(ax, (5.25, 1.9), (6.15, 2.0), CORAL)
    _arrow(ax, (8.85, 2.0), (9.35, 2.0))
    ax.set_title("Query asks, key is asked, value is what you mix in", loc="left", color=NAVY)
    _save(fig, "3.2-self-attention/qkv.png")


def attn_heatmap():
    rng = np.random.default_rng(2)
    words = ["The", "cat", "sat", "on", "mat"]
    A = np.array(
        [
            [0.55, 0.15, 0.10, 0.12, 0.08],
            [0.10, 0.50, 0.22, 0.08, 0.10],
            [0.08, 0.28, 0.40, 0.14, 0.10],
            [0.06, 0.10, 0.18, 0.46, 0.20],
            [0.07, 0.12, 0.16, 0.15, 0.50],
        ]
    )
    fig, ax = plt.subplots(figsize=(5.6, 4.8))
    im = ax.imshow(A, cmap="YlGnBu", vmin=0, vmax=0.6)
    ax.set_xticks(range(5), words)
    ax.set_yticks(range(5), words)
    ax.set_xlabel("key (looked at)")
    ax.set_ylabel("query (looking)")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    ax.set_title("Attention weights for one head")
    _save(fig, "3.2-self-attention/attn-heatmap.png")


def positions():
    pos = np.arange(0, 40)
    fig, ax = plt.subplots(figsize=(8.6, 3.6))
    for i, freq in enumerate([1, 2, 4, 8]):
        ax.plot(pos, np.sin(pos / freq), lw=1.8, label=f"dim {i}")
    ax.set_xlabel("position")
    ax.set_ylabel("sin / cos encoding")
    ax.legend(frameon=False, ncol=4, loc="upper right")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_title("Attention has no order. Positions have to be added.")
    _save(fig, "3.3-transformer-block/positional.png")


def transformer_block():
    fig, ax = plt.subplots(figsize=(6.4, 6.2))
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 8)
    ax.axis("off")
    layers = [
        (0.4, "token + position embeddings", FILL, NAVY),
        (1.6, "+ residual, layer norm", FILL, SLATE),
        (2.8, "multi-head self-attention", FILL2, TEAL),
        (4.0, "+ residual, layer norm", FILL, SLATE),
        (5.2, "feedforward MLP", FILL3, CORAL),
        (6.4, "output", FILL4, GOLD),
    ]
    for y, text, fill, edge in layers:
        _box(ax, (0.7, y), 4.6, 0.95, text, fill, edge, 11)
    for y in (0.4, 1.6, 2.8, 4.0, 5.2):
        _arrow(ax, (3.0, y + 0.95), (3.0, y + 1.15))
    ax.set_title("One transformer block", loc="left", color=NAVY)
    _save(fig, "3.3-transformer-block/block.png")


def gpt_bert():
    fig, axes = plt.subplots(1, 2, figsize=(10.0, 3.6))
    words = ["The", "cat", "sat"]
    xs = [1.0, 3.0, 5.0]
    for ax, title, mask in [
        (axes[0], "GPT: causal (next token)", True),
        (axes[1], "BERT: bidirectional (masked token)", False),
    ]:
        ax.set_xlim(0, 6.2)
        ax.set_ylim(0, 4)
        ax.axis("off")
        ax.set_title(title)
        for i, x in enumerate(xs):
            ax.add_patch(Circle((x, 0.8), 0.32, facecolor=FILL3, edgecolor=CORAL, lw=1.4))
            ax.text(x, 0.8, words[i], ha="center", va="center", fontsize=9, color=NAVY)
            ax.add_patch(Circle((x, 2.9), 0.32, facecolor=FILL, edgecolor=NAVY, lw=1.4))
        for i, x in enumerate(xs):
            for j, y in enumerate(xs):
                if mask and i > j:
                    continue
                ax.annotate("", xy=(y, 2.55), xytext=(x, 1.15),
                            arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.0))
    fig.tight_layout()
    _save(fig, "3.4-gpt-bert/gpt-bert.png")


def joint_coord():
    fig, axes = plt.subplots(1, 2, figsize=(10.0, 3.8))
    for ax in axes:
        ax.set_xlim(0, 6)
        ax.set_ylim(0, 4.4)
        ax.axis("off")
    _box(axes[0], (0.3, 0.4), 1.6, 0.8, "image", FILL3, CORAL, 10)
    _box(axes[0], (2.2, 0.4), 1.6, 0.8, "text", FILL2, TEAL, 10)
    _box(axes[0], (4.1, 0.4), 1.6, 0.8, "audio", FILL4, GOLD, 10)
    _box(axes[0], (1.5, 2.6), 3.0, 1.0, "one joint vector", FILL, NAVY, 11)
    _arrow(axes[0], (1.1, 1.25), (2.4, 2.55))
    _arrow(axes[0], (3.0, 1.25), (3.0, 2.55), TEAL)
    _arrow(axes[0], (4.9, 1.25), (3.6, 2.55), GOLD)
    axes[0].set_title("Joint: fuse into one space")
    _box(axes[1], (0.5, 0.4), 2.0, 0.9, "image enc.", FILL3, CORAL, 10)
    _box(axes[1], (3.5, 0.4), 2.0, 0.9, "text enc.", FILL2, TEAL, 10)
    _box(axes[1], (0.5, 2.5), 2.0, 0.9, r"$z_{img}$", FILL, NAVY, 11)
    _box(axes[1], (3.5, 2.5), 2.0, 0.9, r"$z_{txt}$", FILL, NAVY, 11)
    _arrow(axes[1], (1.5, 1.35), (1.5, 2.45), CORAL)
    _arrow(axes[1], (4.5, 1.35), (4.5, 2.45), TEAL)
    axes[1].annotate("", xy=(3.45, 2.95), xytext=(2.55, 2.95),
                     arrowprops=dict(arrowstyle="<->", color=GOLD, lw=1.6))
    axes[1].text(3.0, 3.35, "match", ha="center", color=GOLD, fontsize=10)
    axes[1].set_title("Coordinated: keep towers, pull them together")
    fig.tight_layout()
    _save(fig, "4.1-multimodal-foundations/joint-coord.png")


def patches():
    fig, ax = plt.subplots(figsize=(9.4, 3.6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4)
    ax.axis("off")
    ax.add_patch(Rectangle((0.4, 0.6), 2.8, 2.8, facecolor="#d9e8f2", edgecolor=NAVY, lw=1.6))
    for i in range(1, 4):
        ax.plot([0.4 + i * 0.7, 0.4 + i * 0.7], [0.6, 3.4], color=NAVY, lw=1)
        ax.plot([0.4, 3.2], [0.6 + i * 0.7, 0.6 + i * 0.7], color=NAVY, lw=1)
    ax.text(1.8, 0.25, "image", ha="center", color=SLATE)
    _arrow(ax, (3.35, 2.0), (4.15, 2.0))
    xs = np.linspace(4.4, 11.2, 6)
    for i, x in enumerate(xs):
        _box(ax, (x, 1.45), 0.95, 1.1, f"p{i+1}", FILL2, TEAL, 10)
    ax.set_title("A ViT treats patches the way an LLM treats tokens", loc="left", color=NAVY)
    _save(fig, "4.2-vision-transformers/patches.png")


def vit():
    fig, ax = plt.subplots(figsize=(10.2, 3.4))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 3.4)
    ax.axis("off")
    steps = [
        (0.25, "patches", FILL3, CORAL),
        (3.15, "+ [CLS] + positions", FILL, NAVY),
        (6.2, "transformer", FILL2, TEAL),
        (9.15, "class / features", FILL4, GOLD),
    ]
    for x, text, fill, edge in steps:
        _box(ax, (x, 1.05), 2.55, 1.3, text, fill, edge, 11)
    for x in (2.85, 5.75, 8.8):
        _arrow(ax, (x, 1.7), (x + 0.28, 1.7))
    ax.set_title("Vision transformer: same block as language, different tokens", loc="left", color=NAVY)
    _save(fig, "4.2-vision-transformers/vit.png")


def contrastive():
    fig, ax = plt.subplots(figsize=(7.2, 5.0))
    labels = ["cat", "dog", "car"]
    M = np.array([[0.92, 0.21, 0.08], [0.18, 0.88, 0.12], [0.10, 0.16, 0.90]])
    im = ax.imshow(M, cmap="YlOrRd", vmin=0, vmax=1)
    ax.set_xticks(range(3), [f"text: {w}" for w in labels], rotation=15)
    ax.set_yticks(range(3), [f"image: {w}" for w in labels])
    for i in range(3):
        for j in range(3):
            ax.text(j, i, f"{M[i, j]:.2f}", ha="center", va="center", color="black" if M[i, j] < 0.6 else "white")
    fig.colorbar(im, ax=ax, fraction=0.046)
    ax.set_title("Contrastive: matched pairs on the diagonal")
    _save(fig, "4.3-contrastive-zeroshot/contrastive.png")


def zeroshot():
    fig, ax = plt.subplots(figsize=(9.6, 3.6))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 3.6)
    ax.axis("off")
    _box(ax, (0.3, 1.2), 2.4, 1.2, "image", FILL3, CORAL, 12)
    _box(ax, (3.4, 2.2), 2.5, 0.9, '"a photo of a dog"', FILL2, TEAL, 10)
    _box(ax, (3.4, 0.5), 2.5, 0.9, '"a photo of a cat"', FILL2, TEAL, 10)
    _box(ax, (6.7, 1.2), 3.8, 1.2, "nearest text vector\n= predicted class", FILL4, GOLD, 11)
    _arrow(ax, (2.75, 1.8), (6.65, 1.8), CORAL)
    _arrow(ax, (5.95, 2.6), (7.3, 2.15), TEAL)
    _arrow(ax, (5.95, 0.95), (7.3, 1.45), TEAL)
    ax.set_title("Zero-shot: class names are text embeddings, not trained heads", loc="left", color=NAVY)
    _save(fig, "4.3-contrastive-zeroshot/zeroshot.png")


def clip_towers():
    fig, ax = plt.subplots(figsize=(9.8, 4.0))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 4.2)
    ax.axis("off")
    _box(ax, (0.3, 2.55), 2.3, 1.0, "image", FILL3, CORAL, 12)
    _box(ax, (0.3, 0.55), 2.3, 1.0, "caption", FILL2, TEAL, 12)
    _box(ax, (3.3, 2.55), 2.6, 1.0, "image encoder", FILL3, CORAL, 11)
    _box(ax, (3.3, 0.55), 2.6, 1.0, "text encoder", FILL2, TEAL, 11)
    _box(ax, (6.7, 1.45), 3.8, 1.3, "shared space\ncontrastive loss", FILL4, GOLD, 12)
    _arrow(ax, (2.65, 3.05), (3.25, 3.05), CORAL)
    _arrow(ax, (2.65, 1.05), (3.25, 1.05), TEAL)
    _arrow(ax, (5.95, 3.05), (7.4, 2.4), CORAL)
    _arrow(ax, (5.95, 1.05), (7.4, 1.8), TEAL)
    ax.set_title("CLIP: two towers, one cosine, a batch of matches", loc="left", color=NAVY)
    _save(fig, "5.1-clip/clip-towers.png")


def blip():
    fig, ax = plt.subplots(figsize=(10.0, 3.4))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 3.4)
    ax.axis("off")
    steps = [
        (0.2, "noisy web\nimage–text", FILL, SLATE),
        (3.15, "filter /\nbootstrap captions", FILL3, CORAL),
        (6.2, "ITC + ITM\n+ LM losses", FILL2, TEAL),
        (9.15, "retrieve or\ncaption", FILL4, GOLD),
    ]
    for x, text, fill, edge in steps:
        _box(ax, (x, 0.9), 2.55, 1.5, text, fill, edge, 11)
    for x in (2.8, 5.75, 8.8):
        _arrow(ax, (x, 1.65), (x + 0.3, 1.65))
    ax.set_title("BLIP: clean the pairs, then learn to match and to write", loc="left", color=NAVY)
    _save(fig, "5.2-blip/blip-pipeline.png")


def retrieval():
    fig, ax = plt.subplots(figsize=(9.6, 3.8))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 4)
    ax.axis("off")
    _box(ax, (0.3, 2.4), 2.4, 1.0, "query image", FILL3, CORAL, 11)
    _box(ax, (0.3, 0.5), 2.4, 1.0, "query text", FILL2, TEAL, 11)
    _box(ax, (3.6, 1.35), 2.5, 1.2, "shared space", FILL, NAVY, 11)
    _box(ax, (7.0, 2.4), 3.6, 1.0, "nearest captions", FILL4, GOLD, 11)
    _box(ax, (7.0, 0.5), 3.6, 1.0, "nearest images", FILL4, GOLD, 11)
    _arrow(ax, (2.75, 2.9), (3.55, 2.1), CORAL)
    _arrow(ax, (2.75, 1.0), (3.55, 1.7), TEAL)
    _arrow(ax, (6.15, 2.1), (6.95, 2.85), GOLD)
    _arrow(ax, (6.15, 1.7), (6.95, 1.05), GOLD)
    ax.set_title("One space, two retrieval directions", loc="left", color=NAVY)
    _save(fig, "5.3-retrieval-bias/retrieval.png")


def vlm_bias():
    fig, ax = plt.subplots(figsize=(7.4, 4.6))
    jobs = {"nurse": (0.8, 1.0), "ceo": (3.3, 3.3), "teacher": (1.4, 1.6), "engineer": (3.0, 2.8)}
    ax.scatter(*zip(*jobs.values()), c=NAVY, s=70)
    for n, (x, y) in jobs.items():
        ax.text(x + 0.08, y + 0.08, n, color=NAVY, fontsize=11)
    ax.annotate("", xy=(2.6, 2.5), xytext=(1.1, 1.2), arrowprops=dict(arrowstyle="->", color=CORAL, lw=2))
    ax.text(1.3, 2.3, "prompt:\n'a photo of a man/woman …'", color=CORAL, fontsize=9)
    ax.set_xlim(0.3, 4.2)
    ax.set_ylim(0.5, 3.9)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_title("VLMs inherit dataset stereotypes in retrieval and zero-shot")
    _save(fig, "5.3-retrieval-bias/vlm-bias.png")


def main():
    _setup()
    rnn_cell()
    rnn_unroll()
    arch_zoo()
    rnn_lm()
    rnn_numeric()
    vanishing()
    explode_vs_vanish()
    bptt()
    eigen_scale()
    clipping()
    lstm_gates()
    gru_gates()
    copy_regime()
    rnn_vs_attention()
    qkv()
    attn_heatmap()
    positions()
    transformer_block()
    gpt_bert()
    joint_coord()
    patches()
    vit()
    contrastive()
    zeroshot()
    clip_towers()
    blip()
    retrieval()
    vlm_bias()
    print("done")


if __name__ == "__main__":
    main()
