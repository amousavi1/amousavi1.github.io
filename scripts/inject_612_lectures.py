"""Inject rendered DATA 612 lecture fragments into site HTML shells.

Preserves each page's existing lecture-meta week/PDF links and course-page-nav,
and adds a Source (.qmd) link.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LECTURES = ROOT / "files" / "data-612" / "lectures"


def clean_fragment(raw: str) -> str:
    raw = raw.strip()
    raw = re.sub(r"<h1[^>]*>.*?</h1>\s*", "", raw, count=1, flags=re.I | re.S)
    raw = raw.replace('class="sourceCode r"', 'class="language-r"')
    raw = raw.replace('<pre class="r"><code>', '<pre><code class="language-r">')
    raw = re.sub(r'<div class="sourceCode"[^>]*>\s*(<pre)', r"\1", raw)
    raw = re.sub(r"(</pre>)\s*</div>", r"\1", raw)
    raw = raw.replace('class="figure"', 'class="lecture-figure"')
    return raw.strip()


def ensure_source_link(meta_html: str, qmd_name: str) -> str:
    if "Source (.qmd)" in meta_html:
        # refresh href
        return re.sub(
            r'<a href="files/data-612/lectures/[^"]+\.qmd">Source \(\.qmd\)</a>',
            f'<a href="files/data-612/lectures/{qmd_name}">Source (.qmd)</a>',
            meta_html,
        )
    # insert before closing </p>
    link = f' &middot; <a href="files/data-612/lectures/{qmd_name}">Source (.qmd)</a>'
    if meta_html.rstrip().endswith("</p>"):
        return meta_html.rstrip()[:-4] + link + "</p>"
    return meta_html + link


def inject_one(stem: str) -> None:
    html_path = ROOT / f"data-612-{stem}.html"
    fragment_path = LECTURES / f"{stem}.fragment.html"
    qmd_name = f"{stem}.qmd"
    if not html_path.exists():
        print("skip missing html", stem)
        return
    if not fragment_path.exists():
        print("skip missing fragment", stem)
        return

    html = html_path.read_text(encoding="utf-8")
    fragment = clean_fragment(fragment_path.read_text(encoding="utf-8"))

    meta_m = re.search(r'<p class="lecture-meta">.*?</p>', html, flags=re.S)
    nav_m = re.search(r'<nav class="course-page-nav".*?</nav>', html, flags=re.S)
    if not meta_m or not nav_m:
        raise SystemExit(f"missing meta/nav in {html_path.name}")

    meta = ensure_source_link(meta_m.group(0), qmd_name)
    nav = nav_m.group(0)

    new_section = (
        '                    <section class="page__content" itemprop="text">\n'
        f"                        {meta}\n"
        f"{fragment}\n"
        f"{nav}\n"
        "                    </section>"
    )
    updated, n = re.subn(
        r'<section class="page__content" itemprop="text">.*?</section>',
        new_section,
        html,
        count=1,
        flags=re.S,
    )
    if n != 1:
        raise SystemExit(f"replace failed for {html_path.name}")
    html_path.write_text(updated, encoding="utf-8", newline="\n")
    print(f"updated {html_path.name}")


def main() -> None:
    stems = sorted(
        p.stem.replace(".fragment", "")
        for p in LECTURES.glob("*.fragment.html")
    )
    # Prefer stems that have both qmd and fragment
    for frag in sorted(LECTURES.glob("*.fragment.html")):
        stem = frag.name.replace(".fragment.html", "")
        inject_one(stem)


if __name__ == "__main__":
    main()
