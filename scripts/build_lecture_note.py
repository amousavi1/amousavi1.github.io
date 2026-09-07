"""Build DATA 612 lecture and lab pages and PDFs from the markdown sources."""

from __future__ import annotations

import pathlib
import re
import subprocess
import sys

try:
    import markdown
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "markdown"])
    import markdown

ROOT = pathlib.Path(__file__).resolve().parents[1]
EDGE = pathlib.Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")

LAST_UPDATED_ISO = "2026-09-07T16:50:00-04:00"
LAST_UPDATED_TEXT = "September 7, 2026, 4:50 PM EDT"

NOTES = [
    {
        "slug": "getting-started",
        "week": 1,
        "title": "1.1 Getting Started with R and RStudio",
        "lead": "Install R and RStudio, run a script, and open a project so R can find your files.",
    },
    {
        "slug": "r-packages-and-the-tidyverse",
        "week": 1,
        "title": "1.2 R Packages and the Tidyverse",
        "lead": "Installing packages, loading them, the tidyverse, and the pipe.",
    },
    {
        "slug": "files-and-paths",
        "week": 1,
        "title": "1.3 Working with Files and Paths",
        "lead": "Find a file, tell R where it is, import it, and save the result.",
    },
    {
        "slug": "introduction-to-r-concepts",
        "week": 1,
        "title": "1.4 Introduction to R Concepts",
        "lead": "Data types, data structures, indexing, functions, and special values.",
    },
    {
        "slug": "r-markdown-and-quarto",
        "week": 1,
        "title": "1.5 R Markdown and Quarto",
        "lead": "Prefer Quarto for new writeups. YAML is the control panel; chunk options decide what the reader sees.",
    },
    {
        "slug": "lab-1-looking-under-the-hood",
        "week": 1,
        "title": "Lab 1: Looking Under the Hood of R",
        "lead": "Predict, then run. The point is to catch R in the act.",
    },
    {
        "slug": "pipes",
        "week": 2,
        "title": "2.1 Pipes",
        "lead": "Read the pipe as then. Chain steps instead of nesting calls or leaving extra objects in the environment.",
    },
    {
        "slug": "writing-functions",
        "week": 2,
        "title": "2.2 Writing Functions",
        "lead": "Write a function when you repeat a calculation. Test it, check the inputs, and document it.",
    },
    {
        "slug": "r-scripts",
        "week": 2,
        "title": "2.3 R Scripts",
        "lead": "Put reusable functions in a .R file and source() them so you are not copy-pasting.",
    },
    {
        "slug": "lab-2-pipes-functions",
        "week": 2,
        "title": "Lab 2: Pipes, Functions, and Conditionals",
        "lead": "Use a pipe, then write a function with a conditional and a check on the inputs.",
    },
    {
        "slug": "ggplot2-grammar",
        "week": 3,
        "title": "3.1 ggplot2: The Grammar of Graphics",
        "lead": "A plot is data, a mapping, and a geom. ggplot() is the canvas; + adds a layer.",
    },
    {
        "slug": "ggplot2-geoms",
        "week": 3,
        "title": "3.2 ggplot2: Geoms",
        "lead": "Choose the geom from the variables: points, smooths, histograms, densities, boxplots.",
    },
    {
        "slug": "ggplot2-facets-themes",
        "week": 3,
        "title": "3.3 ggplot2: Facets, Themes, and Saving",
        "lead": "Facet to add a category, set a theme and a scale, then ggsave() the object.",
    },
    {
        "slug": "lab-3-ggplot2",
        "week": 3,
        "title": "Lab 3: Graphics with ggplot2",
        "lead": "Map, smooth, fix overplotting, and save a faceted boxplot.",
    },
    {
        "slug": "dplyr-rows",
        "week": 4,
        "title": "4.1 dplyr: Rows",
        "lead": "filter(), slice(), and arrange() choose and order rows. Use nycflights13::flights.",
    },
    {
        "slug": "dplyr-columns",
        "week": 4,
        "title": "4.2 dplyr: Columns",
        "lead": "select(), rename(), mutate(), and relocate() keep, name, and create columns.",
    },
    {
        "slug": "dplyr-groups",
        "week": 4,
        "title": "4.3 dplyr: Groups and Summaries",
        "lead": "group_by() marks groups. summarize() collapses them. Always keep n().",
    },
    {
        "slug": "lab-4-dplyr",
        "week": 4,
        "title": "Lab 4: dplyr, Part 1",
        "lead": "Filter, slice, arrange, select, mutate, and summarize flights.",
    },
    {
        "slug": "dplyr-rowwise-across",
        "week": 5,
        "title": "5.1 dplyr: rowwise() and across()",
        "lead": "rowwise() summarizes across columns in one row. across() repeats a function on many columns.",
    },
    {
        "slug": "dplyr-case-when",
        "week": 5,
        "title": "5.2 dplyr: case_when() and Distinct Rows",
        "lead": "case_when() replaces nested if_else(). distinct() and rownames_to_column() clean identifiers.",
    },
    {
        "slug": "lab-5-dplyr",
        "week": 5,
        "title": "Lab 5: dplyr, Part 2",
        "lead": "Row-wise maxima, across(), case_when(), and row names.",
    },
    {
        "slug": "readr-import",
        "week": 6,
        "title": "6.1 readr: Import and Export",
        "lead": "read_lines() then read_csv(). Check types and NAs. write_csv() or saveRDS() to send data back out.",
    },
    {
        "slug": "readr-parsers",
        "week": 6,
        "title": "6.2 readr: Parsers",
        "lead": "parse_date(), parse_number(), and col_types when the import guess is wrong.",
    },
    {
        "slug": "eda-strategy",
        "week": 6,
        "title": "6.3 Exploratory Data Analysis",
        "lead": "One variable, then pairs, then a third variable. Plot before you trust a summary.",
    },
    {
        "slug": "lab-6-readr-eda",
        "week": 6,
        "title": "Lab 6: Import, Parse, and Explore",
        "lead": "Load the hate-crime files, parse a few strings, and explore diamonds.",
    },
]

