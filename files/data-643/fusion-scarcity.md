These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

**Fusion** is when you combine streams. **Scarcity** is why you often cannot train the fused model the way you trained CLIP: paired audio–video–text is rarer than text alone. Note **4.1** introduced joint versus coordinated. This note is **fusion**: early, late, and cross-attention, then the data pyramid. Lab 6 will concat versus add two vectors so you feel the shape change.

---

## 1. What fusion and data scarcity are

**Fusion** is how modalities meet. **Scarcity** is that paired audio/text/video is smaller than text.

**Early:** concatenate (or add) raw features, then one backbone. Cheap at inference if every modality is always there. Missing a stream at test time hurts, unless you trained dropouts.

**Late:** a model per modality, combine decisions (average logits, a small MLP on the scores). Each expert can train on its own data. You lose fine alignment (which word went with which beep).

**Cross-attention (hybrid):** queries from one stream, keys and values from another. Whisper’s decoder already does this for audio \(\to\) text. A video LM does it for frames \(\to\) tokens. This is the default when you want alignment, not just a bag of scores.

![Early, late, and cross-attention fusion](files/data-643/graphics/6.3-fusion-scarcity/fusion.png)

CLIP-style **two towers** are a late/coordinated baseline: you never concatenate pixels with token ids; you compare two vectors. Naming “multimodal” does not name the fusion. Write early, late, or cross-attention, and which loss sees both streams.

Plenty of **unpaired** text, plenty of unlabeled audio, fewer **paired** spectrogram–transcript rows, still fewer labeled tasks (emotion, medical, courtroom diarization). That mismatch is the scarcity half of the note.

---

## 2. Why we use it

Concat is the student default and grows width. Missing a modality at test time breaks naive concat. Add looks similar until the widths differ. Cross-attention is heavier and actually aligns tokens, which is what you want for captioning or transcription.

The data reason is the pyramid. Pretrain the towers where the data is thick; fuse or fine-tune where it is thin. Frozen CLIP or Whisper features plus a small fusion head is a legal project design. Training a new joint stack from 800 paired clips is usually not.

![More unpaired data than paired, than labeled tasks](files/data-643/graphics/6.3-fusion-scarcity/scarcity.png)

Co-learning (note **4.1**): the rich modality teaches the poor one. Write the counts in a report: unpaired hours, paired hours, labeled task rows. “We fused audio and video” without those numbers is incomplete.

A missing-modality plan is part of fusion, not an afterthought. Early concat with no dropout is a **joint** model that assumes every stream is present. Late towers can abstain: if audio is missing, skip that cosine. Cross-attention can mask a whole key set. Name which of those you trained.

---

## 3. Architecture

Draw two towers, then pick concat / add / cross-attention.

![Concat versus add](files/data-643/graphics/6.3-fusion-scarcity/concat-add.png)

Lab 6 will concat versus add two vectors so you feel the shape change. Concat grows \(d\); add needs a shared dimension and assumes the axes already mean the same thing.

- **Concat** \([u;v]\) is legal for any pair of widths. The next linear layer sees \(d_u+d_v\).
- **Add** \(u+v\) needs \(d_u=d_v\). If vision is 256-D and audio is 64-D, map vision first.
- **Late (CLIP-style)** keeps both vectors and compares each to a query. No concatenated blob.
- **Cross-attention** is a map over tokens, not one number. Cosine is not cross-attention.

The data pyramid sits under the picture: lots of unpaired text, less paired audio/video, least labeled task rows. Architecture choices that ignore the pyramid overfit the thin layer.

---

## 4. How it works, step by step

Lab 6: concat vs add on toy vectors. Project: name the fuse and what you do if audio is missing.

1. **Encode each stream** with its own tower (or a shared stem if you truly have early raw concat).
2. **Pick the fuse.** Concat or add at feature level; average logits at decision level; or let text queries attend to spectrogram keys.
3. **Name the missing-modality plan.** Replace a missing vector by 0 only if you trained that dropout. Otherwise skip the tower.
4. **Name the loss.** InfoNCE on tower outputs sees both streams **as vectors**. A captioning CE loss with cross-attention sees tokens aligned to frames. Averaging two classifiers’ logits sees neither alignment.
5. **Respect the pyramid.** Pretrain or freeze where hours are plentiful; train the small head where labels are scarce.

