"""Pedagogical figures for DATA 443/643 Weeks 6–15."""

from __future__ import annotations

import pathlib

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle, FancyBboxPatch as FBox
from matplotlib.collections import LineCollection

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
FILL5 = "#eee8f4"


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


def waveform_spectrogram():
    t = np.linspace(0, 1.0, 800)
    y = 0.7 * np.sin(2 * np.pi * 8 * t) + 0.35 * np.sin(2 * np.pi * 22 * t)
    fig, axes = plt.subplots(2, 1, figsize=(9.2, 5.4), gridspec_kw={"height_ratios": [1, 1.35]})
    axes[0].plot(t, y, color=NAVY, lw=1.4)
    axes[0].set_xlim(0, 1)
    axes[0].set_ylabel("amp")
    axes[0].set_title("Waveform (time) versus spectrogram (time × frequency)", loc="left", color=NAVY)
    axes[0].spines["top"].set_visible(False)
    axes[0].spines["right"].set_visible(False)

    nfft = 64
    frames = []
    hop = 16
    win = np.hanning(nfft)
    for i in range(0, len(y) - nfft, hop):
        spec = np.abs(np.fft.rfft(y[i : i + nfft] * win))
        frames.append(spec)
    S = np.array(frames).T
    axes[1].imshow(S, origin="lower", aspect="auto", cmap="YlGnBu", interpolation="nearest")
    axes[1].set_xlabel("frame")
    axes[1].set_ylabel("frequency bin")
    fig.tight_layout()
    _save(fig, "6.1-audio-spectrograms/wave-spec.png")


def spec_patches():
    fig, ax = plt.subplots(figsize=(9.4, 3.6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4.2)
    ax.axis("off")
    ax.add_patch(Rectangle((0.3, 0.7), 4.4, 2.8, facecolor=FILL, edgecolor=NAVY, lw=1.6))
    rng = np.random.default_rng(2)
    heat = rng.random((6, 10))
    ax.imshow(heat, extent=(0.45, 4.55, 0.85, 3.35), origin="lower", cmap="YlGnBu", aspect="auto")
    ax.text(2.5, 3.75, "spectrogram", ha="center", color=NAVY, fontsize=11)
    for i, x in enumerate([5.6, 7.5, 9.4]):
        _box(ax, (x, 1.4), 1.6, 1.3, f"patch {i+1}", FILL3, CORAL, 10)
        _arrow(ax, (4.75, 2.1), (x, 2.05), CORAL)
    ax.set_title("Same trick as ViT: cut time–frequency patches, then embed", loc="left", color=NAVY)
    _save(fig, "6.1-audio-spectrograms/spec-patches.png")


def whisper_encdec():
    fig, ax = plt.subplots(figsize=(10.2, 3.6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4)
    ax.axis("off")
    _box(ax, (0.3, 1.35), 2.4, 1.3, "log-mel\nspectrogram", FILL3, CORAL, 11)
    _box(ax, (3.4, 1.35), 2.4, 1.3, "encoder\ntransformer", FILL2, TEAL, 11)
    _box(ax, (6.5, 1.35), 2.4, 1.3, "decoder\n(text tokens)", FILL, NAVY, 11)
    _box(ax, (9.6, 1.35), 2.1, 1.3, "transcript", FILL4, GOLD, 11)
    _arrow(ax, (2.75, 2.0), (3.35, 2.0), CORAL)
    _arrow(ax, (5.85, 2.0), (6.45, 2.0), TEAL)
    _arrow(ax, (8.95, 2.0), (9.55, 2.0), NAVY)
    ax.set_title("Whisper-style: audio encoder, text decoder (Week 3 block, new input)", loc="left", color=NAVY)
    _save(fig, "6.2-audio-encoders/whisper.png")


def clap_towers():
    fig, ax = plt.subplots(figsize=(9.0, 3.8))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 4.2)
    ax.axis("off")
    _box(ax, (0.4, 2.4), 2.6, 1.1, "audio encoder", FILL3, CORAL, 12)
    _box(ax, (0.4, 0.5), 2.6, 1.1, "text encoder", FILL2, TEAL, 12)
    _box(ax, (4.3, 1.45), 2.4, 1.2, "shared space", FILL, NAVY, 12)
    _box(ax, (8.0, 1.45), 2.5, 1.2, "contrastive\nloss", FILL4, GOLD, 12)
    _arrow(ax, (3.05, 2.9), (4.25, 2.2), CORAL)
    _arrow(ax, (3.05, 1.05), (4.25, 1.7), TEAL)
    _arrow(ax, (6.75, 2.05), (7.95, 2.05), NAVY)
    ax.set_title("CLAP is CLIP for audio: two towers, cosine, paired captions", loc="left", color=NAVY)
    _save(fig, "6.2-audio-encoders/clap.png")


def fusion_kinds():
    fig, axes = plt.subplots(1, 3, figsize=(11.2, 3.8))
    titles = ["Early fusion", "Late fusion", "Cross-attention"]
    for ax, title in zip(axes, titles):
        ax.set_xlim(0, 5)
        ax.set_ylim(0, 5)
        ax.axis("off")
        ax.set_title(title, color=NAVY, fontsize=12)
        _box(ax, (0.4, 3.5), 1.8, 0.85, "audio", FILL3, CORAL, 10)
        _box(ax, (2.8, 3.5), 1.8, 0.85, "text", FILL2, TEAL, 10)
    _box(axes[0], (1.35, 1.9), 2.3, 0.9, "concat → net", FILL, NAVY, 10)
    _arrow(axes[0], (1.3, 3.45), (2.2, 2.85), CORAL)
    _arrow(axes[0], (3.7, 3.45), (2.8, 2.85), TEAL)
    _box(axes[1], (0.4, 1.9), 1.8, 0.85, "enc A", FILL3, CORAL, 10)
    _box(axes[1], (2.8, 1.9), 1.8, 0.85, "enc T", FILL2, TEAL, 10)
    _box(axes[1], (1.35, 0.45), 2.3, 0.85, "combine", FILL, NAVY, 10)
    _arrow(axes[1], (1.3, 3.45), (1.3, 2.8), CORAL)
    _arrow(axes[1], (3.7, 3.45), (3.7, 2.8), TEAL)
    _arrow(axes[1], (1.3, 1.85), (2.2, 1.35), CORAL)
    _arrow(axes[1], (3.7, 1.85), (2.9, 1.35), TEAL)
    _box(axes[2], (0.35, 1.7), 1.9, 1.1, "queries\nfrom text", FILL2, TEAL, 9)
    _box(axes[2], (2.75, 1.7), 1.9, 1.1, "K,V from\naudio", FILL3, CORAL, 9)
    _arrow(axes[2], (1.3, 3.45), (1.3, 2.85), TEAL)
    _arrow(axes[2], (3.7, 3.45), (3.7, 2.85), CORAL)
    fig.suptitle("Three ways to mix streams. Missing audio at test time punishes early fusion.", color=NAVY, y=1.02)
    fig.tight_layout()
    _save(fig, "6.3-fusion-scarcity/fusion.png")


def data_pyramid():
    fig, ax = plt.subplots(figsize=(8.4, 4.0))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis("off")
    layers = [
        (1.2, 0.4, 7.6, 1.1, "web text  (huge)", FILL, NAVY),
        (2.0, 1.7, 6.0, 1.1, "image–text pairs  (large)", FILL2, TEAL),
        (2.8, 3.0, 4.4, 1.1, "labeled audio  (scarce)", FILL3, CORAL),
    ]
    for x, y, w, h, t, f, e in layers:
        _box(ax, (x, y), w, h, t, f, e, 12)
    ax.set_title("Paired, transcribed audio is the thin top of the data pyramid", loc="left", color=NAVY)
    _save(fig, "6.3-fusion-scarcity/scarcity.png")


def stft_frames():
    fig, ax = plt.subplots(figsize=(10.0, 3.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3.6)
    ax.axis("off")
    ax.add_patch(Rectangle((0.4, 1.55), 9.2, 0.45, facecolor=FILL, edgecolor=NAVY, lw=1.4))
    ax.text(5.0, 2.15, "waveform, length L samples", ha="center", color=NAVY, fontsize=11)
    windows = [(0.5, "N"), (2.3, "hop H"), (4.1, "N"), (5.9, "hop H"), (7.7, "N")]
    for i, (x, _) in enumerate([(0.5, 0), (2.6, 1), (4.7, 2)]):
        ax.add_patch(Rectangle((x, 0.45), 2.15, 0.85, facecolor=FILL3 if i % 2 == 0 else FILL2, edgecolor=CORAL if i % 2 == 0 else TEAL, lw=1.5))
        ax.text(x + 1.07, 0.87, f"frame {i+1}\nwindow N", ha="center", va="center", color=NAVY, fontsize=10)
    ax.annotate("", xy=(2.6, 0.35), xytext=(0.5, 0.35), arrowprops=dict(arrowstyle="<->", color=SLATE, lw=1.3))
    ax.text(1.55, 0.08, "hop H", ha="center", color=SLATE, fontsize=10)
    ax.set_title(r"STFT: slide a window of length $N$ by hop $H$. Frames $T=1+\lfloor(L-N)/H\rfloor$.", loc="left", color=NAVY)
    _save(fig, "6.1-audio-spectrograms/stft-frames.png")


def whisper_chunk():
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 3.5))
    for ax in axes:
        ax.set_xlim(0, 5)
        ax.set_ylim(0, 4)
        ax.axis("off")
    _box(axes[0], (0.35, 1.2), 4.3, 1.6, "30 s at 16 kHz\n= 480,000 samples", FILL3, CORAL, 13)
    axes[0].set_title("Raw waveform")
    _box(axes[1], (0.35, 2.25), 4.3, 1.2, "10 ms hop → 3000 mel frames", FILL2, TEAL, 12)
    _box(axes[1], (0.35, 0.55), 4.3, 1.2, "stride-2 conv → ~1500 tokens", FILL4, GOLD, 12)
    _arrow(axes[1], (2.5, 2.2), (2.5, 1.8), TEAL)
    axes[1].set_title("Whisper front end (CS224S L11)")
    fig.suptitle("The spectrogram exists so the encoder is not a 480k-token transformer.", color=NAVY, y=1.02)
    fig.tight_layout()
    _save(fig, "6.2-audio-encoders/whisper-chunk.png")


