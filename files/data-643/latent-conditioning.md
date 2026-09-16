These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

Pixel-space diffusion on \(256\times 256\) RGB is expensive. **Latent diffusion** (Rombach et al.) denoises in a compressed space. **Text** enters as a condition, usually from a frozen CLIP text tower (Week 5). By the end you should be able to count latent cells against pixels, write classifier-free guidance, and say what \(s=1\) is not.

---

## 1. What latent diffusion and classifier-free guidance are

**Latent diffusion** denoises in a **VAE latent**, not in pixels. A pretrained encoder \(E\) maps an image to \(\boldsymbol{z}_0=E(\boldsymbol{x})\). You run the forward process of note **12.1** on \(\boldsymbol{z}\), not on pixels. A decoder \(D_{\mathrm{VAE}}\) turns the final latent back into an image. Training the U-Net on latents is cheaper; the VAE already threw away some high-frequency detail.

**Classifier-free guidance (CFG)** is how you steer that denoiser with a caption. You train one net with and without the text, then at sample time mix a conditional noise prediction \(\varepsilon_c\) with an unconditional prediction \(\varepsilon_u\). Scale \(s\) sharpens the condition. \(s=1\) is still conditional (it is just the conditional net). \(s=0\) is the uncond branch. High \(s\) is sharper and less diverse.

Text is a CLIP (or T5) vector. CLIP scores pairs; it does not decode a caption (note **5.2**). Here you only need the **text** embedding as a handle. You want \(p(\boldsymbol{x}\mid\text{caption})\), not an unconditional generator.

---

## 2. Why we use it

Pixels are huge. Latent cells are fewer (on the order of \(12\times\) fewer in the classroom cartoon, about \(48\times\) on Stable Diffusion’s public \(64\times 64\times 4\) for \(512^2\)). Fifty reverse steps on the small tensor are cheaper than fifty steps on pixels.

Text needs a condition or you sample generic images. Concatenating a CLIP vector, or using **cross-attention** so latent tokens query text tokens, is how the caption enters the U-Net. CFG exists because a single conditional prediction is often too mild: extrapolating away from the unconditioned guess is a cheap way to raise prompt match, at the cost of variety.

Conditioning does not remove Week 5’s bias story: the same CLIP geometry is in the loop.

---

## 3. Architecture

Three frozen or trained pieces sit around the denoiser you already know.

1. **VAE encoder / decoder.** Frozen at diffusion-training time in the usual recipe. Encode \(x_0\to z_0\), diffuse \(z\), decode at the end.
2. **Denoiser on \(z_t\).** U-Net or DiT, with a time embedding, now also taking a condition \(c\).
3. **Text encoder.** CLIP’s text tower (note **5.1**) or T5. Inject \(c\) by concatenating it to the timestep embedding, or by **cross-attention**.

![Encode, denoise a latent, decode; text as a side input](files/data-643/graphics/12.3-latent-conditioning/ldm.png)

Stable Diffusion is this picture plus a big text-conditioned U-Net. The idea is the same at homework scale: compress, denoise, decode.

Typical sizes to say out loud: an image \(512\times 512\times 3\) becomes a latent like \(64\times 64\times 4\). You pay diffusion steps on the small tensor. A classroom setting is \(D=8\), \(C=16\): \(256\times 256\times 3=196{,}608\) numbers versus \(32\times 32\times 16=16{,}384\) (about \(12\times\) fewer). Stable Diffusion’s public \(64\times 64\times 4\) on \(512^2\) is about \(48\times\). Denoise the small tensor.

![Pixel cells versus latent cells](files/data-643/graphics/12.3-latent-conditioning/latent-count.png)

Modern LDM pipelines can stack a VAE, a GAN (for the decoder), and diffusion. DiT exists. This hour is the VAE-latent picture, not a transformer-block homework. CFG is two forwards at sample time, then a mix: \(\hat{\varepsilon}=\varepsilon_u+s(\varepsilon_c-\varepsilon_u)\).

---

## 4. How it works, step by step

**Latent path.**

1. Encode the image: \(\boldsymbol{z}_0=E(\boldsymbol{x})\).
2. Run the forward noising of note **12.1** on \(\boldsymbol{z}\), train the reverse of note **12.2** on \(\boldsymbol{z}_t\), conditioned on \(c\) when a caption is present.
3. At sample time, start from noise in latent space, walk the reverse chain, decode \(\hat{\boldsymbol{x}}=D_{\mathrm{VAE}}(\boldsymbol{z}_0)\).

**Conditioning.** Encode the caption with CLIP’s text tower. During training, **randomly drop** the text so one net is both conditional and unconditional (the empty prompt \(\varnothing\)).

**Guidance at sample time.**

1. Run the net twice (or batch the two): \(\varepsilon_u=\varepsilon_\theta(z_t,t,\varnothing)\) and \(\varepsilon_c=\varepsilon_\theta(z_t,t,c)\).
2. Mix with scale \(s\): \(\hat{\varepsilon}=\varepsilon_u+s(\varepsilon_c-\varepsilon_u)\).
3. Plug \(\hat{\varepsilon}\) into the reverse-step mean from note **12.2**.