SIDEBAR = """            <div class="sidebar sticky">
                <div itemscope itemtype="https://schema.org/Person">
                    <div class="author__avatar">
                        <img src="assets/images/ahmad-profile.png" alt="Ahmad Mousavi" itemprop="image" />
                    </div>
                    <div class="author__content">
                        <h3 class="author__name" itemprop="name">Ahmad Mousavi</h3>
                        <p class="author__bio" itemprop="description">
                            Assistant Prof. of Data Science,<br />
                            Dept. of Math. and Stat.,<br />
                            American University
                        </p>
                    </div>
                    <div class="author__urls-wrapper">
                        <button type="button" class="btn btn--inverse">Follow</button>
                        <ul class="author__urls social-icons">
                            <li>
                                <a href="mailto:mousavi@american.edu">
                                    <i class="fas fa-fw fa-envelope-square" aria-hidden="true"></i>
                                    <span class="label">Email</span>
                                </a>
                            </li>
                            <li>
                                <a href="https://scholar.google.com/citations?user=IStw0S4AAAAJ&amp;hl=en" target="_blank" rel="noopener">
                                    <i class="ai ai-google-scholar-square ai-fw" aria-hidden="true"></i>
                                    <span class="label">Google Scholar</span>
                                </a>
                            </li>
                            <li>
                                <a href="https://www.linkedin.com/in/ahmad-mousavi-635986b0/" target="_blank" rel="noopener">
                                    <i class="fab fa-fw fa-linkedin" aria-hidden="true"></i>
                                    <span class="label">LinkedIn</span>
                                </a>
                            </li>
                            <li>
                                <a href="https://orcid.org/0000-0003-4518-5857" target="_blank" rel="noopener">
                                    <i class="ai ai-orcid-square ai-fw" aria-hidden="true"></i>
                                    <span class="label">ORCID</span>
                                </a>
                            </li>
                            <li>
                                <a href="https://www.researchgate.net/profile/Ahmad-Mousavi-5?ev=hdr_xprf" target="_blank" rel="noopener">
                                    <i class="ai ai-researchgate-square ai-fw" aria-hidden="true"></i>
                                    <span class="label">ResearchGate</span>
                                </a>
                            </li>
                            <li>
                                <a href="https://github.com/amousavi1" target="_blank" rel="noopener">
                                    <i class="fab fa-fw fa-github" aria-hidden="true"></i>
                                    <span class="label">GitHub</span>
                                </a>
                            </li>
                            <li>
                                <a href="https://www.american.edu/cas/faculty/mousavi.cfm" target="_blank" rel="noopener">
                                    <i class="fas fa-fw fa-university" aria-hidden="true"></i>
                                    <span class="label">AU Profile</span>
                                </a>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>"""

