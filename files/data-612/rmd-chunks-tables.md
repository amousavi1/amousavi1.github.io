## 1. Label every chunk

Note 1.4 covered Render, YAML, and `echo` / `eval` / `include`. This note is the next layer: names, defaults, tables, child files.

Give each chunk a unique **label**. Letters, digits, and hyphens are fine. The older fence `{r bill-summary}` is the same idea.

````markdown
```{r}
#| label: bill-summary

penguins |> summarize(n = n())
```
````

---

## 2. Options that hide or skip work

| Option | What it hides or skips |
| ------ | ---------------------- |
| `eval` | If `false`, R does not run the chunk. The reader can still see the code. |
| `echo` | If `false`, the reader does not see the code. Results still appear. |
| `include` | If `false`, nothing from the chunk is printed. The code still runs if `eval` is true. |
| `warning` | If `false`, warnings are hidden. |
| `message` | If `false`, messages are hidden (`library()` chatter, `read_csv()` types). |
| `cache` | If `true`, knitr stores the result and skips a rerun when the chunk has not changed. |

`include: false` is the usual setup chunk: load packages, read data. Later chunks need those objects. The reader does not need that boilerplate.

`cache: true` is a speed trick. Turn it off for a final Render so you are not looking at a stale object.

---

## 3. Defaults in a setup chunk

Set the usual rules once with `knitr::opts_chunk$set()`. A later chunk can override one option.

````markdown
```{r}
#| label: setup
#| include: false

knitr::opts_chunk$set(
  echo = TRUE,
  message = FALSE,
  warning = FALSE
)
```
````

Quarto's YAML `execute:` block (note 1.4) does the same job. Either is fine. This week we use `opts_chunk$set()` so the habit works in an old `.Rmd` as well as a `.qmd`.

---

## 4. Tables with `kable()`

`print()` of a tibble is readable in the console. In a report, pass the table to `knitr::kable()` and give it a caption.

```r
penguins |>
  group_by(species) |>
  summarize(
    mean_bill = mean(bill_length_mm, na.rm = TRUE),
    n = n(),
    .groups = "drop"
  ) |>
  knitr::kable(caption = "Mean bill length (mm) by species.", digits = 1)
```

`digits` rounds numbers. `{kableExtra}` can style rows; we do not need it this week.

---

## 5. Folding code in the YAML

R Markdown:

```markdown
output:
  html_document:
    code_folding: hide
```

Quarto:

```markdown
format:
  html:
    code-fold: true
```

`hide` / `true` starts with the chunks collapsed. The reader can open one.

---

## 6. Child documents

A long report can pull in another file:

````markdown
```{r, child = "helper.qmd"}
```
````

The child's YAML is **ignored**. Title, author, and `format:` live only in the parent. The child is just Markdown plus chunks, run in the parent's session.

Labels must stay unique across parent and child. If a helper also has a chunk named `setup`, rename one of them.

---

## 7. Load a package only if it is missing

When a child (or a chunk you rerun) would call `library(tidyverse)` a second time, skip it:

````markdown
```{r, eval = !"tidyverse" %in% .packages()}
library(tidyverse)
```
````

`.packages()` is the character vector of attached packages. The `!` flips the test: evaluate the chunk only when tidyverse is **not** already loaded.

The same idea for data: `eval = !exists("penguins")`.

---

## 8. Practice

1. List four chunk options and say what each one hides (or skips).

2. Write a setup chunk that sets `echo = TRUE` and `message = FALSE` for the whole document.
