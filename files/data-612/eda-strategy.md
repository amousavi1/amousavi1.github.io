## 1. A working order

Once the file is in and the types look right, explore before you model. EDA is curiosity with a notebook: many plots, many summaries, then a few questions worth keeping. Write the dead ends down so you are not only keeping the pretty ones.

A useful order:

1. the distribution of each variable
2. every pair of variables
3. a third variable (color or facet)
4. missingness and extremes

`diamonds` is the running example. `skimr::skim()` is a compact alternative to `summary()`.

```r
library(tidyverse)
data("diamonds")
```

---

## 2. One variable

A categorical variable: counts and proportions. `geom_bar()` for the picture; `table()` and `prop.table()` for the numbers.

```r
ggplot(diamonds, aes(x = color)) +
  geom_bar() +
  theme_bw()

prop.table(table(diamonds$color))
```

Ask whether the levels have an order, and whether a rare level is real or a coding accident.

A quantitative variable: `geom_histogram()` or `geom_density()`, plus `mean()`, `sd()`, and `fivenum()` (min, lower hinge, median, upper hinge, max). Look for skew and extra modes.

```r
ggplot(diamonds, aes(x = carat)) +
  geom_histogram(bins = 50) +
  theme_bw()

fivenum(diamonds$carat)
```

Color or `geom_freqpoly()` to split one quantitative variable by a category.

---

## 3. Two variables

- Two quantitative: `geom_point()`, then a smooth. Overplotting: `alpha` or `geom_hex()` (note 3.2).
- One categorical and one quantitative: `geom_boxplot()`, maybe on a log scale.
- Two categorical: `table()`, `prop.table(table(...), margin = 1)` or `margin = 2` for conditional distributions. A count plot is `geom_count()`. A mosaic plot (`ggmosaic`) is optional.

`UCBAdmissions` is the classic Simpson warning: a third variable can reverse an association. The overall admission rate by gender is not the same story as the rate inside each department.

```r
ucb <- as_tibble(UCBAdmissions)
ucb |>
  group_by(Gender) |>
  summarize(p = sum(Freq[Admit == "Admitted"]) / sum(Freq), .groups = "drop")

ucb |>
  group_by(Dept, Gender) |>
  summarize(p = sum(Freq[Admit == "Admitted"]) / sum(Freq), .groups = "drop")
```

```r
ggplot(diamonds, aes(x = carat, y = price)) +
  geom_point(alpha = 0.05) +
  theme_bw()

ggplot(diamonds, aes(x = cut, y = price)) +
  geom_boxplot() +
  scale_y_log10() +
  theme_bw()
```

`GGally::ggpairs()` builds a panel of pairwise plots at once. Use it as a scan, then make the plots you actually need.

---

## 4. Missingness, patterns, outliers

Count `NA`s by column (`across` and `sum(is.na(.x))`, note 5.1). A hole you expected to be filled is information.

A pattern is a relationship you can name: linear, curved, clustered, seasonal. An outlier is a point that does not follow that pattern. Do not delete it by reflex. Ask whether it is a data error or a real rare case. Note 3.1 (Anscombe) is why you plot before you trust a correlation.

---

## 5. This week, in one place

- `read_lines()` then `read_csv()` / `read_tsv()` / `read_csv2()`
- check types, `NA`s, and duplicates
- `parse_*()` and `col_types` when the guess is wrong
- `write_csv()` and `saveRDS()`
- EDA: one variable, then pairs, then a third variable

Chapter 11 of [R for Data Science](https://r4ds.had.co.nz/data-import.html) for readr; Chapter 7 for EDA.

---

## 6. Practice

1. For `diamonds`, a bar chart of `cut` and a histogram of `price`.

2. Boxplots of `price` by `cut`, log-`y`, colored or faceted by `color`.
