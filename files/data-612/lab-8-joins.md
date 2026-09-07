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

---

## 6. Distance from NYC

1. Mean longitude and latitude of the three NYC airports (`EWR`, `JFK`, `LGA`). Treat that as the location of NYC.

2. Write a function `dist_nyc(lon, lat, nyclon, nyclat)` that returns great-circle distance from NYC using `geosphere::distm()`. What unit does `distm()` use?

3. Add that distance to every row of `airports`. Is mean arrival delay at a destination associated with distance from NYC?

---

## 7. Fair-weather takeoffs

For each `tailnum`, the proportion of takeoffs in fair weather: `precip == 0`, `wind_speed < 20`, and `visib >= 10`. Join `weather` on `origin`, `year`, `month`, `day`, and `hour` (`hour` from `dep_time %/% 100`). Is that proportion associated with plane age?
