"""Split DATA 612 weekly materials onto their own pages with previous/next links."""

from __future__ import annotations

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
HUB = ROOT / "data-612.html"

LAST_UPDATED_ISO = "2026-09-19T17:35:00-04:00"
LAST_UPDATED_TEXT = "September 19, 2026, 5:35 PM EDT"

NAV_RE = re.compile(r"\n?<nav class=\"course-page-nav\"[\s\S]*?</nav>\n?")
SECTION_CLOSE = "                    </section>\n                </div>\n            </article>"


def strip_closing_divs(text: str, count: int) -> str:
    out = text.rstrip()
    for _ in range(count):
        out = re.sub(r"</div>\s*$", "", out).rstrip()
    return out.strip()


def parse_schedule(html: str) -> dict[int, tuple[str, str]]:
    table = re.search(r'<table class="course-schedule">([\s\S]*?)</table>', html)
    if not table:
        raise SystemExit("Could not find the class-meetings table.")
    rows = re.findall(
        r"<tr>\s*<td>(?:<a[^>]*>)?(\d+)(?:</a>)?</td>\s*<td>(.*?)</td>\s*<td>(.*?)</td>",
        table.group(1),
    )
    return {int(num): (date, topic) for num, date, topic in rows}


def parse_weeks(html: str) -> dict[int, str]:
    start = html.find("<h2>Weekly Materials</h2>")
    if start < 0:
        start = html.find("<h2>Weekly materials</h2>")
    end = html.find("<h2>Data</h2>")
    if start < 0 or end < 0:
        raise SystemExit("Could not find the weekly-materials block.")
    weekly = html[start:end]
    parts = re.split(r'<div class="course-week-panel" id="week-(\d+)"[^>]*>', weekly)
    weeks: dict[int, str] = {}
    for i in range(1, len(parts), 2):
        num = int(parts[i])
        body = parts[i + 1]
        closings = 2 if i + 2 >= len(parts) else 1
        weeks[num] = strip_closing_divs(body, closings)
    return weeks


def extract_sidebar(html: str) -> str:
    match = re.search(r'(            <div class="sidebar sticky">[\s\S]*?</div>\n\n            <article)', html)
    if not match:
        raise SystemExit("Could not find the sidebar.")
    return match.group(1).replace("\n            <article", "")


def page_nav(prev_href: str | None, prev_label: str | None, next_href: str | None, next_label: str | None, mid_html: str = "") -> str:
    prev = (
        f'<a class="course-page-nav__prev" href="{prev_href}"><span aria-hidden="true">←</span> {prev_label}</a>'
        if prev_href and prev_label
        else '<span class="course-page-nav__prev"></span>'
    )
    nxt = (
        f'<a class="course-page-nav__next" href="{next_href}">{next_label} <span aria-hidden="true">→</span></a>'
        if next_href and next_label
        else '<span class="course-page-nav__next"></span>'
    )
    mid = f"\n                        {mid_html}" if mid_html else ""
    return (
        '                        <nav class="course-page-nav" aria-label="Page">\n'
        f"                            {prev}{mid}\n"
        f"                            {nxt}\n"
        "                        </nav>"
    )


