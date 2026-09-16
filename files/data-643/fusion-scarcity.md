These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

**Fusion** is when you combine streams. **Scarcity** is why you often cannot train the fused model the way you trained CLIP: paired audio–video–text is rarer than text alone. Note **4.1** introduced joint versus coordinated (CMU 11-777). This note is 11-777’s **fusion** lecture in classroom form: early, late, and cross-attention, then the data pyramid.

---

## 1. Three places to fuse

**Early:** concatenate (or add) raw features, then one backbone. Cheap at inference if every modality is always there. Missing a stream at test time hurts, unless you trained dropouts.

**Late:** a model per modality, combine decisions (average logits, a small MLP on the scores). Each expert can train on its own data. You lose fine alignment (which word went with which beep).

**Cross-attention (hybrid):** queries from one stream, keys and values from another. Whisper’s decoder already does this for audio \(\to\) text. A video LM does it for frames \(\to\) tokens. This is the default when you want alignment, not just a bag of scores.

![Early, late, and cross-attention fusion](files/data-643/graphics/6.3-fusion-scarcity/fusion.png)

Lab 6 will concat versus add two vectors so you feel the shape change. Concat grows \(d\); add needs a shared dimension and assumes the axes already mean the same thing.

![Concat versus add](files/data-643/graphics/6.3-fusion-scarcity/concat-add.png)

CLIP-style **two towers** are a late/coordinated baseline: you never concatenate pixels with token ids; you compare two vectors. That is the video’s job this hour.

11-777’s warning, in our words: naming “multimodal” does not name the fusion. Write early, late, or cross-attention, and which loss sees both streams.

---

## 2. The data pyramid

Plenty of **unpaired** text, plenty of unlabeled audio, fewer **paired** spectrogram–transcript rows, still fewer labeled tasks (emotion, medical, courtroom diarization). Pretrain the towers where the data is thick; fuse or fine-tune where it is thin.

![More unpaired data than paired, than labeled tasks](files/data-643/graphics/6.3-fusion-scarcity/scarcity.png)

Co-learning (note **4.1**): the rich modality teaches the poor one. Frozen CLIP or Whisper features plus a small fusion head is a legal project design. Training a new joint stack from 800 paired clips is usually not.

Write the counts in a report: unpaired hours, paired hours, labeled task rows. “We fused audio and video” without those numbers is incomplete.

A missing-modality plan is part of fusion, not an afterthought. Early concat with no dropout is a **joint** model that assumes every stream is present. Late towers can abstain: if audio is missing, skip that cosine. Cross-attention can mask a whole key set. Name which of those you trained.

---

## 3. What to write in a report

Name the fusion, the missing-modality plan, and which loss sees both streams. If you only have late fusion, do not claim cross-modal alignment. If paired data is scarce, say so and justify freezing a tower.

Loss check: InfoNCE on tower outputs sees both streams **as vectors**. A captioning CE loss with cross-attention sees tokens aligned to frames. Averaging two classifiers’ logits sees neither alignment. Use the word that matches the loss.

---

## 4. Teaching this note

About **30 minutes** at the board: three fusion sketches, concat vs add with dimensions, then the pyramid with made-up counts. Play the CLIP two-tower segment as the **late fusion / coordinated** baseline (~10 min). Lab 6 section 3 is the tiny concat/add; do not turn this lecture into the lab.

Write \(128+128=256\) vs \(128+128\) illegal add. If the room cannot say which linear map you need to add a 256-D vision vector into 64-D audio, redo that minute.

---

## 5. Worked example

Audio encoder emits \(a\in\mathbb{R}^{128}\), image encoder emits \(v\in\mathbb{R}^{128}\).

- **Concat:** \([a;v]\in\mathbb{R}^{256}\). A linear head is \(W\in\mathbb{R}^{c\times 256}\). If the microphone dies you have no 256-vector unless you trained a missing-audio dropout (replace \(a\) by \(0\), or a learned mask token).
- **Add:** \(a+v\in\mathbb{R}^{128}\). Illegal if \(a\in\mathbb{R}^{128}\) and \(v\in\mathbb{R}^{256}\). You would first map \(v\) with \(W_v\in\mathbb{R}^{128\times 256}\).
- **Late (CLIP-style):** keep \(a\) and \(v\), score \(\cos(a,t)\) and \(\cos(v,t)\) against a text query, average the two scores. Each tower can have been pretrained on its own pairs. You did **not** align a pixel with a spectrogram bin.

Pyramid: 10{,}000 h unlabeled audio, 600 h paired transcripts (Whisper-scale is much larger; this is a seminar toy), 400 labeled emotion clips. Pretrain or freeze the audio tower on the 600 h; train the emotion head on 400. Do not train a from-scratch joint net on 400 rows.

CLIP video as baseline: two towers, InfoNCE, no early concat. That is coordinated fusion with a **late** comparison. Cross-attention would be a decoder querying the other stream’s tokens. Three different pictures; one hour.

Parameter check, ignore bias. Audio \(d_a=64\), vision \(d_v=256\):

- map vision into 64-D so you can **add**: \(W_v\in\mathbb{R}^{64\times 256}\) has \(16{,}384\) weights;
- **concat** then map to 64-D: \(W\in\mathbb{R}^{64\times 320}\) has \(20{,}480\) weights.

---

## 6. Where students get stuck

- Saying “add is like concat” because both “combine.” Shapes and missing-modality behavior differ.
- Calling two-tower cosine **cross-attention**. Cosine is one number; cross-attention is a map over tokens.
- Planning to train early fusion on a tiny paired set because “multimodal needs joint data.” Freeze the thick tower.

---

## 7. Video

[Yannic Kilcher — OpenAI CLIP, Connecting Text and Images](https://www.youtube.com/watch?v=T9XSU0pKX2E). Play the **two-tower** setup (roughly the first 10–15 min). Pause on the image tower and text tower: that is **late / coordinated fusion**, the baseline for this note. Early concat and cross-attention stay on the board.

---

## 8. Practice

1. Your app must work when the microphone fails but the camera works. Early fusion with no dropout, or late fusion? Why?

2. Why does add fusion require the same vector width, while concat does not?

3. Where on the pyramid would you pretrain Whisper, and where would you train a courtroom speaker-ID head?

4. Audio \(d_a=64\), vision \(d_v=256\). How many parameters is a linear map that **adds** them in 64-D (ignore bias)? How many is a concat then a map to 64-D?

5. You average CLIP-style cosines from audio and from video against one caption. Is that early, late, or cross-attention? What alignment did you **not** learn?
