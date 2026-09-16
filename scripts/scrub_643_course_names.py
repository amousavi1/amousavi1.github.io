"""Strip in-lecture university course codes; keep title-slide credits and hub extras."""

from __future__ import annotations

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
NOTES = ROOT / "files" / "data-643"

# Longest phrases first.
REPLACEMENTS: list[tuple[str, str]] = [
    (
        "Stanford **CS224N 2026 L10** calls the passages **non-parametric memory**: the facts live in an index you can edit, not only inside \\(\\theta\\).",
        "The passages are **non-parametric memory**: the facts live in an index you can edit, not only inside \\(\\theta\\).",
    ),
    (
        "Stanford **CS224N 2026 L10** contrasts **ReAct vs CoT vs self-consistency**.",
        "Contrast **ReAct vs CoT vs self-consistency**.",
    ),
    (
        "Stanford **CS224N 2026 L12** points at Chen et al. (2025): models can **use a hint** without writing it in the CoT. This course’s classroom version is Lab 13: last integer 52, box 42. **CS224N L13** / Lightman et al. (*Let’s Verify Step by Step*): a **process** reward scores the steps; an **outcome** reward scores only the box.",
        "Chen et al. (2025): models can **use a hint** without writing it in the CoT. This course’s classroom version is Lab 13: last integer 52, box 42. Lightman et al. (*Let’s Verify Step by Step*): a **process** reward scores the steps; an **outcome** reward scores only the box.",
    ),
    (
        "Stanford **CS224N 2026 L12** cites Wang et al.: majority vote raised GSM8K by **+17.9 percentage points** versus greedy CoT.",
        "Wang et al.: majority vote raised GSM8K by **+17.9 percentage points** versus greedy CoT.",
    ),
    (
        "Voting on the **answer** (not the wording) lifts GSM8K-style math in the CS224N L12 figure (~+17.9 pp in that citation).",
        "Voting on the **answer** (not the wording) lifts GSM8K-style math (~+17.9 pp in Wang et al.).",
    ),
    (
        "Accuracy can pass while the trace is a lie. Process vs outcome (CS224N L13).",
        "Accuracy can pass while the trace is a lie. Process vs outcome (Lightman et al.).",
    ),
    (
        "Stanford **CS224N 2026 L12**: this is a **prompt / decoding** choice, not a new architecture.",
        "This is a **prompt / decoding** choice, not a new architecture.",
    ),
    (
        "That is the CS224N L12 punch in classroom language.",
        "That is extra test-time compute in classroom language.",
    ),
    (
        "Stanford CS224N 2025: if a component stores the association, intervening on it should change the predicted object.",
        "If a component stores the association, intervening on it should change the predicted object.",
    ),
    (
        "Stanford CS224N 2025 L13: **parametric** recall versus **open-book**.",
        "**Parametric** recall versus **open-book**.",
    ),
    (
        "Stanford CS224N 2025 L11 puts pruning next to LoRA (fewer weights vs a small \\(\\Delta\\)). Distill and speculate stay on this board.",
        "Pruning is fewer weights; LoRA (note **8.3**) is a small \\(\\Delta\\). Distill and speculate stay on this board.",
    ),
    (
        "Stanford CS224N 2025 L11 (PEFT): the reason for LoRA is that a full \\(\\Delta\\) has the same size as \\(\\boldsymbol{W}\\) (GPT-3: 175B extra weights per task).",
        "The reason for LoRA is that a full \\(\\Delta\\) has the same size as \\(\\boldsymbol{W}\\) (GPT-3: 175B extra weights per task).",
    ),
    (
        "CS224N L11’s PEFT motivation is the same geometry: a full fine-tune is a second copy of \\(\\boldsymbol{W}\\), and that copy walks off task A.",
        "A full fine-tune is a second copy of \\(\\boldsymbol{W}\\), and that copy walks off task A.",
    ),
    (
        "Stanford CS224N 2025 L10: instruction fine-tuning is the **first** stage of the InstructGPT / ChatGPT stack.",
        "Instruction fine-tuning is the **first** stage of the InstructGPT / ChatGPT stack.",
    ),
    (
        "Stanford CS224N 2025 L10: **best-of-\\(n\\)** already uses this RM and is a competitive baseline (AlpacaFarm).",
        "**Best-of-\\(n\\)** already uses this RM and is a competitive baseline (AlpacaFarm).",
    ),
    (
        "Stanford CS224N 2025 L10 draws the same three boxes (SFT, RM, RL) and notes that **best-of-\\(n\\)** is already a strong baseline in AlpacaFarm-style studies.",
        "The three boxes are SFT, RM, and RL. **Best-of-\\(n\\)** is already a strong baseline in AlpacaFarm-style studies.",
    ),
    (
        "Stanford CS224N 2025 L10 writes the same derived reward and stresses that the **partition \\(Z(x)\\)** cancels because Bradley–Terry only sees a difference.",
        "The derived reward has a **partition \\(Z(x)\\)** that cancels because Bradley–Terry only sees a difference.",
    ),
    (
        "Stanford CS336 2025 L12 treats safety the same way: **HarmBench** is 510 labeled behaviors; **AIR-Bench** is 314 categories and 5694 prompts; HELM hosts the suites.",
        "**HarmBench** is 510 labeled behaviors; **AIR-Bench** is 314 categories and 5694 prompts; HELM hosts the suites.",
    ),
    (
        "Stanford CS224N 2025 L9’s classroom example: GPT-3 was",
        "GPT-3 was",
    ),
    (
        "Same lecture: a \\(70\\,\\mathrm{B}\\) model trained with enough tokens beat much larger undertrained nets.",
        "A \\(70\\,\\mathrm{B}\\) model trained with enough tokens beat much larger undertrained nets.",
    ),
    (
        "Stanford CS336 2025 L4’s Mixtral row is the one to memorize: **8 routed experts, top-2 active, no shared expert.**",
        "Mixtral’s row to memorize: **8 routed experts, top-2 active, no shared expert.**",
    ),
    (
        "CS224N’s slogan: attention is a **direct connection** from the decoder to the encoder states, so the model can reread instead of remember.",
        "Attention is a **direct connection** from the decoder to the encoder states, so the model can reread instead of remember.",
    ),
    (
        "CS224N’s slogan: **pretrain once, fine-tune many times.**",
        "**Pretrain once, fine-tune many times.**",
    ),
    (
        "That is CMU 11-711’s calculation, and Lab 3.",
        "That is the calculation, and Lab 3.",
    ),
    (
        "Princeton COS 484 L10 is the matching pretraining hour; CS224N’s pretraining lecture is the same fork.",
        "The fork is the objective: causal language modeling versus masked language modeling.",
    ),
    (
        "That is Princeton COS 484’s assembly order.",
        "That is the assembly order.",
    ),
    (
        "CMU 11-777’s list is the map: **representation, alignment, fusion, translation, co-learning**.",
        "The five jobs are **representation, alignment, fusion, translation, co-learning** (Baltrušaitis et al.).",
    ),
    (
        "CLIP is this; CMU 11-777 also puts CCA here",
        "CLIP is this; canonical correlation analysis is another coordinated family",
    ),
    (
        "Note **4.1** introduced joint versus coordinated (CMU 11-777). This note is 11-777’s **fusion** lecture in classroom form: early, late, and cross-attention, then the data pyramid.",
        "Note **4.1** introduced joint versus coordinated. This note is **fusion**: early, late, and cross-attention, then the data pyramid.",
    ),
    (
        "11-777’s warning, in our words: naming “multimodal” does not name the fusion.",
        "Naming “multimodal” does not name the fusion.",
    ),
    (
        "Stanford CS231N 2025 L16 is the matching vision–language hour; CMU 11-777 already called this a **coordination** loss.",
        "This is a **coordination** loss: two towers, a similarity, no fused decoder.",
    ),
    (
        "Stanford CS231N 2025 L16’s punchline is the one we keep: after training you have a **similarity score** between an image and a text, not a captioner.",
        "After training you have a **similarity score** between an image and a text, not a captioner.",
    ),
    (
        "CS231N 2025 L16’s CoCa slide is the sibling idea: add a **decoder**.",
        "CoCa (Yu et al.) is the sibling idea: add a **decoder**.",
    ),
    (
        "CoCa (Yu et al.; the CS231N generation slide) adds a captioning loss on top of contrastive training.",
        "CoCa (Yu et al.) adds a captioning loss on top of contrastive training.",
    ),
    (
        "LLaVA (CS231N’s next family) is a frozen CLIP tower plus an LLM.",
        "LLaVA is a frozen CLIP tower plus an LLM.",
    ),
    (
        "Stanford CS231N 2025 L8 is the matching vision lecture: patchify, linear map, positions, **no causal mask**.",
        "The recipe is patchify, linear map, positions, **no causal mask**.",
    ),
    (
        "CS231N’s extra slogan: that linear map is the same as a convolution with kernel \\(P\\), stride \\(P\\), \\(d\\) output channels.",
        "That linear map is the same as a convolution with kernel \\(P\\), stride \\(P\\), \\(d\\) output channels.",
    ),
    (
        "7. CS231N: the patch linear map is a convolution with which kernel size and stride?",
        "7. The patch linear map is a convolution with which kernel size and stride?",
    ),
    (
        "CS231N 2025 L16 already warned that a single prompt can be peaked; this note measures what that geometry retrieves.",
        "A single prompt can be peaked; this note measures what that geometry retrieves.",
    ),
    (
        "Stanford CS224S (L2 acoustic phonetics; L5 “why spectrograms”) is the matching course: once you have a 2-D time–frequency picture, every vision trick from Week 4 (patches, a transformer, CLIP-style towers) applies to audio.",
        "Once you have a 2-D time–frequency picture, every vision trick from Week 4 (patches, a transformer, CLIP-style towers) applies to audio.",
    ),
    (
        "CS224S’s reason to prefer this over a raw wave:",
        "The reason to prefer this over a raw wave:",
    ),
    (
        "The matching lecture for Whisper is Stanford CS224S 2025 L11 (Conformer / Whisper): log-mel in, two convs, a transformer encoder, a GPT-style decoder, 30-second chunks, no CTC.",
        "Whisper: log-mel in, two convs, a transformer encoder, a GPT-style decoder, 30-second chunks, no CTC.",
    ),
    (
        "CS224S: encoder input is the log-mel plus **two convolutional layers**, then positional embeddings, then standard transformer blocks. The decoder is causal and **cross-attends** to the encoder, like translation in note **3.3**. CS224S’s wording: it is a **GPT-2 style** decoder. There is **no CTC loss**.",
        "Encoder input is the log-mel plus **two convolutional layers**, then positional embeddings, then standard transformer blocks. The decoder is causal and **cross-attends** to the encoder, like translation in note **3.3**. It is a **GPT-2 style** decoder. There is **no CTC loss**.",
    ),
    (
        "(CS224S: on the order of 680{,}000 hours)",
        "(on the order of 680{,}000 hours)",
    ),
    (
        "(as in the paper’s stem / CS224S’s two convs)",
        "(as in the paper’s stem, two convs)",
    ),
    (
        "- Assuming Whisper still uses CTC. CS224S: GPT-2 decoder, no CTC.",
        "- Assuming Whisper still uses CTC. Whisper’s decoder is GPT-2 style; there is no CTC.",
    ),
    (
        "CMU 11-711 writes the softmax/cross-entropy cousin \\(\\partial L/\\partial w=(p-y)x\\). Same “upstream error times input” shape.",
        "The softmax/cross-entropy cousin is \\(\\partial L/\\partial w=(p-y)x\\). Same “upstream error times input” shape.",
    ),
    (
        "Nielsen calls this the **cost**; CS231N calls it the **loss**; a statistician calls it **empirical risk**. Same object.",
        "Nielsen calls this the **cost**; the usual name here is **loss**; a statistician calls it **empirical risk**. Same object.",
    ),
    (
        "CS231N treats each operation as a **gate** with a local derivative.",
        "Treat each operation as a **gate** with a local derivative.",
    ),
    (
        "CS231N’s slogan: multiplying by the activation Jacobian is **almost always a shrink**.",
        "Multiplying by the activation Jacobian is **almost always a shrink**.",
    ),
    (
        "where \\(\\lambda_{\\max}\\) is the largest-magnitude eigenvalue of \\(W_h\\) (CMU 11-785 L14). CS231N says the same thing with the largest **singular value**.",
        "where \\(\\lambda_{\\max}\\) is the largest-magnitude eigenvalue of \\(W_h\\). The same fact is often stated with the largest **singular value**.",
    ),
    (
        "CS224N’s tickets example, shortened:",
        "A long-range example, shortened:",
    ),
    (
        "CMU 11-785’s stability lecture: unless \\(W_h\\) is essentially a wire",
        "Unless \\(W_h\\) is essentially a wire",
    ),
    (
        "CS231N’s warning, which we keep: **LSTM does not guarantee** that every coordinate copies.",
        "**LSTM does not guarantee** that every coordinate copies.",
    ),
    (
        "Stanford CS231N 2025 L13: a GAN is an **implicit** density and a **direct** sample.",
        "A GAN is an **implicit** density and a **direct** sample.",
    ),
    (
        "The optimal discriminator (Goodfellow / CS231N) is",
        "The optimal discriminator (Goodfellow et al.) is",
    ),
    (
        "Stanford CS231N 2025 L13 writes the same minimax and the practical loop: update \\(D\\), then \\(G\\).",
        "The practical loop is the same minimax: update \\(D\\), then \\(G\\).",
    ),
    (
        "CS231N’s GAN recap: you can interpolate in \\(z\\) when the map is healthy (StyleGAN made that famous).",
        "You can interpolate in \\(z\\) when the map is healthy (StyleGAN made that famous).",
    ),
    (
        "Stanford CS231N 2025 L14: pick a noise level, corrupt \\(x\\), then learn to undo a bit.",
        "Pick a noise level, corrupt \\(x\\), then learn to undo a bit.",
    ),
    (
        "CS231N L14: sampling is an **iterative** procedure.",
        "Sampling is an **iterative** procedure.",
    ),
    (
        "Latent cells are fewer (CS231N: on the order of \\(12\\times\\) fewer in the Stable Diffusion cartoon).",
        "Latent cells are fewer (on the order of \\(12\\times\\) fewer in the Stable Diffusion cartoon).",
    ),
    (
        "Stanford CS231N 2025 L14’s classroom setting is \\(D=8\\), \\(C=16\\):",
        "A classroom setting is \\(D=8\\), \\(C=16\\):",
    ),
    (
        "![Pixel cells versus CS231N’s latent cells]",
        "![Pixel cells versus latent cells]",
    ),
    (
        "CS231N L14: randomly **drop** the text in training so one net is both conditional and unconditional.",
        "Randomly **drop** the text in training so one net is both conditional and unconditional.",
    ),
    (
        "CS231N’s next slide after CLIP is **CoCa**:",
        "**CoCa** is next after CLIP:",
    ),
    (
        "CS231N: a single phrase can be too peaked;",
        "A single phrase can be too peaked;",
    ),
    (
        "Zero-shot is what makes CLIP a **foundation** model in CS231N L16.",
        "Zero-shot is what makes CLIP a **foundation** model.",
    ),
    (
        "CS231N’s warning: the raw label `\"dog\"` often loses to `\"a photo of a dog\"`.",
        "The raw label `\"dog\"` often loses to `\"a photo of a dog\"`.",
    ),
    (
        "CS231N’s first listed disadvantage of CLIP-style models: they **rely on batch size** to learn fine-grained concepts.",
        "CLIP-style models **rely on batch size** to learn fine-grained concepts.",
    ),
    (
        "Watch [Stanford CS224N Lecture 6 (RNNs / vanishing gradients)](https://www.youtube.com/watch?v=0LixFSa7yts).",
        "Watch [RNNs and vanishing gradients](https://www.youtube.com/watch?v=0LixFSa7yts).",
    ),
    (
        "Watch [Stanford CS231N 2017 lecture 13, Generative Models](https://www.youtube.com/watch?v=5WoItGTWV54), **46:45–54:00**.",
        "Watch [Generative models: GAN setup](https://www.youtube.com/watch?v=5WoItGTWV54), **46:45–54:00**.",
    ),
    (
        "Watch [Stanford CS231N 2017 lecture 13, Generative Models](https://www.youtube.com/watch?v=5WoItGTWV54), **54:00–64:00**.",
        "Watch [Generative models: training \\(G\\) and \\(D\\)](https://www.youtube.com/watch?v=5WoItGTWV54), **54:00–64:00**.",
    ),
    (
        "Watch [Stanford CS231N 2017 lecture 13, Generative Models](https://www.youtube.com/watch?v=5WoItGTWV54), **64:00–74:00**.",
        "Watch [Generative models: coverage and collapse](https://www.youtube.com/watch?v=5WoItGTWV54), **64:00–74:00**.",
    ),
    (
        "- **Then** play CS231N **46:45–54:00** (GAN setup: give up on density, noise through a generator). Pause when the two-player cartoon appears.",
        "- **Then** play **46:45–54:00** of the assigned video (GAN setup: give up on density, noise through a generator). Pause when the two-player cartoon appears.",
    ),
    (
        "- **Then** play CS231N **54:00–64:00** (minimax objective and the training algorithm). Pause on the “train \\(D\\) then \\(G\\)” slide.",
        "- **Then** play **54:00–64:00** of the assigned video (minimax objective and the training algorithm). Pause on the “train \\(D\\) then \\(G\\)” loop.",
    ),
    (
        "- **Then** play CS231N **64:00–74:00** (training is unstable; you do not have \\(p(x)\\); samples can look good anyway). Pause on the “cons” / summary slide and name that gap **coverage**.",
        "- **Then** play **64:00–74:00** of the assigned video (training is unstable; you do not have \\(p(x)\\); samples can look good anyway). Pause on the summary and name that gap **coverage**.",
    ),
    (
        "Play the vanishing/exploding segment of CS224N (about **45:00–58:00** on the linked older lecture; if chapter marks differ, jump to the Jacobian-product board).",
        "Play the vanishing/exploding segment of the assigned video (about **45:00–58:00**; if chapter marks differ, jump to the Jacobian-product board).",
    ),
    (
        "StatQuest Word2Vec is **homework** (**0:00–12:00**, skip-gram vs. CBOW). Do not play CS224N Lecture 2 in class.",
        "StatQuest Word2Vec is **homework** (**0:00–12:00**, skip-gram vs. CBOW).",
    ),
    (
        "Save vanishing gradients for note 2.2 even if the video teases them. Do not play a full CS224N hour in class.",
        "Save vanishing gradients for note 2.2 even if the video teases them.",
    ),
    (
        "Zero-shot details wait for 4.3; captioning waits for BLIP. Do not play a full 11-777 hour in class.",
        "Zero-shot details wait for 4.3; captioning waits for BLIP.",
    ),
    (
        "Weeks 13–14 follow **CS224N 2026 L12, L13, L10**; Weeks 11–12 follow CS231N 2025 L13–L14.",
        "Weeks 13–14 are CoT, vote/search, faithfulness, RAG, and ReAct; Weeks 11–12 are GANs and diffusion.",
    ),
    (
        "restudy notes **11.1–12.3** and the CS231N / Umar Jamil clips from those weeks.",
        "restudy notes **11.1–12.3** and the assigned clips from those weeks.",
    ),
    (
        "Week 11–12 video recap (not Karpathy): CS231N lecture 13 from **46:45** ([setup / train / collapse](https://www.youtube.com/watch?v=5WoItGTWV54));",
        "Week 11–12 video recap (not Karpathy): generative models from **46:45** ([setup / train / collapse](https://www.youtube.com/watch?v=5WoItGTWV54));",
    ),
    (
        'About **30 minutes** at the board, then **~12 minutes** of video. Then start Lab 13 if the vote note is already done. Lecture ideas follow **CS224N 2026 L12–L13** (unfaithful CoT; process vs outcome).',
        "About **30 minutes** at the board, then **~12 minutes** of video. Then start Lab 13 if the vote note is already done.",
    ),
    (
        "About **35 minutes** at the board, then **~10 minutes** of video. Lecture ideas follow **CS224N 2026 L12** (self-consistency) and the ToT paper for the search cartoon.",
        "About **35 minutes** at the board, then **~10 minutes** of video. Self-consistency is the vote; the ToT paper is the search cartoon.",
    ),
    (
        "About **30 minutes** at the board, then **~8 minutes** of video. First of three Week-13 notes; Lab 13 is constructed traces, not an API. Lecture ideas follow **CS224N 2026 L12**.",
        "About **30 minutes** at the board, then **~8 minutes** of video. First of three Week-13 notes; Lab 13 is constructed traces, not an API.",
    ),
    (
        "Lecture ideas follow **CS224N 2026 L10**. Original notes; that course is not copied.",
        "",
    ),
    (
        "CMU 11-711 cousin: \\(\\partial L/\\partial w=(p-y)x\\).",
        r"Softmax/CE cousin: \(\partial L/\partial w=(p-y)x\).",
    ),
    (
        "Pedagogy drawn from Stanford CS224N (plan + one formula), CS231N (footer, one idea), MIT 6.S191 (diagram + numbers). Original slides; those courses are not copied.",
        "Key goal: one timed meeting, one stack picture, one project sentence.",
    ),
]

