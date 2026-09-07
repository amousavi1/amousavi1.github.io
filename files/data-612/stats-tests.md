## 1. Question, then evidence

A test is the last step, not the first. A useful order:

1. a question you can say in words
2. EDA (a plot, a table)
3. a model that matches the question
4. a test saved as an object
5. a sentence a reader can use

Always assign the test. Printing it once is not enough if you later want the p-value or the interval.

```r
library(tidyverse)
library(palmerpenguins)

tt <- t.test(mpg ~ factor(am), data = mtcars)
tt
tt$p.value
tt$estimate
```

`Sleuth3` has the classic two-sample tables from *The Statistical Sleuth*. Install once in the console, then load a table by name:

```r
install.packages("Sleuth3")
data("case0201", package = "Sleuth3")
```

`case0201` is wide: `Cross` and `Self` are two numeric columns. `t.test(Cross, Self)` is the two-vector form. The formula form needs a long table. If `Sleuth3` is not installed, use `palmerpenguins` or `mtcars`. Those are the fallbacks for the rest of this note.

---

## 2. Two-sample `t.test()`

Plot first. A boxplot of the numeric variable by the two-level group tells you whether the question is even interesting.

```r
ggplot(mtcars, aes(x = factor(am), y = mpg)) +
  geom_boxplot() +
  theme_bw()
```

Then the test. The formula is `y ~ group`. The grouping variable should have **exactly two** levels.

```r
tt <- t.test(mpg ~ factor(am), data = mtcars)
```

`species` in `penguins` has three levels. Filter to a pair, then `droplevels()` so the unused level is gone. Without that, `t.test()` stops.

```r
penguins2 <- penguins |>
  filter(species %in% c("Adelie", "Gentoo")) |>
  droplevels()

ggplot(penguins2, aes(x = species, y = bill_length_mm)) +
  geom_boxplot() +
  theme_bw()

tt_bill <- t.test(bill_length_mm ~ species, data = penguins2)
```

`case0201` after a pivot is the same pattern:

```r
case0201 |>
  pivot_longer(everything(), names_to = "type", values_to = "height") |>
  t.test(height ~ type, data = _)
```

Default `t.test()` does not assume equal variances (Welch). That is the usual choice.

---

## 3. H0 and the p-value

State H0 in words before you look at the number.

For the penguin pair: *mean bill length is the same for Adelie and Gentoo.* For `mtcars`: *mean `mpg` is the same for the two transmission codes.*

The p-value is evidence **against** that H0. A small p-value means the data would be surprising if H0 were true. It is not a stamp that the result is "real," and `0.05` is not a magic cutoff. Report the p-value, the estimates, and the interval. Then write the sentence.

---

## 4. ANOVA and nested models

Three or more groups: `aov(y ~ factor)`, then `summary()`. Save the object.

```r
fit_aov <- aov(bill_length_mm ~ species, data = penguins)
summary(fit_aov)
```

H0 in words: *mean bill length is the same for Adelie, Chinstrap, and Gentoo.* `iris` (`Sepal.Length ~ Species`) and `mtcars` (`mpg ~ factor(cyl)`) are the no-package backups. `Sleuth3` `case0501` is `Lifetime ~ Treatment` if you have the package.

`anova()` compares **nested** models. The smaller model is a special case of the larger one.

```r
m1 <- lm(mpg ~ wt, data = mtcars)
m2 <- lm(mpg ~ wt + hp, data = mtcars)
cmp <- anova(m1, m2)
cmp
```

H0: *once `wt` is in the model, `hp` does not improve the fit.* Same rule: save `cmp`, read the p-value as evidence against that H0, not as a 0.05 switch.

`aov()` is the one-factor (or multi-factor) fit. `anova()` is the comparison. Do not mix the two names by accident.

---

## 5. Practice

1. Boxplot and two-sample `t.test()` for a numeric variable by a two-level group. Use `mpg ~ factor(am)` in `mtcars`, or Adelie vs Gentoo bill length in `penguins` (filter, then `droplevels()`). If you have `Sleuth3`, do `case0201` as well. State H0 in words. Save the test object.

2. `aov()` of a numeric variable by a factor with three or more levels (`bill_length_mm ~ species`, or `mpg ~ factor(cyl)`, or `Sepal.Length ~ Species`). Save the fit. State H0 in words.
