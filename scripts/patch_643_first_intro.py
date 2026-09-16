"""Insert a first-time what/why/arch/how/formula/tradeoffs block into 643 lectures."""

from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
NOTES = ROOT / "files" / "data-643"
MARKER = "**First time this method appears.**"
SKIP_IF = ("## 1. What ", MARKER)

BLOCKS = {
    "neurons-activations": """
**First time this method appears.** A **neuron** is the unit of a net. Answer these before XOR.

**What.** A weighted sum plus a bias, then a nonlinearity. Stack them and you have an MLP.
**Why.** Linear maps compose to one linear map. The bend is what makes depth useful.
**Architecture.** Input \(\\boldsymbol{x}\) → \(z=w^{\\top}x+b\) → \(a=\\sigma(z)\). An MLP stacks that layerwise.
**How.** Pick \(\\sigma\) (ReLU in hidden layers, softmax when classes compete). Train \(w,b\) next note.
**Formula.** \(z=w^{\\top}x+b\), \(a=\\sigma(z)\), \(\\operatorname{softmax}(z)_i=e^{z_i}/\\sum_j e^{z_j}\).
**Tradeoffs.** + ReLU is cheap and sparse. − Sigmoid saturates (bad gradients). No nonlinearity ⇒ no extra function class.
""",
    "gradient-descent": """
**First time this method appears.** **Gradient descent** is how nets learn. Answer these before the ReLU chain rule.

**What.** Repeatedly walk downhill on a loss \(L(\\theta)\). Stochastic GD uses a minibatch, not the full dataset.
**Why.** You cannot solve \(\\nabla L=0\) in closed form for a deep net. This is the training loop of pretraining.
**Architecture.** Forward (compute \(L\)) → backward (compute \(\\nabla_\\theta L\)) → update \(\\theta\).
**How.** Pick a step size \(\\eta\). Too large: diverge. Too small: crawl. Adam is a later variant with per-coordinate scales.
**Formula.** \(\\theta \\leftarrow \\theta - \\eta\\nabla_\\theta L\). Chain rule on one ReLU: \(\\partial L/\\partial w = (\\partial L/\\partial a)\\,\\mathbf{1}_{z>0}\,x\).
**Tradeoffs.** + Simple, scales to millions of steps. − Local minima / saddles, needs a step-size choice, noisy minibatches.
""",
    "embeddings": """
**First time this method appears.** An **embedding** is a map from a token id to a dense vector.

**What.** A short dense vector per word (or subword). Similar usage → nearby vectors.
**Why.** One-hot geometry is orthogonal: *film* and *movie* have inner product 0. You need a geometry you can learn.
**Architecture.** A table \(E\\in\\mathbb{R}^{V\\times d}\). Row \(i\) is the vector for token \(i\). Skip-gram trains it with a softmax classifier you then throw away.
**How.** Windows of neighbors. Skip-gram: from the center, predict a neighbor. Keep the center rows.
**Formula.** \(P(w_o\\mid w_c)=\\exp(u_o^{\\top} v_c)/\\sum_w \\exp(u_w^{\\top} v_c)\). Cosine: \(u^{\\top}v/(\\lVert u\\rVert\\lVert v\\rVert)\).
**Tradeoffs.** + Analogies and nearest neighbors as a debug tool. − Static vectors (one vector per word type); bias in the corpus becomes geometry; Week 3 will replace this with contextual states.
""",
    "sequence-rnns": """
**First time this method appears.** An **RNN** is a net that shares one cell across time.

**What.** Hidden state \(h_t\) is a function of \(h_{t-1}\) and the new token. An RNN-LM predicts the next token from \(h_t\).
**Why.** A fixed window (n-gram / bag) cannot count “the verb agrees with the noun 40 tokens back” without growing width.
**Architecture.** Shared cell \(h_t=\\tanh(W_{hh}h_{t-1}+W_{xh}x_t+b)\), then softmax on \(h_t\). Unroll in time for training (BPTT).
**How.** Read left to right. The same \(W\) at every step. Lab 2 copies the first bit at the end.
**Formula.** \(p(w_t\\mid w_{<t})=\\operatorname{softmax}(W_o h_t)_w\).
**Tradeoffs.** + Variable length, parameter sharing. − Sequential (hard to parallelize), vanishing/exploding gradients (next note).
""",
    "vanishing-gradients": """
**First time this method appears.** **Vanishing (and exploding) gradients** are why vanilla RNNs forget.

**What.** BPTT multiplies the same Jacobian many times. If the largest \(|\\lambda|\) of that map is \(<1\), early tokens stop training. If \(>1\), activations explode.
**Why.** You asked the RNN to carry a bit across \(T\) steps. The gradient is the only teacher for those early weights.
**Architecture.** Unrolled RNN: \(T\) copies of \(W_{hh}\). Gradient of \(L\) w.r.t. \(h_1\) goes through \(T-1\) multiplies.
**How.** Diagnose with gradient norms vs \(T\). Mitigate with clipping (explode) or gates (next note), not by “more layers” of the same cell.
**Formula.** \(\\partial h_t/\\partial h_1\) involves \(\\prod_{s=2}^{t} W_{hh}^{\\top} D_s\). Clip: \(g \\leftarrow g \\cdot \\min(1, C/\\lVert g\\rVert)\).
**Tradeoffs.** + Clipping is cheap. − Clipping does not fix vanishing; gates (LSTM) do. Exploding and vanishing are different bugs.
""",
    "lstm-gru": """
**First time this method appears.** **LSTMs** and **GRUs** are gated RNNs.

**What.** An additive **cell** path that can copy a value when the forget gate is open and the input gate is closed. GRU is the two-gate cousin.
**Why.** Vanilla RNNs vanish. You need a highway whose gradient is \(\\approx 1\) along the copy.
**Architecture.** LSTM: cell \(c_t\), hidden \(h_t\), gates \(i,f,o\). GRU: reset and update, no extra \(c\).
**How.** Copy regime: \(f\\approx 1\), \(i\\approx 0\) ⇒ \(c_t\\approx c_{t-1}\). Lab 2: LSTM vs RNN on a long copy.
**Formula.** \(c_t=f_t\\odot c_{t-1}+i_t\\odot \\tilde{c}_t\), \(h_t=o_t\\odot\\tanh(c_t)\). GRU: \(h_t=(1-z_t)\\odot h_{t-1}+z_t\\odot \\tilde{h}_t\).
**Tradeoffs.** + Long-range copy, still sequential. − More parameters than a vanilla RNN; still not parallel like attention. GRU is cheaper, sometimes enough.
""",
    "attention-need": """
**First time this method appears.** **Attention** is a path of length one between any two positions.

**What.** Instead of squeezing a sentence into one RNN hidden state, each output position **looks at** all encoder states with a weighted sum.
**Why.** Seq2seq RNNs have a bottleneck: one vector for the whole source. Long sources forget the beginning.
**Architecture.** Encoder states \(h_1,\\ldots,h_T\). Decoder query \(q_t\). Weights over source, then mix. Self-attention (next note) uses the same sequence for query and keys.
**How.** Score, softmax, weighted sum. Cost is \(T^2\) scores, not path length \(T\).
**Formula.** Path length 1 at cost \(O(T^2 d)\). Bahdanau: \(e_{ti}=v^{\\top}\\tanh(W_q q_t+W_h h_i)\).
**Tradeoffs.** + No sequential bottleneck, interpretable weights. − Quadratic cost in \(T\); you still need the formula next hour.
""",
    "self-attention": """
**First time this method appears.** **Self-attention** is the calculation inside a transformer layer.

**What.** A weighted sum of **values**, with weights from **queries** compared to **keys**. Every token plays all three roles.
**Why.** RNNs mix left-to-right through \(h_t\). Self-attention mixes any pair in one layer, in parallel.
**Architecture.** \(X\\mapsto Q,K,V\) by three matrices. Scores \(QK^{\\top}/\\sqrt{d_k}\), softmax over keys, mix \(V\). Multi-head: several of those in parallel, then \(W_O\). Causal mask for LMs.
**How.** Lab 3: one head by hand, then a causal mask. Zero is the wrong mask fill; use \(-\\infty\).
**Formula.** \(\\operatorname{Attention}(Q,K,V)=\\operatorname{softmax}(QK^{\\top}/\\sqrt{d_k})V\).
**Tradeoffs.** + Parallel, path length 1, multi-head specialization. − \(O(T^2)\); mixing **keys** instead of values is a common bug; no positions until note 3.3.
""",
    "transformer-block": """
**First time this method appears.** A **transformer block** is attention plus an MLP, with residuals.

**What.** One layer: (masked) self-attention, residual + LayerNorm, token-wise MLP, residual + LayerNorm. Positions added on the embeddings.
**Why.** Attention mixes **across** positions. The MLP mixes **channels** at one position. Residuals keep a highway so depth trains.
**Architecture.** Decoder-only (GPT): causal mask. Encoder (BERT): bidirectional. Encoder–decoder: extra cross-attention.
**How.** Add a positional vector to each token embedding. Pre-norm vs post-norm is a stability knob; we draw residual around sublayers.
**Formula.** \(X^{\\ell+1}=X^\\ell+\\mathrm{MLP}(X^\\ell+\\mathrm{Attn}(X^\\ell))\) (cartoon; norms omitted). Positions: \(X_0=E+P\).
**Tradeoffs.** + Depth, parallelism, one block reused. − Quadratic attention; positions are extra parameters or sinusoids; encoder vs decoder is a method choice, not a vibe.
""",
    "gpt-bert": """
**First time this method appears.** **GPT** and **BERT** are two uses of the same block.

**What.** GPT: causal next-token (left to right). BERT: masked tokens, bidirectional context. Both produce **contextual** vectors, not a static table (Week 1).
**Why.** Language modeling (GPT) is the pretrain that later becomes ChatGPT. BERT-style MLM is a bidirectional encoder for classification and span tasks.
**Architecture.** Same transformer block. GPT masks the future. BERT masks random token ids and reconstructs them. Heads differ (LM vs CLS/span).
**How.** Train on unlabeled text. After pretrain, GPT generates; BERT is usually fine-tuned with a small head.
**Formula.** GPT: \(\\prod_t p(w_t\\mid w_{<t})\). BERT: reconstruct masked positions, not a full joint factorization of the sentence.
**Tradeoffs.** + Contextual geometry. − GPT cannot see the future inside a prompt token; BERT is not a natural generator. “Transformer” is the block; GPT/BERT is the **objective**.
""",
    "multimodal-foundations": """
**First time this method appears.** **Multimodal learning** is more than “glue an image to a caption.”

**What.** Five jobs (Baltrušaitis et al.): represent, align, fuse, translate, co-learn. A model can score a pair (CLIP) without decoding a sentence.
**Why.** Pixels, text, and audio are different sensors. Concatenation is one fusion; it is not the only job.
**Architecture.** Separate encoders per modality, then a fuse (concat, add, or cross-attention) or a score (cosine).
**How.** Pick the job first. Retrieval needs a score. Captioning needs a decoder. Classification can be a linear head on a frozen encoder.
**Formula.** Coordinated: \(s(i,t)=\\cos(f(i),g(t))\). Joint concat: \([f(i);g(t)]\\,W\).
**Tradeoffs.** + You can reuse a frozen encoder. − Concat grows width; alignment needs paired data; “multimodal” without naming the job is not a project.
""",
    "vision-transformers": """
**First time this method appears.** A **ViT** treats an image as a sequence of patches.

**What.** Cut the image into non-overlapping patches, linearly map each to a \(d\)-vector, add positions, run a transformer **without** a causal mask.
**Why.** CNNs are the older default. ViT shows the same block as language can mix patches globally from layer 1.
**Architecture.** Patch embed \(E\\in\\mathbb{R}^{P\\times d}\) plus optional CLS token, then encoder blocks. Classification: CLS or mean pool, then a head.
**How.** Lab 4 flattens patches. No convolution is required for the cartoon. Pretrain on a large image set; small data prefers CNNs or a strong recipe.
**Formula.** For patch size \(p\\times p\) and image \(H\\times W\), sequence length \(T=(H/p)\\cdot(W/p)\). \(X=\\mathrm{LN}(P W_e+E_{\\mathrm{pos}})\).
**Tradeoffs.** + Global mixing, same code as NLP. − Quadratic in patches; needs data or regularization; patch size is a method knob.
""",
    "contrastive-zeroshot": """
**First time this method appears.** **Contrastive learning** pulls matched pairs together and pushes the rest apart. **Zero-shot** is classify by nearest prompt, not a \(C\)-way trained head.

**What.** InfoNCE on a batch of \(N\) matched pairs. Zero-shot: embed class phrases, pick \(\\arg\\max_c \\cos(f(x),g(\\text{prompt}_c))\).
**Why.** You may not have labels for every class at train time. A similarity space transfers to new names.
**Architecture.** Two encoders (or two views of one). A batch matrix of scores. Softmax over the row (or bidirectional).
**How.** Lab 4: four pairs, heatmap of the \(N\\times N\) scores. The diagonal should win.
**Formula.** \(\\mathcal{L}=-\\frac{1}{N}\\sum_i \\log \\frac{\\exp(s_{ii}/\\tau)}{\\sum_j \\exp(s_{ij}/\\tau)}\), \(s_{ij}=\\cos(u_i,v_j)\).
**Tradeoffs.** + No \(C\)-way head, works with prompts. − Needs big batches (many negatives); temperature \(\\tau\) is a knob; compositionality is not free.
""",
    "clip": """
**First time this method appears.** **CLIP** is two towers and a cosine. It scores image–text pairs. It does not write a caption.

**What.** Image encoder + text encoder, InfoNCE on the batch, keep both towers.
**Why.** One model that retrieves and zero-shot classifies without a detector or a decoder.
**Architecture.** `encode_image`, `encode_text`, cosine. No `generate`.
**How.** Train on web pairs. At test, embed the image and a list of prompts. Note 5.2 adds a decoder (BLIP).
**Formula.** Same InfoNCE as 4.3 with learned \(\\tau\\). API is three calls.
**Tradeoffs.** + Zero-shot and retrieval. − Not a captioner; hungry for batch size; prompt wording is method; bias next note.
""",
    "blip": """
**First time this method appears.** **BLIP** is CLIP-style scoring **plus** a decoder that writes text, with a filter on noisy web pairs.

**What.** Three losses: ITC (contrastive), ITM (matched vs unmatched pair), LM (caption tokens). Bootstrap: generate captions, filter, train.
**Why.** CLIP cannot decode a sentence. Naive captioners train on noisy alt-text. BLIP tries to clean the web and add generation.
**Architecture.** Image encoder, text encoder, and a decoder with **cross-attention** into image tokens (queries from text, keys/values from vision).
**How.** ITC aligns. ITM is a binary match head. LM is next-token on the caption. Generation uses the decoder; retrieval can use ITC embeddings.
**Formula.** ITC as InfoNCE; ITM as logistic on a CLS; LM as \(\\sum_t -\\log p(w_t\\mid w_{<t},\\text{image})\).
**Tradeoffs.** + Captions and retrieval in one family. − Hallucinated captions; filter is extra machinery; heavier than frozen CLIP.
""",
    "retrieval-bias": """
**First time this method appears.** **Recall@k** is a retrieval metric. **Bias probes** and **typographic attacks** are how you stress a CLIP-like space.

**What.** recall@k: fraction of queries whose true match sits in the top \(k\). An occupation probe: does “nurse” retrieve stereotyped images? Typographic: a word printed in the photo can hijack the text tower.
**Why.** A pretty cosine is not a fair or robust system. You need a number that can go the wrong way.
**Architecture.** Same two towers. Evaluation is a ranked list plus extra probe sets.
**How.** Rank both directions (image→text and text→image). Report recall@1/@5. Then one occupation table and one typographic miss.
**Formula.** \(\\operatorname{recall}@k=\\frac{1}{Q}\\sum_q \\mathbf{1}[\\mathrm{rank}(q)\\le k]\).
**Tradeoffs.** + Cheap to compute, catches misses. − Does not measure calibration or fairness by itself; probes are datasets, not slogans.
""",
    "audio-spectrograms": """
**First time this method appears.** A **spectrogram** is a picture of sound. Models do not eat 16 kHz samples as a raw list.

**What.** STFT: window the waveform, FFT each frame, plot frequency vs time. A **mel** spectrogram warps frequency to a perceptual scale.
**Why.** Waveforms are long and oscillatory. A 2-D time–frequency map can be patched like a ViT image.
**Architecture.** Waveform → frames → STFT magnitudes (optionally mel + log) → patch embed → transformer.
**How.** Lab 6: sine mixture, STFT, patch. Hop length and window are method knobs.
**Formula.** Frame \(m\): \(X(m,\\omega)=\\sum_n x[n]w[n-mH]e^{-j\\omega n}\). Sequence length ≈ number of frames (or patches of frames).
**Tradeoffs.** + Shares ViT code. − Phase often dropped; time resolution vs frequency resolution; not yet a transcriber (next note).
""",
    "audio-encoders": """
**First time this method appears.** **Whisper** transcribes speech. **CLAP** retrieves audio against text. Same spectrogram, different head.

**What.** Whisper: encoder (audio tokens) + **GPT-style decoder** that writes text (no CTC required in this course). CLAP: two towers like CLIP, audio instead of pixels.
**Why.** ASR needs a decoder. Retrieval needs a score. Do not use Whisper as a search index or CLAP as a transcriber.
**Architecture.** Whisper: spectrogram → conv/embed → encoder blocks → decoder with cross-attention. CLAP: audio encoder \(f\), text encoder \(g\), cosine.
**How.** Whisper: teacher-forced captions of speech, then generate. CLAP: InfoNCE on audio–text pairs (same loss family as 4.3).
**Formula.** Whisper LM: \(\\prod_t p(y_t\\mid y_{<t},\\text{audio})\). CLAP: \(\\cos(f(a),g(t))\).
**Tradeoffs.** + Whisper is a generator; CLAP is cheap retrieval. − Whisper is not a general audio tagger; CLAP does not decode words; paired audio–text is scarce (note 6.3).
""",
    "fusion-scarcity": """
**First time this method appears.** **Fusion** is how modalities meet. **Scarcity** is that paired audio/text/video is smaller than text.

**What.** Early fusion (concat features then one net), late (combine decisions), cross-attention (queries from one side, keys/values from the other).
**Why.** Concat is the student default and grows width. Missing a modality at test time breaks naive concat.
**Architecture.** Draw two towers, then pick concat / add / cross-attn. Data pyramid: lots of unpaired text, less paired A/V.
**How.** Lab 6: concat vs add on toy vectors. Project: name the fuse and what you do if audio is missing.
**Formula.** Concat: \([u;v]\\in\\mathbb{R}^{d_u+d_v}\). Add needs \(d_u=d_v\). Cross-attn: \(\\operatorname{softmax}(Q_u K_v^{\\top}/\\sqrt{d})V_v\).
**Tradeoffs.** + Cross-attn can attend to a spectrogram while generating text. − Width, missing-modality failure, and paired-data cost.
""",
    "scaling-laws": """
**First time this method appears.** A **scaling law** is a fitted curve of pretraining loss versus scale, not a promise of a better chatbot.

**What.** Kaplan: loss vs compute (and \(N\), \(D\)) looks like a power law plus a floor. Chinchilla: at fixed FLOPs, grow **tokens and parameters together** (~20 tokens/parameter in that paper).
**Why.** “We trained a 7B” is not a complete sentence. You need the token budget and whether you were compute-optimal.
**Architecture.** Not a new net. A log–log plot and a recipe \((N,D,C)\).
**How.** Fit \(L\\approx a C^{-b}+L_\\infty\) (Lab 7 algebra). Then do Chinchilla arithmetic: \(7\\mathrm{B}\\times 20=140\\mathrm{B}\) tokens.
**Formula.** \(L(C)\\approx a C^{-b}+L_\\infty\). Training FLOPs cartoon: \(\\approx 6ND\).
**Tradeoffs.** + Planning a run. − \(L\\) is not chat quality; data mixture and alignment sit off the curve; four toy points are not a law.
""",
    "mixture-of-experts": """
**First time this method appears.** A **mixture of experts (MoE)** stores many MLPs and runs only a few per token.

**What.** A **router** picks \(k\) experts (often 2 of 8). Capacity grows with stored experts; FLOPs stay near \(k\) dense MLPs.
**Why.** Dense nets pay every MLP on every token. MoE buys width in parameters without width in compute.
**Architecture.** Attention stays dense. Replace the block MLP with \(E\) copies plus a linear router. Mixtral cartoon: 8 stored, top-2 active, no shared expert.
**How.** Softmax (or noisy top-\(k\)) over router logits, run those experts, weighted sum. Load-balancing so expert 0 does not eat the batch.
**Formula.** \(y=\\sum_{i\\in\\mathcal{T}(x)} g_i(x)\\,E_i(x)\). Stored MLP weights \(\\approx E P\); active FLOPs scale with \(k\).
**Tradeoffs.** + More capacity at similar token-FLOPs. − RAM holds all experts; batching is harder; collapse = a dense net in disguise; serving ≠ “same active FLOPs.”
""",
    "sft-instructions": """
**First time this method appears.** **Supervised fine-tuning (SFT)** is next-token training on **instruction–answer** pairs, with the prompt masked.

**What.** Pretrain already speaks. SFT teaches format: follow the user, answer as an assistant. Loss on the **answer tokens**, not the prompt.
**Why.** A base LM completes text; it does not reliably follow “Write a bullet list.” Preferences (Week 9) come after this.
**Architecture.** Same transformer. Dataset of (prompt, answer). Causal mask unchanged. Label mask: prompt positions are \(-100\) / ignored.
**How.** Collect or write pairs. Train a few epochs. Too many epochs: forget the base (note 8.2).
**Formula.** \(\\mathcal{L}=-\\sum_{t\\in\\mathrm{answer}}\\log p_\\theta(y_t\\mid y_{<t},\\text{prompt})\).
**Tradeoffs.** + Fast behavior change. − Copies answers (including bad ones); can forget; not a preference model; noisy instruction data is method.
""",
    "continual-forgetting": """
**First time this method appears.** **Catastrophic forgetting** is: train on task B and task A slips.

**What.** Sequential training without replay overwrites the weights that did A. Continual learning tries to add B without burying A.
**Why.** You will fine-tune. XOR-then-AND in Lab 8 is the cartoon. Production: new policy PDFs every month.
**Architecture.** Same net. Mitigations: **replay** (mix old batches), freeze layers, **LoRA** (isolate \(\\Delta\) in \(BA\)), or a regularizer toward old \(\\theta\) (EWC cartoon: penalty on important weights).
**How.** Measure A **after** B. If you only plot B, you hid the bug. Replay is the first lever; LoRA is the isolator next note.
**Formula.** Cartoon EWC: \(\\mathcal{L}_B(\\theta)+\\frac{\\lambda}{2}\\sum_i F_i(\\theta_i-\\theta_i^A)^2\). You do not compute a full Fisher in this class; you need the idea.
**Tradeoffs.** + Replay is simple. − Replay needs stored data; freeze can block B; LoRA still forgets if you merge carelessly; EWC is extra knobs.
""",
    "lora-adapters": """
**First time this method appears.** **LoRA** freezes \(W\) and trains a low-rank residual \(BA\).

**What.** \(\\Delta W\\approx BA\) with rank \(r\\ll \\min(d,k)\). Store megabytes per task, not a second 7B.
**Why.** Full fine-tune copies every weight (GPT-3: 175B extra per task) and overwrites (note 8.2).
**Architecture.** Insert \(A,B\) on attention and/or MLP projections. Init \(B=0\) so you start as the base. QLoRA: 4-bit \(W\), float adapters.
**How.** Train only \(A,B\). Merge \(W\\leftarrow W+(\\alpha/r)BA\) at deploy (no extra latency) or swap adapters.
**Formula.** \(h=Wx+(\\alpha/r)BAx\). Trainable count per matrix \(r(d+k)\), not \(dk\).
**Tradeoffs.** + Cheap, mergeable, one adapter per skill. − Small \(r\) may fail hard domain shifts; adapters can leak in federated settings; not a new architecture.
""",
    "preference-rewards": """
**First time this method appears.** A **reward model (RM)** scores completions from **preference pairs** (chosen vs rejected).

**What.** Humans (or a teacher) pick \(y_w\) over \(y_l\) for prompt \(x\). Bradley–Terry turns that into a logistic loss on \(r(x,y)\).
**Why.** SFT copies a single answer. Preferences say “this is better than that” without writing a scalar label by hand.
**Architecture.** Usually the base LM plus a scalar head, or a small classifier on the last token. Best-of-\(n\): sample \(n\), pick \(\\arg\\max r\), no PPO yet.
**How.** Collect pairs. Train \(r\). Chance loss is \(\\log 2\\). Lab 9 is a tiny head.
**Formula.** \(p(y_w\\succ y_l\\mid x)=\\sigma(r(x,y_w)-r(x,y_l))\). Loss \(-\\log\\sigma(\\Delta r)\).
**Tradeoffs.** + Pairwise data is easier than absolute scores. − Reward hacking (next notes); RM error becomes policy error; best-of-\(n\) is compute at decode.
""",
    "rlhf": """
**First time this method appears.** **RLHF** is three stages: SFT, reward model, then **PPO** on the policy with a KL leash.

**What.** After SFT and an RM, you sample from the **current** policy, score with \(r\), update to raise reward minus KL to a frozen reference.
**Why.** SFT does not explore. Best-of-\(n\) uses \(r\) only at decode. RLHF trains \(\\pi\) to look high-reward **as it samples**.
**Architecture.** Policy \(\\pi_\\theta\), reference \(\\pi_{\\mathrm{ref}}\) (usually SFT), RM \(r\\) (frozen in the PPO stage), optional critic.
**How.** PPO clip + advantage. \(\\beta=0\) (no KL) is reward hacking: the policy exploits \(r\).
**Formula.** \(\\max_\\pi \\mathbb{E}[r(x,y)]-\\beta\\,\\mathrm{KL}(\\pi(\\cdot\\mid x)\\|\\pi_{\\mathrm{ref}}(\\cdot\\mid x))\).
**Tradeoffs.** + Can beat SFT on preference evals. − Unstable, expensive, RM misspecification; people look to DPO (next note) to skip PPO.
""",
    "dpo": """
**First time this method appears.** **DPO** fits a policy to the same preference pairs **without** an RM loop and **without** PPO.

**What.** Under Bradley–Terry, the optimal reward is \(r=\\beta\\log(\\pi/\\pi_{\\mathrm{ref}})+c(x)\). Plug into the logistic loss; \(r\) disappears. Train \(\\pi_\\theta\) offline.
**Why.** RLHF’s PPO stage is heavy. DPO is a classification loss on logits of \(y_w\) and \(y_l\).
**Architecture.** Policy + frozen reference. No critic, no sampling-in-the-loop required (you need logprobs of both completions).
**How.** Lab 9: toy scalar logits. Start: \(\\pi=\\pi_{\\mathrm{ref}}\) ⇒ loss \(\\log 2\\).
**Formula.** \(\\mathcal{L}_{\\mathrm{DPO}}=-\\log\\sigma\\big(\\beta\\log\\frac{\\pi_\\theta(y_w\\mid x)}{\\pi_{\\mathrm{ref}}(y_w\\mid x)}-\\beta\\log\\frac{\\pi_\\theta(y_l\\mid x)}{\\pi_{\\mathrm{ref}}(y_l\\mid x)}\\big)\).
**Tradeoffs.** + Offline, no RM. − Still needs pairs and a reference; can overfit; not magic if the pairs are noisy.
""",
    "red-teaming": """
**First time this method appears.** **Red-teaming** is a **safety evaluation**: a fixed list of probes, a rate of successful attacks, rerun after you patch.

**What.** Not a training algorithm. You try to elicit disallowed behavior (HarmBench-style: hundreds of behaviors) and count failures.
**Why.** “The model seems safe in demo” is not a number. After SFT/DPO/edits, the rate can come back.
**Architecture.** Probe set + a success classifier (human or automated) + the model under test. Optional: an attacker LM that writes probes.
**How.** Freeze the probe list. Report attack success rate. After a safety patch, **rerun the same list**.
**Formula.** \(\\mathrm{ASR}=\\#\\{\\text{successful probes}\\}/\\#\\{\\text{probes}\\}\). HarmBench cartoon: 510 behaviors.
**Tradeoffs.** + Comparable over time. − Coverage is only as good as the list; automated judges err; not a proof of safety; not a substitute for formal guarantees.
""",
    "raft-memory": """
**First time RAFT appears.** (RAG itself is defined in one page above, and fully taught in Week 14.1.) **RAFT** is retrieval-augmented **fine-tuning**.

**What.** Train the reader **with** retrieved snippets in context (gold + **distractors**) so it learns to cite or ignore, not only recite pretrain weights.
**Why.** Vanilla RAG at test time with a frozen SFT model often **ignores** the snippet. Index edits then do nothing.
**Architecture.** Same retrieve-then-generate stack as RAG. The difference is the **training rows** and that \(\\theta\) **changes**. Loss is SFT on the answer given the bundle.
**How.** Build rows: question + top-\(k\) texts (some irrelevant) + target answer that uses gold and skips junk. Lab 10’s overlap retriever is the toy ranker.
**Formula.** \(\\mathcal{L}=-\\sum_{t\\in\\mathrm{answer}}\\log p_\\theta(y_t\\mid y_{<t}, q, \\hat{z}_{1:k})\) with \(\\hat{z}\) containing distractors on purpose.
**Tradeoffs.** + Reader learns to use the open book. − Still SFT (can copy); needs a retriever at train time; not a new architecture; gold-only rows never practice skip.
""",
    "gan-idea": """
**First time this method appears.** A **GAN** is two nets: a **generator** that samples in one pass, and a **discriminator** that scores real vs fake.

**What.** You give up on writing \(p(x)\). \(G(z)\) maps noise to a fake. \(D(x)\\in(0,1)\) says “real.”
**Why.** Likelihood models can be blurry or slow to sample. GANs aim for sharp one-pass samples (images, later 11.3’s coverage bugs).
**Architecture.** \(z\\sim p(z)\) → \(G\) → fake. \(D\) sees reals from the data and fakes from \(G\). No encoder required.
**How.** Train both (details next note). Bayes-optimal \(D\) is \(1/2\) where \(G\) matches the data.
**Formula.** \(D^*(x)=p_{\\mathrm{data}}(x)/(p_{\\mathrm{data}}(x)+p_G(x))\). At a perfect \(G\), \(D^*=1/2\).
**Tradeoffs.** + Fast sampling, sharp samples when it works. − No likelihood, unstable train (11.2), mode collapse (11.3), not an LLM method.
""",
    "gan-training": """
**First time this training loop appears.** GAN **training** is a min-max game with two phases per iteration.

**What.** \(D\) climbs to tell real from fake. \(G\) climbs to fool \(D\). The original saturating loss for \(G\) is weak; people use \(-\\log D(G(z))\).
**Why.** If you only train \(D\) to 99%, \(G\) gets no gradient. If you only train \(G\), \(D\) is stale.
**Architecture.** Same two nets. Alternate (or simultaneous) SGD steps. No KL term here; that is RLHF.
**How.** Phase D: maximize log \(D\) on reals + log \((1-D)\) on fakes. Phase G: non-saturating \(-\\log D(G(z))\).
**Formula.** \(J(D,G)=\\mathbb{E}_{x}[\\log D(x)]+\\mathbb{E}_{z}[\\log(1-D(G(z)))]\). \(G\) minimizes a surrogate, not always this \(J\).
**Tradeoffs.** + When balanced, samples improve. − Oscillation, vanishing gradients for \(G\), sensitivity to step sizes; next note is collapse.
""",
    "mode-collapse": """
**First time this failure appears.** **Mode collapse** is when \(G\) parks on a few modes and \(D\) is still happy.

**What.** One pretty sample is not a trained \(G\). Coverage: 92/8 on two Gaussians is collapse; 47/53 is covered.
**Why.** \(D\) only scores “is this fake?” It does not have a missing-mode term. \(G\) can fool \(D\) with one spike.
**Architecture.** Same GAN. Evaluation needs **bins / modes**, not only \(\\mathrm{loss}_G\).
**How.** Lab 11: two 1-D Gaussians. Count mass per mode. Fixes (brief): more diverse \(z\), unrolled/regularized \(D\), or switch to diffusion (Week 12).
**Formula.** There is no extra loss term in vanilla \(J\) that says “visit mode 2.” That is the bug.
**Tradeoffs.** + Easy to demo. − Image metrics (FID) are imperfect coverage proxies; fixing collapse is still research-level.
""",
    "diffusion-forward": """
**First time this method appears.** **Diffusion** (DDPM) **destroys** a sample with Gaussian noise on a schedule, then later learns to reverse it.

**What.** Forward process \(q(x_t\\mid x_0)\) is a **fixed** Gaussian that interpolates from data (\(t=0\)) to nearly isotropic noise (\(t=T\)). You can **jump** to any \(t\) in one shot.
**Why.** GANs fight a min-max. Diffusion trains a denoiser with MSE. The kernel is not learned.
**Architecture.** Markov chain \(x_0\\to x_1\\to\\cdots\\to x_T\). Variance schedule \(\\beta_t\) or \(\\bar{\\alpha}_t\\in[1,0]\).
**How.** Sample \(\\varepsilon\\sim\\mathcal{N}(0,I)\), set \(x_t=\\sqrt{\\bar{\\alpha}_t}x_0+\\sqrt{1-\\bar{\\alpha}_t}\\varepsilon\). Lab 12 does this in 2-D.
**Formula.** \(q(x_t\\mid x_0)=\\mathcal{N}(\\sqrt{\\bar{\\alpha}_t}x_0,(1-\\bar{\\alpha}_t)I)\).
**Tradeoffs.** + Stable training target, likelihood-related. − Forward is easy; reverse sampling is slow (next notes). Not a GAN.
""",
    "diffusion-reverse": """
**First time the reverse process appears.** The **reverse** is: predict the noise you added, take a step toward \(x_0\), repeat \(T\) times.

**What.** A net \(\\varepsilon_\\theta(x_t,t)\) predicts \(\\varepsilon\). Training is MSE on that noise. Sampling starts from \(x_T\\sim\\mathcal{N}(0,I)\) and denoises.
**Why.** You cannot write the true reverse in closed form for images. Predicting \(\\varepsilon\) is equivalent (under the usual parameterization) to predicting the posterior mean.
**Architecture.** U-Net or DiT on \(x_t\) with a time embedding. Lab 12 uses an **oracle** mean so you see the geometry without training.
**How.** Loss: \(\\mathbb{E}\\lVert\\varepsilon-\\varepsilon_\\theta(x_t,t)\\rVert^2\). Sample: \(T\) reverse steps (or fewer with a faster sampler, later papers).
**Formula.** \(x_{t-1}\) from \(\\varepsilon_\\theta\) via the standard DDPM mean; cartoon: subtract a scaled \(\\varepsilon_\\theta\) and add a little noise (except \(t=1\)).
**Tradeoffs.** + MSE is easier than GAN min-max. − Many steps at sample time; quality vs speed; classifier-free guidance is next note.
""",
    "latent-conditioning": """
**First time this appears.** **Latent diffusion** denoises in a **VAE latent**, not in pixels. **CFG** mixes a conditional and an unconditional noise prediction.

**What.** Encode \(x_0\\to z_0\) with a frozen VAE encoder, diffuse \(z\), decode at the end. Text: condition on a CLIP (or T5) vector. CFG scale \(s\) sharpens the condition.
**Why.** Pixels are huge. Latent cells are fewer (CS231N: on the order of \(12\\times\) fewer in the Stable Diffusion cartoon). Text needs a condition or you sample generic images.
**Architecture.** VAE enc/dec (frozen) + denoiser on \(z_t\) + text encoder. CFG: two forwards, \(\\hat{\\varepsilon}=\\varepsilon_u+s(\\varepsilon_c-\\varepsilon_u)\).
**How.** \(s=1\) is still conditional (not “off”). \(s=0\) is the uncond branch. High \(s\): sharper, less diverse.
**Formula.** \(\\hat{\\varepsilon}_\\theta=\\varepsilon_\\theta(z_t,t,\\emptyset)+s\\big(\\varepsilon_\\theta(z_t,t,c)-\\varepsilon_\\theta(z_t,t,\\emptyset)\\big)\).
**Tradeoffs.** + Cheaper than pixel DDPM, steerable with text. − VAE artifacts; CFG is a quality–diversity knob; still many reverse steps.
""",
    "chain-of-thought": """
**First time this method appears.** **Chain-of-thought (CoT)** is writing **steps** before the answer. It is a prompt / decoding choice, not a new net.

**What.** Direct: “What is \(17\\times 24\)?” CoT: “Show your work, then the number.” Few-shot: paste worked traces. Zero-shot: *Let’s think step by step.*
**Why.** Extra tokens are extra test-time compute. Multi-hop arithmetic can use the tape. Weights do not change.
**Architecture.** Same LM. Longer generation. Parse a final boxed answer separately from the trace (note 13.3).
**How.** Freeze the instruction and decoding settings. Temperature 0 is one greedy chain, not a vote (13.2).
**Formula.** Still \(\\prod_t p(y_t\\mid y_{<t},\\text{prompt})\); the prompt asks for steps. No new parameters.
**Tradeoffs.** + Helps multi-hop. − Hurts one-hop lookup; latency/cost; fluent wrong algebra (faithfulness next). Not retrieval or tools.
""",
    "self-consistency-tot": """
**First time these methods appear.** **Self-consistency (SC)** is majority vote over several CoT traces. **Tree-of-Thoughts (ToT)** is **search** among partial thoughts, not i.i.d. samples.

**What.** SC: sample \(k\) traces (temperature \(>0\)), parse answers, vote. ToT: expand nodes, **score**, prune, expand again.
**Why.** One CoT is noisy. Voting on the **answer** (not the wording) lifts GSM8K-style math in the CS224N L12 figure (~+17.9 pp in that citation). ToT helps when you need a tree, not \(k\) independent tapes.
**Architecture.** SC: decoder + parser + vote. ToT: a frontier of partial strings + a scorer (LM or checker) + beam/DFS.
**How.** Temperature 0, \(k=3\) is **not** SC (identical greedy traces). Vote on the parsed number.
**Formula.** SC: \(\\hat{y}=\\mathrm{mode}\\{\\mathrm{parse}(\\tau_1),\\ldots,\\mathrm{parse}(\\tau_k)\\}\). ToT has no single loss; it is search.
**Tradeoffs.** + SC is simple. − \(k\\times\) cost; shared bugs survive the vote; ToT needs a scorer (math not in this hour); ReAct (14.2) calls tools instead of searching thoughts.
""",
    "faithfulness": """
**First time this evaluation appears.** **Faithfulness** asks whether the **steps caused** the answer, not whether the box is lucky.

**What.** Lucky win: last step says 52, box says 42, gold is 42. Accuracy can pass while the trace is a lie. Process vs outcome (CS224N L13).
**Why.** CoT and SC can look careful and still be unfaithful. A project that “shows work” must check the work.
**Architecture.** No new net. A checker: parse intermediates vs the box. Optional process reward (score steps), vs outcome-only.
**How.** Lab 13 flags the 52→42 row. Report accuracy **and** faithful-among-wins.
**Formula.** Cartoon: \(\\mathrm{F}=\\#\{\\text{wins with consistent trace}\\}/\\#\{\\text{wins}\}\). Accuracy alone is not \(F\).
**Tradeoffs.** + Catches theater. − Checkers can be wrong; humans are slow; process rewards are extra training (not this lab).
""",
}


def insert_block(text: str, block: str) -> str:
    if any(s in text for s in SKIP_IF):
        return text
    i = text.find("\n## ")
    if i < 0:
        return text
    return text[:i] + "\n" + block.strip() + "\n" + text[i:]


def main() -> None:
    n_ok = n_skip = 0
    for slug, block in BLOCKS.items():
        path = NOTES / f"{slug}.md"
        if not path.exists():
            print("missing", slug)
            continue
        old = path.read_text(encoding="utf-8")
        new = insert_block(old, block)
        if new == old:
            print("skip", slug)
            n_skip += 1
            continue
        path.write_text(new, encoding="utf-8", newline="\n")
        print("patched", slug)
        n_ok += 1
    print(f"done patched={n_ok} skipped={n_skip}")


if __name__ == "__main__":
    main()