PRINT_CSS = """
@page { size: letter; margin: 0.72in 0.78in 0.78in; }
html, body { margin: 0; padding: 0; }
body {
  font-family: "Segoe UI", "Helvetica Neue", Helvetica, Arial, sans-serif;
  font-size: 11pt;
  line-height: 1.45;
  color: #111;
}
.kicker { margin: 0 0 0.35em; color: #444; font-size: 10.5pt; }
h1 {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 20pt;
  line-height: 1.2;
  margin: 0 0 0.85em;
}
h2 {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 14pt;
  margin: 1.35em 0 0.45em;
  page-break-after: avoid;
}
h3 {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 12pt;
  margin: 1em 0 0.35em;
  page-break-after: avoid;
}
p, li { margin: 0.45em 0; }
ul, ol { padding-left: 1.25em; }
pre {
  font-family: Consolas, "Courier New", monospace;
  font-size: 9.4pt;
  line-height: 1.4;
  background: #f3f3f3;
  border: 1px solid #ddd;
  padding: 0.65em 0.75em;
  white-space: pre-wrap;
  page-break-inside: avoid;
}
code {
  font-family: Consolas, "Courier New", monospace;
  font-size: 0.92em;
}
:not(pre) > code {
  background: #f3f3f3;
  padding: 0.05em 0.25em;
}
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 10pt;
  margin: 0.7em 0;
  page-break-inside: avoid;
}
th, td {
  border-bottom: 1px solid #ccc;
  padding: 0.28em 0.4em;
  text-align: left;
  vertical-align: top;
}
blockquote {
  margin: 0.6em 0;
  padding-left: 0.8em;
  border-left: 3px solid #bbb;
  color: #333;
}
hr { border: none; border-top: 1px solid #ddd; margin: 1.2em 0; }
"""


def markdown_to_html(text: str) -> str:
    html = markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "sane_lists"],
    )
    html = re.sub(r"<table>", '<div class="table-wrap"><table>', html)
    html = re.sub(r"</table>", "</table></div>", html)
    return html


