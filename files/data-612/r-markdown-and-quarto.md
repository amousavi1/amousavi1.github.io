## 1. Three Kinds of Files

RStudio can edit more than one kind of file. The three you will see in this course are:

| File | Extension | What it is for |
| ---- | --------- | -------------- |
| R script | `.R` | Code you want to keep and rerun |
| R Markdown | `.Rmd` | A document that mixes writing and R code |
| Quarto | `.qmd` | A newer document format with the same idea |

A **script** is the right tool when the product is code: a lab, a function, a data-cleaning pipeline.

A **document** is the right tool when the product is something a human should read: a homework writeup, a report, slides. The file holds prose, headings, and code. RStudio can turn that file into HTML, PDF, or Word.

Lab 1 is a script. Later assignments will ask for an R Markdown or Quarto document. You should know how to create one this week so the later request is not a surprise.

---

## 2. R Markdown in Brief

Markdown is a way to write headings, lists, links, and emphasis in plain text. **R Markdown** adds R code to that file.

Create one with **File → New File → R Markdown…**. Choose HTML as the default output. Save it in your project folder.

An `.Rmd` file has three parts:

1. a **YAML header** between `---` lines, which names the document and the output format
2. **text**, formatted with Markdown
3. **code chunks**, which contain R

A small file looks like this:

````markdown
---
title: "Week 1 practice"
author: "Your Name"
output: html_document
---

# A heading

This is ordinary writing. R can compute inline with an `r` expression inside backticks.

```{r}
x <- 1:5
mean(x)
```
````

Insert a code chunk with **Ctrl+Alt+I** (Windows/Linux) or **Cmd+Option+I** (macOS), or **Code → Insert Chunk**.

Run a line or a chunk with **Ctrl+Enter** / **Cmd+Enter**, the same way you run a script. Results appear in the console, and often under the chunk.

When you want a document, click **Knit** (or **Knit to HTML**). Knitting:

- saves the file
- runs the code in a **fresh** R session, not from leftover console objects
- writes an HTML (or PDF, or Word) file next to the `.Rmd`

That fresh session is the point. Everything the document needs must be in the file: `library()` calls, data import, and the code that produces the numbers you quote.

Do **not** put `install.packages()` in the document. Install packages once in the console, as in note **1.2**.

If knitting to PDF fails, you are missing a LaTeX installation. Knit to HTML this week. PDF can wait until a later assignment actually requires it.

---

## 3. Markdown You Will Use Constantly

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

YAML is picky about spacing. If Knit fails with a YAML error, look at indentation around `output:`.

---

## 4. Quarto

**Quarto** is the newer sibling of R Markdown. It uses the same Markdown-plus-code idea, and it also works with Python and other languages. The file extension is `.qmd`.

Create one with **File → New File → Quarto Document…**. The header looks similar:

```markdown
---
title: "Week 1 practice"
author: "Your Name"
format: html
---
```

Code chunks still use `{r}` fences. Instead of **Knit**, you click **Render**.

For this course, R Markdown and Quarto are interchangeable for a simple HTML or PDF writeup. If an assignment specifies one, use that one. If it does not, either is fine.

Jupyter notebooks are a third interactive format, used heavily in Python. We will not use them here.

---

## 5. What to Use When

```text
Need to keep code and rerun it?
  → .R script

Need a readable writeup with results baked in?
  → .Rmd or .qmd

Lab 1
  → lab01.R

Later homework
  → a knitted or rendered document, as the assignment says
```

Note **1.1** is how you run a script and find files. Note **1.2** is how you import `students.csv`. Lab 1 uses both.
