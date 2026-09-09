"""Build DATA 442/642 lecture and lab pages, PDFs, and the weekly hub."""

from __future__ import annotations

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(pathlib.Path(__file__).parent))

from build_lecture_note import PRINT_CSS, SIDEBAR, markdown_to_html  # noqa: E402
from data_642_catalog import BY_SLUG, NOTES, WEEKS  # noqa: E402
from extra_materials_catalog import extras_for  # noqa: E402

EDGE = pathlib.Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")

LAST_UPDATED_ISO = "2026-09-09T02:00:00-04:00"
LAST_UPDATED_TEXT = "September 9, 2026, 2:00 AM EDT"

COURSE = "data-642"
COURSE_TITLE = "DATA 442/642"
COURSE_LONG = "Advanced Machine Learning"
FILES = ROOT / "files" / COURSE


def write_site_page(note: dict, body: str) -> pathlib.Path:
    slug = note["slug"]
    title = note["title"]
    week = note["week"]
    pdf_href = f"files/{COURSE}/{slug}.pdf"
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


def _material_item(title: str, href: str, pdf_href: str | None = None, note: str | None = None) -> str:
    extra = ""
    if pdf_href:
        extra += (
            f'<a class="course-material__pdf" href="{pdf_href}" target="_blank" rel="noopener">(PDF)</a>'
        )
    if note:
        extra += f'<span class="course-material__note"> {note}</span>'
    return f"""                                    <li>
                                        <a class="course-material__title" href="{href}"{' target="_blank" rel="noopener"' if href.startswith("http") or href.endswith(".pdf") else ""}>{title}</a
                                        >{extra}
                                    </li>"""


