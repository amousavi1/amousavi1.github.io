Work in a **Quarto** document. Do **5.1** and **5.2** first. `starwars` comes with dplyr.

```r
library(tidyverse)
```

---

## 1. Row-wise and across

1. For each `starwars` character, the maximum of `height`, `mass`, and `birth_year` (`na.rm = TRUE`). Who is largest? Run it with `rowwise()` and once without.

2. Median of every numeric column, by `species` and `gender`, plus `n()`, sorted by `n` descending.

3. Min and max of every numeric column except `birth_year`, by `species` and `gender`, plus `n()`.

---

## 2. case_when and row names

1. Add a `type` column to `starwars`: `"large"` if height or mass is over 200, `"robot"` if the species is Droid, otherwise `"other"`.

2. Does `mtcars` have row names? If so, make a tibble with a `car` column.

3. Distinct combinations of the `starwars` columns whose names contain `"color"`.