def clap_rank():
    fig, ax = plt.subplots(figsize=(7.8, 3.8))
    names = ["clip 2", "clip 3", "clip 1"]
    scores = [0.72, 0.40, 0.11]
    ax.barh(names, scores, color=[TEAL, FILL, FILL3], edgecolor=NAVY)
    ax.set_xlim(0, 1.0)
    ax.set_xlabel("cosine to query  a dog barking")
    ax.set_title("CLAP retrieval: rank clips. No decoder ran. Transcripts are Whisper’s job.", loc="left", color=NAVY)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    _save(fig, "6.2-audio-encoders/clap-rank.png")


def concat_add():
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.6))
    for ax in axes:
        ax.set_xlim(0, 6)
        ax.set_ylim(0, 4.2)
        ax.axis("off")
    _box(axes[0], (0.3, 2.5), 2.2, 1.1, r"audio $128$", FILL3, CORAL, 12)
    _box(axes[0], (0.3, 0.7), 2.2, 1.1, r"image $128$", FILL2, TEAL, 12)
    _box(axes[0], (3.3, 1.45), 2.4, 1.4, r"$[a;v]\in\mathbb{R}^{256}$", FILL4, GOLD, 13)
    _arrow(axes[0], (2.55, 3.05), (3.25, 2.4), CORAL)
    _arrow(axes[0], (2.55, 1.25), (3.25, 1.85), TEAL)
    axes[0].set_title("Concat grows width")
    _box(axes[1], (0.3, 2.5), 2.2, 1.1, r"audio $128$", FILL3, CORAL, 12)
    _box(axes[1], (0.3, 0.7), 2.2, 1.1, r"image $128$", FILL2, TEAL, 12)
    _box(axes[1], (3.3, 1.45), 2.4, 1.4, r"$a+v\in\mathbb{R}^{128}$", FILL, NAVY, 13)
    _arrow(axes[1], (2.55, 3.05), (3.25, 2.4), CORAL)
    _arrow(axes[1], (2.55, 1.25), (3.25, 1.85), TEAL)
    axes[1].set_title("Add needs a shared axis")
    fig.suptitle("If widths differ, add is illegal until you map. Missing audio breaks concat unless you trained a mask.", color=NAVY, y=1.02)
    fig.tight_layout()
    _save(fig, "6.3-fusion-scarcity/concat-add.png")


def scaling_curve():
    C = np.logspace(3, 7, 40)
    L = 2.5 * C ** (-0.07) + 1.4
    fig, ax = plt.subplots(figsize=(8.0, 4.0))
    ax.loglog(C, L, color=NAVY, lw=2.2)
    ax.set_xlabel("compute (arbitrary units)")
    ax.set_ylabel("pretraining loss")
    ax.set_title("Scaling laws: smoother on a log–log plot, until data or params starve", loc="left", color=NAVY)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    _save(fig, "7.1-scaling-laws/compute-loss.png")


def chinchilla():
    fig, ax = plt.subplots(figsize=(8.2, 4.2))
    params = np.array([0.1, 0.4, 1.5, 6, 20])
    under = 20 * params ** 0.4
    opt = 20 * params
    ax.plot(params, under, color=CORAL, lw=2.2, marker="o", label="too few tokens (undertrained)")
    ax.plot(params, opt, color=TEAL, lw=2.2, marker="s", label="compute-optimal tokens (sketch)")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("parameters (relative)")
    ax.set_ylabel("tokens (relative)")
    ax.legend(frameon=False)
    ax.set_title("Chinchilla: bigger is not enough if you do not feed it tokens", loc="left", color=NAVY)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    _save(fig, "7.1-scaling-laws/chinchilla.png")


def moe():
    fig, ax = plt.subplots(figsize=(10.0, 4.0))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4.5)
    ax.axis("off")
    _box(ax, (0.3, 1.7), 2.2, 1.2, "token", FILL3, CORAL, 12)
    _box(ax, (3.1, 1.7), 2.2, 1.2, "router", FILL4, GOLD, 12)
    for i, y in enumerate([3.15, 1.7, 0.25]):
        _box(ax, (6.2, y), 2.3, 1.0, f"expert {i+1}", FILL2, TEAL, 11)
    _box(ax, (9.4, 1.7), 2.2, 1.2, "weighted\nsum", FILL, NAVY, 11)
    _arrow(ax, (2.55, 2.3), (3.05, 2.3), CORAL)
    _arrow(ax, (5.35, 2.5), (6.15, 3.6), GOLD)
    _arrow(ax, (5.35, 2.3), (6.15, 2.2), GOLD)
    _arrow(ax, (8.55, 3.65), (9.4, 2.55), TEAL)
    _arrow(ax, (8.55, 2.2), (9.4, 2.3), TEAL)
    ax.set_title("Sparse MoE: most experts stay off for a given token", loc="left", color=NAVY)
    _save(fig, "7.2-mixture-of-experts/moe.png")


