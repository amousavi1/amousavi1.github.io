Work in a **Quarto** document. Do **8.1** and **8.2** first.

```r
library(tidyverse)
library(nycflights13)
```

---

## 1. The five tables

Load `flights`, `planes`, `airlines`, `airports`, and `weather`. For each table, name a primary key (or say that there is none). Check uniqueness with `count()` and `filter(n > 1)`.

---

## 2. Destinations and airports

1. How many distinct `dest` values are in `flights`?

2. Destinations that do not appear in `airports` (`anti_join` with `dest` = `faa`). How many flights is that?

3. Airports that never appear as a destination.

4. The ten most common destinations: FAA code, airport name, and flight count.

---

## 3. Delay by timezone

Join `airports` onto `flights` by destination. Mean `arr_delay` by `tzone`. Plot it.

---

## 4. Worst delay days

The ten days with the highest median `dep_delay`. Then `semi_join()` to keep every flight on those days.

---

## 5. Plane age and delay

Join `planes`. Age is `2013 - year` of manufacture. Plot age against `dep_delay` (`geom_hex()` or `geom_smooth()`).
