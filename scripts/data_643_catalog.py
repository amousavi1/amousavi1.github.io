"""Lecture, lab, and hub metadata for DATA 443/643."""

NOTES = [
    {
        "slug": "course-map",
        "week": 1,
        "title": "1.1 Course Map and the Semester Project",
        "lead": "A self-contained LLM course. Week 1 is the base of the stack; the project starts now.",
        "slide": "1.1-course-map",
    },
    {
        "slug": "neurons-activations",
        "week": 1,
        "title": "1.2 Neurons, Activations, and Feedforward Nets",
        "lead": "A weighted sum, a nonlinearity, and why stacking linear layers is not enough.",
        "slide": "1.2-neurons-activations",
    },
    {
        "slug": "gradient-descent",
        "week": 1,
        "title": "1.3 Gradient Descent",
        "lead": "Forward, loss, backward, update. That loop is pretraining and fine-tuning.",
        "slide": "1.3-gradient-descent",
    },
    {
        "slug": "embeddings",
        "week": 1,
        "title": "1.4 Word Embeddings and Semantic Geometry",
        "lead": "Dense vectors, skip-gram, analogies, and why geometry can encode bias.",
        "slide": "1.4-embeddings",
    },
    {
        "slug": "lab-1-xor-embeddings",
        "week": 1,
        "title": "Lab 1: XOR, Autograd, and a Tiny Embedding Space",
        "lead": "PyTorch tensors, a two-layer net on XOR, then cosine and a bias probe on constructed 2-D vectors.",
    },
    {
        "slug": "project-overview",
        "week": 1,
        "title": "Project Overview",
        "lead": "The semester is a measured system plus, for graduate students, a short paper reproduction.",
    },
]

BY_SLUG = {n["slug"]: n for n in NOTES}

WEEKS = {
    1: {
        "label": "Module 1 — Neural networks and word embeddings",
        "lectures": ["course-map", "neurons-activations", "gradient-descent", "embeddings"],
        "labs": [("lab-1-xor-embeddings", False)],
        "readings": [
            ("Goodfellow, Bengio, Courville: Deep feedforward networks (Ch. 6)", "https://www.deeplearningbook.org/contents/mlp.html"),
            ("Mikolov et al., Efficient estimation of word representations", "https://arxiv.org/abs/1301.3781"),
            ("Jurafsky & Martin, Vector semantics and embeddings", "https://web.stanford.edu/~jurafsky/slp3/6.pdf"),
        ],
        "discussion": [
            "Intrinsic vs. extrinsic evaluation of embeddings: which number belongs in a project report, and which one is for debugging?",
            "Name one way embedding geometry can encode a stereotype. What would you measure?",
            "Why can this course skip DATA 641 and 642 and still start from neurons this week?",
        ],
    },
    2: {
        "label": "Module 1 — Sequence models: RNNs, LSTMs, and GRUs",
        "topics": "Sequential modeling, vanishing and exploding gradients, gating, hidden-state dynamics.",
        "discussion": [
            "What does the hidden state have to carry across a long sentence?",
            "Why do we move from recurrence to attention in Week 3?",
        ],
    },
    3: {
        "label": "Module 1 — Attention and transformers",
        "topics": "Self-attention (Q/K/V), positional encoding, encoder–decoder, GPT and BERT as systems.",
        "discussion": [
            "What does a query attend to that an RNN state cannot see in one step?",
        ],
    },
    4: {
        "label": "Module 2 — Multimodal foundations and vision transformers",
        "topics": "Image patches as tokens, contrastive learning, modality alignment, zero-shot transfer.",
    },
    5: {
        "label": "Module 2 — Vision–language models (CLIP and BLIP)",
        "topics": "Cross-modal retrieval, captioning, bootstrapped pretraining, bias and robustness.",
    },
    6: {
        "label": "Module 2 — Audio and cross-modal integration",
        "topics": "Spectrograms as tokens, fusion, unified embeddings, data scarcity.",
    },
    7: {
        "label": "Module 3 — Scaling, efficiency, and deployment",
        "topics": "Scaling laws, mixture-of-experts, pruning, quantization, distillation, speculative decoding.",
    },
    8: {
        "label": "Module 3 — SFT, continual learning, and adapters",
        "topics": "Instruction tuning, prompt design, catastrophic forgetting, LoRA, federated updates.",
    },
    9: {
        "label": "Module 3 — RLHF and direct preference optimization",
        "topics": "Reward models, policy optimization, preference learning, human feedback.",
    },
    10: {
        "label": "Module 3 — Safety, editing, and retrieval-augmented training",
        "topics": "Red-teaming, unlearning, ROME/MEMIT, RAFT, memory-augmented models.",
    },
    11: {
        "label": "Module 4 — Generative models I: GANs",
        "topics": "Adversarial training, generator–discriminator dynamics, mode collapse.",
    },
    12: {
        "label": "Module 4 — Generative models II: diffusion",
        "topics": "Forward and reverse processes, latent diffusion, text-to-image conditioning.",
    },
    13: {
        "label": "Module 4 — Reasoning and chain-of-thought",
        "topics": "Step-by-step reasoning, self-consistency, Tree-of-Thoughts, faithfulness.",
    },
    14: {
        "label": "Module 4 — Tools, RAG, and final presentations",
        "topics": "RAG pipelines, ReAct, uncertainty, evaluation of applications. Project talks.",
    },
    15: {
        "label": "Final exam and remaining talks",
        "topics": "Cumulative exam. Remaining presentations as posted on Canvas.",
    },
}
