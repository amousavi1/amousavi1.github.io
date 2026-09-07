## 1. Parse after the file is in

Sometimes `read_csv()` guesses a character column because one bad token spoiled the first 1,000 rows. `parse_*()` converts a character vector in place. The same parsers sit behind `col_types`.

```r
library(tidyverse)

dfdat <- tribble(
  ~date,        ~time,      ~number, ~factor, ~logical,
  "12-01-1988", "10:10:02", "2",     "A",     "TRUE",
  "11-12-1987", "11:10:57", "4",     "A",     "TRUE",
  "02-03-1989", "10:10:25", "6",     "B",     "FALSE",
  "06-03-1982", "22:10:55", "2",     "B",     "TRUE",
  "09-21-1981", "10:10:02", "1",     "A",     "N-A"
)
```

---

## 2. Dates and times

`parse_date()` expects `"YYYY-MM-DD"` unless you set `format`. `parse_datetime()` includes a time zone.

```r
parse_date("2018-01-02")
parse_date("02/01/2018")                    # fails
parse_date("02/01/2018", format = "%m/%d/%Y")
parse_date("January 1, 2018", format = "%B %d, %Y")

dfdat |> mutate(date = parse_date(date, format = "%m-%d-%Y"))
```

Useful tokens: `%d` day, `%m` month number, `%b` Jan, `%B` January, `%y` two-digit year, `%Y` four-digit year.

Times: `%H` 0–23, `%I` 1–12 with `%p` for am/pm, `%M` minutes, `%S` seconds.

```r
dfdat |> mutate(time = parse_time(time, format = "%H:%M:%S"))
parse_time("10:40 pm", format = "%I:%M %p")
```

---

## 3. Numbers, logicals, factors

`parse_double()` and `parse_integer()` fail on `$` or `%`. `parse_number()` strips the extra characters.

```r
parse_double("$2.11")     # fail
parse_number("$2.11")
parse_number("2%")
parse_number("2.555,11", locale = locale(grouping_mark = ".", decimal_mark = ","))
```

`parse_logical()`, `parse_factor()`, `parse_character()`. Any parser accepts `na = "N-A"` or a vector of missing tokens.

```r
dfdat |> mutate(logical = parse_logical(logical, na = "N-A"))
```

---

## 4. `col_types` at import

Guessing from the first 1,000 rows is fast and can be wrong. Set types when you know them. The letters are wrappers for the parsers: `c` character, `i` integer, `d` double, `l` logical, `f` factor, `D` date, `T` datetime, `t` time, `_` skip.

```r
estate <- read_csv("data/estate.csv")
estate <- read_csv(
  "data/estate.csv",
  col_types = cols(price = col_double(), ac = col_logical())
)
```

`problems(estate)` lists rows that did not parse.

---

## 5. Practice

1. Parse `"01, January 2018"`, `"01-January/2000"`, and `"1 Jan 19"`.

2. Parse `"10:40 pm"` and `"23:40-22"`.
