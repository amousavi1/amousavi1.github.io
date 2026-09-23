"""Inject rendered ggplot lecture fragments into site HTML shells."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LECTURES = ROOT / "files" / "data-612" / "lectures"

PAGES = [
    {
        "html": ROOT / "data-612-ggplot2-grammar.html",
        "fragment": LECTURES / "ggplot2-grammar.fragment.html",
        "qmd": "ggplot2-grammar.qmd",
        "meta_pdf": "files/data-612/ggplot2-grammar.pdf",
        "prev": ("data-612-lab-2-solutions.html", "Lab 2 solutions"),
        "next": ("data-612-ggplot2-geoms.html", "3.2 ggplot2: Geoms"),
    },
    {
        "html": ROOT / "data-612-ggplot2-geoms.html",
        "fragment": LECTURES / "ggplot2-geoms.fragment.html",
        "qmd": "ggplot2-geoms.qmd",
        "meta_pdf": "files/data-612/ggplot2-geoms.pdf",
        "prev": ("data-612-ggplot2-grammar.html", "3.1 ggplot2: The Grammar of Graphics"),
        "next": ("data-612-ggplot2-facets-themes.html", "3.3 ggplot2: Facets, Themes, and Saving"),
    },
    {
        "html": ROOT / "data-612-ggplot2-facets-themes.html",
        "fragment": LECTURES / "ggplot2-facets-themes.fragment.html",
        "qmd": "ggplot2-facets-themes.qmd",
        "meta_pdf": "files/data-612/ggplot2-facets-themes.pdf",
        "prev": ("data-612-ggplot2-geoms.html", "3.2 ggplot2: Geoms"),
        "next": ("data-612-lab-3-ggplot2.html", "Lab 3: Graphics with ggplot2"),
    },
]


def clean_fragment(raw: str) -> str:
    raw = raw.strip()
    raw = re.sub(r"<h1[^>]*>.*?</h1>\s*", "", raw, count=1, flags=re.I | re.S)
    raw = raw.replace('class="sourceCode r"', 'class="language-r"')
    raw = raw.replace('<pre class="r"><code>', '<pre><code class="language-r">')
    raw = re.sub(r'<div class="sourceCode"[^>]*>\s*(<pre)', r"\1", raw)
    raw = re.sub(r"(</pre>)\s*</div>", r"\1", raw)
    raw = raw.replace('class="figure"', 'class="lecture-figure"')
    return raw.strip()


def build_nav(prev_href: str, prev_label: str, next_href: str, next_label: str) -> str:
    return f"""                        <nav class="course-page-nav" aria-label="Page">
                            <a class="course-page-nav__prev" href="{prev_href}"><span aria-hidden="true">←</span> {prev_label}</a>
                        <a class="course-page-nav__week" href="data-612-week-3.html">Week 3</a>
                            <a class="course-page-nav__next" href="{next_href}">{next_label} <span aria-hidden="true">→</span></a>
                        </nav>"""


def inject(page: dict) -> None:
    fragment = clean_fragment(page["fragment"].read_text(encoding="utf-8"))
    html = page["html"].read_text(encoding="utf-8")

    meta = f"""                        <p class="lecture-meta">
                            <a href="data-612.html">DATA 412/612</a> &middot; <a href="data-612-week-3.html">Week 3</a> &middot;
                            <a href="{page['meta_pdf']}" target="_blank" rel="noopener">PDF</a>
                            &middot; <a href="files/data-612/lectures/{page['qmd']}">Source (.qmd)</a>
                        </p>
"""
    nav = build_nav(page["prev"][0], page["prev"][1], page["next"][0], page["next"][1])
    new_section = (
        '                    <section class="page__content" itemprop="text">\n'
        + meta
        + fragment
        + "\n"
        + nav
        + "\n                    </section>"
    )
    updated, n = re.subn(
        r'<section class="page__content" itemprop="text">.*?</section>',
        new_section,
        html,
        count=1,
        flags=re.S,
    )
    if n != 1:
        raise SystemExit(f"Could not replace page__content in {page['html'].name}")
    page["html"].write_text(updated, encoding="utf-8", newline="\n")
    print(f"updated {page['html'].name}")


def main() -> None:
    for page in PAGES:
        if not page["fragment"].exists():
            raise SystemExit(f"Missing fragment: {page['fragment']}")
        inject(page)


if __name__ == "__main__":
    main()
