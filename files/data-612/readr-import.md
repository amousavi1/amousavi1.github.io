## 1. Paths, once more

Note 1.3 is the full story. A short reminder: store course files under a project, use a **relative** path from that project, and do not hard-code `C:/Users/...`. `getwd()` is the console's working directory. A Quarto file in `analysis/` reaches data with `"../data/hate_crimes2.csv"` or `here::here("data", "hate_crimes2.csv")`.

The Data section of the course page has the `hate_crimes*.csv` files. Download them into a `data/` folder in your project. They are not tied to one week.

---

## 2. `readr` reads flat files into tibbles

`readr` comes with `library(tidyverse)`. It is faster than `read.csv()` and it does **not** turn characters into factors.

A `.csv` separates columns with commas. A `.tsv` uses tabs (`\t` in `read_lines()`). `read_csv2()` uses semicolons.

```r
library(tidyverse)

read_lines("data/hate_crimes2.csv", n_max = 10)
hate_crimes <- read_csv("data/hate_crimes2.csv")
```

`read_lines()` is how you see the delimiter before you choose a reader. A URL works as `file` if the file is public.

Do not import an Excel workbook if you can avoid it. Export a sheet to CSV, then read the CSV. Watch for empty columns Excel leaves behind.

---

## 3. Check the import immediately

readr prints the types it guessed. Then check:

```r
str(hate_crimes)
nrow(hate_crimes)
ncol(hate_crimes)
head(hate_crimes, 10)
tail(hate_crimes, 10)

hate_crimes |>
  summarize(across(everything(), ~ sum(is.na(.x))))

nrow(distinct(hate_crimes))
```

If a column that should be numeric is character, `unique()` usually shows why: `"missing"`, `"."`, `"-99"`.

Tell `read_csv()` those strings are missing:

```r
read_csv("data/hate_crimes_1a.csv", na = "missing")
```

Other useful arguments:

- `col_types` — you set the types (note 6.2)
- `skip` — drop leading comment lines
- `comment = "#"` — drop lines that start with `#`
- `locale` — decimal mark and other regional defaults (US by default)

---

## 4. Write files back out

```r
write_csv(hate_crimes, "data/hate_crimes_clean.csv")
```

`write_tsv()` and `write_csv2()` match the readers. `saveRDS(obj, "obj.rds")` and `readRDS("obj.rds")` keep a single R object with its types. That is for your own later session, not for sharing with Excel.

---

## 5. Practice

1. `read_lines()` on each `hate_crimes*.csv` in the Data section, then load it with the matching `read_*()`. Check `head()` and the `NA` counts.

2. Load `hate_crimes_1a.csv` once as-is and once with `na = "missing"`.
