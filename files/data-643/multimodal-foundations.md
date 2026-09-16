These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

Module 2 leaves pure text. **Multimodal** systems see more than one stream: image and caption, video and audio, a PDF’s pixels and its words. Complementary signal (the label says flammable; the photo does not) and redundant signal (lips plus audio) are both useful, and they are not the same job. If you only train on text, you cannot answer “what is in this photo?” without an image tower or a captioner. That is why Weeks 4–5 exist.

---

## 1. What multimodal learning is

**Multimodal learning** is not “glue an image to a caption.” It is a family of jobs on more than one stream of data. Baltrušaitis et al. name five of them: **representation, alignment, fusion, translation, co-learning**. A model can score a pair (CLIP) without ever decoding a sentence. Another model can write a caption (BLIP) without being a good retriever. The word “multimodal” without the job is not a method.

![Represent, align, fuse, translate, co-learn](files/data-643/graphics/4.1-multimodal-foundations/five-challenges.png)

| Job | Question | This course |
| --- | -------- | ----------- |
| Represent | One vector, or two towers? | Joint vs coordinated |
| Align | Which region matches which phrase? | Attention, or one cosine on the whole pair |
| Fuse | When do you mix features? | Early / late / cross-attention |
| Translate | Map one stream into another? | Captioning (BLIP), not CLIP |
| Co-learn | Can a rich stream help a poor one? | Zero-shot in 4.3 |

Translation is not fusion. Captioning **maps** image \(\to\) text. CLIP **scores** image \(\leftrightarrow\) text. If your demo must output a sentence, you need a decoder. If it must search a gallery, you need two towers and a cosine.

A detector that puts a box on “the red mug” is alignment at **region** level. A single cosine on the whole image versus the whole caption is alignment at **instance** level. Know which one your project needs.

---

## 2. Why we use it

Pixels, text, and audio are different sensors. They disagree usefully (complementary) and they agree usefully (redundant). A text-only model cannot look at a photo. An image-only classifier cannot take a typed query. Concatenation is one way to mix features; it is not the only job, and it is a poor default when you will later need to query from one side only.

Three product questions keep coming back.

1. **Search a gallery with words.** You need a score between an image vector and a text vector, not a fused blob.
2. **Write a sentence about an image.** You need translation: a decoder, not a cosine.
3. **A rich stream helping a poor one.** English captions are plentiful; labels in another language, or in a rare medical code, are not. Co-learning is the hope that the rich side teaches the poor side through a shared space.

Week 4.3 will make that last job concrete as zero-shot classification. This note is the map of jobs so you stop calling every image–text demo “CLIP.”

---

## 3. Architecture

There is no single multimodal layer. You pick a **representation** first: joint or coordinated.

**Joint:** mash the streams into **one** vector (early fusion, a concatenating MLP). At train time you always have both sides. At test time, missing a modality hurts, unless you trained a special dropout path. On the board this is two arrows that you **add** or **concat**.

**Coordinated:** keep a tower per modality, then pull the towers together with a similarity (CLIP is this; canonical correlation analysis is another coordinated family). You can query with either side. On the board this is two arrows that you **dot**. CLIP never concatenates pixels with token ids during pretraining; it only scores pairs.

![Joint fusion versus coordinated towers](files/data-643/graphics/4.1-multimodal-foundations/joint-coord.png)

We do not derive Deep CCA. The slogan is enough: a coordination **loss**, not a concatenating layer.

After the towers (or the fused vector) you still have to choose an interaction. Retrieval uses a score such as cosine. Classification can sit a linear head on a frozen encoder. Captioning attaches a decoder. Fusion later in the course (note **6.3**) will name early, late, and cross-attention; this hour you only need to know that concat is one fuse among several.

---

## 4. How it works, step by step

Pick the **job** first. The architecture follows.

1. **Name the streams.** Image and caption, spectrogram and transcript, PDF pixels and words.
2. **Name the output.** A ranked list, a class name, a generated sentence, a box on a region.
3. **Choose joint or coordinated.** Search with a typed query wants coordinated towers. A classifier that always sees both sensors can be joint.
4. **Choose the interaction.** Retrieval needs a score. Captioning needs a decoder. Classification can be a linear head on a frozen encoder.
5. **Decide what happens if a stream is missing.** A joint MLP trained on concatenations cannot score the text alone unless you trained that path. A coordinated text tower still embeds the query.

If the image is missing, that last step is the whole method. Students who concatenate first and ask questions later discover this in the project, not at the board.

---

