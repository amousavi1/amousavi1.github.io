These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

Pixel-space diffusion on \(256\times 256\) RGB is expensive. **Latent diffusion** (Rombach et al.) denoises in a compressed space. **Text** enters as a condition, usually from a frozen CLIP text tower (Week 5).

---

## 1. Diffuse in latent space

A pretrained encoder \(E\) maps an image to \(\boldsymbol{z}_0=E(\boldsymbol{x})\). You run the forward process of note **12.1** on \(\boldsymbol{z}\), not on pixels. A decoder \(D_{\mathrm{VAE}}\) turns the final latent back into an image. Training the U-Net on latents is cheaper; the VAE already threw away some high-frequency detail.

![Encode, denoise a latent, decode; text as a side input](files/data-643/graphics/12.3-latent-conditioning/ldm.png)

Stable Diffusion is this picture plus a big text-conditioned U-Net. The idea is the same at homework scale: compress, denoise, decode.

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

## 4. Practice

1. Why denoise latents instead of pixels if you already have a VAE?

2. CLIP’s image tower is optional at sample time for text-to-image. Which CLIP tower is not?

3. Guidance scale \(s=1\) versus \(s=12\): what do you expect to happen to prompt match and to variety?
