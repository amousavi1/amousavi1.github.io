Work in a **Quarto** document. Do **9.1** and **9.2** first. `words` comes with stringr.

```r
library(tidyverse)
```

---

## 1. Pieces and replacement

1. From `full <- "To be or not to be, that is the question."`, use `str_sub()` to pull two pieces and `str_c()` to join them so `writeLines()` prints a two-line quote.

2. Replace `"back"` and `"lack"` with `"foo"` in one call. Run it on `c("back", "lack")` and on `c("back", "lack", "black")`.

---

## 2. Regular expressions

Use `words`. For each item, print the matching words.

1. Four-letter words that start with `a`.

2. Words that start with a vowel.

3. Words that end in `ed` but not `eed`.

4. Words that start with three consonants.

5. Words that end in a consonant.

6. Words that end in `ing` or `ise`.

7. Words with two or more vowel-consonant pairs in a row (`[aeiou][^aeiou]` twice).
