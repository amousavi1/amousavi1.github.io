"""Build DATA 641 lecture and lab pages and PDFs from the markdown sources."""

from __future__ import annotations

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(pathlib.Path(__file__).parent))

from build_lecture_note import PRINT_CSS, SIDEBAR, markdown_to_html  # noqa: E402
from data_641_catalog import BY_SLUG, DATA_FILES, NOTES, WEEKS  # noqa: E402
from extra_materials_catalog import extras_for  # noqa: E402

EDGE = pathlib.Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")

LAST_UPDATED_ISO = "2026-09-09T02:40:00-04:00"
LAST_UPDATED_TEXT = "September 9, 2026, 2:40 AM EDT"

# Weeks whose lecture titles open written notes; (slides) still opens the original deck.
PROSE_NOTE_WEEKS = {1}

COURSE = "data-641"
COURSE_TITLE = "DATA 441/641"
COURSE_LONG = "Applied Natural Language Processing"
FILES = ROOT / "files" / COURSE


def write_site_page(note: dict, body: str) -> pathlib.Path:
    slug = note["slug"]
    title = note["title"]
    week = note["week"]
    slide = note.get("slide")
    slide_path = FILES / "slides" / f"{slide}.pdf" if slide else None
    notes_pdf = f"files/{COURSE}/{slug}.pdf"
    meta_bits = [
        f'<a href="{COURSE}.html">{COURSE_TITLE}</a> &middot; Week {week}',
        f'<a href="{notes_pdf}" target="_blank" rel="noopener">PDF</a>',
    ]
    if slide_path and slide_path.exists():
        meta_bits.append(
            f'<a href="files/{COURSE}/slides/{slide}.pdf" target="_blank" rel="noopener">Slides</a>'
        )
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
                            {" &middot; ".join(meta_bits)}
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


