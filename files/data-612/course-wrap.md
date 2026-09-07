## 1. The lifecycle

A data analysis is a loop, not a straight line:

1. a question
2. tidy the table
3. plot
4. model
5. communicate

You go around more than once. A plot changes the question. A model sends you back to the table. The last step is a document someone else can rerun.

---

## 2. Tools you have now

| Job | What you reach for |
| --- | ------------------ |
| Rows, columns, groups | dplyr verbs, `across()`, `case_when()` |
| Pictures | ggplot2 |
| Files in and out | readr |
| Wider / longer tables | tidyr |
| Two tables | joins |
| Strings, factors, dates | stringr, forcats, lubridate |
| A mean difference or a line | `t.test()`, `lm()` |
| A writeup | Quarto / R Markdown |

Iteration — loops and `purrr::map` — is the last verb: do the same thing to many pieces.

---

## 3. Last lesson

Iterate. Save the file. Render again. The competence is not one clever plot. It is being able to change a step and get a new document that still runs.

You already have the verbs. Week 14 is the habit of applying them to many pieces at once.

---

## 4. Practice

Write five bullets of work you can do now that you could not do in week 1. Be specific (a verb and a data set), not "I learned R."