def week_page(sidebar: str, num: int, date: str, topic: str, body: str, total: int) -> str:
    prev_href = f"data-612-week-{num - 1}.html" if num > 1 else "data-612.html"
    prev_label = f"Week {num - 1}" if num > 1 else "Course hub"
    next_href = f"data-612-week-{num + 1}.html" if num < total else "data-612.html"
    next_label = f"Week {num + 1}" if num < total else "Course hub"
    nav = page_nav(prev_href, prev_label, next_href, next_label)
    title = f"Week {num}: {topic}"
    return f"""<!doctype html>
<html lang="en" class="no-js">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>{title} - DATA 412/612 - Ahmad Mousavi</title>
        <link rel="stylesheet" href="assets/css/main.css" />
        <link rel="stylesheet" href="assets/css/site.css" />
        <link rel="stylesheet" href="assets/css/academicons.css" />
    </head>
    <body class="layout--single page-courses page-week">
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
{sidebar}
            <article class="page" itemscope itemtype="https://schema.org/LearningResource">
                <div class="page__inner-wrap">
                    <header>
                        <h1 id="page-title" class="page__title" itemprop="name">{title}</h1>
                    </header>
                    <section class="page__content" itemprop="text">
                        <p class="lecture-meta">
                            <a href="data-612.html">DATA 412/612</a> &middot; {date}
                        </p>
{body}
{nav}
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


def week_index(schedule: dict[int, tuple[str, str]]) -> str:
    items = []
    for num in sorted(schedule):
        date, topic = schedule[num]
        items.append(
            "                            <li>\n"
            f'                                <a class="course-material__title" href="data-612-week-{num}.html">Week {num}</a>\n'
            f'                                <span class="course-week-index__meta">{date} &middot; {topic}</span>\n'
            "                            </li>"
        )
    return (
        "                        <h2>Weekly materials</h2>\n"
        '                        <p class="course-weeks-intro">\n'
        "                            Open a week for its lectures, labs, readings, and discussion prompts.\n"
        "                            Canvas remains the official list of required reading.\n"
        "                        </p>\n"
        '                        <ul class="course-week-index">\n'
        + "\n".join(items)
        + "\n                        </ul>\n\n"
    )


def replace_weekly_block(html: str, index_html: str) -> str:
    start = html.find("<h2>Weekly Materials</h2>")
    if start < 0:
        start = html.find("<h2>Weekly materials</h2>")
    end = html.find("<h2>Data</h2>")
    if start < 0 or end < 0:
        raise SystemExit("Could not replace the weekly-materials block.")
    return html[:start] + index_html + "                        " + html[end:]


def link_schedule_weeks(html: str) -> str:
    def repl_table(match: re.Match[str]) -> str:
        return re.sub(
            r"(<tr>\s*)<td>(?:<a href=\"data-612-week-\d+\.html\">)?(\d+)(?:</a>)?</td>",
            lambda m: f'{m.group(1)}<td><a href="data-612-week-{m.group(2)}.html">{m.group(2)}</a></td>',
            match.group(0),
        )

    return re.sub(r'<table class="course-schedule">[\s\S]*?</table>', repl_table, html, count=1)


def collect_sequence(weeks: dict[int, str]) -> list[tuple[str, str, int]]:
    seen: set[str] = set()
    sequence: list[tuple[str, str, int]] = []
    for num in sorted(weeks):
        for href, title in re.findall(
            r'href="(data-612-[^"]+\.html)"[^>]*>\s*([^<]+?)\s*<',
            weeks[num],
        ):
            if href.startswith("data-612-week-") or href in seen:
                continue
            seen.add(href)
            sequence.append((href, re.sub(r"\s+", " ", title).strip(), num))
    return sequence


def insert_nav(html: str, nav: str) -> str:
    html = NAV_RE.sub("\n", html)
    if SECTION_CLOSE not in html:
        raise SystemExit("Could not find the page section close.")
    return html.replace(SECTION_CLOSE, f"{nav}\n{SECTION_CLOSE}", 1)


def link_week_in_meta(html: str, week: int) -> str:
    return re.sub(
        r'(<a href="data-612\.html">DATA 412/612</a> &middot; )(?:<a href="data-612-week-\d+\.html">)?Week \d+(?:</a>)?',
        rf'\1<a href="data-612-week-{week}.html">Week {week}</a>',
        html,
        count=1,
    )


def write_text(path: pathlib.Path, text: str) -> None:
    path.write_text(text.replace("\r\n", "\n"), encoding="utf-8", newline="\n")


def main() -> None:
    hub = HUB.read_text(encoding="utf-8")
    sidebar = extract_sidebar(hub)
    schedule = parse_schedule(hub)
    weeks = parse_weeks(hub)
    if set(weeks) != set(schedule):
        raise SystemExit(f"Week mismatch: panels {sorted(weeks)} vs schedule {sorted(schedule)}")

    total = max(weeks)
    for num, body in weeks.items():
        date, topic = schedule[num]
        write_text(ROOT / f"data-612-week-{num}.html", week_page(sidebar, num, date, topic, body, total))

    hub = replace_weekly_block(hub, week_index(schedule))
    hub = link_schedule_weeks(hub)
    write_text(HUB, hub)

    sequence = collect_sequence(weeks)
    for i, (href, title, week) in enumerate(sequence):
        path = ROOT / href
        if not path.exists():
            print(f"skip missing {href}")
            continue
        page = path.read_text(encoding="utf-8")
        prev_href = sequence[i - 1][0] if i else f"data-612-week-{week}.html"
        prev_label = sequence[i - 1][1] if i else f"Week {week}"
        next_href = sequence[i + 1][0] if i + 1 < len(sequence) else f"data-612-week-{week}.html"
        next_label = sequence[i + 1][1] if i + 1 < len(sequence) else f"Week {week}"
        mid = f'<a class="course-page-nav__week" href="data-612-week-{week}.html">Week {week}</a>'
        page = insert_nav(page, page_nav(prev_href, prev_label, next_href, next_label, mid))
        page = link_week_in_meta(page, week)
        write_text(path, page)

    print(f"Wrote {len(weeks)} week pages and updated {len(sequence)} lecture/lab pages.")


if __name__ == "__main__":
    main()
