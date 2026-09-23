# Render all DATA 612 lecture .qmd files under files/data-612/lectures/.
# Run from repo root:
#   & "C:\Program Files\R\R-4.6.1\bin\Rscript.exe" scripts/render_612_lectures.R

root <- normalizePath(".")
lectures <- file.path(root, "files", "data-612", "lectures")

pandoc_candidates <- c(
  "C:/Program Files/RStudio/resources/app/bin/quarto/bin/tools/pandoc.exe",
  file.path(Sys.getenv("LOCALAPPDATA"), "Programs/Quarto/bin/tools/pandoc.exe")
)
for (p in pandoc_candidates) {
  if (nzchar(p) && file.exists(p)) {
    Sys.setenv(RSTUDIO_PANDOC = dirname(p))
    break
  }
}

args <- commandArgs(trailingOnly = TRUE)
qmds <- list.files(lectures, pattern = "\\.qmd$", full.names = FALSE)
if (length(args)) {
  qmds <- paste0(args, ".qmd")
}

render_one <- function(qmd_name) {
  stem <- sub("\\.qmd$", "", qmd_name)
  qmd_path <- file.path(lectures, qmd_name)
  fragment_path <- file.path(lectures, paste0(stem, ".fragment.html"))
  fig_rel <- paste0("_figs/", stem, "/")
  dir.create(file.path(lectures, "_figs", stem), showWarnings = FALSE, recursive = TRUE)

  lines <- readLines(qmd_path, warn = FALSE)
  lines <- sub('fig.path = "[^"]+"', paste0('fig.path = "', fig_rel, '"'), lines)

  rmd_path <- file.path(lectures, paste0(stem, ".render.Rmd"))
  writeLines(lines, rmd_path)
  on.exit({
    if (file.exists(rmd_path)) unlink(rmd_path)
    unlink(file.path(lectures, paste0(stem, ".fragment_files")), recursive = TRUE)
  }, add = TRUE)

  ok <- TRUE
  tryCatch(
    {
      rmarkdown::render(
        input = rmd_path,
        output_format = rmarkdown::html_fragment(self_contained = FALSE),
        output_file = paste0(stem, ".fragment.html"),
        output_dir = lectures,
        quiet = TRUE,
        envir = new.env(parent = globalenv())
      )
    },
    error = function(e) {
      ok <<- FALSE
      message("FAILED ", stem, ": ", conditionMessage(e))
    }
  )
  if (!ok || !file.exists(fragment_path)) return(invisible(FALSE))

  html <- paste(readLines(fragment_path, warn = FALSE), collapse = "\n")
  site_fig <- paste0("files/data-612/lectures/_figs/", stem, "/")
  html <- gsub(
    paste0("src=\"(_figs/|\\.\\./)*_figs/", stem, "/"),
    paste0("src=\"", site_fig),
    html,
    perl = TRUE
  )
  html <- gsub(
    paste0("src=\"[^\"]*/_figs/", stem, "/"),
    paste0("src=\"", site_fig),
    html
  )
  html <- sub("<h1[^>]*>.*?</h1>\\s*", "", html, perl = TRUE)
  writeLines(html, fragment_path)
  nfig <- length(list.files(file.path(lectures, "_figs", stem)))
  message("Rendered ", stem, " (", nfig, " figs)")
  invisible(TRUE)
}

for (q in qmds) {
  message("=== ", q, " ===")
  render_one(q)
}
message("Done.")
