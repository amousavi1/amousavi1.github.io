Work in a **Quarto** document. Do **10.1** and **10.2** first. Put `wmata_ridership.csv` in a `data/` folder of your project (see the Data section of the course page).

```r
library(tidyverse)
library(lubridate)
```

---

## 1. Factors

```r
fc <- factor(c("D","C","C","A","A","C","D","A","C","C","A","A","C","A","C","B","C","A","C","B"))
```

1. Add level `"E"` without adding any observations.

2. Bar chart of `fc` by frequency, most frequent on the **right**.

3. Put the levels in reverse alphabetical order.

4. Remove the observations that are `"C"`, then drop the unused level.

5. Collapse `"A"` and `"B"` into `"z"`.

---

## 2. Dates

Use `data/wmata_ridership.csv`.

1. Parse `Date`. Add `year`, `month`, and `wday` columns with `label = TRUE` where it applies.

2. Drop 2004.

3. Boxplot of daily `Total` by weekday.

4. How long is the span as a duration and as an interval?

---

## 3. Capital Bikeshare (sample)

Use `data/capital_trips_sample.csv` (a short extract of the 2016 trips file). Column names have spaces.

1. `glimpse()` the file. Rename columns so they have no spaces.

2. Parse start and end with `mdy_hm()`.

3. Compute trip duration from start and end. Compare it to `duration_ms`. Where do they disagree by about an hour?

4. Those hour-scale gaps sit on 13 March 2016 (spring-forward). `force_tz(..., tzone = "America/New_York")` on both times, then recompute.

5. Time from the first start to the last end, as a duration.

6. Plot duration against hour of day.