def compress_pipeline():
    fig, ax = plt.subplots(figsize=(10.6, 3.2))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 3.2)
    ax.axis("off")
    labs = ["dense\nmodel", "prune", "quantize", "distill", "serve"]
    cols = [FILL, FILL3, FILL4, FILL2, FILL5]
    edges = [NAVY, CORAL, GOLD, TEAL, NAVY]
    xs = [0.3, 2.8, 5.3, 7.8, 10.3]
    for x, lab, c, e in zip(xs, labs, cols, edges):
        _box(ax, (x, 0.9), 2.1, 1.3, lab, c, e, 11)
    for i in range(4):
        _arrow(ax, (xs[i] + 2.15, 1.55), (xs[i + 1], 1.55))
    ax.set_title("Compression is a pipeline. Measure quality after each cut.", loc="left", color=NAVY)
    _save(fig, "7.3-efficiency-deploy/compress.png")


def speculative():
    fig, ax = plt.subplots(figsize=(10.0, 3.6))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 4)
    ax.axis("off")
    _box(ax, (0.3, 1.4), 2.6, 1.3, "small draft\nmodel", FILL3, CORAL, 11)
    _box(ax, (3.6, 1.4), 3.4, 1.3, "draft tokens\n$\\hat{y}_{t:t+k}$", FILL4, GOLD, 11)
    _box(ax, (7.6, 1.4), 3.0, 1.3, "large model\nverifies", FILL2, TEAL, 11)
    _arrow(ax, (2.95, 2.05), (3.55, 2.05), CORAL)
    _arrow(ax, (7.05, 2.05), (7.55, 2.05), GOLD)
    ax.set_title("Speculative decoding: guess many tokens, accept the prefix the big model agrees on", loc="left", color=NAVY)
    _save(fig, "7.3-efficiency-deploy/speculative.png")


def sft_stack():
    fig, ax = plt.subplots(figsize=(9.2, 3.6))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 4)
    ax.axis("off")
    _box(ax, (0.3, 1.4), 2.8, 1.3, "pretrain\nnext token", FILL, NAVY, 12)
    _box(ax, (3.8, 1.4), 3.0, 1.3, "SFT on\ninstructions", FILL2, TEAL, 12)
    _box(ax, (7.5, 1.4), 3.1, 1.3, "chat / tool\nbehavior", FILL3, CORAL, 12)
    _arrow(ax, (3.15, 2.05), (3.75, 2.05))
    _arrow(ax, (6.85, 2.05), (7.45, 2.05), TEAL)
    ax.set_title("Instruction data is a distribution shift, not a new architecture", loc="left", color=NAVY)
    _save(fig, "8.1-sft-instructions/sft.png")


def prompt_pair():
    fig, ax = plt.subplots(figsize=(9.0, 3.4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3.6)
    ax.axis("off")
    _box(ax, (0.4, 1.3), 4.2, 1.5, "User: Summarize this\nin one sentence.", FILL3, CORAL, 11)
    _box(ax, (5.4, 1.3), 4.2, 1.5, "Assistant: The paper\nargues that …", FILL2, TEAL, 11)
    _arrow(ax, (4.65, 2.05), (5.35, 2.05), NAVY)
    ax.set_title("One SFT row: a request and a completion you would actually want", loc="left", color=NAVY)
    _save(fig, "8.1-sft-instructions/pair.png")


def forgetting():
    tasks = ["A", "B", "C"]
    acc_a = [0.92, 0.55, 0.41]
    acc_b = [np.nan, 0.88, 0.62]
    acc_c = [np.nan, np.nan, 0.90]
    fig, ax = plt.subplots(figsize=(8.0, 4.0))
    x = np.arange(3)
    ax.plot(x, acc_a, color=CORAL, marker="o", lw=2.2, label="task A (first)")
    ax.plot(x, acc_b, color=TEAL, marker="s", lw=2.2, label="task B")
    ax.plot(x, acc_c, color=NAVY, marker="^", lw=2.2, label="task C (latest)")
    ax.set_xticks(x, ["after A", "after B", "after C"])
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("accuracy")
    ax.legend(frameon=False)
    ax.set_title("Catastrophic forgetting: later tasks overwrite earlier ones", loc="left", color=NAVY)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    _save(fig, "8.2-continual-forgetting/forget.png")


def replay():
    fig, ax = plt.subplots(figsize=(9.4, 3.4))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 3.8)
    ax.axis("off")
    _box(ax, (0.3, 1.3), 2.6, 1.3, "new batch\n(task B)", FILL3, CORAL, 11)
    _box(ax, (3.4, 1.3), 2.6, 1.3, "replay\n(task A)", FILL2, TEAL, 11)
    _box(ax, (6.5, 1.3), 4.0, 1.3, "mix → update\n(less overwrite)", FILL, NAVY, 11)
    _arrow(ax, (2.95, 1.95), (3.35, 1.95), CORAL)
    _arrow(ax, (6.05, 1.95), (6.45, 1.95), TEAL)
    ax.set_title("Replay (or freeze, or LoRA) is how you keep task A alive", loc="left", color=NAVY)
    _save(fig, "8.2-continual-forgetting/replay.png")


def lora_ba():
    fig, ax = plt.subplots(figsize=(9.6, 3.8))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 4.2)
    ax.axis("off")
    _box(ax, (0.3, 1.3), 2.4, 1.6, r"$W$ frozen", FILL, NAVY, 13)
    ax.text(3.15, 2.1, "+", fontsize=22, ha="center", va="center", color=SLATE)
    _box(ax, (3.6, 2.35), 2.0, 1.2, r"$B$", FILL3, CORAL, 13)
    _box(ax, (3.6, 0.65), 2.0, 1.2, r"$A$", FILL2, TEAL, 13)
    ax.text(6.1, 2.1, r"$\approx BA$", fontsize=16, ha="center", va="center", color=NAVY)
    _box(ax, (7.3, 1.3), 3.2, 1.6, r"$W + BA$", FILL4, GOLD, 13)
    ax.set_title("LoRA: train a thin pair $BA$, leave $W$ alone", loc="left", color=NAVY)
    _save(fig, "8.3-lora-adapters/lora.png")


