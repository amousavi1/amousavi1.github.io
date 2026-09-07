Work in a **Quarto** document. Do notes **14.1** and **14.2** first.

```r
library(tidyverse)
```

`diamonds` is in ggplot2. `geom_hex()` needs the `hexbin` package for the optional plot.

---

## 1. A sampling distribution

1. Draw 1000 samples of size 30 from `rexp(n = 30, rate = 1)`. Store the mean of each sample. Use a **for-loop** and pre-allocate the vector of means. Histogram the 1000 means.

2. The same 1000 means with `map_dbl()`.

3. The same 1000 means with `replicate()`.

4. Repeat the `replicate()` version for `n` in `c(5, 50, 100, 500)`. Histogram each set of means. Write two sentences about how the shape changes as `n` grows.

---

## 2. Diamonds

1. Summary of every numeric column of `diamonds` with purrr, then again with `across()`. What is different about the two results?

2. `split()` by `color`. Fit `lm(price ~ depth)` in each piece. Extract the p-value for `depth` and the adjusted R-squared.

3. Optional: a hex plot of `depth` vs `price`, faceted by `color`, with an OLS line. Do the p-values and R-squared values match what the panels look like?
