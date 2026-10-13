## 1. `select()` keeps columns

```r
flights |> select(dep_delay, arr_delay)
flights |> select(year:carrier)
flights |> select(-dep_delay, -arr_delay)
flights |> select(-(year:day))
```

Helpers (from tidyselect) match **names**:

- `starts_with("dep")`
- `ends_with("delay")`
- `contains("arr_")`
- `matches("(.)\\1")` — a regular expression; we will do those in the strings week
- `num_range("x", 1:3)` — `x1`, `x2`, `x3`

```r
flights |> select(ends_with("delay"))
flights |> select(starts_with("dep"), year, month, day)
```

`select()` talks about **names** (or positions). Bare names are allowed. Quoted names are also allowed: `select(flights, c("carrier", "tailnum"))`.

---

## 2. `rename()`

`rename(new = old)`. The old name goes away.

```r
flights |> rename(departure_time = dep_time)
```

---

## 3. `mutate()` and `transmute()`

`mutate()` adds or overwrites columns. New columns go on the right unless you set `.before` or `.after`. Use `=` inside `mutate()`, not `<-`.

```r
flights |>
  mutate(
    gain = dep_delay - arr_delay,
    speed = distance / air_time * 60
  ) |>
  select(year:day, gain, speed)

flights |>
  mutate(distance = distance * 1.60934)
```

`transmute()` keeps only the new columns.

Nothing is saved until you assign:

```r
flights_k <- flights |>
  mutate(distance_km = distance * 1.60934)
```

`mutate()` talks about **vectors**. The name `dep_time` means the whole column, not the string `"dep_time"`.

A useful conversion: `dep_time` is stored as 517 for 5:17. Minutes past midnight are `hours * 60 + minutes`:

```r
flights |>
  mutate(
    dep_h = dep_time %/% 100,
    dep_m = dep_time %% 100,
    dep_elapsed_min = dep_h * 60 + dep_m
  )
```

`%/%` is integer division. `%%` is the remainder.

---

## 4. `relocate()`

Same selection language as `select()`. Default is the left side. `.before` and `.after` place the block.

```r
flights |> relocate(origin:dest)
flights |> relocate(starts_with("d"), .after = day)
flights |> relocate(where(is.character))
```

---

## 5. Practice

1. Keep `origin` and `dest` two ways.

2. Keep every arrival column plus `year`, `month`, and `day`. Use as few characters as you can.

3. Convert `dep_time` and `sched_dep_time` to minutes past midnight. Assign the result if you want to keep it.

4. Move columns that end with `"time"` to just before `flight`. Then put the `sched` columns before the actual times.
