These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

Once image and text share a space, **retrieval** is nearest neighbors. The same geometry that makes search work also encodes **stereotypes** from the training web.

---

## 1. Two directions

**Text \(\to\) image:** a query string, rank photos. **Image \(\to\) text:** a photo, rank captions or documents. Dual retrieval is why coordinated towers beat a joint vector that you can only query from one side.

![Query with an image or with text](files/data-643/graphics/5.3-retrieval-bias/retrieval.png)

Report **recall@k** and a few failure cases (wrong object, wrong count, text that ignores the image). For a project, freeze the gallery embeddings; do not re-encode millions of images on every demo.

Recall@1 on a 2-item toy is not a paper. On a 100k gallery, recall@1 can look terrible while recall@10 is usable. Always state \(k\) and gallery size.

---

## 2. Bias and robustness

Occupation and gender, geography and skin tone, “a terrorist” versus a news photo: CLIP-style models pick up the co-occurrences of the web. Zero-shot prompts (`a photo of a man who is a nurse`) move the query along the same directions you saw in Week 1’s toy embeddings.

![Prompted stereotypes in a vision–language space](files/data-643/graphics/5.3-retrieval-bias/vlm-bias.png)

**Robustness:** typographic attacks (text painted in the image), distribution shift (medical, sketches), and language variety. A high ImageNet zero-shot number does not certify your domain.

If your project ranks people, jobs, or health content, put a probe in the report: a small, documented set of prompts and the retrievals they return. Debiasing is incomplete; measuring is required.

Lab 5’s occupation probe (`nurse` / `ceo` vs `man` / `woman` in `toy_clip.csv`) is the miniature of this section. Real CLIP is the same cosine, trained on the web.

A probe is a **fixed list** of prompts and a rule for a bad hit (wrong gender default, violent stereotype, medical advice). Put the list in an appendix. Do not “debias” by deleting one axis and claiming the space is fair; say what you measured.

Typographic attack cartoon: a photo of an apple with the word `iPod` printed on it. CLIP’s text bias can rank it with gadgets. That is robustness, not occupancy of occupations, but it is the same nearest-neighbor geometry.

---

## 3. Teaching this note

**30–40 minutes.** Dual retrieval, recall@k with a tiny ranking, then the occupation probe **with numbers**. Play the **second half** of the CLIP video (robustness / broader impact, about **37:40–47:00**). Mention Lab 5’s occupation rows by name so the lab is not a surprise.

Minute plan: 8 min two retrieval directions; 10 min recall@k arithmetic; 10 min occupation probe; 10 min video second half. Do not skip the probe to “save time.”

---

## 4. Worked example

Gallery of three \(\ell_2\)-normalized image vectors:

\[
\text{cat}=\begin{bmatrix}1\\0\end{bmatrix},\;
\text{nurse}=\begin{bmatrix}0.2\\0.98\end{bmatrix},\;
\text{ceo}=\begin{bmatrix}0.98\\0.2\end{bmatrix}.
\]

Query text \(\text{woman}\approx\begin{bmatrix}0.1\\1\end{bmatrix}\). Cosines \(\approx 0.10,\; 0.999,\; 0.30\). Rank: nurse, ceo, cat.

Query text \(\text{man}\approx\begin{bmatrix}1\\0.1\end{bmatrix}\). Cosines \(\approx 0.995,\; 0.30,\; 0.999\). Rank: ceo (tie-ish with cat), nurse last.

That is an **occupation probe**: who is nearest to `man` vs `woman`. Lab 5 asks you to run it on `toy_clip.csv`. A production system that ranks résumés needs the same table in the report, on real photos, with documented prompts.

Recall@1 for query `cat` is 1 if cat is the top image. If you only report recall@1 on 100k images, a model that puts the right photo at rank 3 looks like a zero.

---

## 5. Where students get stuck

- Throwing away one tower and then being unable to query from that side.
- Reporting a single recall@1 without \(k\) or gallery size.
- Skipping a bias probe because “it’s just a toy.”

---

## 6. Video

Watch the **second half** of [Yannic Kilcher: OpenAI CLIP, Connecting Text and Images](https://www.youtube.com/watch?v=T9XSU0pKX2E).

Start around **robustness to data shift (37:40)** and **broader impact (44:20)**. Pause on prompt sensitivity and on who is harmed when retrieval ranks people. Pair that with Lab 5’s occupation probes (`nurse`/`ceo` vs `man`/`woman`), not with a vibe check.

---

## 7. Practice

1. You can retrieve with a caption but not with a photo. What did you probably throw away?

2. Why is recall@1 a poor single number for a 100k image gallery?

3. Write one probe prompt you would be embarrassed to ship, and what you would count as a bad retrieval.

4. Cosines of a query to four images: \(0.11, 0.40, 0.39, 0.38\). What is recall@1? recall@3? If the gold item is the \(0.40\) image, both are 1; if gold is \(0.38\), write both numbers.

5. Vectors \(\boldsymbol{q}=\begin{bmatrix}0\\1\end{bmatrix}\), \(\boldsymbol{a}=\begin{bmatrix}0.6\\0.8\end{bmatrix}\), \(\boldsymbol{b}=\begin{bmatrix}0.8\\0.6\end{bmatrix}\) (not yet normalized). Rank \(a,b\) by cosine to \(\boldsymbol{q}\). Then \(\ell_2\)-normalize \(\boldsymbol{a}\) and \(\boldsymbol{b}\) and rank again. Did the order change?
