These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

**Fusion** is when you combine streams. **Scarcity** is why you often cannot train the fused model the way you trained CLIP: paired audio–video–text is rarer than text alone. Note **4.1** introduced joint versus coordinated; this note is the practical menu.

---

## 1. Three places to fuse

**Early:** concatenate (or add) raw features, then one backbone. Cheap at inference if every modality is always there. Missing a stream at test time hurts, unless you trained dropouts.

**Late:** a model per modality, combine decisions (average logits, a small MLP on the scores). Each expert can train on its own data. You lose fine alignment (which word went with which beep).

**Cross-attention (hybrid):** queries from one stream, keys and values from another. Whisper’s decoder already does this for audio \(\to\) text. A video LM does it for frames \(\to\) tokens. This is the default when you want alignment, not just a bag of scores.

![Early, late, and cross-attention fusion](files/data-643/graphics/6.3-fusion-scarcity/fusion.png)

Lab 6 will concat versus add two vectors so you feel the shape change. Concat grows \(d\); add needs a shared dimension and assumes the axes already mean the same thing.

---

## 2. The data pyramid

Plenty of **unpaired** text, plenty of unlabeled audio, fewer **paired** spectrogram–transcript rows, still fewer labeled tasks (emotion, medical, courtroom diarization). Pretrain the towers where the data is thick; fuse or fine-tune where it is thin.

![More unpaired data than paired, than labeled tasks](files/data-643/graphics/6.3-fusion-scarcity/scarcity.png)

Co-learning (note **4.1**): the rich modality teaches the poor one. Frozen CLIP or Whisper features plus a small fusion head is a legal project design. Training a new joint stack from 800 paired clips is usually not.

---

## 3. What to write in a report

Name the fusion, the missing-modality plan, and which loss sees both streams. If you only have late fusion, do not claim cross-modal alignment. If paired data is scarce, say so and justify freezing a tower.

---

## 4. Practice

1. Your app must work when the microphone fails but the camera works. Early fusion with no dropout, or late fusion? Why?

2. Why does add fusion require the same vector width, while concat does not?

3. Where on the pyramid would you pretrain Whisper, and where would you train a courtroom speaker-ID head?