def write_hub() -> pathlib.Path:
    tab_btns = []
    panels = []
    for week in range(1, 16):
        selected = "true" if week == 1 else "false"
        hidden = "" if week == 1 else " hidden"
        tabindex = "" if week == 1 else ' tabindex="-1"'
        tab_btns.append(
            f"""                                <button type="button" role="tab" id="tab-week-{week}" aria-controls="week-{week}" aria-selected="{selected}"{tabindex}>
                                    Week {week}
                                </button>"""
        )
        spec = WEEKS[week]
        chunks = []
        label = spec.get("label")
        if label:
            chunks.append(f'                                <p class="course-group-title">{label}</p>')
        lectures = spec.get("lectures") or []
        if lectures:
            items = []
            for slug in lectures:
                note = BY_SLUG[slug]
                slide = note.get("slide")
                slide_path = FILES / "slides" / f"{slide}.pdf" if slide else None
                if slide_path and slide_path.exists():
                    pdf = f"files/{COURSE}/slides/{slide}.pdf"
                    items.append(_material_item(note["title"], pdf, pdf))
                else:
                    items.append(
                        _material_item(
                            note["title"],
                            f"{COURSE}-{slug}.html",
                            f"files/{COURSE}/{slug}.pdf",
                        )
                    )
            chunks.append(
                '                                <p class="course-group-title">Notes</p>\n'
                '                                <ul class="course-materials">\n'
                + "\n".join(items)
                + "\n                                </ul>"
            )
        lab_items = []
        for slug, _has_solutions in spec.get("labs") or []:
            note = BY_SLUG[slug]
            lab_items.append(
                _material_item(note["title"], f"{COURSE}-{slug}.html", f"files/{COURSE}/{slug}.pdf")
            )
        for title, filename in spec.get("lab_files") or []:
            href = f"files/{COURSE}/{filename}"
            if not (ROOT / "files" / COURSE / filename).exists():
                continue
            lab_items.append(_material_item(title, href, href))
        if lab_items:
            chunks.append(
                '                                <p class="course-group-title">Labs</p>\n'
                '                                <ul class="course-materials">\n'
                + "\n".join(lab_items)
                + "\n                                </ul>"
            )
        homework = spec.get("homework") or []
        if homework:
            items = []
            for title, filename in homework:
                href = f"files/{COURSE}/{filename}"
                if not (ROOT / "files" / COURSE / filename).exists():
                    continue
                items.append(_material_item(title, href, href))
            if items:
                chunks.append(
                    '                                <p class="course-group-title">Homework</p>\n'
                    '                                <ul class="course-materials">\n'
                    + "\n".join(items)
                    + "\n                                </ul>"
                )
        extra_items = []
        for kind in ("notes", "homework"):
            for title, filename in extras_for(COURSE, week, kind):
                href = f"files/{COURSE}/{filename}"
                if not (ROOT / "files" / COURSE / filename).exists():
                    continue
                extra_items.append(_material_item(title, href, href))
        if extra_items:
            chunks.append(
                '                                <p class="course-group-title">Additional</p>\n'
                '                                <ul class="course-materials">\n'
                + "\n".join(extra_items)
                + "\n                                </ul>"
            )
        discussion = spec.get("discussion") or []
        if discussion:
            lis = "\n".join(f"                                    <li>{q}</li>" for q in discussion)
            chunks.append(
                '                                <p class="course-group-title">Discussion</p>\n'
                '                                <ul class="course-discussion">\n'
                + lis
                + "\n                                </ul>"
            )
        panels.append(
            f"""                            <div class="course-week-panel" id="week-{week}" role="tabpanel" aria-labelledby="tab-week-{week}"{hidden}>
{chr(10).join(chunks)}
                            </div>"""
        )

    page = f"""<!doctype html>
<html lang="en" class="no-js">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>{COURSE_TITLE}: {COURSE_LONG} - Ahmad Mousavi</title>
        <link rel="stylesheet" href="assets/css/main.css" />
        <link rel="stylesheet" href="assets/css/site.css" />
        <link rel="stylesheet" href="assets/css/academicons.css" />
    </head>
    <body class="layout--single page-courses">
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

            <article class="page" itemscope itemtype="https://schema.org/Course">
                <div class="page__inner-wrap">
                    <header>
                        <h1 id="page-title" class="page__title" itemprop="name">{COURSE_TITLE}: {COURSE_LONG}</h1>
                    </header>
                    <section class="page__content" itemprop="text">
                        <p class="course-meta">American University</p>
                        <p>
                            Weekly lecture slides, labs, and homework for Advanced Machine Learning.
                            Canvas is official for due dates and submissions. Notes are the original
                            course slide decks. Questions:
                            <a href="mailto:mousavi@american.edu">mousavi@american.edu</a>.
                        </p>
                        <p><a href="courses.html">All courses</a></p>

                        <h2>Syllabus and project</h2>
                        <ul class="course-materials">
                            <li>
                                <a class="course-material__title" href="files/{COURSE}/syllabus.pdf" target="_blank" rel="noopener">Syllabus</a
                                ><a class="course-material__pdf" href="files/{COURSE}/syllabus.pdf" target="_blank" rel="noopener">(PDF)</a>
                            </li>
                            <li>
                                <a class="course-material__title" href="files/{COURSE}/project-proposal.pdf" target="_blank" rel="noopener">Project proposal</a
                                ><a class="course-material__pdf" href="files/{COURSE}/project-proposal.pdf" target="_blank" rel="noopener">(PDF)</a>
                            </li>
                            <li>
                                <a class="course-material__title" href="files/{COURSE}/project-report.pdf" target="_blank" rel="noopener">Presentation and final report</a
                                ><a class="course-material__pdf" href="files/{COURSE}/project-report.pdf" target="_blank" rel="noopener">(PDF)</a>
                            </li>
                        </ul>

                        <h2>Weekly Materials</h2>
                        <div class="course-weeks">
                            <div class="course-week-tabs" role="tablist" aria-label="Course weeks">
{chr(10).join(tab_btns)}
                            </div>
{chr(10).join(panels)}
                        </div>
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
    page_path = ROOT / f"{COURSE}.html"
    page_path.write_text(page.replace("\r\n", "\n"), encoding="utf-8", newline="\n")
    return page_path


def write_print_page(note: dict, md_path: pathlib.Path) -> pathlib.Path:
    print_path = FILES / f"_print-{note['slug']}.html"
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
    if "--notes" in sys.argv:
        slugs = {a for a in sys.argv[1:] if not a.startswith("--") and not a.isdigit()}
        week = None
        for a in sys.argv[1:]:
            if a.isdigit():
                week = int(a)
                break
        for note in NOTES:
            if note.get("slide"):
                continue
            if week is not None and note["week"] != week:
                continue
            if slugs and note["slug"] not in slugs:
                continue
            if not (FILES / f"{note['slug']}.md").exists():
                continue
            build_note(note)
    write_hub()
    print("Wrote data-642.html")


if __name__ == "__main__":
    main()
