![semi_join keeps x rows that match y](files/data-612/graphics/join-semi.png)

![anti_join keeps x rows that do not match y](files/data-612/graphics/join-anti.png)

![One-to-many: a key that repeats in x](files/data-612/graphics/join-one-to-many.png)

![Many-to-many: the same key repeats in both tables](files/data-612/graphics/join-many-to-many.png)

## 1. `semi_join()` and `anti_join()`

A mutating join **adds columns**. A filtering join **keeps or drops rows** of `x` and leaves the columns of `x` alone.

- `semi_join(x, y)` — rows of `x` that have a match in `y`
- `anti_join(x, y)` — rows of `x` that do **not** have a match in `y`

```r
library(tidyverse)
library(nycflights13)

flights |>
  semi_join(planes, by = "tailnum")

flights |>
  anti_join(planes, by = "tailnum")
```

`inner_join(x, y)` also drops unmatched `x` rows, but it **duplicates** an `x` row once per match in `y`. `semi_join()` never duplicates `x`. If you only want "does a match exist?", use `semi_join()`.

`anti_join()` is the diagnostic: destinations with no airport row, planes that never flew, weather hours with no flights.

```r
flights |>
  anti_join(airports, by = c("dest" = "faa")) |>
  distinct(dest)
```

---

## 2. Duplicate keys and many-to-many

If a key appears twice in `x` and three times in `y`, an inner or left join returns six rows for that key. That is a many-to-many join. Sometimes it is what you want; often it is a bad key.

```r
x <- tribble(
  ~key, ~val_x,
     1, "x1",
     1, "x2"
)
y <- tribble(
  ~key, ~val_y,
     1, "y1",
     1, "y2"
)

left_join(x, y, by = "key")
semi_join(x, y, by = "key")
```

The left join has four rows. The semi join still has two — the original `x`. Check keys with `count()` before you join (note 8.1).

---

## 3. Worst delay days, then those flights

Ten days with the highest median `dep_delay`, then every flight on those days. Build a small table of keys, then `semi_join()`.

```r
worst <- flights |>
  group_by(year, month, day) |>
  summarize(med_del = median(dep_delay, na.rm = TRUE), .groups = "drop") |>
  slice_max(med_del, n = 10)

flights |>
  semi_join(worst, by = c("year", "month", "day"))
```

`filter()` with a long `%in%` list is clumsier once the key has several columns.

---

## 4. Plane age and delay

`planes$year` is the year of manufacture. Age in 2013 is `2013 - year`. Join, then plot. Rename `year` first so it does not clash with `flights$year`.

```r
flights |>
  left_join(
    planes |> select(tailnum, plane_year = year),
    by = "tailnum"
  ) |>
  mutate(age = 2013 - plane_year) |>
  filter(!is.na(age), !is.na(dep_delay)) |>
  ggplot(aes(x = age, y = dep_delay)) +
  geom_hex() +
  geom_smooth(se = FALSE) +
  theme_bw()
```

`geom_hex()` needs the `hexbin` package. `geom_smooth()` alone is enough if you do not want the bins.

---

## 5. Practice

1. Destinations in `flights` that are missing from `airports`. How many flights is that?

2. Airports that never appear as a `dest`.

3. The ten days with the highest median `dep_delay`, then all flights on those days.

4. A plot of plane age against `dep_delay`.
