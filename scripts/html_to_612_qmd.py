"""Convert DATA 612 lecture HTML bodies into Quarto .qmd sources."""
from __future__ import annotations

import html as html_lib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LECTURES = ROOT / "files" / "data-612" / "lectures"

# html filename stem (after data-612-) -> qmd stem / fig folder
LECTURE_STEMS = [
    # weeks 11–14
    "stats-tests",
    "stats-regression-summaries",
    "lab-11-stats",
    "rmd-presentations",
    "lab-12-presentations",
    "rmd-chunks-tables",
    "rmd-citations-bookdown",
    "lab-13-rmarkdown",
    "vectors-lists",
    "purrr-iteration",
    "course-wrap",
    "lab-14-iteration",
]

SKIP_IF_EXISTS = {
    "ggplot2-grammar",
    "ggplot2-geoms",
    "ggplot2-facets-themes",
}

UNSAFE_PATTERNS = [
    r"install\.packages\s*\(",
    r"devtools::",
    r"setwd\s*\(",
    r"file\.choose\s*\(",
    r"readline\s*\(",
    r"View\s*\(",
    r"browseURL\s*\(",
    r"download\.file\s*\(",
    r"read_csv\s*\(\s*[\"'](?!http)",  # local csv paths often missing
    r"read\.csv\s*\(\s*[\"']",
    r"read_delim\s*\(",
    r"read_tsv\s*\(",
    r"source\s*\(",
    r"load\s*\(",
    r"ggsave\s*\(",
    r"write_",
    r"write\.",
    r"saveRDS\s*\(",
    r"png\s*\(",
    r"pdf\s*\(",
    r"library\s*\(\s*shiny",
]


def extract_body(html: str) -> tuple[str, str]:
    """Return (title, inner content without meta/nav)."""
    title_m = re.search(
        r'<h1[^>]*class="page__title"[^>]*>(.*?)</h1>', html, flags=re.S | re.I
    )
    title = re.sub(r"<[^>]+>", "", title_m.group(1)).strip() if title_m else "Lecture"
    sec_m = re.search(
        r'<section class="page__content"[^>]*>(.*?)</section>', html, flags=re.S | re.I
    )
    if not sec_m:
        raise ValueError("no page__content")
    body = sec_m.group(1)
    body = re.sub(r'<p class="lecture-meta">.*?</p>\s*', "", body, count=1, flags=re.S)
    body = re.sub(r'<nav class="course-page-nav".*?</nav>\s*', "", body, count=1, flags=re.S)
    return title, body.strip()


def html_inline_to_md(text: str) -> str:
    text = re.sub(r"<code>(.*?)</code>", r"`\1`", text, flags=re.S)
    text = re.sub(r"<strong>(.*?)</strong>", r"**\1**", text, flags=re.S)
    text = re.sub(r"<em>(.*?)</em>", r"*\1*", text, flags=re.S)
    text = re.sub(
        r'<a href="([^"]+)"[^>]*>(.*?)</a>',
        lambda m: f"[{re.sub(r'<[^>]+>', '', m.group(2)).strip()}]({m.group(1)})",
        text,
        flags=re.S,
    )
    text = re.sub(r"<br\s*/?>", "  \n", text, flags=re.I)
    text = re.sub(r"<[^>]+>", "", text)
    return html_lib.unescape(text).strip()


def list_to_md(block: str, ordered: bool) -> str:
    items = re.findall(r"<li[^>]*>(.*?)</li>", block, flags=re.S | re.I)
    lines = []
    for i, item in enumerate(items, 1):
        # nested paragraphs
        item = re.sub(r"</?p[^>]*>", "\n", item, flags=re.I)
        md = html_inline_to_md(item)
        md = re.sub(r"\n+", "\n  ", md).strip()
        prefix = f"{i}." if ordered else "-"
        lines.append(f"{prefix} {md}")
    return "\n".join(lines)


def should_eval_false(code: str) -> bool:
    for pat in UNSAFE_PATTERNS:
        if re.search(pat, code):
            return True
    # bare pipe operator demos that are not valid R statements
    stripped = code.strip()
    if stripped.startswith("|>") or stripped.startswith("%>%"):
        return True
    if re.search(r"^\s*#", stripped) and "\n" not in stripped.strip():
        return True
    return False


def needs_tidyverse(code: str) -> bool:
    return bool(
        re.search(
            r"\b(tidyverse|dplyr|ggplot|tidyr|readr|stringr|forcats|purrr|tibble|magrittr)\b",
            code,
        )
    )


