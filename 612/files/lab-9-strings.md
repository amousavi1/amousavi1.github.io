Work in a **Quarto** document. The parts follow the notes. Do them in order. `words` comes with stringr.

```r
library(tidyverse)

contacts <- tibble(
  line = c(
    "Ada Lovelace <ada@analytical.org> 202-555-0142 born 1815-12-10",
    "Alan Turing <alan@bletchley.uk> 202-555-0199 born 1912-06-23",
    "Grace Hopper <grace@navy.mil> 301-555-0100 born 1906-12-09",
    "notice: do not call 000-000-0000",
    "Katherine Johnson <katherine@nasa.gov> 202-555-0177 born 1918-08-26"
  )
)
```

Turn in the rendered HTML. Each answer should show the code and the printed result.

## Part A. Literal strings (note 9.1)

1. From `full <- "To be or not to be, that is the question."`, use `str_sub()` to pull two pieces and `str_c()` to join them so `writeLines()` prints a two-line quote. The first line is characters 1–18. The second starts at character 21.

2. Replace `"back"` and `"lack"` with `"foo"` in one call. Run it on `c("back", "lack")` and on `c("back", "lack", "black")`. In one sentence, say what happens to `"black"`.

## Part B. Patterns (note 9.2)

Use `words`. Print the matching words.

3. Four-letter words that start with `a`.

4. Words that start with a vowel.

5. Words that end in `ed` but not `eed`.

6. Words that start with three consonants.

On `contacts`:

7. Which lines contain `@`? Use `str_detect()`.

8. Pull the email from each line with `str_extract()`. The notice line should be `NA`.

## Part C. Groups (notes 9.5 and 9.6)

9. Write one pattern for `str_match()` that, on a person line, captures the name, the email, the phone, the year, the month, and the day. The notice line should be a row of missing values.

10. With `str_replace()`, turn each date `YYYY-MM-DD` into `DD/MM/YYYY`.

11. From the phone column in question 9, turn `202-555-0142` into `(202) 555-0142`.

## Part D. Lookaheads (note 9.7)

12. From `fees <- "fee $40, tax $2, qty 3"`, extract the numbers that follow a `$`. The `3` should stay out.

13. Predict, then run `str_extract("50 dollars", "\\d+(?! dollars)")`. In one sentence, say why the result is not `NA`. Then write a pattern that returns `NA` for `"50 dollars"` and `"20"` for `"50 dollars, 20 euros"`.

14. Keep the contact lines that are not a notice. Do it with `str_subset()` and a negative lookahead. Then do the same job with `!str_detect()`, and say which form you would use in a pipeline.
