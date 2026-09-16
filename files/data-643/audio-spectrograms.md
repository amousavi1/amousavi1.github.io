These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

A waveform is a 1-D list of samples. A **spectrogram** is that list cut into short windows, each turned into a frequency snapshot. Stanford CS224S (L2 acoustic phonetics; L5 “why spectrograms”) is the matching course: once you have a 2-D time–frequency picture, every vision trick from Week 4 (patches, a transformer, CLIP-style towers) applies to audio.

---

> **First time this method appears.** A **spectrogram** is a picture of sound. Models do not eat 16 kHz samples as a raw list.
>
> **What.** STFT: window the waveform, FFT each frame, plot frequency vs time. A **mel** spectrogram warps frequency to a perceptual scale.
> **Why.** Waveforms are long and oscillatory. A 2-D time–frequency map can be patched like a ViT image.
> **Architecture.** Waveform → frames → STFT magnitudes (optionally mel + log) → patch embed → transformer.
> **How.** Lab 6: sine mixture, STFT, patch. Hop length and window are method knobs.
> **Formula.** Frame \(m\): \(X(m,\omega)=\sum_n x[n]w[n-mH]e^{-j\omega n}\). Sequence length ≈ number of frames (or patches of frames).
> **Tradeoffs.** + Shares ViT code. − Phase often dropped; time resolution vs frequency resolution; not yet a transcriber (next note).
>
## 1. Waveforms and the STFT

You record pressure \(x[n]\) at a sampling rate \(f_s\) (16 kHz is a common speech default). A sine of \(f\) hertz is \(x[n]=\sin(2\pi f n/f_s)\). Mixtures add; that is still one stream.

The **short-time Fourier transform (STFT)** windows the signal (Hann, hop \(H\), FFT size \(N\)), then takes a DFT of each frame. The **magnitude spectrogram** \(S(t,f)=|X(t,f)|\) is what you plot. Phase exists, but most audio encoders drop it and keep magnitudes or a **mel** compression of them (log-mel filterbank).

![Waveform next to its spectrogram](files/data-643/graphics/6.1-audio-spectrograms/wave-spec.png)

A tall band that stays put is a steady tone. A sweep that climbs is a chirp. Speech looks like stacked formants that move.

Frame count, without padding, is

\[
T = 1 + \left\lfloor \frac{L-N}{H} \right\rfloor
\]

when the length \(L \ge N\). Hop \(H\) is the time step; \(N\) is the frequency resolution. You cannot make both arbitrarily fine: small \(H\) means more frames (and more tokens later); large \(N\) means narrower Hertz bins and a longer window that smears onsets.

![Sliding windows](files/data-643/graphics/6.1-audio-spectrograms/stft-frames.png)

CS224S’s reason to prefer this over a raw wave: a transformer on 16 kHz samples would see 16{,}000 tokens per second. An STFT with a 25 ms window and a 10 ms hop sees 100 frames per second. Those frames last long enough to see a phoneme, not a single pressure sample.

---

## 2. Spectrograms as images, then as tokens

Treat \(S\) as a single-channel image. A CNN can ingest it. A ViT can **patch** it: tiles of time \(\times\) frequency, flatten, linear map to width \(d\), add positions. Lab 6 does that cut by hand.

![Spectrogram cut into patch tokens](files/data-643/graphics/6.1-audio-spectrograms/spec-patches.png)

Time is not quite space. Adjacent frequency bins are related (harmonics); adjacent frames are related (smooth speech). Positions should know which axis is which. Still, “patch then attend” is the default modern front end.

Non-overlapping \(p\times p\) tiles on an \(F\times T\) grid give \( (F/p)\times(T/p) \) tokens if both axes divide. Remainders are padded or cropped; Lab 6 crops.

---

## 3. What this is not

A spectrogram is not a transcript, a speaker id, or a music tag. Those are **tasks** on top of the tokens. Whisper (note **6.2**) will decode text from this picture. CLAP will embed the picture next to a caption. If your project uses audio, write \(f_s\), window, hop, and whether you used mel or raw STFT. Those choices change the tokens.

Log-mel is a compressive front end: fewer bands than a linear STFT, spaced the way hearing is. It is still a spectrogram. Do not skip the plot; if the 440 Hz band is missing, the rest of the pipeline is theater.

Bin \(k\) of an \(N\)-point FFT sits near \(k\cdot f_s/N\) hertz (real FFT: \(k=0,\ldots,N/2\)). That conversion is how you check Lab 6’s two sines.

---

## 4. Teaching this note

About **35 minutes** at the board in the two-hour week: draw one second of a 440 Hz sine, mark a window of length \(N\) and hop \(H\), count frames, then cut a toy mel grid into patches. Play the STFT video (**~10–12 min**; see Video). Lab 6 (sine mixture, STFT, concat vs add) is studio time after notes **6.2–6.3**, not this block.

---

## 5. Worked example

One second of speech at \(f_s=16\,\mathrm{kHz}\): \(L=16000\) samples. Take \(N=400\), hop \(H=160\). Window \(400/16000=25\,\mathrm{ms}\), hop \(10\,\mathrm{ms}\). Those are **Whisper’s default** front-end numbers (note **6.2**).

\[
T = 1 + \left\lfloor\frac{16000-400}{160}\right\rfloor = 1+97 = 98
\]

frames. Each real FFT has \(N/2+1=201\) bins. A 440 Hz tone sits near bin \(k \approx 440\cdot 400/16000 = 11\).

Double the hop to \(H=320\) and keep \(N\) fixed:

\[
T' = 1 + \left\lfloor\frac{15600}{320}\right\rfloor = 1+48 = 49.
\]

About half as many frames; each frame is twice as far apart in time (20 ms). Frequency bins did not change, because \(N\) did not.

Now patch a log-mel grid of shape \(80\times 400\) with non-overlapping \(16\times 16\) tiles (ignore remainder):

\[
\frac{80}{16}\times\frac{400}{16} = 5\times 25 = 125
\]

tokens. That is the number Lab 6 is practicing in miniature, and the number a Whisper-style encoder would attend over.

---

## 6. Where students get stuck

- Counting **samples** as **frames**. \(L/f_s\) is duration in seconds; \(T\) is how many windows you placed.
- Thinking a larger FFT “hears more of the clip.” It hears a **longer window**, so onsets blur; hop still sets the time grid.
- Patching \(F\times T\) as if it were a square image and forgetting which axis is frequency. Remainders: crop in the lab; do not silently drop a formant band.

---

## 7. Video

[Valerio Velardo — Short-Time Fourier Transform Explained Easily](https://www.youtube.com/watch?v=-Yxj3yfvY-4). Play the STFT / spectrogram walkthrough in class (~10–12 min). Pause when the window slides: that hop is \(H\) in the formula above. Search **“Valerio Velardo Short-Time Fourier Transform”** if you need the rest of the Sound of AI series. The board hour is the frame count and the patch count, not the complex-phase algebra.

---

## 8. Practice

1. You double the hop length and keep \(N\) fixed. What happens to the number of time frames, and to time resolution?

2. Why is a spectrogram a better input to a transformer than the raw waveform at 16 kHz?

3. Count patch tokens for a mel grid of \(80\times 400\) with \(16\times 16\) tiles (ignore remainder).

4. \(f_s=8000\), one second, \(N=256\), hop \(H=128\). How many STFT frames? What Hertz spacing is one FFT bin (\(f_s/N\))?

5. Same clip as (4), but you pad so the last frame is included and \(T=\lceil L/H\rceil\). What is \(T\), and why might a library report that instead of \(1+\lfloor(L-N)/H\rfloor\)?
