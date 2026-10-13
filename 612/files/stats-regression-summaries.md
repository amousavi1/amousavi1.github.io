## 1. Fit a linear model

`lm(y ~ x1 + x2)` is ordinary least squares. Save the fit. The same lifecycle as note 11.1 still applies: question, plot, model, then a sentence.

```r
library(tidyverse)
library(palmerpenguins)

fit <- lm(mpg ~ wt + hp, data = mtcars)
```

`wt` is weight; `hp` is horsepower. Both are in `mtcars`, which is built in. `palmerpenguins` is the other table this note uses (`bill_length_mm ~ flipper_length_mm + body_mass_g`). If `Sleuth3` is installed you can load a Sleuth regression table the same way as in 11.1 (`install.packages("Sleuth3")` once, then `data("case0201", package = "Sleuth3")` is the two-sample table; pick a later `case*` with a numeric response for regression). The examples below stay on `mtcars` and `penguins` so they run without extra files.

Plot the main relationship before you trust the coefficients:

```r
ggplot(mtcars, aes(x = wt, y = mpg)) +
  geom_point() +
  geom_smooth(method = lm, se = FALSE) +
  theme_bw()
```

---

## 2. Read the fit

Four things you will actually use:

```r
summary(fit)
coef(fit)
confint(fit)
broom::tidy(fit, conf.int = TRUE)
```

`summary()` is the printed report: coefficients, standard errors, t statistics, p-values, and R-squared. `coef()` is just the estimates. `confint()` is the interval for each coefficient. `broom::tidy()` puts the same numbers in a tibble you can pipe.

Install `broom` once in the console if it is missing. Do not put `install.packages()` in the Quarto file.

Read one coefficient in words. For `mpg ~ wt + hp`, the `wt` number is the change in fitted `mpg` associated with a one-unit change in `wt` **holding `hp` fixed**. The p-value on that row is evidence against "this coefficient is zero," not a quality stamp for the whole model.

---

## 3. Residual plots

A residual is observed minus fitted. If the model is a good description, residuals look like unstructured noise around zero.

```r
plot(fit, which = 1)
plot(fit, which = 2)
```

`which = 1` is residuals versus fitted. `which = 2` is the normal QQ plot. The ggplot version of the first one:

```r
aug <- broom::augment(fit)

ggplot(aug, aes(x = .fitted, y = .resid)) +
  geom_point() +
  geom_hline(yintercept = 0) +
  geom_smooth(se = FALSE) +
  theme_bw()
```

If the residual cloud **fans out** (small spread on the left, wide on the right), the variance is not constant. A transform of the response is the first thing to try, often `log(y)`:

```r
fit_log <- lm(log(mpg) ~ wt + hp, data = mtcars)
plot(fit_log, which = 1)
```

Refit, then look at the residual plot again. Do not transform only because a p-value looked nicer.

---

## 4. Numerical summaries

`summary()` on a data frame is the base-R scan: min, quartiles, mean, max, and a count of `NA`s for each column.

```r
summary(penguins)
summary(mtcars)
```

For a tibble of chosen summaries, use `across()` with a named list. `{.col}_{.fn}` builds the output names. `na.rm` belongs on the function, so pass a formula `~ mean(.x, na.rm = TRUE)` rather than the bare `mean`:

```r
penguins |>
  summarize(
    across(
      where(is.numeric),
      list(
        mean = ~ mean(.x, na.rm = TRUE),
        sd = ~ sd(.x, na.rm = TRUE)
      ),
      .names = "{.col}_{.fn}"
    )
  )
```

`list(mean = mean, sd = sd)` is the same idea without `na.rm`. On `penguins` that will propagate `NA`s. Prefer the formula form.

`skimr::skim()` is a compact one-function scan (types, missingness, mean, sd, quantiles). Install `skimr` once if you want it. It does not replace a plot.

```r
skimr::skim(penguins)
```

---

## 5. Practice

1. `fit <- lm(mpg ~ wt + hp, data = mtcars)`. Read `summary(fit)` and `confint(fit)`. Write one sentence that interprets the `wt` coefficient. Glance at `plot(fit, which = 1)`.

2. `across()` summaries of every numeric column in `penguins` or `mtcars`: mean and sd, `.names = "{.col}_{.fn}"`, `na.rm` via `~ mean(.x, na.rm = TRUE)`. If `skimr` is installed, run `skim()` on the same table.
