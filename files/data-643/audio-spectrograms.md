These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

A waveform is a 1-D list of samples. A **spectrogram** is that list cut into short windows, each turned into a frequency snapshot. Once you have a 2-D time–frequency picture, every vision trick from Week 4 (patches, a transformer, CLIP-style towers) applies to audio.

---

## 1. Waveforms and the STFT

You record pressure \(x[n]\) at a sampling rate \(f_s\) (16 kHz is a common speech default). A sine of \(f\) hertz is \(x[n]=\sin(2\pi f n/f_s)\). Mixtures add; that is still one stream.

The **short-time Fourier transform (STFT)** windows the signal (Hann, hop \(H\), FFT size \(N\)), then takes a DFT of each frame. The **magnitude spectrogram** \(S(t,f)=|X(t,f)|\) is what you plot. Phase exists, but most audio encoders drop it and keep magnitudes or a **mel** compression of them (log-mel filterbank).

![Waveform next to its spectrogram](files/data-643/graphics/6.1-audio-spectrograms/wave-spec.png)

A tall band that stays put is a steady tone. A sweep that climbs is a chirp. Speech looks like stacked formants that move.

---

## 2. Spectrograms as images, then as tokens

Treat \(S\) as a single-channel image. A CNN can ingest it. A ViT can **patch** it: tiles of time \(\times\) frequency, flatten, linear map to width \(d\), add positions. Lab 6 does that cut by hand.

![Spectrogram cut into patch tokens](files/data-643/graphics/6.1-audio-spectrograms/spec-patches.png)

Time is not quite space. Adjacent frequency bins are related (harmonics); adjacent frames are related (smooth speech). Positions should know which axis is which. Still, “patch then attend” is the default modern front end.

---

## 3. What this is not

A spectrogram is not a transcript, a speaker id, or a music tag. Those are **tasks** on top of the tokens. Whisper (note **6.2**) will decode text from this picture. CLAP will embed the picture next to a caption. If your project uses audio, write \(f_s\), window, hop, and whether you used mel or raw STFT. Those choices change the tokens.

Log-mel is a compressive front end: fewer bands than a linear STFT, spaced the way hearing is. It is still a spectrogram. Do not skip the plot; if the 440 Hz band is missing, the rest of the pipeline is theater.

---

## 4. Practice

1. You double the hop length and keep \(N\) fixed. What happens to the number of time frames, and to time resolution?

2. Why is a spectrogram a better input to a transformer than the raw waveform at 16 kHz?

3. Count patch tokens for a mel grid of \(80\times 400\) with \(16\times 16\) tiles (ignore remainder).
