"""Build the DATA 442/642 weekly hub from complementary notes."""

from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(pathlib.Path(__file__).parent))

from build_data_641 import _material_item  # noqa: E402
from build_lecture_note import SIDEBAR  # noqa: E402
from data_642_catalog import WEEKS  # noqa: E402
from extra_materials_catalog import extras_for  # noqa: E402

LAST_UPDATED_ISO = "2026-09-08T20:45:00-04:00"
LAST_UPDATED_TEXT = "September 8, 2026, 8:45 PM EDT"

COURSE = "data-642"
COURSE_TITLE = "DATA 442/642"
COURSE_LONG = "Advanced Machine Learning"


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
        for kind, heading in (
            ("notes", "Complementary notes"),
            ("practice", "Practice"),
            ("homework", "Homework / extra credit"),
        ):
            items = []
            for title, filename in extras_for(COURSE, week, kind):
                href = f"files/{COURSE}/{filename}"
                if not (ROOT / "files" / COURSE / filename).exists():
                    continue
                items.append(_material_item(title, href, href))
            if items:
                chunks.append(
                    f'                                <p class="course-group-title">{heading}</p>\n'
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
        if not any("course-materials" in c for c in chunks):
            chunks.append(
                "                                <p>Complementary notes for this week will appear here once compiled.</p>"
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
                            This is a complementary course hub. Canvas is the official site for this semester.
                            The weekly notes below are extra files prepared while teaching 442/642.
                            They follow the six-module schedule (math and optimization, sparsity,
                            kernels, SVMs, unsupervised learning, then factorization and neural nets).
                            Questions: <a href="mailto:mousavi@american.edu">mousavi@american.edu</a>.
                        </p>
                        <p><a href="courses.html">All courses</a></p>

                        <h2>Syllabus</h2>
                        <ul class="course-materials">
                            <li>
                                <a class="course-material__title" href="files/{COURSE}/syllabus.pdf" target="_blank" rel="noopener">Syllabus</a
                                ><a class="course-material__pdf" href="files/{COURSE}/syllabus.pdf" target="_blank" rel="noopener">(PDF)</a>
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


def main() -> None:
    write_hub()
    print("Wrote data-642.html")


if __name__ == "__main__":
    main()
