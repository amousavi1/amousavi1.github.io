"""Lecture, lab, and hub metadata for DATA 443/643."""

NOTES = [
    {
        "slug": "course-map",
        "week": 1,
        "title": "1.1 Course Map and the Semester Project",
        "lead": "A self-contained LLM course. Week 1 is the base of the stack; next-token NLL is the cost; the project starts now.",
        "slide": "1.1-course-map",
    },
    {
        "slug": "neurons-activations",
        "week": 1,
        "title": "1.2 Neurons, Activations, and Feedforward Nets",
        "lead": "A weighted sum, a nonlinearity, softmax, and an explicit two-ReLU XOR table.",
        "slide": "1.2-neurons-activations",
    },
    {
        "slug": "gradient-descent",
        "week": 1,
        "title": "1.3 Gradient Descent",
        "lead": "Forward, loss, backward, update, and one ReLU unit’s chain rule. That loop is pretraining.",
        "slide": "1.3-gradient-descent",
    },
    {
        "slug": "embeddings",
        "week": 1,
        "title": "1.4 Word Embeddings and Semantic Geometry",
        "lead": "Dense vectors, skip-gram softmax on a tiny vocab, analogies, and a signed-projection bias probe.",
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
    {
        "slug": "audio-spectrograms",
        "week": 6,
        "title": "6.1 Waveforms, Spectrograms, and Time–Frequency Tokens",
        "lead": "Sound is a 1-D wave. A spectrogram is an image the Week 4 stack already knows how to read.",
        "slide": "6.1-audio-spectrograms",
    },
    {
        "slug": "audio-encoders",
        "week": 6,
        "title": "6.2 Audio Encoders and Speech Models",
        "lead": "Patch or frame the spectrogram, then a transformer. Whisper-style encoder–decoder.",
        "slide": "6.2-audio-encoders",
    },
    {
        "slug": "fusion-scarcity",
        "week": 6,
        "title": "6.3 Fusion, Unified Embeddings, and Data Scarcity",
        "lead": "Early, late, and cross-attention fusion. Audio-labeled data is the bottleneck.",
        "slide": "6.3-fusion-scarcity",
    },
    {
        "slug": "lab-6-spectrograms",
        "week": 6,
        "title": "Lab 6: A Spectrogram and a Tiny Fusion",
        "lead": "STFT of a sine mixture, patch it, then concat versus add two modalities.",
    },
    {
        "slug": "scaling-laws",
        "week": 7,
        "title": "7.1 Scaling Laws",
        "lead": "Loss falls as a power of compute, data, and parameters — until you starve one of them.",
        "slide": "7.1-scaling-laws",
    },
    {
        "slug": "mixture-of-experts",
        "week": 7,
        "title": "7.2 Mixture of Experts",
        "lead": "A router sends each token to a few experts. Capacity without dense FLOPs.",
        "slide": "7.2-mixture-of-experts",
    },
    {
        "slug": "efficiency-deploy",
        "week": 7,
        "title": "7.3 Compression and Deployment",
        "lead": "Prune, quantize, distill, then speculative decoding at serving time.",
        "slide": "7.3-efficiency-deploy",
    },
    {
        "slug": "lab-7-scale-quantize",
        "week": 7,
        "title": "Lab 7: A Scaling Curve and Int8",
        "lead": "Fit a toy power law, then quantize a weight matrix and measure error.",
    },
    {
        "slug": "sft-instructions",
        "week": 8,
        "title": "8.1 Supervised Fine-Tuning and Instruction Data",
        "lead": "Pretraining next-token is not the same as following a request. SFT is the first alignment step.",
        "slide": "8.1-sft-instructions",
    },
    {
        "slug": "continual-forgetting",
        "week": 8,
        "title": "8.2 Continual Learning and Forgetting",
        "lead": "Train on task B and task A slips. Replay, freeze, or isolate the change.",
        "slide": "8.2-continual-forgetting",
    },
    {
        "slug": "lora-adapters",
        "week": 8,
        "title": "8.3 LoRA, Adapters, and Federated Updates",
        "lead": "A low-rank pair BA instead of rewriting W. Small deltas you can ship or keep local.",
        "slide": "8.3-lora-adapters",
    },
    {
        "slug": "lab-8-lora-forget",
        "week": 8,
        "title": "Lab 8: A Low-Rank Update and a Forgetting Demo",
        "lead": "Factor a 4×4 update, then train XOR then AND and watch the first task drop.",
    },
    {
        "slug": "preference-rewards",
        "week": 9,
        "title": "9.1 Preference Data and Reward Models",
        "lead": "Humans (or a proxy) pick chosen over rejected. A reward model scores completions.",
        "slide": "9.1-preference-rewards",
    },
    {
        "slug": "rlhf",
        "week": 9,
        "title": "9.2 RLHF",
        "lead": "SFT, then a reward model, then a policy that climbs the reward without wandering too far.",
        "slide": "9.2-rlhf",
    },
    {
        "slug": "dpo",
        "week": 9,
        "title": "9.3 Direct Preference Optimization",
        "lead": "The same pairwise data, no separate reward model and no PPO loop.",
        "slide": "9.3-dpo",
    },
    {
        "slug": "lab-9-preferences",
        "week": 9,
        "title": "Lab 9: Pairwise Preferences and a Toy DPO Loss",
        "lead": "Rank two completions, train a tiny reward head, then a DPO-style logistic on logits.",
    },
    {
        "slug": "red-teaming",
        "week": 10,
        "title": "10.1 Red-Teaming and Safety Evaluation",
        "lead": "You cannot claim a model is safe without trying to break it on purpose.",
        "slide": "10.1-red-teaming",
    },
    {
        "slug": "editing-unlearning",
        "week": 10,
        "title": "10.2 Editing and Unlearning",
        "lead": "ROME/MEMIT locate a fact and rewrite it. Unlearning tries to forget a set, not one key.",
        "slide": "10.2-editing-unlearning",
    },
    {
        "slug": "raft-memory",
        "week": 10,
        "title": "10.3 RAFT and Memory-Augmented Models",
        "lead": "Train with retrieved documents in the prompt. Parametric memory is not the only store.",
        "slide": "10.3-raft-memory",
    },
    {
        "slug": "lab-10-edit-retrieve",
        "week": 10,
        "title": "Lab 10: Edit a Toy Fact, Then Retrieve It",
        "lead": "Overwrite one key in a lookup table, then compare parametric recall to a retrieved snippet.",
    },
    {
        "slug": "gan-idea",
        "week": 11,
        "title": "11.1 Generative Adversarial Nets",
        "lead": "A generator fakes samples. A discriminator tries to tell them from the data.",
        "slide": "11.1-gan-idea",
    },
    {
        "slug": "gan-training",
        "week": 11,
        "title": "11.2 Training Dynamics",
        "lead": "A min–max game. If one player wins too early, the other stops learning.",
        "slide": "11.2-gan-training",
    },
    {
        "slug": "mode-collapse",
        "week": 11,
        "title": "11.3 Mode Collapse and Evaluation",
        "lead": "The generator can cover one mode and still fool a weak discriminator.",
        "slide": "11.3-mode-collapse",
    },
    {
        "slug": "lab-11-toy-gan",
        "week": 11,
        "title": "Lab 11: A One-Dimensional GAN Sketch",
        "lead": "Two Gaussians as data. Watch a tiny generator miss a mode.",
    },
    {
        "slug": "diffusion-forward",
        "week": 12,
        "title": "12.1 The Forward Process",
        "lead": "Add a little Gaussian noise for T steps until the sample is almost prior noise.",
        "slide": "12.1-diffusion-forward",
    },
    {
        "slug": "diffusion-reverse",
        "week": 12,
        "title": "12.2 The Reverse Process",
        "lead": "Learn to denoise. Each step predicts the noise (or the clean sample) and takes a step back.",
        "slide": "12.2-diffusion-reverse",
    },
    {
        "slug": "latent-conditioning",
        "week": 12,
        "title": "12.3 Latent Diffusion and Text Conditioning",
        "lead": "Diffuse in a VAE latent. Condition on a text embedding (often CLIP from Week 5).",
        "slide": "12.3-latent-conditioning",
    },
    {
        "slug": "lab-12-denoise",
        "week": 12,
        "title": "Lab 12: Noise a Point, Then Take One Reverse Step",
        "lead": "A 2-D schedule, a known score, one denoising update.",
    },
    {
        "slug": "chain-of-thought",
        "week": 13,
        "title": "13.1 Chain-of-Thought",
        "lead": "Ask for steps before the answer. Intermediate tokens can carry scratch work.",
        "slide": "13.1-chain-of-thought",
    },
    {
        "slug": "self-consistency-tot",
        "week": 13,
        "title": "13.2 Self-Consistency and Tree-of-Thoughts",
        "lead": "Sample several traces and vote. Search a tree of partial thoughts when one path is not enough.",
        "slide": "13.2-self-consistency-tot",
    },
    {
        "slug": "faithfulness",
        "week": 13,
        "title": "13.3 Faithfulness of Explanations",
        "lead": "A correct final answer can sit on invented steps. Process and outcome are different claims.",
        "slide": "13.3-faithfulness",
    },
    {
        "slug": "lab-13-reasoning",
        "week": 13,
        "title": "Lab 13: Direct Answers, Traces, and a Majority Vote",
        "lead": "Compare short answers to step traces on arithmetic, then vote, then flag an unfaithful trace.",
    },
    {
        "slug": "rag-pipeline",
        "week": 14,
        "title": "14.1 Retrieval-Augmented Generation",
        "lead": "Index documents, retrieve chunks, then generate with those chunks in context.",
        "slide": "14.1-rag-pipeline",
    },
    {
        "slug": "react-tools",
        "week": 14,
        "title": "14.2 ReAct and Tool Use",
        "lead": "Thought, action, observation. The model calls a tool instead of guessing the lookup.",
        "slide": "14.2-react-tools",
    },
    {
        "slug": "eval-presentations",
        "week": 14,
        "title": "14.3 Evaluating Applications and Giving the Talk",
        "lead": "Citation, uncertainty, and a measured demo. The presentation is part of the method.",
        "slide": "14.3-eval-presentations",
    },
    {
        "slug": "lab-14-toy-rag",
        "week": 14,
        "title": "Lab 14: A Five-Document RAG Loop",
        "lead": "Embed toy snippets, retrieve for a query, then write an answer that cites a chunk id.",
    },
    {
        "slug": "exam-review",
        "week": 15,
        "title": "15.1 Exam Review",
        "lead": "Four modules, one stack. The exam asks you to connect a method to a measurement.",
        "slide": "15.1-exam-review",
    },
]

BY_SLUG = {n["slug"]: n for n in NOTES}

# One primary classroom video per lecture. Title includes a watch cue.
VIDEOS = {
    "course-map": (
        "Karpathy: Intro to Large Language Models (0:00–8:00 in class; finish 0:00–20:00 as homework)",
        "https://www.youtube.com/watch?v=zjkBMFhNj_g",
    ),
    "neurons-activations": (
        "3Blue1Brown: But what is a neural network? (~19 min)",
        "https://www.youtube.com/watch?v=aircAruvnKk",
    ),
    "gradient-descent": (
        "3Blue1Brown: Gradient descent, how neural networks learn (~21 min)",
        "https://www.youtube.com/watch?v=IHZwWFHWa-w",
    ),
    "embeddings": (
        "StatQuest: Word Embedding and Word2Vec, Clearly Explained (~16 min)",
        "https://www.youtube.com/watch?v=viZrOnJclY0",
    ),
    "sequence-rnns": (
        "StatQuest: Recurrent Neural Networks, Clearly Explained (~21 min)",
        "https://www.youtube.com/watch?v=AsNTP8Kwu80",
    ),
    "vanishing-gradients": (
        "Stanford CS224N: Simple and LSTM RNNs (watch the vanishing/exploding segment)",
        "https://www.youtube.com/watch?v=0LixFSa7yts",
    ),
    "lstm-gru": (
        "StatQuest: Long Short-Term Memory (LSTM), Clearly Explained (~21 min)",
        "https://www.youtube.com/watch?v=YCzL96nL7j0",
    ),
    "attention-need": (
        "3Blue1Brown: But what is a GPT? Visual intro to transformers (~27 min)",
        "https://www.youtube.com/watch?v=wjZofJX0v4M",
    ),
    "self-attention": (
        "3Blue1Brown: Attention in transformers, step-by-step (~26 min)",
        "https://www.youtube.com/watch?v=eMlx5fFNoYc",
    ),
    "transformer-block": (
        "Umar Jamil: Transformer explained (architecture + code; watch the block walkthrough)",
        "https://www.youtube.com/watch?v=bCz4OMemCcA",
    ),
    "gpt-bert": (
        "Karpathy: Let's build GPT (watch through the first attention implementation)",
        "https://www.youtube.com/watch?v=kCc8FmEb1nY",
    ),
    "multimodal-foundations": (
        "Yannic Kilcher: OpenAI CLIP, Connecting Text and Images (watch the two-tower setup)",
        "https://www.youtube.com/watch?v=T9XSU0pKX2E",
    ),
    "vision-transformers": (
        "Umar Jamil: Vision Transformer explained (watch the patch embedding section)",
        "https://www.youtube.com/watch?v=j6kuzuy2ZZo",
    ),
    "contrastive-zeroshot": (
        "Yannic Kilcher: OpenAI CLIP (InfoNCE batch and zero-shot prompts)",
        "https://www.youtube.com/watch?v=T9XSU0pKX2E",
    ),
    "clip": (
        "Yannic Kilcher: OpenAI CLIP, Connecting Text and Images (full paper)",
        "https://www.youtube.com/watch?v=T9XSU0pKX2E",
    ),
    "blip": (
        "What's AI: OpenAI's Whisper Model Explained (encoder–decoder analog; pair with the BLIP paper)",
        "https://www.youtube.com/watch?v=uFOkMme19Zs",
    ),
    "retrieval-bias": (
        "Yannic Kilcher: OpenAI CLIP (prompting, retrieval, and failure modes in the second half)",
        "https://www.youtube.com/watch?v=T9XSU0pKX2E",
    ),
    "audio-spectrograms": (
        "Valerio Velardo: Short-Time Fourier Transform explained (Sound of AI)",
        "https://www.youtube.com/watch?v=-Yxj3yfvY-4",
    ),
    "audio-encoders": (
        "What's AI: OpenAI's Whisper Model Explained (~12 min)",
        "https://www.youtube.com/watch?v=uFOkMme19Zs",
    ),
    "fusion-scarcity": (
        "Yannic Kilcher: OpenAI CLIP (coordinated towers as a fusion baseline)",
        "https://www.youtube.com/watch?v=T9XSU0pKX2E",
    ),
    "scaling-laws": (
        "Karpathy: Intro to Large Language Models (scaling and pretraining after 20:00)",
        "https://www.youtube.com/watch?v=zjkBMFhNj_g",
    ),
    "mixture-of-experts": (
        "Karpathy: Deep Dive into LLMs like ChatGPT (internals 20:11–26:01; routing on the board)",
        "https://www.youtube.com/watch?v=7xTGNNLPyMI",
    ),
    "efficiency-deploy": (
        "Umar Jamil: LoRA explained (small deltas at deploy time; pair with the quantization section)",
        "https://www.youtube.com/watch?v=PXWYUTMt-AU",
    ),
    "sft-instructions": (
        "Karpathy: Intro to Large Language Models (assistant / SFT, watch 14:14–21:05)",
        "https://www.youtube.com/watch?v=zjkBMFhNj_g",
    ),
    "continual-forgetting": (
        "Umar Jamil: LoRA explained (why a thin adapter forgets less than full FT)",
        "https://www.youtube.com/watch?v=PXWYUTMt-AU",
    ),
    "lora-adapters": (
        "Umar Jamil: LoRA, explained visually + PyTorch from scratch",
        "https://www.youtube.com/watch?v=PXWYUTMt-AU",
    ),
    "preference-rewards": (
        "Karpathy: Intro to Large Language Models (RLHF / preferences, 21:05–25:43)",
        "https://www.youtube.com/watch?v=zjkBMFhNj_g",
    ),
    "rlhf": (
        "Karpathy: Intro to Large Language Models (RLHF loop, 21:05–25:43)",
        "https://www.youtube.com/watch?v=zjkBMFhNj_g",
    ),
    "dpo": (
        "Karpathy: Deep Dive into LLMs like ChatGPT (preference / RLHF, 2:48:26–3:09:39)",
        "https://www.youtube.com/watch?v=7xTGNNLPyMI",
    ),
    "red-teaming": (
        "Karpathy: Intro to Large Language Models (limitations/security, 45:43–58:37)",
        "https://www.youtube.com/watch?v=zjkBMFhNj_g",
    ),
    "editing-unlearning": (
        "Karpathy: Deep Dive into LLMs (knowledge / hallucination, 1:20:32–1:41:46)",
        "https://www.youtube.com/watch?v=7xTGNNLPyMI",
    ),
    "raft-memory": (
        "Karpathy: Intro to Large Language Models (tools/retrieval, 27:43–33:32)",
        "https://www.youtube.com/watch?v=zjkBMFhNj_g",
    ),
    "gan-idea": (
        "Stanford CS231N: Generative models (GAN setup; 2017 lecture 13)",
        "https://www.youtube.com/watch?v=5WoItGTWV54",
    ),
    "gan-training": (
        "Stanford CS231N: Generative models (training dynamics of G vs D)",
        "https://www.youtube.com/watch?v=5WoItGTWV54",
    ),
    "mode-collapse": (
        "Stanford CS231N: Generative models (mode collapse / evaluation)",
        "https://www.youtube.com/watch?v=5WoItGTWV54",
    ),
    "diffusion-forward": (
        "Umar Jamil: How diffusion models work — explanation and code (forward process)",
        "https://www.youtube.com/watch?v=I1sPXkm2NH4",
    ),
    "diffusion-reverse": (
        "Umar Jamil: How diffusion models work — explanation and code (reverse / loss)",
        "https://www.youtube.com/watch?v=I1sPXkm2NH4",
    ),
    "latent-conditioning": (
        "Umar Jamil: Coding Stable Diffusion (watch 0:00–45:00: VAE, CLIP, UNet)",
        "https://www.youtube.com/watch?v=ZBKpAp_6TGI",
    ),
    "chain-of-thought": (
        "Karpathy: Intro to Large Language Models (reasoning / system-2 remarks)",
        "https://www.youtube.com/watch?v=zjkBMFhNj_g",
    ),
    "self-consistency-tot": (
        "Karpathy: Deep Dive into LLMs like ChatGPT (sampling several traces)",
        "https://www.youtube.com/watch?v=7xTGNNLPyMI",
    ),
    "faithfulness": (
        "Karpathy: Deep Dive into LLMs like ChatGPT (why a fluent trace can still be wrong)",
        "https://www.youtube.com/watch?v=7xTGNNLPyMI",
    ),
    "rag-pipeline": (
        "Karpathy: Intro to Large Language Models (retrieval and tools)",
        "https://www.youtube.com/watch?v=zjkBMFhNj_g",
    ),
    "react-tools": (
        "Karpathy: Intro to Large Language Models (tool-use demo in the second half)",
        "https://www.youtube.com/watch?v=zjkBMFhNj_g",
    ),
    "eval-presentations": (
        "Simon Peyton Jones: How to give a great research talk (watch 0:00–20:00)",
        "https://www.youtube.com/watch?v=sT_-owjKIbA",
    ),
    "exam-review": (
        "Karpathy: Intro to Large Language Models (full recap of the stack)",
        "https://www.youtube.com/watch?v=zjkBMFhNj_g",
    ),
}

VIDEO_EXTRA = {
    "course-map": (
        "MIT 6.S191 Lecture 1: perceptron through loss and gradient descent (homework, ~17:20–44:22)",
        "https://www.youtube.com/watch?v=ErnWZxJovaM",
    ),
    "gpt-bert": (
        "CodeEmporium: BERT Neural Network — EXPLAINED!",
        "https://www.youtube.com/watch?v=xI0HHN5XKDo",
    ),
    "gradient-descent": (
        "3Blue1Brown: What is backpropagation really doing? (~14 min, after class)",
        "https://www.youtube.com/watch?v=Ilg3gGewQ5U",
    ),
    "lstm-gru": (
        "StatQuest: Gated Recurrent Units (GRU), Clearly Explained",
        "https://www.youtube.com/watch?v=tOuXgORsXJ4",
    ),
}

WEEKS = {
    1: {
        "label": "Module 1 — Neural networks and word embeddings",
        "lectures": ["course-map", "neurons-activations", "gradient-descent", "embeddings"],
        "labs": [("lab-1-xor-embeddings", False)],
        "readings": [
            ("Goodfellow, Bengio, Courville: Deep feedforward networks, Ch. 6 opening and §6.1 XOR", "https://www.deeplearningbook.org/contents/mlp.html"),
            ("Nielsen, Neural Networks and Deep Learning, Ch. 1 (gradient descent; stop before long MNIST)", "http://neuralnetworksanddeeplearning.com/chap1.html"),
            ("Jurafsky & Martin, Speech and Language Processing, Ch. 5 Embeddings (draft of 19 Aug 2026)", "https://web.stanford.edu/~jurafsky/slp3/5.pdf"),
            ("Mikolov et al. 2013, Efficient estimation of word representations, §§1–3", "https://arxiv.org/abs/1301.3781"),
            ("Stanford CS224N: word vectors and neural nets (copy intuitions; skip the skip-gram Jacobian)", "https://stanford.edu/class/cs224n/"),
            ("CS231N notes: neuron, backprop as gates, SGD", "https://cs231n.github.io/neural-networks-1/"),
        ],
        "discussion": [
            "Intrinsic vs. extrinsic evaluation of embeddings: which number belongs in a project report, and which one is for debugging?",
            "Name one way embedding geometry can encode a stereotype. What would you measure with the Lab 1 projection?",
            "Why can this course skip DATA 641 and 642 and still start from neurons this week?",
            "Goodfellow’s two-ReLU XOR vs. Lab 1’s 33-parameter MLP: what did the extra units buy you that the table already showed?",
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
        "lectures": ["audio-spectrograms", "audio-encoders", "fusion-scarcity"],
        "labs": [("lab-6-spectrograms", False)],
        "readings": [
            ("Radford et al., Whisper", "https://arxiv.org/abs/2212.04356"),
            ("Elizalde et al., CLAP", "https://arxiv.org/abs/2206.04769"),
        ],
        "discussion": [
            "Why is a spectrogram a more natural transformer input than the raw waveform for this course?",
            "Name one fusion choice you would defend if audio is often missing at test time.",
        ],
    },
    7: {
        "label": "Module 3 — Scaling, efficiency, and deployment",
        "lectures": ["scaling-laws", "mixture-of-experts", "efficiency-deploy"],
        "labs": [("lab-7-scale-quantize", False)],
        "readings": [
            ("Kaplan et al., Scaling laws for neural language models", "https://arxiv.org/abs/2001.08361"),
            ("Hoffmann et al., Chinchilla / training compute-optimal LLMs", "https://arxiv.org/abs/2203.15556"),
        ],
        "discussion": [
            "If you can 10× parameters or 10× tokens but not both, which does Chinchilla push you toward?",
            "Quantization is not a free lunch. What would you measure besides perplexity?",
        ],
    },
    8: {
        "label": "Module 3 — SFT, continual learning, and adapters",
        "lectures": ["sft-instructions", "continual-forgetting", "lora-adapters"],
        "labs": [("lab-8-lora-forget", False)],
        "readings": [
            ("Wei et al., Finetuned language models are zero-shot learners (FLAN)", "https://arxiv.org/abs/2109.01652"),
            ("Hu et al., LoRA", "https://arxiv.org/abs/2106.09685"),
        ],
        "discussion": [
            "Why can a model that next-token-predicts Wikipedia still fail a polite instruction?",
            "When is LoRA the wrong tool (name one setting)?",
        ],
    },
    9: {
        "label": "Module 3 — RLHF and direct preference optimization",
        "lectures": ["preference-rewards", "rlhf", "dpo"],
        "labs": [("lab-9-preferences", False)],
        "readings": [
            ("Ouyang et al., InstructGPT / RLHF", "https://arxiv.org/abs/2203.02155"),
            ("Rafailov et al., Direct Preference Optimization", "https://arxiv.org/abs/2305.18290"),
        ],
        "discussion": [
            "What can go wrong if the reward model is cheaper to game than the human raters were?",
            "DPO skips PPO. What assumption on the preference data remains?",
        ],
    },
    10: {
        "label": "Module 3 — Safety, editing, and retrieval-augmented training",
        "lectures": ["red-teaming", "editing-unlearning", "raft-memory"],
        "labs": [("lab-10-edit-retrieve", False)],
        "readings": [
            ("Meng et al., ROME / locating and editing factual associations", "https://arxiv.org/abs/2202.05262"),
            ("Zhang et al., RAFT", "https://arxiv.org/abs/2403.10131"),
        ],
        "discussion": [
            "Editing one fact is not unlearning a behavior. Give an example of each.",
            "When would you train with retrieved context (RAFT) instead of only retrieving at test time?",
        ],
    },
    11: {
        "label": "Module 4 — Generative models I: GANs",
        "lectures": ["gan-idea", "gan-training", "mode-collapse"],
        "labs": [("lab-11-toy-gan", False)],
        "readings": [
            ("Goodfellow et al., Generative adversarial nets", "https://arxiv.org/abs/1406.2661"),
            ("Salimans et al., Improved techniques for training GANs", "https://arxiv.org/abs/1606.03498"),
        ],
        "discussion": [
            "Why is “the discriminator accuracy is 99%” not proof the generator is good?",
            "Name one evaluation that would catch mode collapse that a single sample would miss.",
        ],
    },
    12: {
        "label": "Module 4 — Generative models II: diffusion",
        "lectures": ["diffusion-forward", "diffusion-reverse", "latent-conditioning"],
        "labs": [("lab-12-denoise", False)],
        "readings": [
            ("Ho et al., Denoising diffusion probabilistic models", "https://arxiv.org/abs/2006.11239"),
            ("Rombach et al., Latent diffusion / Stable Diffusion", "https://arxiv.org/abs/2112.10752"),
        ],
        "discussion": [
            "What does the network actually predict in a typical DDPM training step?",
            "Why does latent diffusion help text-to-image more than pixel-space diffusion does?",
        ],
    },
    13: {
        "label": "Module 4 — Reasoning and chain-of-thought",
        "lectures": ["chain-of-thought", "self-consistency-tot", "faithfulness"],
        "labs": [("lab-13-reasoning", False)],
        "readings": [
            ("Wei et al., Chain-of-thought prompting", "https://arxiv.org/abs/2201.11903"),
            ("Wang et al., Self-consistency", "https://arxiv.org/abs/2203.11171"),
            ("Yao et al., Tree of Thoughts", "https://arxiv.org/abs/2305.10601"),
        ],
        "discussion": [
            "Self-consistency can raise accuracy without making any one trace more faithful. Why?",
            "When would you refuse to put a CoT trace in a user-facing product?",
        ],
    },
    14: {
        "label": "Module 4 — Tools, RAG, and final presentations",
        "lectures": ["rag-pipeline", "react-tools", "eval-presentations"],
        "labs": [("lab-14-toy-rag", False)],
        "readings": [
            ("Lewis et al., RAG", "https://arxiv.org/abs/2005.11401"),
            ("Yao et al., ReAct", "https://arxiv.org/abs/2210.03629"),
        ],
        "discussion": [
            "What failure does RAG not fix if the retrieved chunk is itself wrong?",
            "In a project talk, which number belongs on the slide: a demo GIF, or an ablation?",
        ],
    },
    15: {
        "label": "Final exam and remaining talks",
        "lectures": ["exam-review"],
        "readings": [
            ("Course hub: weeks 1–14 notes", "data-643.html"),
        ],
        "discussion": [
            "Pick one method from Modules 1–4 and name the measurement you would report, not the architecture.",
            "Remaining talks: as posted on Canvas. Bring one failure case, not only the best run.",
        ],
    },
}