def federated():
    fig, ax = plt.subplots(figsize=(9.2, 3.8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.2)
    ax.axis("off")
    _box(ax, (3.6, 3.0), 2.8, 0.9, "server (average)", FILL, NAVY, 11)
    for i, x in enumerate([0.4, 3.6, 6.8]):
        _box(ax, (x, 0.5), 2.6, 1.1, f"site {i+1}\nLoRA only", FILL2, TEAL, 10)
        _arrow(ax, (x + 1.3, 1.65), (5.0, 2.95), TEAL)
    ax.set_title("Federated sketch: ship adapters, not raw documents", loc="left", color=NAVY)
    _save(fig, "8.3-lora-adapters/federated.png")


def gpt3_tokens():
    fig, ax = plt.subplots(figsize=(8.4, 4.0))
    names = ["GPT-3\n175B / 300B tok", "Chinchilla thumb\n20 tok / param"]
    vals = [300 / 175, 20]
    ax.bar(names, vals, color=[CORAL, TEAL], edgecolor=NAVY)
    ax.set_ylabel("tokens per parameter")
    ax.set_title("CS224N L9: GPT-3 was underfed tokens for its size.", loc="left", color=NAVY)
    for i, v in enumerate(vals):
        ax.text(i, v + 0.4, f"{v:.1f}", ha="center", color=NAVY)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_ylim(0, 24)
    fig.tight_layout()
    _save(fig, "7.1-scaling-laws/gpt3-tokens.png")


def moe_collapse():
    fig, ax = plt.subplots(figsize=(8.6, 3.8))
    experts = [f"E{i}" for i in range(8)]
    load = [22, 2, 21, 1, 1, 1, 2, 2]
    colors = [CORAL if v > 10 else TEAL for v in load]
    ax.bar(experts, load, color=colors, edgecolor=NAVY)
    ax.axhline(8, color=SLATE, ls="--", lw=1)
    ax.set_ylabel("tokens (k=2, 32 tokens → 64 slots)")
    ax.set_title("Uniform load is 8. Collapse: two experts ate the batch.", loc="left", color=NAVY)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    _save(fig, "7.2-mixture-of-experts/moe-collapse.png")


def int8_table():
    fig, ax = plt.subplots(figsize=(8.8, 3.5))
    ax.axis("off")
    rows = [
        [r"$q=128$", r"$s(q-128)=0$"],
        [r"$q=255$", r"$s\cdot 127\approx 0.996$"],
        [r"no $z$", "cannot represent negatives"],
    ]
    table = ax.table(
        cellText=rows,
        colLabels=[r"INT8 on $[-1,1]$", "value"],
        loc="center",
        cellLoc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.15, 1.8)
    for (r, c), cell in table.get_celld().items():
        cell.set_edgecolor(SLATE)
        if r == 0:
            cell.set_facecolor(FILL)
            cell.set_text_props(color=NAVY)
        else:
            cell.set_facecolor("white")
    ax.set_title(r"$s=2/255$, $z=128$. Drop $z$ and the map cannot go below 0.", loc="left", color=NAVY, pad=12)
    _save(fig, "7.3-efficiency-deploy/int8-numeric.png")


def sft_mask():
    fig, ax = plt.subplots(figsize=(10.2, 3.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3.2)
    ax.axis("off")
    for i, lab in enumerate(["[user]", "List", "two", "colors", ".", "red", "blue", "EOS"]):
        x = 0.25 + i * 1.2
        fill, edge = (FILL3, CORAL) if i < 5 else (FILL2, TEAL)
        _box(ax, (x, 1.35), 1.1, 1.1, lab, fill, edge, 9)
        ax.text(x + 0.55, 0.55, "0" if i < 5 else "1", ha="center", color=NAVY, fontsize=12)
    ax.set_title("SFT mask: zeros on the prompt, ones on the response.", loc="left", color=NAVY)
    _save(fig, "8.1-sft-instructions/sft-mask.png")


def lora_count():
    fig, ax = plt.subplots(figsize=(8.8, 3.5))
    ax.axis("off")
    rows = [
        [r"$dk$", r"$4096^2=16.8\mathrm{M}$"],
        [r"$r(d+k)$", r"$8\cdot 8192=65{,}536$"],
        ["ratio", r"$0.39\%$"],
    ]
    table = ax.table(cellText=rows, colLabels=[r"$d=k=4096$, $r=8$", "count"], loc="center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.15, 1.8)
    for (r, c), cell in table.get_celld().items():
        cell.set_edgecolor(SLATE)
        if r == 0:
            cell.set_facecolor(FILL)
            cell.set_text_props(color=NAVY)
        else:
            cell.set_facecolor("white")
    ax.set_title("CS224N L11: a full copy of W is 175B extra for GPT-3. LoRA is this table.", loc="left", color=NAVY, pad=12)
    _save(fig, "8.3-lora-adapters/lora-count.png")


def preference_pair():
    fig, ax = plt.subplots(figsize=(9.4, 3.6))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 4)
    ax.axis("off")
    _box(ax, (0.3, 1.4), 2.6, 1.3, "prompt", FILL, NAVY, 12)
    _box(ax, (3.5, 2.35), 3.2, 1.15, "chosen  $y_w$", FILL2, TEAL, 12)
    _box(ax, (3.5, 0.5), 3.2, 1.15, "rejected  $y_l$", FILL3, CORAL, 12)
    _box(ax, (7.4, 1.4), 3.2, 1.3, "label:\n$y_w \\succ y_l$", FILL4, GOLD, 12)
    _arrow(ax, (2.95, 2.3), (3.45, 2.85), NAVY)
    _arrow(ax, (2.95, 1.8), (3.45, 1.1), NAVY)
    _arrow(ax, (6.75, 2.9), (7.35, 2.2), TEAL)
    _arrow(ax, (6.75, 1.05), (7.35, 1.85), CORAL)
    ax.set_title("One preference row is a comparison, not a score out of 100", loc="left", color=NAVY)
    _save(fig, "9.1-preference-rewards/pair.png")


def reward_model():
    fig, ax = plt.subplots(figsize=(9.0, 3.4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3.6)
    ax.axis("off")
    _box(ax, (0.3, 1.2), 3.4, 1.3, r"$(x, y)$", FILL, NAVY, 13)
    _box(ax, (4.3, 1.2), 2.4, 1.3, r"$r_\phi$", FILL2, TEAL, 13)
    _box(ax, (7.3, 1.2), 2.3, 1.3, "scalar", FILL4, GOLD, 12)
    _arrow(ax, (3.75, 1.85), (4.25, 1.85))
    _arrow(ax, (6.75, 1.85), (7.25, 1.85), TEAL)
    ax.set_title("A reward model is a classifier of “better completion,” trained on pairs", loc="left", color=NAVY)
    _save(fig, "9.1-preference-rewards/reward.png")


def rlhf_loop():
    fig, ax = plt.subplots(figsize=(10.4, 3.6))
    ax.set_xlim(0, 12.2)
    ax.set_ylim(0, 4)
    ax.axis("off")
    _box(ax, (0.25, 1.4), 2.5, 1.3, "SFT\npolicy", FILL, NAVY, 11)
    _box(ax, (3.2, 1.4), 2.6, 1.3, "sample\ncompletions", FILL3, CORAL, 11)
    _box(ax, (6.2, 1.4), 2.5, 1.3, "reward\nmodel", FILL4, GOLD, 11)
    _box(ax, (9.15, 1.4), 2.7, 1.3, "PPO / RL\nupdate", FILL2, TEAL, 11)
    for a, b in [(2.8, 3.15), (5.85, 6.15), (8.75, 9.1)]:
        _arrow(ax, (a, 2.05), (b, 2.05))
    ax.annotate(
        "",
        xy=(1.5, 1.35),
        xytext=(10.4, 1.35),
        arrowprops=dict(arrowstyle="-|>", color=SLATE, connectionstyle="arc3,rad=-0.35", lw=1.4),
    )
    ax.set_title("RLHF: climb the reward, stay near the SFT policy (KL penalty)", loc="left", color=NAVY)
    _save(fig, "9.2-rlhf/loop.png")


def dpo_skip():
    fig, ax = plt.subplots(figsize=(9.6, 3.6))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 4)
    ax.axis("off")
    _box(ax, (0.3, 2.4), 3.2, 1.1, "preference pairs", FILL, NAVY, 12)
    _box(ax, (4.4, 2.4), 2.8, 1.1, "reward + PPO", FILL3, CORAL, 12)
    _box(ax, (8.0, 2.4), 2.6, 1.1, "aligned π", FILL2, TEAL, 12)
    _arrow(ax, (3.55, 2.95), (4.35, 2.95), CORAL)
    _arrow(ax, (7.25, 2.95), (7.95, 2.95), CORAL)
    ax.text(5.8, 2.15, "RLHF path", ha="center", color=CORAL, fontsize=10)
    _box(ax, (4.4, 0.4), 2.8, 1.1, "DPO loss", FILL4, GOLD, 12)
    _arrow(ax, (1.9, 2.35), (4.35, 1.0), GOLD)
    _arrow(ax, (7.25, 0.95), (9.1, 2.35), GOLD)
    ax.text(5.8, 0.15, "DPO path", ha="center", color=GOLD, fontsize=10)
    ax.set_title("DPO fits the same pairwise data without an explicit reward model", loc="left", color=NAVY)
    _save(fig, "9.3-dpo/dpo.png")


def redteam():
    fig, ax = plt.subplots(figsize=(9.6, 3.6))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 4)
    ax.axis("off")
    _box(ax, (0.3, 1.4), 2.8, 1.3, "benign\nprompts", FILL2, TEAL, 12)
    _box(ax, (3.6, 1.4), 3.6, 1.3, "model under test", FILL, NAVY, 12)
    _box(ax, (7.7, 2.35), 2.9, 1.15, "allowed", FILL2, TEAL, 11)
    _box(ax, (7.7, 0.5), 2.9, 1.15, "harmful / leak", FILL3, CORAL, 11)
    _arrow(ax, (3.15, 2.05), (3.55, 2.05), TEAL)
    _arrow(ax, (7.25, 2.2), (7.65, 2.85), NAVY)
    _arrow(ax, (7.25, 1.85), (7.65, 1.1), CORAL)
    ax.set_title("Red-teaming is an evaluation, not a vibe. Log attacks that work.", loc="left", color=NAVY)
    _save(fig, "10.1-red-teaming/probe.png")


def locate_edit():
    fig, ax = plt.subplots(figsize=(10.0, 3.6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4)
    ax.axis("off")
    _box(ax, (0.3, 1.4), 2.6, 1.3, "subject\n(Eiffel Tower)", FILL3, CORAL, 11)
    _box(ax, (3.4, 1.4), 2.8, 1.3, "locate MLP\n(ROME)", FILL4, GOLD, 11)
    _box(ax, (6.7, 1.4), 2.4, 1.3, "write value", FILL2, TEAL, 11)
    _box(ax, (9.5, 1.4), 2.2, 1.3, "new fact", FILL, NAVY, 11)
    for a, b in [(2.95, 3.35), (6.25, 6.65), (9.15, 9.45)]:
        _arrow(ax, (a, 2.05), (b, 2.05))
    ax.set_title("Locate, then write. One key, not a new pretraining run.", loc="left", color=NAVY)
    _save(fig, "10.2-editing-unlearning/rome.png")


def unlearn_vs_edit():
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.6))
    for ax, title, labels, colors in [
        (axes[0], "Edit one association", ["Paris → ?\n(rewrite)"], [TEAL]),
        (axes[1], "Unlearn a set", ["docs to forget", "retain the rest"], [CORAL, TEAL]),
    ]:
        ax.set_xlim(0, 5)
        ax.set_ylim(0, 4)
        ax.axis("off")
        ax.set_title(title, color=NAVY)
    _box(axes[0], (1.1, 1.4), 2.8, 1.4, "Paris → ?\nrewrite", FILL2, TEAL, 11)
    _box(axes[1], (0.4, 2.3), 4.2, 1.1, "documents to forget", FILL3, CORAL, 11)
    _box(axes[1], (0.4, 0.6), 4.2, 1.1, "everything else stays", FILL2, TEAL, 11)
    fig.tight_layout()
    _save(fig, "10.2-editing-unlearning/unlearn.png")


