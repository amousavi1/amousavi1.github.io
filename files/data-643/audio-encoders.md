These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

Two audio systems you will cite: **Whisper** transcribes (encoder–decoder), **CLAP** retrieves (two towers, like CLIP). Same spectrogram tokens, different heads.

---

## 1. Whisper: listen, then write

Radford et al. (2022). The encoder is a transformer on log-mel spectrogram patches (note **6.1**). The decoder is causal and **cross-attends** to the encoder, like translation in note **3.3**. The output is text, plus special tokens for language, timestamps, and task (transcribe versus translate).

![Whisper encoder on audio, decoder on text](files/data-643/graphics/6.2-audio-encoders/whisper.png)

Pretraining is weakly supervised: a huge pile of audio paired with transcripts from the web, filtered rather than hand-labeled. Multilingual is the point. You do not train this from scratch in the lab; you would load a checkpoint. The architecture is what you need to draw.

---

## 2. CLAP: CLIP, but the image is sound

**CLAP** (Contrastive Language–Audio Pretraining) is coordinated, not joint. An audio encoder (CNN or transformer on the spectrogram) and a text encoder emit vectors in one space. InfoNCE on audio–caption pairs. After training you keep both towers.

![CLAP audio and text towers](files/data-643/graphics/6.2-audio-encoders/clap.png)

Zero-shot tagging: encode `"a dog barking"`, rank clips by cosine. Retrieval both ways. It is not a transcriber. If you need words, use Whisper (or a CTC ASR). If you need “find the clip that matches this sentence,” use CLAP.

---

## 3. Which one in a project

| Need | Model |
| ---- | ----- |
| Transcript, subtitles, timestamps | Whisper |
| Search / zero-shot tags / audio–text retrieval | CLAP |
| Generate a caption in free text | a decoder with an audio encoder (Whisper-like, or a BLIP-style audio LM) |

Fusing audio with vision or text is next (note **6.3**). Do not concatenate a Whisper hidden state into CLIP and call it a paper; say how you aligned the rates and the losses.

---

## 4. Practice

1. Whisper’s decoder is causal. Why can CLAP’s text tower be bidirectional like BERT?

2. You have a gallery of podcast clips and a typed query. Whisper or CLAP? Why?

3. Name one special token Whisper uses that CLIP never needed.
