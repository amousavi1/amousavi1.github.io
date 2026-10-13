Work in a **Quarto** document. Number the exercises. Do **4.1** through **4.3** first.

```r
library(tidyverse)
library(nycflights13)
data("flights")
```

---

## 1. Filter and slice

1. Flights in odd months, or on even days of even months.

2. Flights to Houston (`IAH` or `HOU`), on UA, AA, or DL, in July–September, that arrived more than 15 minutes late and did not leave late.

3. Rows 10, 100, 1000, 10000, and 100000.

4. The last 10 of the first 30 Newark (`EWR`) flights.

5. `set.seed(1)`. A random 1% sample, and a sample of 3367 rows. Are the last 10 rows the same? Why?

6. The 50 longest `air_time`s, then the 10 smallest `arr_delay`s among those. Repeat after `filter(air_time < 300)`. What does `with_ties = FALSE` change?

---

## 2. Arrange, select, mutate

1. Longest `distance`, ties broken by `air_time`.

2. Keep every arrival column plus `year`, `month`, and `day`.

3. Convert `dep_time` and `sched_dep_time` to minutes past midnight.

4. Move columns ending in `"time"` to just before `flight`. Then put `sched` columns before the actual times.

---

## 3. Summarize and group

1. Standard deviation of `dep_delay`.

2. Maximum `dep_delay` by `origin` in one pipeline.

3. For each `day`, the number and proportion of canceled flights (`is.na(dep_delay) | is.na(arr_delay)`). Plot the proportion against day, and against average departure delay.
