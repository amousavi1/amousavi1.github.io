Work in a **Quarto** document. Do **6.1** through **6.3** first. Put the course CSV files in a `data/` folder of your project (see the Data section of the course page).

```r
library(tidyverse)
```

---

## 1. Import

1. `read_lines()` on `hate_crimes1.csv` through `hate_crimes7.csv` and `hate_crimes_1a.csv`. Then load each with the matching `read_*()`. Check `head()` and the number of `NA`s per column.

2. Load `hate_crimes_1a.csv` once as-is and once with `na = "missing"`. What changed?

---

## 2. Parsers

1. Parse `"01, January 2018"`, `"01-January/2000"`, and `"1 Jan 19"` as dates.

2. Parse `"10:40 pm"` and `"23:40-22"` as times.

3. Load `estate.csv`. Use `problems()` if anything looks off. Set `col_types` for at least one column.

---

## 3. EDA

Using `diamonds` (or `estate` if you prefer):

1. The distribution of one categorical variable and one quantitative variable.

2. A scatterplot of two quantitative variables, with overplotting handled.

3. A boxplot of a quantitative variable by a categorical variable.
