These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

Module 2 leaves pure text. **Multimodal** systems see more than one stream: image and caption, video and audio, a PDF’s pixels and its words. The hard parts are the same list as Baltrušaitis, Ahuja, and Morency: representation, translation, alignment, fusion, co-learning.

---

## 1. Why more than one stream

A photo of a bottle does not say “flammable.” The label does. A transcript does not show who is speaking; the face does. Complementary signal, and redundant signal (lip motion plus audio). Language models in this course become **conditioned** on other modalities, or retrieve across them.

If you only train on text, you cannot answer “what is in this photo?” without an image tower or a captioner. That is why Weeks 4–5 exist.

---

## 2. Joint versus coordinated

**Joint:** mash the streams into **one** vector (early fusion, a concatenating MLP). Missing a modality at test time hurts.

**Coordinated:** keep a tower per modality, then pull the towers together with a similarity (CLIP is this). You can query with either side.

![Joint fusion versus coordinated towers](files/data-643/graphics/4.1-multimodal-foundations/joint-coord.png)

On the board: two arrows that you **add** (joint) vs two arrows that you **dot** (coordinated). CLIP never concatenates pixels with token ids during pretraining; it only scores pairs.

---

## 3. Alignment and fusion, in slogans

**Alignment:** which region of the image goes with which phrase. Attention is the default modern tool.

**Fusion:** when you combine. Early (features), late (decisions), or hybrid (cross-attention).

**Translation:** captioning, text-to-image, speech-to-text. Week 5’s BLIP is a translation model with a matching loss.

**Zero-shot / co-learning:** use a rich modality to help a poor one. Week **4.3**.

A detector that puts a box on “the red mug” is alignment at region level. A single cosine on the whole image vs the whole caption is alignment at instance level. Know which one your project needs.

Translation is not fusion. Captioning **maps** image \(\to\) text. CLIP **scores** image \(\leftrightarrow\) text. If your demo must output a sentence, you need a decoder (BLIP, Whisper, an LLM). If it must search a gallery, you need two towers and a cosine.

Co-learning: a rich labeled modality (English captions) can supervise a poorer one (a language with few labels) if they share the image. That slogan is Week 4.3’s zero-shot, not a new architecture.

---

## 4. Teaching this note

**30–40 minutes.** Motivate two streams, then spend the block on joint vs coordinated with the 2-D cosine example. Play Yannic Kilcher CLIP **4:40–14:40** (connecting image and text; two towers as a coordinated space). Zero-shot details wait for 4.3; captioning waits for BLIP.

---

## 5. Worked example

Image vector \(\boldsymbol{v}=\begin{bmatrix}1\\0\end{bmatrix}\). Matching caption \(\boldsymbol{t}_{+}=\begin{bmatrix}0.8\\0.2\end{bmatrix}\), other caption \(\boldsymbol{t}_{-}=\begin{bmatrix}0\\1\end{bmatrix}\).

\[
\cos(\boldsymbol{v},\boldsymbol{t}_{+})=0.8/\sqrt{0.68}\approx 0.97,\qquad
\cos(\boldsymbol{v},\boldsymbol{t}_{-})=0.
\]

Coordinated retrieval: rank captions by cosine. Joint fusion: \(\mathrm{concat}(\boldsymbol{v},\boldsymbol{t})\) is 4-D; you need **both** at test time, and a typed query with no image has the wrong shape.

If the image is missing, a joint MLP trained on concatenations cannot score the text alone unless you trained a special “image dropout” path. A coordinated text tower still embeds the query.

---

## 6. Where students get stuck

- Concatenating then calling it CLIP.
- Assuming a joint model can take a text-only query at test time.
- Mixing alignment (what matches what) with fusion (when you mix features).

---

## 7. Video

Watch [Yannic Kilcher: OpenAI CLIP, Connecting Text and Images](https://www.youtube.com/watch?v=T9XSU0pKX2E).

Play **4:40–14:40**. Pause when the two encoders emit vectors in one space, and when a cosine (not a concatenating MLP) is the interaction. That is coordinated representation.

---

## 8. Practice

1. Your app must search photos with a typed query. Joint or coordinated? Why?

2. Give one example of alignment that is not “the whole image vs the whole caption.”

3. What breaks if a joint model never saw audio-only examples and you drop the image at test time?

4. Compute \(\cos(\begin{bmatrix}3\\4\end{bmatrix},\begin{bmatrix}4\\3\end{bmatrix})\). If you fuse by concatenation instead, what is the dimension of \(\mathrm{concat}(\boldsymbol{u},\boldsymbol{v})\)?

5. Two images \(\boldsymbol{v}_1=\begin{bmatrix}1\\0\end{bmatrix}\), \(\boldsymbol{v}_2=\begin{bmatrix}0\\1\end{bmatrix}\) and one query \(\boldsymbol{q}=\begin{bmatrix}0.6\\0.8\end{bmatrix}\). Which image ranks first by cosine?