def raft():
    fig, ax = plt.subplots(figsize=(10.2, 3.6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4)
    ax.axis("off")
    _box(ax, (0.3, 1.4), 2.4, 1.3, "question", FILL, NAVY, 12)
    _box(ax, (3.2, 1.4), 2.6, 1.3, "retrieve\nchunks", FILL3, CORAL, 11)
    _box(ax, (6.3, 1.4), 2.6, 1.3, "train to\nuse them", FILL2, TEAL, 11)
    _box(ax, (9.4, 1.4), 2.3, 1.3, "cite / answer", FILL4, GOLD, 11)
    for a, b in [(2.75, 3.15), (5.85, 6.25), (8.95, 9.35)]:
        _arrow(ax, (a, 2.05), (b, 2.05))
    ax.set_title("RAFT: retrieval is in the training loop, not only at demo time", loc="left", color=NAVY)
    _save(fig, "10.3-raft-memory/raft.png")


def two_memories():
    fig, ax = plt.subplots(figsize=(8.8, 3.6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis("off")
    _box(ax, (0.4, 1.2), 4.2, 1.8, "weights\n(parametric)", FILL, NAVY, 13)
    _box(ax, (5.4, 1.2), 4.2, 1.8, "index / docs\n(non-parametric)", FILL2, TEAL, 13)
    ax.set_title("Two stores. Editing one does not automatically fix the other.", loc="left", color=NAVY)
    _save(fig, "10.3-raft-memory/memory.png")


def _numeric_table(rel, title, headers, rows):
    fig, ax = plt.subplots(figsize=(8.8, 3.5))
    ax.axis("off")
    table = ax.table(cellText=rows, colLabels=headers, loc="center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.15, 1.8)
    for (r, c), cell in table.get_celld().items():
        cell.set_edgecolor(SLATE)
        if r == 0:
            cell.set_facecolor(FILL)
            cell.set_text_props(color=NAVY)
        else:
            cell.set_facecolor("white")
    ax.set_title(title, loc="left", color=NAVY, pad=12)
    _save(fig, rel)


def rm_numeric():
    _numeric_table(
        "9.1-preference-rewards/rm-numeric.png",
        r"Chance is $\log 2\approx 0.693$. Only $\Delta=r_w-r_l$ enters.",
        [r"$\Delta$", r"$\sigma(\Delta)$", "loss"],
        [["0", "0.500", r"$\log 2\approx 0.693$"], ["2", "0.881", "0.127"], ["-2", "0.119", "2.13"]],
    )


def kl_numeric():
    fig, ax = plt.subplots(figsize=(8.4, 4.0))
    names = [r"$\pi_{\mathrm{ref}}$ on $a$", r"$\pi_\theta$ on $a$"]
    vals = [0.7, 0.99]
    ax.bar(names, vals, color=[TEAL, CORAL], edgecolor=NAVY)
    ax.set_ylabel("mass on token a")
    ax.set_ylim(0, 1.15)
    ax.set_title(r"Spike to 0.99: $\mathrm{KL}(\pi_\theta\|\pi_{\mathrm{ref}})\approx 0.31$.", loc="left", color=NAVY)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    _save(fig, "9.2-rlhf/kl-numeric.png")


def dpo_init():
    fig, ax = plt.subplots(figsize=(8.4, 4.0))
    names = [r"init $\pi_\theta=\pi_{\mathrm{ref}}$", "after the toy step"]
    vals = [0.693, 0.201]
    ax.bar(names, vals, color=[CORAL, TEAL], edgecolor=NAVY)
    ax.set_ylabel("DPO loss (nats)")
    ax.set_title(r"$\sigma(0)=1/2$ at start. A +1.5 logit gap cuts the loss.", loc="left", color=NAVY)
    for i, v in enumerate(vals):
        ax.text(i, v + 0.02, f"{v:.3f}", ha="center", color=NAVY)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_ylim(0, 0.85)
    fig.tight_layout()
    _save(fig, "9.3-dpo/dpo-init.png")


def probe_rates():
    fig, ax = plt.subplots(figsize=(8.6, 3.8))
    names = ["over-refusal", "privacy", "stereotype", "disallowed"]
    vals = [0, 1, 2, 1]
    ax.bar(names, vals, color=[TEAL, CORAL, CORAL, CORAL], edgecolor=NAVY)
    ax.set_ylabel("fails / 10 probes")
    ax.set_ylim(0, 4)
    ax.set_title("Same list: 4/40 = 10%. Log ids, not a vibe.", loc="left", color=NAVY)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    _save(fig, "10.1-red-teaming/probe-rates.png")


def edit_probes():
    _numeric_table(
        "10.2-editing-unlearning/edit-probes.png",
        "A flipped prompt is not an isolated fact.",
        ["probe", "success"],
        [["edit (France→Berlin)", "8/10"], ["neighbor (Italy)", "2/10"], ["retain (unrelated)", "9/10"]],
    )


def overlap_retrieve():
    fig, ax = plt.subplots(figsize=(8.6, 3.8))
    names = ["1 gold", "2 exam", "3 hours", "4 old"]
    vals = [5, 1, 1, 4]
    colors = [TEAL, SLATE, SLATE, CORAL]
    ax.bar(names, vals, color=colors, edgecolor=NAVY)
    ax.axhline(0, color=SLATE, lw=0.6)
    ax.set_ylabel("token overlap with the query")
    ax.set_title("Top-3 at k=3: gold, old, exam. Train the reader to skip 4.", loc="left", color=NAVY)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    _save(fig, "10.3-raft-memory/overlap-retrieve.png")


def gan_players():
    fig, ax = plt.subplots(figsize=(9.6, 3.8))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 4.2)
    ax.axis("off")
    _box(ax, (0.3, 2.5), 2.4, 1.1, r"$z \sim p(z)$", FILL4, GOLD, 12)
    _box(ax, (3.3, 2.5), 2.4, 1.1, "generator $G$", FILL3, CORAL, 12)
    _box(ax, (6.4, 2.5), 2.2, 1.1, r"$G(z)$ fake", FILL3, CORAL, 11)
    _box(ax, (6.4, 0.45), 2.2, 1.1, "real $x$", FILL2, TEAL, 12)
    _box(ax, (9.1, 1.35), 1.7, 1.4, r"$D$", FILL, NAVY, 14)
    _arrow(ax, (2.75, 3.05), (3.25, 3.05), GOLD)
    _arrow(ax, (5.75, 3.05), (6.35, 3.05), CORAL)
    _arrow(ax, (8.65, 3.05), (9.1, 2.3), CORAL)
    _arrow(ax, (8.65, 1.0), (9.1, 1.7), TEAL)
    ax.set_title("GAN: $G$ tries to fool $D$; $D$ tries not to be fooled", loc="left", color=NAVY)
    _save(fig, "11.1-gan-idea/players.png")


def gan_minmax():
    fig, ax = plt.subplots(figsize=(8.2, 3.8))
    t = np.linspace(0, 8, 200)
    d = 0.5 + 0.25 * np.sin(2.2 * t) * np.exp(-0.08 * t)
    g = 0.5 - 0.22 * np.sin(2.2 * t + 0.6) * np.exp(-0.08 * t)
    ax.plot(t, d, color=NAVY, lw=2.1, label="discriminator accuracy")
    ax.plot(t, g, color=CORAL, lw=2.1, label="generator quality (sketch)")
    ax.set_ylim(0.15, 0.9)
    ax.set_xlabel("training time")
    ax.legend(frameon=False)
    ax.set_title("The two losses should stay in tension. A 99% $D$ is often a dead $G$.", loc="left", color=NAVY)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    _save(fig, "11.2-gan-training/dynamics.png")


def mode_collapse():
    rng = np.random.default_rng(0)
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 3.8), sharex=True, sharey=True)
    real = np.vstack(
        [
            rng.normal([-1.6, 0], 0.28, size=(80, 2)),
            rng.normal([1.6, 0], 0.28, size=(80, 2)),
        ]
    )
    fake = rng.normal([-1.55, 0.05], 0.22, size=(120, 2))
    axes[0].scatter(real[:, 0], real[:, 1], s=18, c=TEAL, alpha=0.75)
    axes[0].set_title("data: two modes", color=NAVY)
    axes[1].scatter(fake[:, 0], fake[:, 1], s=18, c=CORAL, alpha=0.75)
    axes[1].set_title("collapsed generator: one mode", color=NAVY)
    for ax in axes:
        ax.set_aspect("equal")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])
    fig.tight_layout()
    _save(fig, "11.3-mode-collapse/collapse.png")