def convert_body_to_qmd(title: str, body: str, stem: str) -> str:
    parts: list[str] = [
        "---",
        f'title: "{title.replace(chr(34), chr(39))}"',
        "---",
        "",
        "```{r}",
        "#| label: setup",
        "#| include: false",
        "knitr::opts_chunk$set(",
        "  echo = TRUE,",
        "  message = FALSE,",
        "  warning = FALSE,",
        "  fig.width = 6,",
        "  fig.height = 3.6,",
        "  fig.align = \"center\",",
        "  dpi = 120,",
        "  error = TRUE,",
        f'  fig.path = "_figs/{stem}/"',
        ")",
        "library(tidyverse)",
        "```",
        "",
    ]

    chunk_i = 0
    pos = 0
    # tokenize by pre/code blocks and block elements
    token_re = re.compile(
        r"(<pre><code class=\"language-r\">(.*?)</code></pre>)"
        r"|(<h2[^>]*>(.*?)</h2>)"
        r"|(<h3[^>]*>(.*?)</h3>)"
        r"|(<hr\s*/?>)"
        r"|(<ul[^>]*>.*?</ul>)"
        r"|(<ol[^>]*>.*?</ol>)"
        r"|(<p[^>]*>.*?</p>)"
        r"|(<blockquote[^>]*>.*?</blockquote>)"
        r"|(<figure[^>]*>.*?</figure>)"
        r"|(<div[^>]*>.*?</div>)",
        flags=re.S | re.I,
    )

    for m in token_re.finditer(body):
        # ignore leftover text between tokens lightly
        if m.group(1) is not None:
            code = html_lib.unescape(m.group(2))
            code = code.replace("\r\n", "\n").strip("\n")
            chunk_i += 1
            label = f"chunk-{chunk_i}"
            opts = [f"#| label: {label}"]
            if should_eval_false(code):
                opts.append("#| eval: false")
            parts.append("```{r}")
            parts.extend(opts)
            parts.append(code)
            parts.append("```")
            parts.append("")
        elif m.group(3) is not None:
            parts.append(f"## {html_inline_to_md(m.group(4))}")
            parts.append("")
        elif m.group(5) is not None:
            parts.append(f"### {html_inline_to_md(m.group(6))}")
            parts.append("")
        elif m.group(7) is not None:
            parts.append("---")
            parts.append("")
        elif m.group(8) is not None:
            parts.append(list_to_md(m.group(8), ordered=False))
            parts.append("")
        elif m.group(9) is not None:
            parts.append(list_to_md(m.group(9), ordered=True))
            parts.append("")
        elif m.group(10) is not None:
            phtml = m.group(10)
            imgs = re.findall(
                r'<img[^>]+src="([^"]+)"[^>]*(?:alt="([^"]*)")?[^>]*>',
                phtml,
                flags=re.I,
            )
            if imgs:
                for src, alt in imgs:
                    alt = alt or ""
                    parts.append(f"![{alt}]({src})")
                    parts.append("")
            else:
                parts.append(html_inline_to_md(phtml))
                parts.append("")
        elif m.group(11) is not None:
            parts.append(f"> {html_inline_to_md(m.group(11))}")
            parts.append("")
        elif m.group(12) is not None:
            imgs = re.findall(
                r'<img[^>]+src="([^"]+)"[^>]*(?:alt="([^"]*)")?[^>]*>',
                m.group(12),
                flags=re.I,
            )
            for src, alt in imgs:
                parts.append(f"![{alt or ''}]({src})")
                parts.append("")
        elif m.group(13) is not None:
            inner = html_inline_to_md(m.group(13))
            if inner:
                parts.append(inner)
                parts.append("")

    # If no tokens matched much, fall back to stripping tags
    if chunk_i == 0 and len(parts) < 20:
        text = re.sub(r"<pre><code class=\"language-r\">(.*?)</code></pre>", r"\n```r\n\1\n```\n", body, flags=re.S)
        text = re.sub(r"<h2[^>]*>(.*?)</h2>", lambda m: f"\n## {html_inline_to_md(m.group(1))}\n", text, flags=re.S)
        text = re.sub(r"<p[^>]*>(.*?)</p>", lambda m: f"\n{html_inline_to_md(m.group(1))}\n", text, flags=re.S)
        text = re.sub(r"<[^>]+>", "", text)
        parts.append(html_lib.unescape(text).strip())
        parts.append("")

    return "\n".join(parts).rstrip() + "\n"


def main(stems: list[str] | None = None) -> None:
    import sys

    LECTURES.mkdir(parents=True, exist_ok=True)
    targets = stems or (sys.argv[1:] if len(sys.argv) > 1 else LECTURE_STEMS)
    for stem in targets:
        if stem in SKIP_IF_EXISTS:
            continue
        html_path = ROOT / f"data-612-{stem}.html"
        qmd_path = LECTURES / f"{stem}.qmd"
        if not html_path.exists():
            print("MISSING html", stem)
            continue
        title, body = extract_body(html_path.read_text(encoding="utf-8"))
        qmd = convert_body_to_qmd(title, body, stem)
        # Avoid duplicate setup labels from lecture content that documents setup chunks
        parts = qmd.split("#| label: setup")
        if len(parts) > 2:
            rebuilt = parts[0] + "#| label: setup"
            for i, p in enumerate(parts[1:], 1):
                rebuilt += p if i == 1 else f"#| label: setup-doc-{i}" + p
            qmd = rebuilt
        qmd_path.write_text(qmd, encoding="utf-8", newline="\n")
        n_chunks = qmd.count("```{r}")
        print(f"wrote {qmd_path.name} ({n_chunks} r blocks) title={title!r}")


if __name__ == "__main__":
    main()
