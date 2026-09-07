## 1. `rowwise()` is a group of one

`group_by()` groups many rows. `rowwise()` makes each row its own group so a summary runs **across columns in that row**. `ungroup()` removes it.

```r
df <- tibble(name = c("Mara", "Hadley"), x = 1:2, y = 3:4, z = 5:6)

df |> mutate(m = mean(c(x, y, z)))
# one mean for the whole table

df |>
  rowwise(name) |>
  summarize(m = mean(c(x, y, z)), .groups = "drop")
# one mean per row
```

`c_across()` selects several columns with the same helpers as `select()`:

```r
df <- tibble(id = 1:6, w = 10:15, x = 20:25, y = 30:35, z = 40:45)
rf <- df |> rowwise(id)

rf |> mutate(total = sum(c_across(w:z)))
rf |> mutate(total = sum(c_across(where(is.numeric))))
```

For speed on a whole frame, `rowSums()` and `rowMeans()` avoid the split-and-join:

```r
df |> mutate(total = rowSums(across(where(is.numeric))))
```

`starwars` (in dplyr) is the usual practice table. Without `rowwise()`, `max(height, mass, birth_year)` is one number for the whole column stack, repeated on every row.

---

## 2. `across()` repeats a function on columns

`across()` lives **inside** `mutate()`, `summarize()`, `filter()`, and the other data-masking verbs. It does not change the data by itself.

Two arguments:

- `.cols`: tidyselect, default `everything()`
- `.fns`: a function, a named list of functions, or a formula `~ median(.x, na.rm = TRUE)`. `.x` is the current column.

```r
starwars |>
  summarize(across(where(is.numeric), ~ median(.x, na.rm = TRUE)), .groups = "drop")

starwars |>
  group_by(species) |>
  filter(n() > 1) |>
  summarize(
    across(c(sex, gender, homeworld), ~ length(unique(.x))),
    n = n()
  )
```

Grouping variables are skipped so you do not summarize them by accident.

A named list makes several summaries per column:

```r
min_max <- list(
  min = ~ min(.x, na.rm = TRUE),
  max = ~ max(.x, na.rm = TRUE)
)
starwars |> summarize(across(where(is.numeric), min_max))
```

Order matters. If you compute `n = n()` first, `n` is numeric, so a later `across(where(is.numeric), sd)` will try to take the SD of that constant and give `NA`. Put `n = n()` last.

`across()` replaces the old `*_if()`, `*_at()`, and `*_all` helpers. `select()` and `rename()` already use tidyselect; use `rename_with()` to change names with a function.

---

## 3. Practice

1. For each `starwars` character, the maximum of `height`, `mass`, and `birth_year` (`na.rm = TRUE`). Who is largest? Try it with and without `rowwise()`.

2. Median of every numeric column, by `species` and `gender`, plus `n()`, sorted by `n` descending.