def forward_noise():
    rng = np.random.default_rng(1)
    fig, axes = plt.subplots(1, 4, figsize=(10.4, 2.8))
    x = rng.normal([0, 0], 0.15, size=(40, 2)) + np.array([0.0, 0.0])
    shape = np.array([[-0.6, -0.4], [0.7, -0.3], [0.2, 0.7]])
    pts0 = rng.normal(0, 0.08, size=(50, 2))
    pts0[:, 0] += np.linspace(-0.7, 0.7, 50)
    pts0[:, 1] += 0.4 * np.sin(3 * pts0[:, 0])
    ts = [0, 0.3, 0.65, 1.0]
    titles = [r"$x_0$", r"$x_t$", r"$x_{t'}$", r"$x_T$"]
    for ax, t, title in zip(axes, ts, titles):
        pts = np.sqrt(1 - t) * pts0 + np.sqrt(t) * rng.normal(0, 0.55, size=pts0.shape)
        ax.scatter(pts[:, 0], pts[:, 1], s=14, c=NAVY if t < 0.9 else SLATE, alpha=0.8)
        ax.set_xlim(-2.2, 2.2)
        ax.set_ylim(-2.0, 2.0)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(title, color=NAVY)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    fig.suptitle("Forward process: data becomes noise", color=NAVY, y=1.08)
    fig.tight_layout()
    _save(fig, "12.1-diffusion-forward/forward.png")


def reverse_denoise():
    fig, ax = plt.subplots(figsize=(10.2, 3.0))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 3.2)
    ax.axis("off")
    labs = [r"$x_T$", r"$x_{t}$", r"$x_{t-1}$", r"$x_0$"]
    xs = [0.4, 3.4, 6.4, 9.4]
    cols = [SLATE, NAVY, TEAL, CORAL]
    fills = [FILL, FILL, FILL2, FILL3]
    for x, lab, c, f in zip(xs, labs, cols, fills):
        _box(ax, (x, 0.85), 2.2, 1.3, lab, f, c, 13)
    for i in range(3):
        _arrow(ax, (xs[i] + 2.25, 1.5), (xs[i + 1], 1.5), TEAL)
    ax.set_title("Reverse: a network predicts the noise (or $x_0$) and steps toward data", loc="left", color=NAVY)
    _save(fig, "12.2-diffusion-reverse/reverse.png")


def latent_ldm():
    fig, ax = plt.subplots(figsize=(10.6, 3.8))
    ax.set_xlim(0, 12.5)
    ax.set_ylim(0, 4.4)
    ax.axis("off")
    _box(ax, (0.25, 2.4), 2.3, 1.15, "image", FILL3, CORAL, 12)
    _box(ax, (3.0, 2.4), 2.3, 1.15, "VAE encoder", FILL, NAVY, 11)
    _box(ax, (5.8, 2.4), 2.5, 1.15, "latent UNet\n(+ noise)", FILL2, TEAL, 11)
    _box(ax, (8.8, 2.4), 3.2, 1.15, "VAE decoder", FILL, NAVY, 11)
    _box(ax, (5.8, 0.45), 2.5, 1.15, "text / CLIP", FILL4, GOLD, 12)
    _arrow(ax, (2.6, 2.95), (2.95, 2.95), CORAL)
    _arrow(ax, (5.35, 2.95), (5.75, 2.95))
    _arrow(ax, (8.35, 2.95), (8.75, 2.95), TEAL)
    _arrow(ax, (7.05, 1.65), (7.05, 2.35), GOLD)
    ax.set_title("Latent diffusion: denoise a cheap latent, condition on text", loc="left", color=NAVY)
    _save(fig, "12.3-latent-conditioning/ldm.png")


def d_bayes():
    _numeric_table(
        "11.1-gan-idea/d-bayes.png",
        r"G parked on $+2$. Bayes $D(+2)=1/2$; the left mode is uncontested.",
        ["location", "what D sees", r"$D(x)$"],
        [[r"$x=+2$", "half real, half fake", "0.5"], [r"$x=-2$", "only reals", "1"], ["elsewhere", "only fakes, if any", r"$\approx 0$"]],
    )


