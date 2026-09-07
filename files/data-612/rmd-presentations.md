## 1. Why knit slides from code

A slide deck that is also a source file has one job: the numbers and plots on the slide come from the same code you would put in a homework file. Knit (or Render) again after a data fix and the deck updates. You are not pasting a screenshot of a plot you can no longer reproduce.

The file is still Markdown plus chunks. The output is slides instead of a scrolling report. Note 1.5 is the document system; this note is the slide formats.

---

## 2. Formats

R Markdown presentation outputs you will see:

| Output | What you get |
| ------ | ------------ |
| `ioslides_presentation` | HTML slides (the usual starting point) |
| `slidy_presentation` | HTML slides, W3C Slidy |
| `beamer_presentation` | PDF slides. Needs LaTeX |
| `powerpoint_presentation` | A `.pptx` file |
| `xaringan::moon_reader` | HTML slides (remark.js). Needs the `xaringan` package |

Quarto's HTML slide format is `format: revealjs`. Lab 12 accepts that as well.

Pick **one** HTML format and stay with it for the lab. Beamer is for when you already have LaTeX and want a PDF. PowerPoint is for a file someone else will click through in PowerPoint.

---

## 3. YAML and slide breaks

R Markdown uses `output:`. A minimal ioslides header:

```markdown
---
title: "Arrival delay"
author: "Your Name"
output: ioslides_presentation
---
```

The title slide is built from `title` and `author`. Every later slide starts with `##`.

````markdown
## A slide title

A sentence.

```{r}
mean(mtcars$mpg)
```
````

`#` is a section (ioslides can turn it into a divider). The slides you write are `##`.

xaringan is the exception: slides are separated by a line with only `---`, not by `##`. If you pick xaringan, follow a xaringan template. If you pick ioslides or slidy, use `##`.

Quarto reveal uses `format: revealjs` and the same `##` slide titles.

---

## 4. What to show

Do **not** show package-load code. Put `library()` in a setup chunk with `echo = FALSE` (R Markdown) or `#| echo: false` / `#| include: false` (Quarto). The reader came for the table and the plot.

````markdown
```{r setup, include=FALSE}
library(tidyverse)
```
````

A chunk that **computes** a table can show the code (`echo = TRUE`). A chunk that **draws** the plot the audience should look at often hides the code (`echo = FALSE`). Both chunks still run.

HTML widgets (an interactive `plotly` chart, a `DT` table) need an **HTML** format: ioslides, slidy, xaringan, or Quarto reveal. They will not appear in Beamer or PowerPoint.

PowerPoint is one-way. Knit writes a `.pptx`. Edits you then make in PowerPoint do not come back into the `.Rmd`. If you need to change a number, change the source and knit again.

---

## 5. One idea per slide

A slide is not a report page. One claim, one table, or one plot. If you need a second plot, it is a second slide.

A few habits that keep a short deck readable:

- title the slide with the claim, not the function name
- show the code only when the code is the point
- give the plot room; drop `theme_bw()` legends you do not need
- end with a sentence the audience can repeat

---

## 6. Practice

Outline a 3-slide deck (do not spend the hour polishing fonts):

1. Title slide (YAML `title` / `author`).
2. A slide with a small table (a `summarize()` of a built-in table, or `mtcars` / `penguins`).
3. A slide with a plot and **no** code (`echo = FALSE`).