def _material_item(
    title: str,
    href: str,
    pdf_href: str | None = None,
    note: str | None = None,
    extra_label: str = "(PDF)",
) -> str:
    extra = ""
    if pdf_href:
        extra += (
            f'<a class="course-material__pdf" href="{pdf_href}" target="_blank" rel="noopener">{extra_label}</a>'
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
    for week in sorted(WEEKS):
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
        lectures = spec.get("lectures") or []
        if lectures:
            items = []
            for slug in lectures:
                note = BY_SLUG[slug]
                slide = note.get("slide")
                slide_path = FILES / "slides" / f"{slide}.pdf" if slide else None
                notes_page = ROOT / f"{COURSE}-{slug}.html"
                notes_md = FILES / f"{slug}.md"
                slides_href = f"files/{COURSE}/slides/{slide}.pdf" if slide_path and slide_path.exists() else None
                if (
                    note["week"] in PROSE_NOTE_WEEKS
                    and notes_md.exists()
                    and notes_page.exists()
                    and slides_href
                ):
                    items.append(
                        _material_item(
                            note["title"],
                            f"{COURSE}-{slug}.html",
                            slides_href,
                            extra_label="(slides)",
                        )
                    )
                elif slides_href:
                    items.append(_material_item(note["title"], slides_href, slides_href))
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
        labs = spec.get("labs") or []
        if labs:
            items = []
            for slug, has_solutions in labs:
                note = BY_SLUG[slug]
                items.append(
                    _material_item(note["title"], f"{COURSE}-{slug}.html", f"files/{COURSE}/{slug}.pdf")
                )
                if has_solutions:
                    lab_n = _lab_number(slug)
                    items.append(
                        _material_item(
                            f"Lab {lab_n} solutions",
                            f"{COURSE}-lab-{lab_n}-solutions.html",
                            note="(password)",
                        )
                    )
            chunks.append(
                '                                <p class="course-group-title">Labs</p>\n'
                '                                <ul class="course-materials">\n'
                + "\n".join(items)
                + "\n                                </ul>"
            )
        homework = spec.get("homework") or []
        if homework:
            items = []
            for title, filename in homework:
                href = f"files/{COURSE}/{filename}"
                items.append(_material_item(title, href, href))
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
        readings = spec.get("readings") or []
        if readings:
            items = []
            for title, url in readings:
                items.append(_material_item(title, url))
            chunks.append(
                '                                <p class="course-group-title">Additional readings</p>\n'
                '                                <ul class="course-materials">\n'
                + "\n".join(items)
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

    data_lis = "\n".join(
        f'                            <li><a href="files/{COURSE}/{name}">{name}</a></li>'
        for name in DATA_FILES
    )
    page_path = ROOT / f"{COURSE}.html"
    # Keep the existing chrome; only the weekly block is generated above.
    existing = page_path.read_text(encoding="utf-8")
    start = existing.index('<h2>Weekly Materials</h2>')
    end = existing.index('<h2>Data</h2>')
    weekly = f"""<h2>Weekly Materials</h2>
                        <div class="course-weeks">
                            <div class="course-week-tabs" role="tablist" aria-label="Course weeks">
{chr(10).join(tab_btns)}
                            </div>
{chr(10).join(panels)}
                        </div>

                        """
    data_block_end = existing.index('<h2>Resources</h2>')
    data = f"""<h2>Data</h2>
                        <ul class="course-data-list">
{data_lis}
                        </ul>

                        """
    new = existing[:start] + weekly + data + existing[data_block_end:]
    page_path.write_text(new.replace("\r\n", "\n"), encoding="utf-8", newline="\n")
    return page_path


def _lab_number(slug: str) -> str:
    return slug.split("-")[1]


def labs_with_solutions() -> list[tuple[int, str, str]]:
    out: list[tuple[int, str, str]] = []
    for week, spec in WEEKS.items():
        for slug, has_solutions in spec.get("labs") or []:
            if has_solutions:
                out.append((week, slug, _lab_number(slug)))
    return out


def write_solutions_page(week: int, slug: str, lab_n: str) -> pathlib.Path:
    page_path = ROOT / f"{COURSE}-lab-{lab_n}-solutions.html"
    page = f"""<!doctype html>
<html lang="en" class="no-js">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="robots" content="noindex, nofollow" />
        <title>Lab {lab_n} solutions - {COURSE_TITLE} - Ahmad Mousavi</title>
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
                        <h1 id="page-title" class="page__title" itemprop="name">Lab {lab_n} solutions</h1>
                    </header>
                    <section class="page__content" itemprop="text">
                        <p class="lecture-meta">
                            <a href="{COURSE}.html">{COURSE_TITLE}</a> &middot; Week {week} &middot;
                            <a href="{COURSE}-{slug}.html">Lab {lab_n}</a>
                        </p>
                        <p>
                            This page is locked. The solutions stay encrypted in the browser until the password is entered.
                        </p>
                        <form
                            id="lab-solutions-form"
                            class="lab-solutions-form"
                            data-enc-url="files/{COURSE}/lab-{lab_n}-solutions.enc.json"
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
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    hub_only = "--hub" in flags
    html_only = "--html-only" in flags
    week = None
    slugs = None
    if args:
        if args[0].isdigit():
            week = int(args[0])
        else:
            slugs = set(args)
    if not hub_only:
        for note in NOTES:
            if week is not None and note["week"] != week:
                continue
            if slugs is not None and note["slug"] not in slugs:
                continue
            if html_only:
                md_path = FILES / f"{note['slug']}.md"
                if not md_path.exists():
                    print(f"Skip missing {md_path.name}")
                    continue
                body = markdown_to_html(md_path.read_text(encoding="utf-8"))
                page_path = write_site_page(note, body)
                print(f"Wrote {page_path.name}")
            else:
                build_note(note)
        for lab_week, slug, lab_n in labs_with_solutions():
            write_solutions_page(lab_week, slug, lab_n)
            print(f"Wrote {COURSE}-lab-{lab_n}-solutions.html")
    write_hub()
    print("Wrote data-641.html")


if __name__ == "__main__":
    main()