DROP_LINE_PREFIXES = (
    "The matching university lecture",
    "The matching university lectures",
    "The matching *form* lectures",
    "The matching university course",
)

SLIDE_REPLACEMENTS: list[tuple[str, str]] = [
    ("After Stanford CS224N Lecture 2: distributional meaning, skip-gram softmax, then evaluation.",
     "Distributional meaning, skip-gram softmax, then evaluation."),
    ("After Stanford CS224N W26 L4: any-length input, shared weights, then an RNN-LM.",
     "Any-length input, shared weights, then an RNN-LM."),
    ("After CS231N L7 (BPTT, singular values) and CS224N L4 (near vs. long-term effects).",
     "BPTT, singular values, near vs. long-term effects."),
    ("After CMU 11-785 L14: a cell that can copy, plus input-dependent gates.",
     "A cell that can copy, plus input-dependent gates."),
    ("After Stanford CS224N W26 L5: the bottleneck, then a direct look at the source.",
     "The bottleneck, then a direct look at the source."),
    ("After CMU 11-711: scaled dots, mix values, then a causal mask.",
     "Scaled dots, mix values, then a causal mask."),
    ("After CMU 11-777: five jobs, then joint versus coordinated.",
     "Five jobs, then joint versus coordinated."),
    ("After Stanford CS231N 2025 L8: patches, a linear map, positions, no causal mask.",
     "Patches, a linear map, positions, no causal mask."),
    ("CS224N L9: 175B parameters, 300B tokens.",
     "GPT-3: 175B parameters, 300B tokens."),
    ("CS224N L11 also puts LoRA here. Algebra is note 8.3.",
     "LoRA is a small Δ, not pruning. Algebra is note 8.3."),
    ("CS224N L10: instruction FT is the first InstructGPT stage.",
     "Instruction fine-tuning is the first InstructGPT stage."),
    ("No. XOR accuracy on the frozen net cannot move. CS224N L11: that is why PEFT exists.",
     "No. XOR accuracy on the frozen net cannot move. That is why PEFT exists."),
    ("CS224N: a full GPT-3 copy is 175B extra per task.",
     "A full GPT-3 copy is 175B extra per task."),
    ("CS224N L10: the RM is already useful",
     "The RM is already useful"),
    ("CS224N L10: InstructGPT scaled this stack.",
     "InstructGPT scaled this stack."),
    ("CS224N L10: the optimal r is a log-ratio plus Z(x).",
     "The optimal r is a log-ratio plus Z(x)."),
    ("Judge, Spot-check a 10% sample. CS224N L12: look at the outputs.",
     "Judge, Spot-check a 10% sample. Look at the outputs."),
    ("CS224N: if a component stores the fact, intervening on it should change the object.",
     "If a component stores the fact, intervening on it should change the object."),
    ("CS224N L13: parametric recall versus open-book.",
     "Parametric recall versus open-book."),
    ("CS224N L12: the weights do not change. The tape gets longer.",
     "The weights do not change. The tape gets longer."),
    ("CS224N L12: extra tokens are extra compute. SC spends k of them.",
     "Extra tokens are extra compute. SC spends k of them."),
    ("Wang et al., cited in CS224N L12: +17.9 pp vs greedy CoT.",
     "Wang et al.: +17.9 pp vs greedy CoT."),
    ("CS224N L13 / Lightman: a process reward scores steps, not only the box.",
     "Lightman et al.: a process reward scores steps, not only the box."),
    ("Chen et al. 2025 (CS224N L12): models can use a hint they never write.",
     "Chen et al. 2025: models can use a hint they never write."),
]