def write_site_page(note: dict, body: str) -> pathlib.Path:
    slug = note["slug"]
    title = note["title"]
    lead = note["lead"]
    week = note["week"]
    pdf_href = f"files/data-612/{slug}.pdf"
    page_path = ROOT / f"data-612-{slug}.html"
    page = f"""<!doctype html>
<html lang="en" class="no-js">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>{title} - DATA 612 - Ahmad Mousavi</title>
        <link rel="stylesheet" href="assets/css/main.css" />
        <link rel="stylesheet" href="assets/css/site.css" />
        <link rel="stylesheet" href="assets/css/academicons.css" />
    </head>
    <body class="layout--single page-courses page-lecture">
        <nav class="skip-links">
            <a href="#main" class="screen-reader-shortcut">Skip to content</a>
        </nav>

        <div class="masthead">
            <div class="masthead__inner-wrap">
                <nav id="site-nav" class="greedy-nav masthead-nav-bar" aria-label="Primary">
                    <a class="site-title" href="index.html">Ahmad Mousavi</a>
                    <ul class="visible-links">
                        <li class="masthead__menu-item"><a href="index.html">Bio</a></li>
                        <li class="masthead__menu-item"><a href="news.html">News</a></li>
                        <li class="masthead__menu-item"><a href="research.html">Research</a></li>
                        <li class="masthead__menu-item"><a href="publications.html">Publications</a></li>
                        <li class="masthead__menu-item"><a href="teaching.html">Teaching</a></li>
                        <li class="masthead__menu-item"><a href="courses.html" class="active">Courses</a></li>
                        <li class="masthead__menu-item"><a href="cv.html">CV</a></li>
                    </ul>
                    <button id="theme-toggle" type="button" aria-label="Toggle theme">
                        <i id="theme-icon" class="fas fa-sun" aria-hidden="true"></i>
                    </button>
                </nav>
            </div>
        </div>

        <div id="main" role="main">
{SIDEBAR}

            <article class="page" itemscope itemtype="https://schema.org/LearningResource">
                <div class="page__inner-wrap">
                    <header>
                        <h1 id="page-title" class="page__title" itemprop="name">{title}</h1>
                    </header>
                    <section class="page__content" itemprop="text">
                        <p class="lecture-meta">
                            <a href="data-612.html">DATA 612</a> &middot; Week {week} &middot;
                            <a href="{pdf_href}" target="_blank" rel="noopener">PDF</a>
                        </p>
                        <p>
                            {lead}
                        </p>
{body}
                    </section>
                </div>
            </article>
        </div>

        <div class="page__footer">
            <footer>
                <div class="page__footer-copyright">&copy; 2026 Ahmad Mousavi</div>
                <div class="page__footer-updated">Last updated: <time class="js-site-last-updated" datetime="{LAST_UPDATED_ISO}">{LAST_UPDATED_TEXT}</time></div>
            </footer>
        </div>

        <script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token": "__CF_BEACON_TOKEN__"}}'></script>
        <script src="assets/js/site.js"></script>
    </body>
</html>
"""
    page_path.write_text(page.replace("\r\n", "\n"), encoding="utf-8", newline="\n")
    return page_path


def write_print_page(note: dict, md_path: pathlib.Path) -> pathlib.Path:
    print_path = ROOT / "files" / "data-612" / f"_print-{note['slug']}.html"
    print_body = markdown_to_html(md_path.read_text(encoding="utf-8"))
    print_body = print_body.replace('<div class="table-wrap">', "").replace("</div>", "")
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>{note["title"]}</title>
  <style>{PRINT_CSS}</style>
</head>
<body>
  <p class="kicker">DATA 612 &middot; Statistical Programming in R &middot; Week {note["week"]}</p>
  <h1>{note["title"]}</h1>
  <p>{note["lead"]}</p>
  {print_body}
</body>
</html>
"""
    print_path.write_text(html.replace("\r\n", "\n"), encoding="utf-8", newline="\n")
    return print_path


def write_pdf(note: dict, print_path: pathlib.Path) -> pathlib.Path:
    if not EDGE.exists():
        raise FileNotFoundError(f"Edge not found: {EDGE}")
    pdf_path = ROOT / "files" / "data-612" / f"{note['slug']}.pdf"
    uri = print_path.resolve().as_uri()
    cmd = [
        str(EDGE),
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        uri,
    ]
    subprocess.run(cmd, check=True)
    print_path.unlink(missing_ok=True)
    return pdf_path


def build_note(note: dict) -> None:
    md_path = ROOT / "files" / "data-612" / f"{note['slug']}.md"
    body = markdown_to_html(md_path.read_text(encoding="utf-8"))
    page_path = write_site_page(note, body)
    print_path = write_print_page(note, md_path)
    pdf_path = write_pdf(note, print_path)
    print(f"Wrote {page_path.name}")
    print(f"Wrote {pdf_path.name} ({pdf_path.stat().st_size} bytes)")


def main() -> None:
    week = None
    if len(sys.argv) > 1:
        week = int(sys.argv[1])
    for note in NOTES:
        if week is not None and note["week"] != week:
            continue
        build_note(note)


if __name__ == "__main__":
    main()
