Work in a **Quarto** document. Do notes **13.1** and **13.2** first. Render to HTML. You will need `tidyverse`, `palmerpenguins`, and `knitr`.

---

## 1. Setup and packages

1. A setup chunk that calls `knitr::opts_chunk$set()` with `echo = TRUE` and `message = FALSE`. Hide the setup chunk itself (`include: false`).

2. Load `tidyverse` and `palmerpenguins` without printing package startup text. `data(penguins)` if the tibble is not already attached.

---

## 2. A table and a plot

1. A `kable` of a **three-column** summary of bill length by species (species, mean bill length, and `n` is enough). Give the table a caption.

2. A scatterplot of `bill_length_mm` vs `bill_depth_mm`, colored by `species`. Give the figure a caption.

---

## 3. A citation and folding

1. One sentence that would cite `@horst2020palmerpenguins` if a `refs.bib` file existed. You may add a real `.bib` and a `bibliography:` line, or leave the `@key` in the prose so the syntax is visible.

2. Optional: fold the code in the YAML (`code-fold: true` in Quarto, or `code_folding: hide` in an `.Rmd`).
