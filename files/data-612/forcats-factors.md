## 1. A factor is an integer plus labels

A factor stores a categorical vector as integer codes plus a `levels` attribute. What prints is the label. What sits underneath is `1`, `2`, `3`, … in the order of the levels.

That is why `as.numeric()` on a factor of numbers is the **index**, not the printed value.

```r
library(tidyverse)

xf <- factor(c(10, 11, 13, 10))
xf
as.numeric(xf)
parse_number(as.character(xf))
parse_number(levels(xf)[xf])
```

`as.character()` (or `levels(xf)[xf]`) gets the labels back. `parse_number()` turns them into numbers.

Create a factor with `factor()`. Set `levels` yourself when the order is not alphabetical.

```r
month_levels <- c("Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
factor(c("Dec", "Apr", "Jan", "Mar"), levels = month_levels)
```

Values that are not in `levels` become `NA`. Extra levels stay in the attribute even if no row uses them.

---

## 2. `gss_cat`

`gss_cat` is a General Social Survey slice that ships with forcats. `?gss_cat`. Useful factors: `marital`, `rincome`, `partyid`, `relig`.

```r
gss_cat
count(gss_cat, partyid)
```

`forcats` comes with `library(tidyverse)`. Every helper starts with `fct_`.

---

## 3. Reorder levels

Plots follow the level order. Change the order, not the data.

- `fct_reorder(f, x)` — order `f` by a summary of `x` (median by default). The usual choice for a scatter or bar of a summary.
- `fct_infreq(f)` — most common level first.
- `fct_rev(f)` — reverse the current levels.
- `fct_relevel(f, ...)` — move named levels to the front (or pass a function).

```r
gss_cat |>
  group_by(relig) |>
  summarize(tv = mean(tvhours, na.rm = TRUE), n = n()) |>
  mutate(relig = fct_reorder(relig, tv)) |>
  ggplot(aes(x = tv, y = relig)) +
  geom_point() +
  theme_bw()

gss_cat |>
  mutate(partyid = fct_relevel(partyid, "Independent")) |>
  count(partyid)
```

`fct_infreq()` then `fct_rev()` puts the most common level on the **right** of a bar chart.

---

## 4. Recode, collapse, lump

`fct_recode()` renames levels. Old name on the right. Drop a level with `NULL = "old"`.

```r
gss_cat |>
  mutate(partyid = fct_recode(
    partyid,
    "Rep, strong" = "Strong republican",
    "Rep, weak"   = "Not str republican",
    "Dem, weak"   = "Not str democrat",
    "Dem, strong" = "Strong democrat"
  )) |>
  count(partyid)
```

`fct_collapse()` is recode for many-to-one. `fct_lump()` folds rare levels into `Other`. `n` keeps the most common; `prop` keeps levels above a share.

```r
gss_cat |>
  mutate(partyid = fct_collapse(
    partyid,
    other = c("No answer", "Don't know", "Other party"),
    rep   = c("Strong republican", "Not str republican"),
    ind   = c("Ind,near rep", "Independent", "Ind,near dem"),
    dem   = c("Not str democrat", "Strong democrat")
  )) |>
  count(partyid)

gss_cat |>
  mutate(relig = fct_lump(relig, n = 5)) |>
  count(relig)
```

---

## 5. Add, drop, and missing levels

```r
f <- factor(c("A", "B", "A"), levels = c("A", "B", "C"))
fct_drop(f)

g <- factor(c("A", "B"))
fct_expand(g, "C", "D")

h <- factor(c("A", NA, "B"))
fct_explicit_na(h, na_level = "(Missing)")
```

`fct_drop()` removes unused levels. `fct_expand()` adds empty ones. `fct_explicit_na()` turns `NA` into a real level so it appears in tables and plots. Filtering out rows does **not** drop the level; call `fct_drop()` after.

---

## 6. Practice

Use `gss_cat`.

1. Reorder `partyid` alphabetically.

2. Move `rincome` level `"Not applicable"` to the front.

3. Abbreviate `marital` with `fct_recode()`.
