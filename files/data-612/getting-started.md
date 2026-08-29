## 1. Install R, then RStudio

R is the language. RStudio (Posit) is an editor that makes R easier to use.

Install them in this order:

1. [R](https://www.r-project.org/) for Windows, macOS, or Linux.
2. [RStudio Desktop](https://posit.co/download/rstudio-desktop/).

RStudio will not work properly if R is not installed first.

When you open RStudio, you will typically see several panes:

- the **console**, where R evaluates code immediately
- a **script** editor, where you write code you want to keep
- an environment / history pane
- a files / plots / help pane

---

## 2. The Console

The console is the pane with the `>` prompt.

Type:

```r
1 + 1
```

and press Enter.

R prints:

```r
# [1] 2
```

The `[1]` is not part of the answer. It is the index of the first element R is showing you.

The console is useful for short experiments. It is a poor place to keep your work. When you close RStudio, console history is not a script.

---

## 3. Scripts

A **script** is a text file of R code, usually with a `.R` extension.

Create one with **File → New File → R Script**.

Type this into the script:

```r
x <- 10
x * 2
```

Place the cursor on a line and run it with **Ctrl+Enter** (Windows/Linux) or **Cmd+Enter** (macOS). You can also click **Run**.

The code is sent to the console, and the console shows the result.

A useful habit is:

> Type in a script. Run from the script. Treat the console as a scratch pad.

Save the script. You can reopen it in a later session.

---

## 4. Comments

R ignores anything after `#` on a line:

```r
# This line is only for humans.

x <- 10   # store 10 in x
```

Comments are how you explain *why* you wrote something, not how you hide code you might need later.

---

## 5. Assignment

We store a value with `<-`:

```r
greeting <- "Hello"
greeting
```

In this course:

- `<-` stores a value in an object
- `=` names an argument inside a function call, for example `mean(x, na.rm = TRUE)`

---

## 6. Where Are Your Files?

R reads and writes files relative to the **working directory**.

```r
getwd()
```

In RStudio you can also use **Session → Set Working Directory**.

For a course project, a better habit is **File → New Project**. An RStudio project keeps the working directory attached to that folder, so `read.csv("students.csv")` works when the file is in the project folder.

If `read.csv("students.csv")` fails, the usual reason is that the file is not in the working directory.

---

## 7. Errors Are Information

If R cannot run a line, it prints an error. Read it from the top.

Common first-week mistakes include:

- a missing quotation mark
- a missing parenthesis
- running `install.packages(ggplot2)` without quotes
- calling a function from a package you have not loaded

You do not need to memorize every error. You do need to read it.

---

## 8. What to Do Next

Once R and RStudio are installed and you can run a line from a script, continue with:

- **1.1** R Packages and the Tidyverse
- **1.2** Introduction to R Concepts
- **Lab 1**, which asks you to predict what R will do *before* you run the code