def apply_pairs(text: str, pairs: list[tuple[str, str]]) -> str:
    for old, new in pairs:
        text = text.replace(old, new)
    return text


def drop_matching_paragraphs(text: str) -> str:
    out = []
    for para in re.split(r"(\n\n+)", text):
        stripped = para.strip()
        if any(stripped.startswith(p) for p in DROP_LINE_PREFIXES):
            continue
        out.append(para)
    text = "".join(out)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def scrub_notes() -> int:
    n = 0
    for path in sorted(NOTES.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        new = apply_pairs(text, REPLACEMENTS)
        new = drop_matching_paragraphs(new)
        if new != text:
            path.write_text(new.replace("\r\n", "\n"), encoding="utf-8", newline="\n")
            n += 1
    return n


def scrub_slides() -> None:
    path = ROOT / "scripts" / "export_643_slides_pdf.py"
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    out = []
    for line in lines:
        if '"credit":' in line:
            out.append(line)
            continue
        out.append(apply_pairs(apply_pairs(line, REPLACEMENTS), SLIDE_REPLACEMENTS))
    path.write_text("".join(out), encoding="utf-8", newline="\n")


def main() -> None:
    n = scrub_notes()
    scrub_slides()
    print(f"updated {n} notes; slides rewritten (credits kept)")


if __name__ == "__main__":
    main()