def j_numeric():
    _numeric_table(
        "11.2-gan-training/j-numeric.png",
        r"$D(G(z))=0.01$: saturating $G$ loss is flat; $-\log D$ still has slope.",
        ["quantity", "value"],
        [
            [r"$J$ sample ($D_x=0.9$, $D_g=0.2$)", r"$-0.328$"],
            [r"$\log(1-D)$ at $0.01$", r"$-0.010$"],
            [r"$-\log D$ at $0.01$", "4.605"],
        ],
    )


def coverage_bins():
    fig, ax = plt.subplots(figsize=(8.4, 4.0))
    names = ["seed A\n92 / 8", "seed B\n47 / 53"]
    left = [92, 47]
    right = [8, 53]
    x = np.arange(2)
    ax.bar(x - 0.18, left, 0.36, color=CORAL, edgecolor=NAVY, label="mode A")
    ax.bar(x + 0.18, right, 0.36, color=TEAL, edgecolor=NAVY, label="mode B")
    ax.axhline(10, color=SLATE, ls="--", lw=1)
    ax.set_xticks(x)
    ax.set_xticklabels(names)
    ax.set_ylabel("fakes / 100")
    ax.set_ylim(0, 110)
    ax.legend(frameon=False)
    ax.set_title("Lab 11: a bin under 10% is collapse. Same net, two seeds.", loc="left", color=NAVY)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    _save(fig, "11.3-mode-collapse/coverage-bins.png")


def alphabar_table():
    _numeric_table(
        "12.1-diffusion-forward/alphabar.png",
        r"$x_0=1$, $\varepsilon=2$. At $\bar\alpha=0.64$ you already sit at 2.0.",
        [r"$\bar\alpha_t$", r"$\sqrt{\bar\alpha}\,x_0$", r"$x_t$"],
        [["1", "1.0", "1.0"], ["0.64", "0.8", "2.0"], ["0", "0", "2.0"]],
    )


def reverse_mean():
    _numeric_table(
        "12.2-diffusion-reverse/reverse-mean.png",
        r"Oracle $\varepsilon_\theta=\varepsilon=2$: one reverse mean lands on $x_0=1$.",
        ["piece", "value"],
        [
            [r"$x_t$", "2.0"],
            [r"$(1-\alpha_t)/\sqrt{1-\bar\alpha_t}\cdot\varepsilon$", "1.2"],
            [r"$x_{t-1}$ mean", "1.0"],
        ],
    )


def latent_count():
    fig, ax = plt.subplots(figsize=(8.4, 4.0))
    names = ["pixels\n256×256×3", "CS231N latent\n32×32×16"]
    vals = [256 * 256 * 3 / 1000, 32 * 32 * 16 / 1000]
    ax.bar(names, vals, color=[CORAL, TEAL], edgecolor=NAVY)
    ax.set_ylabel("thousands of numbers")
    ax.set_title("CS231N L14: D=8, C=16. Denoise 12× fewer cells.", loc="left", color=NAVY)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    _save(fig, "12.3-latent-conditioning/latent-count.png")


def cfg_scale():
    fig, ax = plt.subplots(figsize=(8.4, 4.0))
    s = np.array([1, 3, 7.5])
    hat = 0.8 - 0.6 * s
    ax.bar([r"$s=1$", r"$s=3$", r"$s=7.5$"], hat, color=[TEAL, GOLD, CORAL], edgecolor=NAVY)
    ax.axhline(0.2, color=SLATE, ls="--", lw=1)
    ax.set_ylabel(r"$\hat\varepsilon$")
    ax.set_title(r"$\varepsilon_\varnothing=0.8$, $\varepsilon_c=0.2$. $s=1$ is still conditional.", loc="left", color=NAVY)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    _save(fig, "12.3-latent-conditioning/cfg-scale.png")


def cot_vs_direct():
    fig, axes = plt.subplots(1, 2, figsize=(9.8, 3.6))
    for ax in axes:
        ax.set_xlim(0, 5)
        ax.set_ylim(0, 5)
        ax.axis("off")
    axes[0].set_title("Direct", color=NAVY)
    axes[1].set_title("Chain-of-thought", color=NAVY)
    _box(axes[0], (0.5, 3.3), 4.0, 0.9, "question", FILL, NAVY, 11)
    _box(axes[0], (0.5, 1.5), 4.0, 0.9, "answer", FILL3, CORAL, 11)
    _arrow(axes[0], (2.5, 3.25), (2.5, 2.45), CORAL)
    _box(axes[1], (0.5, 3.7), 4.0, 0.7, "question", FILL, NAVY, 11)
    _box(axes[1], (0.5, 2.3), 4.0, 0.9, "steps …", FILL2, TEAL, 11)
    _box(axes[1], (0.5, 0.7), 4.0, 0.9, "answer", FILL3, CORAL, 11)
    _arrow(axes[1], (2.5, 3.65), (2.5, 3.25), TEAL)
    _arrow(axes[1], (2.5, 2.25), (2.5, 1.65), CORAL)
    fig.tight_layout()
    _save(fig, "13.1-chain-of-thought/cot.png")


def tot_tree():
    fig, ax = plt.subplots(figsize=(9.2, 4.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis("off")
    _box(ax, (3.7, 4.05), 2.6, 0.7, "problem", FILL, NAVY, 11)
    nodes = [(1.0, 2.5, "path A"), (3.7, 2.5, "path B"), (6.4, 2.5, "path C")]
    for x, y, t in nodes:
        _box(ax, (x, y), 2.4, 0.75, t, FILL2, TEAL, 10)
        _arrow(ax, (5.0, 4.0), (x + 1.2, y + 0.8), TEAL)
    _box(ax, (3.7, 0.45), 2.6, 0.8, "vote / search", FILL4, GOLD, 11)
    _arrow(ax, (2.2, 2.45), (4.2, 1.3), GOLD)
    _arrow(ax, (4.9, 2.45), (5.0, 1.3), GOLD)
    _arrow(ax, (7.6, 2.45), (5.8, 1.3), GOLD)
    ax.set_title("Self-consistency votes; Tree-of-Thoughts searches partial steps", loc="left", color=NAVY)
    _save(fig, "13.2-self-consistency-tot/tree.png")


def faithfulness():
    fig, ax = plt.subplots(figsize=(9.4, 3.6))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 4)
    ax.axis("off")
    _box(ax, (0.3, 1.3), 4.6, 1.6, "trace looks careful\n(but the algebra is wrong)", FILL3, CORAL, 11)
    _box(ax, (6.0, 1.3), 4.6, 1.6, "final number happens\nto be correct", FILL2, TEAL, 11)
    ax.set_title("Faithfulness: do the steps actually cause the answer?", loc="left", color=NAVY)
    _save(fig, "13.3-faithfulness/unfaithful.png")


def rag_pipe():
    fig, ax = plt.subplots(figsize=(10.6, 3.6))
    ax.set_xlim(0, 12.4)
    ax.set_ylim(0, 4)
    ax.axis("off")
    _box(ax, (0.2, 1.4), 2.3, 1.3, "corpus", FILL, NAVY, 12)
    _box(ax, (2.9, 1.4), 2.4, 1.3, "index\n(embed)", FILL2, TEAL, 11)
    _box(ax, (5.7, 1.4), 2.4, 1.3, "retrieve\n$k$ chunks", FILL3, CORAL, 11)
    _box(ax, (8.5, 1.4), 3.5, 1.3, "generate with\nchunks in context", FILL4, GOLD, 11)
    for a, b in [(2.55, 2.85), (5.35, 5.65), (8.15, 8.45)]:
        _arrow(ax, (a, 2.05), (b, 2.05))
    ax.set_title("RAG: non-parametric memory at inference (and, in RAFT, at train time)", loc="left", color=NAVY)
    _save(fig, "14.1-rag-pipeline/rag.png")


def react_loop():
    fig, ax = plt.subplots(figsize=(9.8, 3.6))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 4)
    ax.axis("off")
    _box(ax, (0.3, 1.45), 2.4, 1.2, "Thought", FILL, NAVY, 12)
    _box(ax, (3.3, 1.45), 2.4, 1.2, "Action\n(tool)", FILL3, CORAL, 12)
    _box(ax, (6.3, 1.45), 2.4, 1.2, "Observation", FILL2, TEAL, 12)
    _box(ax, (9.2, 1.45), 1.5, 1.2, "…", FILL4, GOLD, 14)
    _arrow(ax, (2.75, 2.05), (3.25, 2.05))
    _arrow(ax, (5.75, 2.05), (6.25, 2.05), CORAL)
    _arrow(ax, (8.75, 2.05), (9.15, 2.05), TEAL)
    ax.annotate(
        "",
        xy=(1.5, 1.4),
        xytext=(9.9, 1.4),
        arrowprops=dict(arrowstyle="-|>", color=SLATE, connectionstyle="arc3,rad=-0.32", lw=1.4),
    )
    ax.set_title("ReAct: think, call a tool, read the result, repeat", loc="left", color=NAVY)
    _save(fig, "14.2-react-tools/react.png")