If the microphone dies, early fusion with no dropout has no legal input. Late fusion can still use the camera.

---

## 5. Mathematical formulas

Concat stacks features:

\[
[u;v]\in\mathbb{R}^{d_u+d_v}.
\]

Add needs matching width: \(u+v\) only if \(d_u=d_v\). Cross-attention from stream \(u\) into stream \(v\) is the usual scaled dot product:

\[
\operatorname{softmax}\bigl(Q_u K_v^{\top}/\sqrt{d}\bigr)V_v.
\]

Parameter check, ignore bias. Audio \(d_a=64\), vision \(d_v=256\):

- map vision into 64-D so you can **add**: \(W_v\in\mathbb{R}^{64\times 256}\) has \(16{,}384\) weights;
- **concat** then map to 64-D: \(W\in\mathbb{R}^{64\times 320}\) has \(20{,}480\) weights.

---

## 6. Positive points and negative points

**Positive.**

- Cross-attention can attend to a spectrogram while generating text (Whisper already does this).
- Late towers can train on each modality’s own data and abstain when a stream is missing.
- Frozen CLIP or Whisper plus a small fusion head is a legal design when paired rows are scarce.

**Negative.**

- Concat grows width and fails if a modality is missing and you never trained dropout.
- Add is illegal until the widths match; the axes still have to mean the same thing.
- Two-tower cosine is not cross-attention; you did not align a pixel with a spectrogram bin.
- Training early fusion on a tiny paired set because “multimodal needs joint data” usually destroys the pretrained towers.

**When not to.** If you only have late fusion, do not claim cross-modal alignment. If paired data is scarce, freeze the thick tower.

---

## 7. What to write in a report

Name the fusion, the missing-modality plan, and which loss sees both streams. If you only have late fusion, do not claim cross-modal alignment. If paired data is scarce, say so and justify freezing a tower.

Loss check: InfoNCE on tower outputs sees both streams **as vectors**. A captioning CE loss with cross-attention sees tokens aligned to frames. Averaging two classifiers’ logits sees neither alignment. Use the word that matches the loss.

---

## 8. Teaching this note

About **30 minutes** at the board: three fusion sketches, concat vs add with dimensions, then the pyramid with made-up counts. Play the CLIP two-tower segment as the **late fusion / coordinated** baseline (~10 min). Lab 6 section 3 is the tiny concat/add; do not turn this lecture into the lab.

Write \(128+128=256\) vs \(128+128\) illegal add. If the room cannot say which linear map you need to add a 256-D vision vector into 64-D audio, redo that minute.

---

## 9. Worked example

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

## 10. Where students get stuck

- Saying “add is like concat” because both “combine.” Shapes and missing-modality behavior differ.
- Calling two-tower cosine **cross-attention**. Cosine is one number; cross-attention is a map over tokens.
- Planning to train early fusion on a tiny paired set because “multimodal needs joint data.” Freeze the thick tower.

---

## 11. Video

[Yannic Kilcher — OpenAI CLIP, Connecting Text and Images](https://www.youtube.com/watch?v=T9XSU0pKX2E). Play the **two-tower** setup (roughly the first 10–15 min). Pause on the image tower and text tower: that is **late / coordinated fusion**, the baseline for this note. Early concat and cross-attention stay on the board.

---

## 12. Practice

1. Your app must work when the microphone fails but the camera works. Early fusion with no dropout, or late fusion? Why?

2. Why does add fusion require the same vector width, while concat does not?

3. Where on the pyramid would you pretrain Whisper, and where would you train a courtroom speaker-ID head?

4. Audio \(d_a=64\), vision \(d_v=256\). How many parameters is a linear map that **adds** them in 64-D (ignore bias)? How many is a concat then a map to 64-D?

5. You average CLIP-style cosines from audio and from video against one caption. Is that early, late, or cross-attention? What alignment did you **not** learn?
