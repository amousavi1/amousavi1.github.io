# Render ggplot lecture .qmd files to HTML fragments (+ figures).
# Run from the repo root.

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

jobs <- list(
  list(stem = "ggplot2-grammar", fig = "grammar"),
  list(stem = "ggplot2-geoms", fig = "geoms"),
  list(stem = "ggplot2-facets-themes", fig = "facets")
)

render_one <- function(job) {
  qmd_path <- file.path(lectures, paste0(job$stem, ".qmd"))
  fragment_path <- file.path(lectures, paste0(job$stem, ".fragment.html"))
  # Relative to the Rmd (in lectures/), so figures land in lectures/_figs/<fig>/
  fig_rel <- paste0("_figs/", job$fig, "/")
  dir.create(file.path(lectures, "_figs", job$fig), showWarnings = FALSE, recursive = TRUE)

  lines <- readLines(qmd_path, warn = FALSE)
  lines <- sub(
    'fig.path = "files/data-612/lectures/_figs/[^"]+/"',
    paste0('fig.path = "', fig_rel, '"'),
    lines
  )
  # Also handle already-relative fig.path in qmd if we change sources later
  lines <- sub(
    'fig.path = "_figs/[^"]+/"',
    paste0('fig.path = "', fig_rel, '"'),
    lines
  )

  rmd_path <- file.path(lectures, paste0(job$stem, ".render.Rmd"))
  writeLines(lines, rmd_path)
  on.exit({
    if (file.exists(rmd_path)) unlink(rmd_path)
    unlink(file.path(lectures, paste0(job$stem, ".fragment_files")), recursive = TRUE)
  }, add = TRUE)

  rmarkdown::render(
    input = rmd_path,
    output_format = rmarkdown::html_fragment(self_contained = FALSE),
    output_file = paste0(job$stem, ".fragment.html"),
    output_dir = lectures,
    quiet = TRUE,
    envir = new.env(parent = globalenv())
  )

  html <- paste(readLines(fragment_path, warn = FALSE), collapse = "\n")
  # Site pages live at repo root, so rewrite figure URLs.
  site_fig <- paste0("files/data-612/lectures/_figs/", job$fig, "/")
  html <- gsub(
    paste0("src=\"(_figs/|\\.\\./)*_figs/", job$fig, "/"),
    paste0("src=\"", site_fig),
    html,
    perl = TRUE
  )
  html <- gsub(
    paste0("src=\"[^\"]*/_figs/", job$fig, "/"),
    paste0("src=\"", site_fig),
    html
  )
  html <- sub("<h1[^>]*>.*?</h1>\\s*", "", html, perl = TRUE)
  writeLines(html, fragment_path)
  message("Rendered ", job$stem, " (", length(list.files(file.path(lectures, "_figs", job$fig))), " figs)")
}

for (job in jobs) render_one(job)
message("Done.")
