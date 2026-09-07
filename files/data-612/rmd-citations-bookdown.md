## 1. Numbered figures and tables

A caption on a plot is ordinary text until the document format knows how to number it. Two routes:

- R Markdown: `bookdown::html_document2` (or `pdf_document2`) instead of `html_document`
- Quarto: `format: html` already numbers figures and tables that have captions

```markdown
output:
  bookdown::html_document2:
    toc: true
```

Install `bookdown` once in the console if you are knitting an `.Rmd`. A `.qmd` does not need that package for numbers.

Put a caption on the chunk. In Quarto:

````markdown
```{r}
#| label: fig-bills
#| fig-cap: "Bill length vs bill depth."

ggplot(penguins, aes(x = bill_length_mm, y = bill_depth_mm, color = species)) +
  geom_point() +
  theme_bw()
```
````

The HTML then prints **Figure 1:** in front of that sentence. `knitr::kable(caption = "...")` gets **Table 1:** the same way.

---

## 2. Cross-references

Once the figure has a label and a caption, you can point at it in the prose.

Quarto: `Figure @fig-bills` or `@fig-bills`.

bookdown: `\@ref(fig:bills)` when the chunk is labeled `bills` and has `fig.cap`.

A heading can have a label too. Quarto uses `{#sec-methods}` after the heading. bookdown uses `{#methods}`. You do not need either for Lab 13.

---

## 3. A `.bib` file

Citations come from a BibTeX file, not from typing the reference by hand. A small `refs.bib` looks like this:

```text
@Manual{horst2020palmerpenguins,
  title = {palmerpenguins: Palmer Archipelago penguin data},
  author = {Allison Horst and Alison Hill and Kristen Gorman},
  year = {2020},
  url = {https://allisonhorst.github.io/palmerpenguins/},
}
```

The word after `{` is the **key**. You cite the key, not the title.

Point the document at the file. Quarto and R Markdown both use:

```markdown
bibliography: refs.bib
```

Put that line in the YAML, at the same indent as `title:`.

---

## 4. Cite in the text

`@horst2020palmerpenguins` becomes an in-text citation when you Render. Wrapping it, `[@horst2020palmerpenguins]`, puts the citation in parentheses.

`nocite: '@*'` in the YAML lists **every** entry in the `.bib`, even keys you never typed. Useful for a reading list. Leave it out if you only want the sources you cited.

Add a heading `# References` (or `# Bibliography`) at the end. Quarto and pandoc write the list there.

---

## 5. Style with CSL

The default author–year look is fine for this course. To match a journal, add a Citation Style Language file:

```markdown
bibliography: refs.bib
csl: apa.csl
```

Download a `.csl` from [zotero.org/styles](https://www.zotero.org/styles) and keep it next to the `.qmd`. You do not write CSL by hand.

---

## 6. The same idea in Quarto

A compact header:

```markdown
---
title: "Penguin bills"
author: "Your Name"
format: html
bibliography: refs.bib
---
```

No `bookdown::` output. Captions still get numbers. `@key` still cites. The `.bib` format does not change.

If you are handed an `.Rmd` that already uses `bookdown::html_document2`, knit it. Do not rewrite it as Quarto just to get a citation.

---

## 7. Practice

1. Sketch a four-line BibTeX entry for a package or a paper (type, key, title, author or year).

2. Write one sentence that cites that key with `@`.