## 5. Mathematical formulas

**Coordinated** scoring. Let \(f\) be the image encoder and \(g\) the text encoder. Similarity is cosine:

\[
s(i,t)=\cos\bigl(f(i),g(t)\bigr)=\frac{f(i)^{\top}g(t)}{\lVert f(i)\rVert\,\lVert g(t)\rVert}.
\]

Rank captions (or images) by \(s\). That is retrieval. Zero-shot classification is the same score against a list of class phrases.

**Joint** concat. If \(f(i)\in\mathbb{R}^{d_i}\) and \(g(t)\in\mathbb{R}^{d_t}\),

\[
[f(i);g(t)]\,W,\qquad W\in\mathbb{R}^{(d_i+d_t)\times h},
\]

is a fused vector of width \(h\). You need **both** streams at test time, and a typed query with no image has the wrong shape.

---

## 6. Positive points and negative points

**Positive.**

- You can reuse a frozen encoder as one tower and train only the other side or a small head.
- Coordinated spaces let you query from either modality after training.
- Naming the five jobs keeps a retrieval demo from being graded as a captioner.

**Negative.**

- Concatenation grows width and assumes every stream is present.
- Alignment, whether instance-level cosine or region-level boxes, needs paired data.
- Calling a project “multimodal” without naming the job is not a method.
- Joint models cannot take a text-only query unless you trained that path.

**When not to.** If you only need to search a gallery with words, do not train a concatenating captioner. If you must emit a sentence, a cosine is the wrong head.

---

## 7. Teaching this note

**~16 minutes.** Five-job table, then joint vs coordinated with the 2-D cosine example. Play Yannic Kilcher CLIP **4:40–14:40** (two towers as a coordinated space). Zero-shot details wait for 4.3; captioning waits for BLIP.

---

## 8. Worked example

Image vector \(\boldsymbol{v}=\begin{bmatrix}1\\0\end{bmatrix}\). Matching caption \(\boldsymbol{t}_{+}=\begin{bmatrix}0.8\\0.2\end{bmatrix}\), other caption \(\boldsymbol{t}_{-}=\begin{bmatrix}0\\1\end{bmatrix}\).

\[
\cos(\boldsymbol{v},\boldsymbol{t}_{+})=0.8/\sqrt{0.68}\approx 0.97,\qquad
\cos(\boldsymbol{v},\boldsymbol{t}_{-})=0.
\]

![Match versus mismatch](files/data-643/graphics/4.1-multimodal-foundations/cosine-numeric.png)

Coordinated retrieval: rank captions by cosine. Joint fusion: concat(\(\boldsymbol{v},\boldsymbol{t}\)) is 4-D; you need **both** at test time, and a typed query with no image has the wrong shape.

If the image is missing, a joint MLP trained on concatenations cannot score the text alone unless you trained a special “image dropout” path. A coordinated text tower still embeds the query.

---

## 9. Where students get stuck

- Concatenating then calling it CLIP.
- Assuming a joint model can take a text-only query at test time.
- Mixing alignment (what matches what) with fusion (when you mix features) with translation (when you generate the other stream).

---

## 10. Video

Watch [Yannic Kilcher: OpenAI CLIP, Connecting Text and Images](https://www.youtube.com/watch?v=T9XSU0pKX2E).

Play **4:40–14:40**. Pause when the two encoders emit vectors in one space, and when a cosine (not a concatenating MLP) is the interaction. That is coordinated representation.

---

## 11. Practice

1. Your app must search photos with a typed query. Joint or coordinated? Why?

2. Give one example of alignment that is not “the whole image vs the whole caption.”

3. What breaks if a joint model never saw audio-only examples and you drop the image at test time?

4. Compute \(\cos(\begin{bmatrix}3\\4\end{bmatrix},\begin{bmatrix}4\\3\end{bmatrix})\). If you fuse by concatenation instead, what is the dimension of concat(\(\boldsymbol{u},\boldsymbol{v}\))?

5. Two images \(\boldsymbol{v}_1=\begin{bmatrix}1\\0\end{bmatrix}\), \(\boldsymbol{v}_2=\begin{bmatrix}0\\1\end{bmatrix}\) and one query \(\boldsymbol{q}=\begin{bmatrix}0.6\\0.8\end{bmatrix}\). Which image ranks first by cosine?

6. Captioning versus CLIP, in one sentence each: which job from the five-job table?

7. Co-learning: English captions are plentiful, labels in another language are not. What is the shared stream that lets the rich side help the poor side?
