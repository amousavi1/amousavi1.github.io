Work in a **Quarto** document. A Quarto `revealjs` deck or an R Markdown HTML presentation (`ioslides_presentation` or `slidy_presentation`) are both fine. Do **12.1** first.

Load packages **silently** (`include = FALSE` or `#| include: false`). You will need `tidyverse` and `nycflights13`. `flights` is already 2013.

```r
library(tidyverse)
library(nycflights13)
```

---

## 1. Cover

A title slide. YAML `title` and `author` are enough. Add a subtitle if you want.

---

## 2. Mean arrival delay by day

A slide that **shows the code** that computes mean `arr_delay` by calendar day from `nycflights13::flights`. Use `make_date(year, month, day)` (lubridate, loaded with tidyverse), then `group_by(date)` and `summarize()`. Save the summary tibble. Print it or `head()` it so a table appears on the slide.

---

## 3. The line plot, no code

A slide that shows a line plot of that daily mean against date. Hide the code (`echo = FALSE`). The plot is the slide.
