Work in a **Quarto** document. Do **7.1** and **7.2** first. Put the course CSV files in a `data/` folder of your project (see the Data section of the course page).

```r
library(tidyverse)
library(nycflights13)
```

---

## 1. Longer

1. Load `monkeymem.csv`. Pivot `Week2` through `Week16` longer. Each row should be one monkey-week. The week names go in one column; accuracy goes in another.

2. On `table4a`, show a `pivot_longer()` call that fails because the year names are written as numbers, then the call that works. In a sentence, why the first one fails.

---

## 2. Wider, separate, unite

1. Load `flowers1.csv` with `read_delim("data/flowers1.csv", delim = ";")`. Widen so `Variable` becomes column names and `Value` fills the cells. Fix the decimal commas if `Value` is not numeric.

2. Load `flowers2.csv`. Separate `Flowers/Intensity` into two numeric columns. Unite those two columns again with a comma.

3. In `flights`, select `month`, `day`, `hour`, and `minute`. Unite `hour` and `minute` into `sd_time`, then parse that column as a time. What happens, and why? Fix it with `paste0()` or `stringr` so minutes stay two digits.
