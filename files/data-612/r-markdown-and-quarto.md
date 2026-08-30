## 1. Three Kinds of Files

RStudio can edit more than one kind of file. The three you will see in this course are:

| File | Extension | What it is for |
| ---- | --------- | -------------- |
| R script | `.R` | Code you want to keep and rerun |
| Quarto | `.qmd` | A document that mixes writing and R code. **This is the format we use.** |
| R Markdown | `.Rmd` | The older document format with the same idea |

A **script** is the right tool when the product is code: a lab, a function, a data-cleaning pipeline.

A **document** is the right tool when the product is something a human should read: a homework writeup, a report, slides. The file holds prose, headings, and code. RStudio can turn that file into HTML, PDF, or Word.

Lab 1 is a script. Later assignments will ask for a Quarto document. You should create and render one this week so that request is not a surprise.

---

## 2. Why Quarto

**Quarto** is the current document system from Posit, the same people who make RStudio. It is the successor to R Markdown.

The department wants you to learn Quarto. New work in this course should be a `.qmd` file, not a `.Rmd` file, unless an assignment says otherwise.

Quarto is the better default because:

- it is what is maintained and taught now
- the same file can become HTML, PDF, Word, or slides
- it still uses ordinary Markdown and R code chunks
- it also works with Python and other languages later, if you need that
- RStudio's **Render** button is built around it

R Markdown is not wrong. You will still open `.Rmd` files in older notes, Stack Overflow answers, and some textbooks. Read those files. For new work here, start a Quarto document.

Quarto is a **program** that RStudio calls. It is not an R package. Recent RStudio / Posit Desktop already includes it. If **Render** is missing, install Quarto from [quarto.org](https://quarto.org/) and reopen RStudio.

You can confirm it is available in RStudio's **Terminal** pane:

```text
quarto --version
```

---

## 3. Create a Quarto Document

1. **File → New File → Quarto Document…**
2. Choose **HTML** as the default format this week.
3. Give it a title and your name.
4. Save it in your project folder with a `.qmd` extension, for example `week01_practice.qmd`.

An `.qmd` file has three parts:

1. a **YAML header** between `---` lines, which names the document and the output format
2. **text**, formatted with Markdown
3. **code chunks**, which contain R

A small file looks like this:

````markdown
---
title: "Week 1 practice"
author: "Your Name"
format: html
---

# A heading

This is ordinary writing. R can compute inline with an `r` expression inside backticks.

```{r}
x <- 1:5
mean(x)
```
````

Notice `format: html`, not `output: html_document`. That is the Quarto header. `format: pdf` and `format: docx` are the usual alternatives.

Insert a code chunk with **Ctrl+Alt+I** (Windows/Linux) or **Cmd+Option+I** (macOS), or **Code → Insert Chunk**.

Run a line or a chunk with **Ctrl+Enter** / **Cmd+Enter**, the same way you run a script. Results appear in the console, and often under the chunk.

---

## 4. Render

When you want a document, click **Render** (not **Knit**). Rendering:

- saves the file
- runs the code in a **fresh** R session, not from leftover console objects
- writes an HTML (or PDF, or Word) file next to the `.qmd`

That fresh session is the point. Everything the document needs must be in the file: `library()` calls, data import, and the code that produces the numbers you quote.

Do **not** put `install.packages()` in the document. Install packages once in the console, as in note **1.2**.

If rendering to PDF fails, you are missing a LaTeX installation. Render to HTML this week. PDF can wait until a later assignment actually requires it. When that happens, a common path is:

```r
install.packages("tinytex")
tinytex::install_tinytex()
```

then close and reopen RStudio.

---

## 5. Markdown You Will Use Constantly

The same Markdown works in Quarto and in R Markdown:

```text
# Heading
## Subheading

*italic*  **bold**  `code`

- a list
- of items

1. a numbered list
1. the numbers update themselves

[a link](https://example.com)
```

A single Enter does not start a new paragraph. Leave a blank line, or end a line with two spaces.

YAML is picky about spacing. If Render fails with a YAML error, look at indentation around `format:`.

---

## 6. A Few Quarto Options Worth Knowing Now

You can ask Quarto for a table of contents and numbered headings:

```markdown
---
title: "Week 1 practice"
author: "Your Name"
format:
  html:
    toc: true
    number-sections: true
---
```

Indentation under `format:` matters. Two extra spaces, or a missing space after a colon, will stop Render.

Chunk options go on `#|` lines at the top of the chunk. That is the Quarto style:

````markdown
```{r}
#| echo: true
#| warning: false

mean(1:5)
```
````

`echo: true` keeps the code visible in the output. `warning: false` hides package startup noise. You do not need many options in week 1. Put `library(tidyverse)` in an early chunk so every later chunk can use it.

Inline R still uses an `r` expression inside backticks. Use that for a number you have already computed, so the writeup updates when you Render again.

---

## 7. R Markdown, Briefly

**R Markdown** is the older sibling. Create one with **File → New File → R Markdown…**. The file extension is `.Rmd`. The header uses `output:` instead of `format:`:

```markdown
---
title: "Week 1 practice"
author: "Your Name"
output: html_document
---
```

The button is **Knit**, not **Render**. The idea is the same: Markdown plus code chunks, run in a fresh session.

If an old assignment or a book gives you a `.Rmd` file, you can still knit it. Do not convert every file you find. For new work in DATA 612, use Quarto.

Jupyter notebooks are a third interactive format, used heavily in Python. We will not use them here.

---

## 8. What to Use When

```text
Need to keep code and rerun it?
  → .R script

Need a readable writeup with results baked in?
  → .qmd (Quarto)

Someone handed you an old .Rmd?
  → knit it; do not rewrite it unless you were asked to

Lab 1
  → lab01.R

Later homework
  → a Quarto document, unless the assignment says otherwise
```

Note **1.1** is how you run a script and find the working directory. Note **1.3** is how you import `students.csv`. Lab 1 uses both. Lab 1 does not need this note.
