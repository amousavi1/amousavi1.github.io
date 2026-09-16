These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

Module 2 leaves pure text. **Multimodal** systems see more than one stream: image and caption, video and audio, a PDF’s pixels and its words. The five jobs are **representation, alignment, fusion, translation, co-learning** (Baltrušaitis et al.). Complementary signal (the label says flammable; the photo does not) and redundant signal (lips plus audio).

If you only train on text, you cannot answer “what is in this photo?” without an image tower or a captioner. That is why Weeks 4–5 exist.

---

> **First time this method appears.** **Multimodal learning** is more than “glue an image to a caption.”
>
> **What.** Five jobs (Baltrušaitis et al.): represent, align, fuse, translate, co-learn. A model can score a pair (CLIP) without decoding a sentence.
> **Why.** Pixels, text, and audio are different sensors. Concatenation is one fusion; it is not the only job.
> **Architecture.** Separate encoders per modality, then a fuse (concat, add, or cross-attention) or a score (cosine).
> **How.** Pick the job first. Retrieval needs a score. Captioning needs a decoder. Classification can be a linear head on a frozen encoder.
> **Formula.** Coordinated: \(s(i,t)=\cos(f(i),g(t))\). Joint concat: \([f(i);g(t)]\,W\).
> **Tradeoffs.** + You can reuse a frozen encoder. − Concat grows width; alignment needs paired data; “multimodal” without naming the job is not a project.
>
## 1. Five jobs, not one architecture

![Represent, align, fuse, translate, co-learn](files/data-643/graphics/4.1-multimodal-foundations/five-challenges.png)

| Job | Question | This course |
| --- | -------- | ----------- |
| Represent | One vector, or two towers? | Joint vs coordinated |
| Align | Which region matches which phrase? | Attention, or one cosine on the whole pair |
| Fuse | When do you mix features? | Early / late / cross-attention |
| Translate | Map one stream into another? | Captioning (BLIP), not CLIP |
| Co-learn | Can a rich stream help a poor one? | Zero-shot in 4.3 |

Translation is not fusion. Captioning **maps** image \(\to\) text. CLIP **scores** image \(\leftrightarrow\) text. If your demo must output a sentence, you need a decoder. If it must search a gallery, you need two towers and a cosine.

A detector that puts a box on “the red mug” is alignment at **region** level. A single cosine on the whole image vs the whole caption is alignment at **instance** level. Know which one your project needs.

---

## 2. Joint versus coordinated

**Joint:** mash the streams into **one** vector (early fusion, a concatenating MLP). Missing a modality at test time hurts.

**Coordinated:** keep a tower per modality, then pull the towers together with a similarity (CLIP is this; canonical correlation analysis is another coordinated family). You can query with either side.

![Joint fusion versus coordinated towers](files/data-643/graphics/4.1-multimodal-foundations/joint-coord.png)

On the board: two arrows that you **add** (joint) vs two arrows that you **dot** (coordinated). CLIP never concatenates pixels with token ids during pretraining; it only scores pairs.

We do not derive Deep CCA. The slogan is enough: a coordination **loss**, not a concatenating layer.

---

## 3. Teaching this note

**~16 minutes.** Five-job table, then joint vs coordinated with the 2-D cosine example. Play Yannic Kilcher CLIP **4:40–14:40** (two towers as a coordinated space). Zero-shot details wait for 4.3; captioning waits for BLIP.

---

## 4. Worked example

Image vector \(\boldsymbol{v}=\begin{bmatrix}1\\0\end{bmatrix}\). Matching caption \(\boldsymbol{t}_{+}=\begin{bmatrix}0.8\\0.2\end{bmatrix}\), other caption \(\boldsymbol{t}_{-}=\begin{bmatrix}0\\1\end{bmatrix}\).

\[
\cos(\boldsymbol{v},\boldsymbol{t}_{+})=0.8/\sqrt{0.68}\approx 0.97,\qquad
\cos(\boldsymbol{v},\boldsymbol{t}_{-})=0.
\]

![Match versus mismatch](files/data-643/graphics/4.1-multimodal-foundations/cosine-numeric.png)

Coordinated retrieval: rank captions by cosine. Joint fusion: concat(\(\boldsymbol{v},\boldsymbol{t}\)) is 4-D; you need **both** at test time, and a typed query with no image has the wrong shape.

If the image is missing, a joint MLP trained on concatenations cannot score the text alone unless you trained a special “image dropout” path. A coordinated text tower still embeds the query.

---

## 5. Where students get stuck

- Concatenating then calling it CLIP.
- Assuming a joint model can take a text-only query at test time.
- Mixing alignment (what matches what) with fusion (when you mix features) with translation (when you generate the other stream).

---

## 6. Video

Watch [Yannic Kilcher: OpenAI CLIP, Connecting Text and Images](https://www.youtube.com/watch?v=T9XSU0pKX2E).

Play **4:40–14:40**. Pause when the two encoders emit vectors in one space, and when a cosine (not a concatenating MLP) is the interaction. That is coordinated representation.

---

## 7. Practice

1. Your app must search photos with a typed query. Joint or coordinated? Why?

2. Give one example of alignment that is not “the whole image vs the whole caption.”

3. What breaks if a joint model never saw audio-only examples and you drop the image at test time?

4. Compute \(\cos(\begin{bmatrix}3\\4\end{bmatrix},\begin{bmatrix}4\\3\end{bmatrix})\). If you fuse by concatenation instead, what is the dimension of concat(\(\boldsymbol{u},\boldsymbol{v}\))?

5. Two images \(\boldsymbol{v}_1=\begin{bmatrix}1\\0\end{bmatrix}\), \(\boldsymbol{v}_2=\begin{bmatrix}0\\1\end{bmatrix}\) and one query \(\boldsymbol{q}=\begin{bmatrix}0.6\\0.8\end{bmatrix}\). Which image ranks first by cosine?

6. Captioning versus CLIP, in one sentence each: which job from the five-job table?

7. Co-learning: English captions are plentiful, labels in another language are not. What is the shared stream that lets the rich side help the poor side?
