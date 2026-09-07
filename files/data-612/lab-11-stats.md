Work in a **Quarto** document. Do **11.1** and **11.2** first. Prefer `mtcars`, `palmerpenguins`, or `iris` so the lab runs without extra files. `Sleuth3` is optional.

```r
library(tidyverse)
library(palmerpenguins)
```

---

## 1. Two-sample t-test

1. Boxplot of a numeric variable by a **two-level** group.

2. `t.test()` with the formula `y ~ group`. Save the object.

Use `mpg` by `am` in `mtcars`, or Adelie vs Gentoo bill length in `penguins` after `filter()` and `droplevels()`. State H0 in words. Report the p-value as evidence against that H0.

---

## 2. ANOVA

`aov()` of a numeric variable by a factor with **three or more** levels. Save the fit and `summary()` it.

`bill_length_mm ~ species` in `penguins`, `mpg ~ factor(cyl)` in `mtcars`, or `Sepal.Length ~ Species` in `iris` are all fine. State H0 in words.

---

## 3. Regression

`lm()` with **two** predictors. Interpret one coefficient in a sentence (holding the other predictor fixed). Glance at the residual-versus-fitted plot (`plot(fit, which = 1)` or `broom::augment()`).

`mpg ~ wt + hp` in `mtcars` is the intended default.

---

## 4. Column summaries

1. `across()` on every numeric column: mean and sd, `.names = "{.col}_{.fn}"`, `na.rm` via a formula `~ mean(.x, na.rm = TRUE)`.

2. If `skimr` is installed, `skimr::skim()` on the same table.
