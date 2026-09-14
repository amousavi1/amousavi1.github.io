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
    {
        "slug": "sequence-rnns",
        "week": 2,
        "title": "2.1 Sequential Models and RNNs",
        "lead": "A hidden state that reads the sequence one token at a time, with shared weights.",
        "slide": "2.1-sequence-rnns",
    },
    {
        "slug": "vanishing-gradients",
        "week": 2,
        "title": "2.2 Vanishing and Exploding Gradients",
        "lead": "Backprop through time is a product of Jacobians. Long-range signal dies or blows up.",
        "slide": "2.2-vanishing-gradients",
    },
    {
        "slug": "lstm-gru",
        "week": 2,
        "title": "2.3 LSTMs and GRUs",
        "lead": "Gates keep a near-1 path through time. LSTM has a cell; GRU does not.",
        "slide": "2.3-lstm-gru",
    },
    {
        "slug": "lab-2-long-range",
        "week": 2,
        "title": "Lab 2: Long-Range Memory",
        "lead": "Copy the first bit of a long sequence: vanilla RNN versus LSTM.",
    },
    {
        "slug": "attention-need",
        "week": 3,
        "title": "3.1 From Recurrence to Attention",
        "lead": "A chain of states is a bottleneck. Attention gives every token a path of length one.",
        "slide": "3.1-attention-need",
    },
    {
        "slug": "self-attention",
        "week": 3,
        "title": "3.2 Self-Attention (Q, K, V)",
        "lead": "Queries ask, keys are asked, values are mixed. Softmax weights over the sequence.",
        "slide": "3.2-self-attention",
    },
    {
        "slug": "transformer-block",
        "week": 3,
        "title": "3.3 The Transformer Block",
        "lead": "Positions, multi-head attention, residuals, layer norm, and a token-wise MLP.",
        "slide": "3.3-transformer-block",
    },
    {
        "slug": "gpt-bert",
        "week": 3,
        "title": "3.4 GPT and BERT",
        "lead": "Same block, different mask and objective: next-token versus masked tokens.",
        "slide": "3.4-gpt-bert",
    },
    {
        "slug": "lab-3-self-attention",
        "week": 3,
        "title": "Lab 3: Self-Attention by Hand",
        "lead": "Q, K, V, a heatmap, then a causal mask on four tokens.",
    },
    {
        "slug": "multimodal-foundations",
        "week": 4,
        "title": "4.1 Multimodal Foundations",
        "lead": "Joint versus coordinated spaces; alignment, fusion, and translation.",
        "slide": "4.1-multimodal-foundations",
    },
    {
        "slug": "vision-transformers",
        "week": 4,
        "title": "4.2 Vision Transformers",
        "lead": "Image patches as tokens. The Week 3 block on pixels.",
        "slide": "4.2-vision-transformers",
    },
    {
        "slug": "contrastive-zeroshot",
        "week": 4,
        "title": "4.3 Contrastive Learning and Zero-Shot Transfer",
        "lead": "Matched pairs on the diagonal. Class names as text embeddings.",
        "slide": "4.3-contrastive-zeroshot",
    },
    {
        "slug": "lab-4-patches-contrastive",
        "week": 4,
        "title": "Lab 4: Patches and a Tiny Contrastive Loss",
        "lead": "Flatten image patches, then InfoNCE on four constructed pairs.",
    },
    {
        "slug": "clip",
        "week": 5,
        "title": "5.1 CLIP",
        "lead": "Two towers, cosine, web-scale pairs. Retrieval and zero-shot, not captioning.",
        "slide": "5.1-clip",
    },
    {
        "slug": "blip",
        "week": 5,
        "title": "5.2 BLIP and Captioning",
        "lead": "Filter noisy pairs, then match and decode. Bootstrap the captions.",
        "slide": "5.2-blip",
    },
    {
        "slug": "retrieval-bias",
        "week": 5,
        "title": "5.3 Retrieval, Bias, and Robustness",
        "lead": "Nearest neighbors in two directions, and the stereotypes that come with them.",
        "slide": "5.3-retrieval-bias",
    },
    {
        "slug": "lab-5-toy-clip",
        "week": 5,
        "title": "Lab 5: Retrieval in a Toy CLIP Space",
        "lead": "Rank images and texts in 2-D, then a gender–occupation probe.",
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
        "lectures": ["sequence-rnns", "vanishing-gradients", "lstm-gru"],
        "labs": [("lab-2-long-range", False)],
        "readings": [
            ("Understanding LSTM networks (Olah)", "https://colah.github.io/posts/2015-08-Understanding-LSTMs/"),
            ("Sherstinsky, Fundamentals of RNN and LSTM", "https://arxiv.org/abs/1808.03314"),
        ],
        "discussion": [
            "What does the hidden state have to carry across a long sentence?",
            "Why do vanishing gradients push us toward gates, then toward attention in Week 3?",
        ],
    },
    3: {
        "label": "Module 1 — Attention and transformers",
        "lectures": ["attention-need", "self-attention", "transformer-block", "gpt-bert"],
        "labs": [("lab-3-self-attention", False)],
        "readings": [
            ("Vaswani et al., Attention is all you need", "https://arxiv.org/abs/1706.03762"),
            ("Illustrated transformer (Alammar)", "https://jalammar.github.io/illustrated-transformer/"),
        ],
        "discussion": [
            "What does a query attend to that an RNN state cannot see in one step?",
            "GPT versus BERT: which mask, and which project would pick which?",
        ],
    },
    4: {
        "label": "Module 2 — Multimodal foundations and vision transformers",
        "lectures": ["multimodal-foundations", "vision-transformers", "contrastive-zeroshot"],
        "labs": [("lab-4-patches-contrastive", False)],
        "readings": [
            ("Dosovitskiy et al., An image is worth 16x16 words", "https://arxiv.org/abs/2010.11929"),
            ("Baltrušaitis et al., Multimodal machine learning survey", "https://arxiv.org/abs/1705.09406"),
        ],
        "discussion": [
            "When would you keep two towers instead of concatenating image and text features?",
            "Why do ViT patches still need positional encodings?",
        ],
    },
    5: {
        "label": "Module 2 — Vision–language models (CLIP and BLIP)",
        "lectures": ["clip", "blip", "retrieval-bias"],
        "labs": [("lab-5-toy-clip", False)],
        "readings": [
            ("Radford et al., CLIP", "https://arxiv.org/abs/2103.00020"),
            ("Li et al., BLIP", "https://arxiv.org/abs/2201.12086"),
        ],
        "discussion": [
            "CLIP retrieves; BLIP can write. Which one belongs in a captioning project?",
            "Name one retrieval probe you would run before ranking people or jobs.",
        ],
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
