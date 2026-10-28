## 1. A pattern is a regular expression

Note 9.1 used literal text. A **regular expression** describes a set of strings. `stringr` (through `stringi`) uses ICU regex. Write the pattern as an ordinary R string, so backslashes double: the regex `\.` is `"\\."` in R.

`words` is 980 common English words that come with stringr. Use it for the examples.

```r
library(tidyverse)

str_view(words, "ie")
```

`str_view()` shows the match. It is the fastest way to test a pattern.

---

## 2. The language, in pieces

`.` matches any single character (except a newline). Escape it when you want a real dot: `"\\."`.

```r
str_view(c("abc", "a.c", "ac"), "a.c")
str_view(c("abc", "a.c", "ac"), "a\\.")
```

`^` is the start of the string. `$` is the end.

```r
str_view(words, "^a")
str_view(words, "x$")
str_view(words, "^apple$")
```

A **character class** matches one character from a set: `[abc]`, `[a-z]`, `[0-9]`. `[^aeiou]` is “not a vowel.” `[^ ]` is “not a space.”

```r
str_view(words, "^[aeiou]")
str_view(c("a b", "ab"), "[^ ]")
```

`(?i)` at the front makes the rest of the pattern case-insensitive.

```r
str_detect(c("Apple", "BANANA", "pear"), "(?i)^a")
```

Repetition sits after the thing it repeats:

- `?` — 0 or 1
- `+` — 1 or more
- `*` — 0 or more
- `{n}` — exactly n
- `{n,}` — n or more
- `{n,m}` — between n and m

```r
str_view(words, "^a.{3}$")
str_view(c("color", "colour"), "colou?r")
```

Parentheses make a **group**. `\\1` is “whatever group 1 matched.” Note 4.2 used `matches("(.)\\1")` in `select()`. That is a repeated character.

```r
str_view(words, "(.)\\1")
str_replace("apple", "(.)(.)", "\\2\\1")
```

---

## 3. Capturing groups, non-capturing groups, and lookaheads

Note 9.5 is the full lesson, with more cases and practice questions. The examples here are the ones to work in class.

### Capturing groups `(...)`

A capturing group saves the text it matched. `str_match()` puts the whole match in column 1, then one column for each group, from left to right.

```r
str_match("John123", "([A-Za-z]+)([0-9]+)")
```

Column 2 is the letters. Column 3 is the digits.

```r
str_match(c("Alice45", "Bob789", "Sam"), "([A-Za-z]+)([0-9]+)")
```

`"Sam"` has letters but no digits, so that row is missing.

```r
str_match("2026-10-28", "(\\d{4})-(\\d{2})-(\\d{2})")
```

The three groups are the year, the month, and the day.

### Non-capturing groups `(?:...)`

`(?:...)` matches, and it does not get a column. It also does not count when you number `\\1` and `\\2`.

```r
str_match("John123", "(?:[A-Za-z]+)([0-9]+)")
str_match("John123", "([A-Za-z]+)(?:[0-9]+)")
```

The first pattern keeps only the digits. The second keeps only the name. The whole match is still `"John123"`.

```r
str_detect(c("gray", "grey", "green"), "gr(?:a|e)y")
```

`(?:a|e)` is `a` or `e`. `gray` and `grey` match. `green` does not. `str_detect()` returns true or false, so there is no column to capture.

### Positive lookahead `(?=...)`

`(?=...)` checks what comes next. It does not take those characters, and it does not move past them.

```r
str_extract(c("cat123", "catABC", "dog9"), "cat(?=[0-9])")
```

`"cat123"` is `cat` followed by a digit, so the match is `"cat"`. `"catABC"` is `cat` followed by a letter, so it fails. `"dog9"` has no `cat`.

```r
str_extract(c("50 dollars", "50 cents", "7 dollars"), "\\d+(?= dollars)")
```

The match is the number. `(?= dollars)` only checks that the word `dollars` comes next. `"50 cents"` fails that check.

```r
str_extract(c("notes.pdf", "notes.docx", "plot.pdf"), "\\w+(?=\\.pdf)")
```

The match is the file name. `(?=\\.pdf)` checks for a literal `.pdf` and does not take it. `"notes.docx"` fails that check.

A pattern that takes the next character keeps it:

```r
str_extract("cat123", "cat[0-9]")
str_extract("cat123", "cat(?=[0-9])")
```

The first result is `"cat1"`. The second is `"cat"`.

### Negative lookahead `(?!...)`

`(?!...)` checks that a pattern does not come next. It does not take any characters.

```r
str_detect(c("cat", "catalog", "dog", "bird"), "^(?!cat)")
```

`FALSE` means the string starts with `cat`. `"catalog"` fails for the same reason: it starts with `cat`. `"dog"` and `"bird"` do not.

```r
str_extract(c("cat", "cats", "dog"), "cat(?!s)")
```

`"cat"` is not followed by `s`, so it matches. `"cats"` is `cat` followed by `s`, so the check fails. `"dog"` has no `cat`.

```r
str_detect(c("all good", "an error here", "no problem"), "^(?!.*error).*$")
```

`(?!.*error)` fails when `error` appears anywhere later in the string. The other two strings match.

A group, capturing or not, is part of the match. A lookahead only tests a condition.

---

## 4. Detect, count, extract, split, replace

All of these take the vector first, then the pattern.

```r
x <- c("apple", "banana", "pear", "mango")

str_detect(x, "a")
x[str_detect(x, "^p")]
str_subset(x, "^p")

str_count(x, "a")
str_count("abababa", "aba")

str_extract(x, "[aeiou]")
str_extract_all(x, "[aeiou]")

str_split("a-b-c", "-")
str_replace(x, "[aeiou]", "-")
str_replace_all(x, "[aeiou]", "-")
```

`str_count()` counts **non-overlapping** matches. `"aba"` in `"abababa"` is 2, not 3.

`str_extract()` is the first match. `str_extract_all()` is every match, as a list.

`str_subset(x, pattern)` is `x[str_detect(x, pattern)]`.

---

## 5. `separate()` with a regex

`tidyr::separate()` splits one column into several. `sep` can be a regex, not only a fixed character.

```r
tibble(x = c("a-1", "b.2", "c 3")) |>
  separate(x, into = c("letter", "num"), sep = "[^[:alnum:]]")
```

`[^[:alnum:]]` is any character that is not a letter or a digit: a hyphen, a dot, or a space.

---

## 6. Practice

Use `words`. Print the matches (or `str_view()` them).

1. Four-letter words that start with `a`.

2. Words that start with a vowel.

3. Words that end in `ed` but not `eed`.

4. Words that start with three consonants.
