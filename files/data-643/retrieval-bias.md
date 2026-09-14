These notes match the lecture slides. Use **(slides)** on the course hub for the deck.

Once image and text share a space, **retrieval** is nearest neighbors. The same geometry that makes search work also encodes **stereotypes** from the training web.

---

## 1. Two directions

**Text \(\to\) image:** a query string, rank photos. **Image \(\to\) text:** a photo, rank captions or documents. Dual retrieval is why coordinated towers beat a joint vector that you can only query from one side.

![Query with an image or with text](files/data-643/graphics/5.3-retrieval-bias/retrieval.png)

Report **recall@k** and a few failure cases (wrong object, wrong count, text that ignores the image). For a project, freeze the gallery embeddings; do not re-encode millions of images on every demo.

---

## 2. Bias and robustness

Occupation and gender, geography and skin tone, “a terrorist” versus a news photo: CLIP-style models pick up the co-occurrences of the web. Zero-shot prompts (`a photo of a man who is a nurse`) move the query along the same directions you saw in Week 1’s toy embeddings.

![Prompted stereotypes in a vision–language space](files/data-643/graphics/5.3-retrieval-bias/vlm-bias.png)

**Robustness:** typographic attacks (text painted in the image), distribution shift (medical, sketches), and language variety. A high ImageNet zero-shot number does not certify your domain.

If your project ranks people, jobs, or health content, put a probe in the report: a small, documented set of prompts and the retrievals they return. Debiasing is incomplete; measuring is required.

---

## 3. Practice

1. You can retrieve with a caption but not with a photo. What did you probably throw away?

2. Why is recall@1 a poor single number for a 100k image gallery?

3. Write one probe prompt you would be embarrassed to ship, and what you would count as a bad retrieval.
