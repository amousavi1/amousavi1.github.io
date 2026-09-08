"""Build DATA 641 lecture and lab pages and PDFs from the markdown sources."""

from __future__ import annotations

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(pathlib.Path(__file__).parent))

from build_lecture_note import PRINT_CSS, SIDEBAR, markdown_to_html  # noqa: E402

EDGE = pathlib.Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")

LAST_UPDATED_ISO = "2026-09-07T18:50:00-04:00"
LAST_UPDATED_TEXT = "September 7, 2026, 6:50 PM EDT"

COURSE = "data-641"
COURSE_TITLE = "DATA 441/641"
COURSE_LONG = "Applied Natural Language Processing"
FILES = ROOT / "files" / COURSE

NOTES = [
    {
        "slug": "nlp-in-the-real-world",
        "week": 1,
        "title": "1.1 NLP in the Real World",
        "lead": "What NLP is, the core tasks, and why human language is a hard input.",
    },
    {
        "slug": "ml-dl-nlp-overview",
        "week": 1,
        "title": "1.2 Machine Learning, Deep Learning, and NLP",
        "lead": "Rules, then learning from examples, then stacked representations.",
    },
    {
        "slug": "python-tour",
        "week": 1,
        "title": "1.3 A Python Tour for NLP",
        "lead": "Types, strings, containers, control flow, functions, files, NumPy, and a small class.",
    },
    {
        "slug": "lab-1-numpy-nltk-files",
        "week": 1,
        "title": "Lab 1: NumPy, NLTK, and Files",
        "lead": "Arrays, stemming versus lemmatization, and a movie script.",
    },
]


def write_site_page(note: dict, body: str) -> pathlib.Path:
    slug = note["slug"]
    title = note["title"]
    week = note["week"]
    slide_pdfs = {
        "nlp-in-the-real-world": "files/data-641/slides/1.1-nlp-in-the-real-world.pdf",
        "ml-dl-nlp-overview": "files/data-641/slides/1.2-ml-dl-nlp-overview.pdf",
        "python-tour": "files/data-641/slides/1.3-python-tour.pdf",
    }
    pdf_href = slide_pdfs.get(slug, f"files/{COURSE}/{slug}.pdf")
    page_path = ROOT / f"{COURSE}-{slug}.html"
    page = f"""<!doctype html>
<html lang="en" class="no-js">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>{title} - {COURSE_TITLE} - Ahmad Mousavi</title>
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
                            <a href="{COURSE}.html">{COURSE_TITLE}</a> &middot; Week {week} &middot;
                            <a href="{pdf_href}" target="_blank" rel="noopener">PDF</a>
                        </p>
                        <p>
                            {note["lead"]}
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


def write_solutions_page() -> pathlib.Path:
    page_path = ROOT / f"{COURSE}-lab-1-solutions.html"
    page = f"""<!doctype html>
<html lang="en" class="no-js">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="robots" content="noindex, nofollow" />
        <title>Lab 1 solutions - {COURSE_TITLE} - Ahmad Mousavi</title>
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
                        <h1 id="page-title" class="page__title" itemprop="name">Lab 1 solutions</h1>
                    </header>
                    <section class="page__content" itemprop="text">
                        <p class="lecture-meta">
                            <a href="{COURSE}.html">{COURSE_TITLE}</a> &middot; Week 1 &middot;
                            <a href="{COURSE}-lab-1-numpy-nltk-files.html">Lab 1</a>
                        </p>
                        <p>
                            This page is locked. The solutions stay encrypted in the browser until the password is entered.
                        </p>
                        <form
                            id="lab-solutions-form"
                            class="lab-solutions-form"
                            data-enc-url="files/{COURSE}/lab-1-solutions.enc.json"
                        >
                            <label for="lab-solutions-password">Password</label>
                            <input
                                id="lab-solutions-password"
                                name="passphrase"
                                type="password"
                                autocomplete="off"
                                spellcheck="false"
                            />
                            <button type="submit">Open solutions</button>
                        </form>
                        <p id="lab-solutions-status" class="lab-solutions-status" role="status"></p>
                        <div id="lab-solutions-output" class="lab-solutions-output" hidden></div>
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
        <script src="assets/js/lab-solutions.js"></script>
    </body>
</html>
"""
    page_path.write_text(page.replace("\r\n", "\n"), encoding="utf-8", newline="\n")
    return page_path


def write_print_page(note: dict, md_path: pathlib.Path) -> pathlib.Path:
    print_path = FILES / f"_print-{note['slug']}.html"
    print_body = markdown_to_html(md_path.read_text(encoding="utf-8"))
    print_body = print_body.replace('<div class="table-wrap">', "").replace("</div>", "")
    print_body = print_body.replace(f"files/{COURSE}/graphics/", "graphics/")
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>{note["title"]}</title>
  <style>{PRINT_CSS}</style>
</head>
<body>
  <p class="kicker">{COURSE_TITLE} &middot; {COURSE_LONG} &middot; Week {note["week"]}</p>
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
    pdf_path = FILES / f"{note['slug']}.pdf"
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
    md_path = FILES / f"{note['slug']}.md"
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
    write_solutions_page()
    print("Wrote data-641-lab-1-solutions.html")


if __name__ == "__main__":
    main()
