Work in a **Quarto** document. Number the exercises. Keep the plots. Do **3.1** through **3.3** first. You will need `ggplot2` (from `library(tidyverse)`), `mpg`, `iris`, and `diamonds`.

```r
library(tidyverse)
data("mpg")
data("iris")
data("diamonds")
```

---

## 1. Mappings

1. What happens when you map a categorical variable to `size` or `alpha`? Try it on `mpg` with `drv`. Write one sentence about whether the mapping is a good idea.

2. Look at `head(iris)`. Name the variables and say whether each is quantitative or categorical.

3. Scatterplot petal length vs petal width, colored by species. What do you notice?

4. What happens when you map a quantitative variable to `shape`? Try `shape = cty` on an `mpg` scatterplot of `displ` vs `hwy`.

5. On `iris`, plot petal length vs petal width, and also map species, sepal length, and sepal width. Is the plot still readable?

---

## 2. Smooths and overplotting

1. Scatterplot petal length vs petal width. Color the points by species. Add **one** linear smooth (`method = lm`, `se = FALSE`) that does not use species.

2. Plot `price` vs `carat` in `diamonds`. Show the overplotted version and a version that you can actually read.

---

## 3. Distributions and boxplots

1. Histogram of diamond `price`, filled by `cut`. Try `bins = 50`.

2. Boxplot of `price` vs `cut` on a log-`y` scale. Does anything surprise you? Add a second plot that helps explain it.

---

## 4. Facets, theme, and save

1. Boxplots of `price` vs `cut`, log-`y`, faceted by `color`.

2. Same plot: orange fill, `theme_bw()`.

3. Save the plot from (2) with `ggsave()`. Put it in a folder you already have. `ggsave()` overwrites without asking.
