These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

Pixel-space diffusion on \(256\times 256\) RGB is expensive. **Latent diffusion** (Rombach et al.) denoises in a compressed space. **Text** enters as a condition, usually from a frozen CLIP text tower (Week 5).

---

## 1. Diffuse in latent space

A pretrained encoder \(E\) maps an image to \(\boldsymbol{z}_0=E(\boldsymbol{x})\). You run the forward process of note **12.1** on \(\boldsymbol{z}\), not on pixels. A decoder \(D_{\mathrm{VAE}}\) turns the final latent back into an image. Training the U-Net on latents is cheaper; the VAE already threw away some high-frequency detail.

![Encode, denoise a latent, decode; text as a side input](files/data-643/graphics/12.3-latent-conditioning/ldm.png)

Stable Diffusion is this picture plus a big text-conditioned U-Net. The idea is the same at homework scale: compress, denoise, decode.

Typical sizes to say out loud: an image \(512\times 512\times 3\) becomes a latent like \(64\times 64\times 4\). You pay diffusion steps on the small tensor.

---

## 2. Conditioning with CLIP text

You want \(p(\boldsymbol{x}\mid\text{caption})\), not an unconditional generator. Encode the caption with CLIP’s **text** tower (note **5.1**). Inject that vector by:

- concatenating it to the U-Net’s timestep embedding, or
- **cross-attention**: image (or latent) tokens query the text tokens.

Classifier-free guidance trains with and without the text, then at sample time does

\[
\hat{\boldsymbol{\varepsilon}}
=
\boldsymbol{\varepsilon}_\theta(\boldsymbol{z}_t,t,\varnothing)
+
s\bigl(
\boldsymbol{\varepsilon}_\theta(\boldsymbol{z}_t,t,\boldsymbol{c})
-
\boldsymbol{\varepsilon}_\theta(\boldsymbol{z}_t,t,\varnothing)
\bigr).
\]

Scale \(s>1\) sharpens adherence to the prompt and can wash out diversity. Report \(s\).

CLIP scores pairs; it does not decode a caption (note **5.2**). Here you only need the text embedding as a handle.

---

## 3. What to measure

Text-to-image is not “the picture looks nice.” Report a prompt-alignment score (CLIP cosine of image vs text), a coverage or diversity check, and a failure case (wrong count, wrong object, reading text in the image). Conditioning does not remove Week 5’s bias story: the same CLIP geometry is in the loop.

---

## 4. Teaching this note

About **35 minutes** at the board, then **~12 minutes** of selected video from the first 45 minutes (do not play the five-hour coding rest).

- **0–12 min.** Why latents: VAE encode / denoise / decode. Count pixels vs latent cells.
- **12–22 min.** CLIP text tower as \(c\). Cross-attention in one sentence.
- **22–33 min.** Classifier-free guidance with numbers. Diversity vs prompt match.
- **Then** play Umar Jamil Stable Diffusion **4:30–12:07** (what SD is; forward/reverse in this stack) and **22:20–31:00** (CFG). Optional 31:00–39:54 (CLIP + VAE + text-to-image) if time. Stop by **45:00**.

---

## 5. Worked example

**Latent size.** A \(512\times 512\times 3\) image is \(786{,}432\) numbers. A \(64\times 64\times 4\) latent is \(16{,}384\) numbers: about \(48\times\) fewer. Fifty reverse steps on the latent are cheaper than fifty steps on pixels.

**Guidance.** Let the net’s two noise guesses (one scalar, to see the algebra) be \(\varepsilon_\theta(z_t,t,\varnothing)=0.8\) (unconditional) and \(\varepsilon_\theta(z_t,t,c)=0.2\) (with prompt \(c\)). The difference is \(0.2-0.8=-0.6\).

\[
\hat{\varepsilon}
=
0.8+s(-0.6)
=
0.8-0.6s.
\]

| \(s\) | \(\hat{\varepsilon}\) | reading |
| ----- | --------------------- | ------- |
| \(1\) | \(0.2\) | just the conditional net |
| \(3\) | \(-1.0\) | step farther along the prompt direction |
| \(7.5\) | \(-3.7\) | very sharp prompt match; variety usually drops |

\(s=1\) is “use the text-conditioned prediction.” \(s>1\) **extrapolates** away from the unconditioned guess. That is why a huge \(s\) can look like a poster of the prompt and still miss modes (Week 11’s coverage lesson, now in prompt space).

---

## 6. Where students get stuck

- Fine-tuning CLIP’s image tower at sample time. Text-to-image needs the **text** tower (and a VAE decoder). The image tower is for scoring pairs, not for sampling.
- Calling \(s=1\) “no text.” \(s=1\) is still conditional; the empty prompt \(\varnothing\) is the other call.
- Measuring only FID or only “looks nice,” with no prompt-alignment number and no failure case.

---

## 7. Video

Watch [Umar Jamil, Coding Stable Diffusion from scratch in PyTorch](https://www.youtube.com/watch?v=ZBKpAp_6TGI), **0:00–45:00** assigned, with in-class pauses at **4:30–12:07** (what Stable Diffusion is; forward/reverse) and **22:20–39:54** (classifier-free guidance, CLIP, VAE, text-to-image).

Do not start the coding chapters (VAE implementation from 44:30 onward) in this lecture. The board is the picture; the lab is still 2-D denoising from notes **12.1–12.2**.

---

## 8. Practice

1. Why denoise latents instead of pixels if you already have a VAE?

2. CLIP’s image tower is optional at sample time for text-to-image. Which CLIP tower is not?

3. Guidance scale \(s=1\) versus \(s=12\): what do you expect to happen to prompt match and to variety?

4. \(\varepsilon_{\text{uncond}}=1.0\), \(\varepsilon_{\text{cond}}=0.4\), \(s=5\). Compute \(\hat{\varepsilon}\).

5. A \(256\times 256\times 3\) image vs an \(32\times 32\times 4\) latent: how many numbers in each, and what is the ratio (image / latent)?