\(s=1\) recovers \(\varepsilon_c\): still conditional, not “off.” \(s>1\) **extrapolates** away from the unconditioned guess. A huge \(s\) can look like a poster of the prompt and still miss modes (Week 11’s coverage lesson, now in prompt space). Report \(s\).

The lab for this week is still 2-D denoising from notes **12.1–12.2**. This note is the picture that products use; you do not train Stable Diffusion here.

---

## 5. Mathematical formulas

Classifier-free guidance mixes two noise predictions:

\[
\hat{\boldsymbol{\varepsilon}}_\theta
=
\boldsymbol{\varepsilon}_\theta(\boldsymbol{z}_t,t,\varnothing)
+
s\bigl(
\boldsymbol{\varepsilon}_\theta(\boldsymbol{z}_t,t,\boldsymbol{c})
-
\boldsymbol{\varepsilon}_\theta(\boldsymbol{z}_t,t,\varnothing)
\bigr).
\]

At \(s=1\), \(\hat{\varepsilon}_\theta=\varepsilon_\theta(z_t,t,c)\). At \(s=0\), you are on the unconditional branch. The latent forward process is the same Gaussian jump as note **12.1**, with \(z\) in place of \(x\).

---

## 6. Positive points and negative points

**Positive.**

- Denoising a latent is cheaper than pixel DDPM by a large constant (classroom \(\sim 12\times\), public SD \(\sim 48\times\)).
- A frozen CLIP text tower is enough to steer generation without decoding a caption.
- CFG is one scalar \(s\) that raises prompt match without training a separate classifier.
- Randomly dropping text in training gives you both branches from one net.

**Negative.**

- The VAE throws away high-frequency detail; decode artifacts are part of the method.
- CFG is a quality–diversity knob: high \(s\) sharpens and washes out variety.
- You still pay many reverse steps, now twice per step if you run both branches.
- CLIP’s image tower is for scoring pairs, not for sampling; fine-tuning it at sample time is the wrong tower.

**When not to.** Unconditional 2-D denoising (Lab 12) does not need a VAE or CFG. A task that only needs a CLIP similarity score does not need a decoder.

---

## 7. What to measure

Text-to-image is not “the picture looks nice.” Report a prompt-alignment score (CLIP cosine of image vs text), a coverage or diversity check, and a failure case (wrong count, wrong object, reading text in the image). Conditioning does not remove Week 5’s bias story: the same CLIP geometry is in the loop.

---

## 8. Teaching this note

About **35 minutes** at the board, then **~12 minutes** of selected video from the first 45 minutes (do not play the five-hour coding rest).

- **0–12 min.** Why latents: VAE encode / denoise / decode. Count pixels vs latent cells.
- **12–22 min.** CLIP text tower as \(c\). Cross-attention in one sentence.
- **22–33 min.** Classifier-free guidance with numbers. Diversity vs prompt match.
- **Then** play Umar Jamil Stable Diffusion **4:30–12:07** (what SD is; forward/reverse in this stack) and **22:20–31:00** (CFG). Optional 31:00–39:54 (CLIP + VAE + text-to-image) if time. Stop by **45:00**.

---

## 9. Worked example

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

![CFG scale \(s=1,3,7.5\) on a scalar pair](files/data-643/graphics/12.3-latent-conditioning/cfg-scale.png)

Randomly **drop** the text in training so one net is both conditional and unconditional. Two forwards at sample time, then mix with \(s\).

---

## 10. Where students get stuck

- Fine-tuning CLIP’s image tower at sample time. Text-to-image needs the **text** tower (and a VAE decoder). The image tower is for scoring pairs, not for sampling.
- Calling \(s=1\) “no text.” \(s=1\) is still conditional; the empty prompt \(\varnothing\) is the other call.
- Measuring only FID or only “looks nice,” with no prompt-alignment number and no failure case.

---

## 11. Video

Watch [Umar Jamil, Coding Stable Diffusion from scratch in PyTorch](https://www.youtube.com/watch?v=ZBKpAp_6TGI), **0:00–45:00** assigned, with in-class pauses at **4:30–12:07** (what Stable Diffusion is; forward/reverse) and **22:20–39:54** (classifier-free guidance, CLIP, VAE, text-to-image).

Do not start the coding chapters (VAE implementation from 44:30 onward) in this lecture. The board is the picture; the lab is still 2-D denoising from notes **12.1–12.2**.

---

## 12. Practice

1. Why denoise latents instead of pixels if you already have a VAE?

2. CLIP’s image tower is optional at sample time for text-to-image. Which CLIP tower is not?

3. Guidance scale \(s=1\) versus \(s=12\): what do you expect to happen to prompt match and to variety?

4. \(\varepsilon_{\text{uncond}}=1.0\), \(\varepsilon_{\text{cond}}=0.4\), \(s=5\). Compute \(\hat{\varepsilon}\).

5. A \(256\times 256\times 3\) image vs an \(32\times 32\times 4\) latent: how many numbers in each, and what is the ratio (image / latent)?