def talk_eval():
    fig, ax = plt.subplots(figsize=(9.2, 3.8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.2)
    ax.axis("off")
    items = [
        (0.3, 2.5, "question +\nmetric"),
        (3.5, 2.5, "baseline +\nablation"),
        (6.7, 2.5, "failure case"),
        (2.0, 0.6, "cite sources"),
        (5.2, 0.6, "uncertainty"),
    ]
    for x, y, t in items:
        _box(ax, (x, y), 2.8, 1.2, t, FILL, NAVY, 11)
    ax.set_title("A talk is an evaluation story, not a gallery of screenshots", loc="left", color=NAVY)
    _save(fig, "14.3-eval-presentations/talk.png")


def exam_map():
    fig, ax = plt.subplots(figsize=(10.4, 4.2))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5)
    ax.axis("off")
    mods = [
        (0.3, 2.6, 2.6, 1.6, "M1\nnets → transformers", FILL, NAVY),
        (3.2, 2.6, 2.6, 1.6, "M2\nvision, audio, CLIP", FILL2, TEAL),
        (6.1, 2.6, 2.6, 1.6, "M3\nscale, SFT, RLHF", FILL3, CORAL),
        (9.0, 2.6, 2.6, 1.6, "M4\nGAN, diffusion, RAG", FILL4, GOLD),
    ]
    for x, y, w, h, t, f, e in mods:
        _box(ax, (x, y), w, h, t, f, e, 11)
        if x < 8:
            _arrow(ax, (x + w + 0.05, y + h / 2), (x + 2.85, y + h / 2))
    _box(ax, (3.2, 0.5), 5.6, 1.3, "exam: connect a method to a measurement", FILL5, NAVY, 12)
    ax.set_title("Four modules, one stack. The project sits on top of all four.", loc="left", color=NAVY)
    _save(fig, "15.1-exam-review/map.png")


def cot_partial():
    _numeric_table(
        "13.1-chain-of-thought/cot-partial.png",
        r"$17\times 24$: three lines hold the partial products. Direct decode has no tape.",
        ["step", "value"],
        [[r"$10\times 24$", "240"], [r"$7\times 24$", "168"], ["sum", "408"]],
    )


def sc_vote():
    fig, ax = plt.subplots(figsize=(8.4, 4.0))
    names = ["trace A", "trace B", "trace C"]
    vals = [42, 32, 42]
    colors = [TEAL, CORAL, TEAL]
    ax.bar(names, vals, color=colors, edgecolor=NAVY)
    ax.axhline(42, color=SLATE, ls="--", lw=1)
    ax.set_ylabel("parsed answer")
    ax.set_title("Vote on answers: 42, 32, 42. Majority is 42. k=1 on B would miss.", loc="left", color=NAVY)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    _save(fig, "13.2-self-consistency-tot/sc-vote.png")


def gsm8k_sc():
    fig, ax = plt.subplots(figsize=(8.4, 4.0))
    names = ["greedy CoT", "self-consistency"]
    vals = [0, 17.9]
    ax.bar(names, vals, color=[SLATE, TEAL], edgecolor=NAVY)
    ax.set_ylabel("GSM8K lift vs greedy CoT (pp)")
    ax.set_title("CS224N L12: Wang et al. majority vote, +17.9 pp on GSM8K.", loc="left", color=NAVY)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    _save(fig, "13.2-self-consistency-tot/gsm8k-sc.png")


def lucky_win():
    _numeric_table(
        "13.3-faithfulness/lucky-win.png",
        "Correct box, wrong last step: accuracy +1, faithfulness 0.",
        ["field", "value"],
        [["last integer in steps", "52"], ["box / answer", "42"], ["gold", "42"]],
    )


def cosine_rank():
    fig, ax = plt.subplots(figsize=(8.4, 4.0))
    names = ["d1 library close", "d3 library hours", "d2 shuttle"]
    vals = [1.0, 0.707, 0.0]
    colors = [TEAL, GOLD, SLATE]
    ax.bar(names, vals, color=colors, edgecolor=NAVY)
    ax.set_ylabel("cosine with q")
    ax.set_ylim(0, 1.15)
    ax.set_title(r"$k=1$ stuffs d1. $k=2$ also stuffs the near-miss d3.", loc="left", color=NAVY)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    _save(fig, "14.1-rag-pipeline/cosine-rank.png")


def seed_spread():
    fig, ax = plt.subplots(figsize=(8.4, 4.0))
    names = ["mean lift", "seed spread"]
    vals = [0.02, 0.04]
    ax.bar(names, vals, color=[GOLD, CORAL], edgecolor=NAVY)
    ax.set_ylabel("accuracy points")
    ax.set_title("RAG +2 pp; seeds move by 4 pp. n=50. Do not lead with the lift.", loc="left", color=NAVY)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    _save(fig, "14.3-eval-presentations/seed-spread.png")


def exam_metric():
    _numeric_table(
        "15.1-exam-review/fail-metric.png",
        "Exam shape: name the method, then the number that would have caught it.",
        ["failure", "measure"],
        [
            ["same face, low lossG", "mode bins"],
            ["right box, last step 52", "faithful among wins"],
            ["cite [d5], fact in [d1]", "attribution + recall@k"],
        ],
    )


def main():
    _setup()
    waveform_spectrogram()
    spec_patches()
    whisper_encdec()
    clap_towers()
    fusion_kinds()
    data_pyramid()
    stft_frames()
    whisper_chunk()
    clap_rank()
    concat_add()
    scaling_curve()
    chinchilla()
    moe()
    compress_pipeline()
    speculative()
    sft_stack()
    prompt_pair()
    forgetting()
    replay()
    lora_ba()
    federated()
    gpt3_tokens()
    moe_collapse()
    int8_table()
    sft_mask()
    lora_count()
    preference_pair()
    reward_model()
    rlhf_loop()
    dpo_skip()
    redteam()
    locate_edit()
    unlearn_vs_edit()
    raft()
    two_memories()
    rm_numeric()
    kl_numeric()
    dpo_init()
    probe_rates()
    edit_probes()
    overlap_retrieve()
    gan_players()
    gan_minmax()
    mode_collapse()
    forward_noise()
    reverse_denoise()
    latent_ldm()
    d_bayes()
    j_numeric()
    coverage_bins()
    alphabar_table()
    reverse_mean()
    latent_count()
    cfg_scale()
    cot_vs_direct()
    tot_tree()
    faithfulness()
    rag_pipe()
    react_loop()
    talk_eval()
    exam_map()
    cot_partial()
    sc_vote()
    gsm8k_sc()
    lucky_win()
    cosine_rank()
    seed_spread()
    exam_metric()
    print("done")


if __name__ == "__main__":
    main()
