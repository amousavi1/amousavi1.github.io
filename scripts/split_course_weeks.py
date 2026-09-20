"""Split 641/642/643 hub tab panels into 412-style week pages and table hubs."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FOOTER_DT = "2026-09-20T18:55:00-04:00"
FOOTER_LABEL = "September 20, 2026, 6:55 PM EDT"

COURSES = {
    "641": {
        "hub": "data-641.html",
        "prefix": "data-641",
        "code": "DATA 441/641",
        "full": "DATA 441/641: Applied Natural Language Processing",
        "intro": (
            "This is a complementary course hub. Canvas is the official site for this semester.\n"
            "                            Questions: <a href=\"mailto:mousavi@american.edu\">mousavi@american.edu</a>."
        ),
        "weeks_intro": (
            "Open a week for its lectures, labs, readings, and discussion prompts.\n"
            "                            Canvas remains the official list of required reading."
        ),
        "topics": {
            1: "NLP in the real world and Python",
            2: "Data acquisition and preprocessing",
            3: "Feature engineering, modeling, and evaluation",
            4: "Text representation",
            5: "Deep learning and Word2Vec",
            6: "Text classification",
            7: "CNNs for text",
            8: "Recurrent neural networks",
            9: "Midterm review",
            10: "Information extraction",
            11: "Named entity recognition",
            12: "Chatbots and dialog systems",
            13: "SVD and topic modeling",
            14: "LDA and NMF topic models",
            15: "Summarization, translation, and recommenders",
        },
    },
    "642": {
        "hub": "data-642.html",
        "prefix": "data-642",
        "code": "DATA 442/642",
        "full": "DATA 442/642: Advanced Machine Learning",
        "intro": (
            "Weekly lecture notes, labs, and homework for Advanced Machine Learning.\n"
            "                            Canvas is official for due dates and submissions. Questions:\n"
            "                            <a href=\"mailto:mousavi@american.edu\">mousavi@american.edu</a>."
        ),
        "weeks_intro": (
            "Open a week for its lectures, labs, readings, and discussion prompts.\n"
            "                            Canvas remains official for due dates."
        ),
        "topics": {
            1: "Machine learning and vector calculus",
            2: "Unconstrained optimization",
            3: "Constrained optimization, LP, and QP",
            4: "Sparsity-aware learning",
            5: "Hilbert spaces, kernels, and SVMs",
            6: "PCA",
            7: "Multimodal learning, CCA, and IVA",
            8: "Tensors",
            9: "Midterm",
            10: "Clustering",
            11: "GMMs and anomaly detection",
            12: "Perceptrons and multilayer nets",
            13: "Training neural nets",
            14: "Autoencoders and VAEs",
            15: "GANs",
        },
    },
    "643": {
        "hub": "data-643.html",
        "prefix": "data-643",
        "code": "DATA 443/643",
        "full": "DATA 443/643: Advanced Concepts in Large Language Models",
        "intro": (
            "Complementary notes, slides, and labs. Canvas is official for due dates and submissions.\n"
            "                            The listed prerequisite is DATA 427/627. DATA 441/641 and DATA 442/642 are\n"
            "                            <strong>not</strong> required; overlap with those courses is intentional so this\n"
            "                            sequence is self-contained. The semester is <strong>project-based</strong>.\n"
            "                            Questions: <a href=\"mailto:mousavi@american.edu\">mousavi@american.edu</a>."
        ),
        "weeks_intro": (
            "Open a week for its notes, labs, slides, videos, and discussion prompts.\n"
            "                            A weekly meeting is <strong>two hours</strong>: teach the notes (worked examples at the board),\n"
            "                            play about 10–20 minutes of the listed video, then the discussion prompts.\n"
            "                            Labs fill remaining studio time or homework. Canvas remains official for due dates."
        ),
        "topics": {
            1: "Neural networks and word embeddings",
            2: "Sequence models: RNNs, LSTMs, and GRUs",
            3: "Attention and transformers",
            4: "Multimodal foundations and vision transformers",
            5: "Vision–language models (CLIP and BLIP)",
            6: "Audio and cross-modal integration",
            7: "Scaling, efficiency, and deployment",
            8: "SFT, continual learning, and adapters",
            9: "RLHF and direct preference optimization",
            10: "Safety, editing, and retrieval-augmented training",
            11: "Generative models I: GANs",
            12: "Generative models II: diffusion",
            13: "Reasoning and chain-of-thought",
            14: "Tools, RAG, and final presentations",
            15: "Final exam and remaining talks",
        },
    },
}

SIDEBAR = r'''            <div class="sidebar sticky">
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
                                <a href="https://scholar.google.com/citations?user=IStw0S4AAAAJ&amp;hl=en" target="_blank" rel="noopener">
                                    <i class="ai ai-google-scholar-square ai-fw" aria-hidden="true"></i>
                                    <span class="label">Google Scholar</span>
                                </a>
                            </li>
                            <li>
                                <a href="https://orcid.org/0000-0003-4518-5857" target="_blank" rel="noopener">
                                    <i class="ai ai-orcid-square ai-fw" aria-hidden="true"></i>
                                    <span class="label">ORCID</span>
                                </a>
                            </li>
                            <li>
                                <a href="https://openreview.net/profile?id=%7EAhmad_Mousavi1" target="_blank" rel="noopener">
                                    <i class="icon-brand icon-openreview" aria-hidden="true"></i>
                                    <span class="label">OpenReview</span>
                                </a>
                            </li>
                            <li>
                                <a href="https://github.com/amousavi1" target="_blank" rel="noopener">
                                    <i class="fab fa-fw fa-github" aria-hidden="true"></i>
                                    <span class="label">GitHub</span>
                                </a>
                            </li>
                            <li>
                                <a href="https://www.researchgate.net/profile/Ahmad-Mousavi-5?ev=hdr_xprf" target="_blank" rel="noopener">
                                    <i class="ai ai-researchgate-square ai-fw" aria-hidden="true"></i>
                                    <span class="label">ResearchGate</span>
                                </a>
                            </li>
                            <li>
                                <a href="mailto:mousavi@american.edu">
                                    <i class="fas fa-fw fa-envelope-square" aria-hidden="true"></i>
                                    <span class="label">Email</span>
                                </a>
                            </li>
                            <li>
                                <a href="https://www.american.edu/cas/faculty/mousavi.cfm" target="_blank" rel="noopener">
                                    <i class="icon-brand icon-au" aria-hidden="true"></i>
                                    <span class="label">AU Profile</span>
                                </a>
                            </li>
                            <li>
                                <a href="https://www.linkedin.com/in/ahmad-mousavi-635986b0/" target="_blank" rel="noopener">
                                    <i class="fab fa-fw fa-linkedin" aria-hidden="true"></i>
                                    <span class="label">LinkedIn</span>
                                </a>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>'''


def extract_week_panels(html: str) -> dict[int, str]:
    pattern = re.compile(r'<div class="course-week-panel" id="week-(\d+)"[^>]*>')
    matches = list(pattern.finditer(html))
    if not matches:
        raise SystemExit("No week panels found")
    panels: dict[int, str] = {}
    for i, match in enumerate(matches):
        week = int(match.group(1))
        start = match.end()
        if i + 1 < len(matches):
            chunk = html[start : matches[i + 1].start()]
            chunk = re.sub(r"</div>\s*$", "", chunk)
        else:
            rest = html[start:]
            close = rest.find("</div>\n                        </div>")
            if close == -1:
                close = rest.find("</div>\r\n                        </div>")
            if close == -1:
                raise SystemExit(f"Could not find end of week {week} panel")
            chunk = rest[:close]
        panels[week] = chunk.strip("\n")
    return panels


def week_nav(prefix: str, hub: str, week: int, last: int) -> str:
    if week == 1:
        prev = f'<a class="course-page-nav__prev" href="{hub}"><span aria-hidden="true">←</span> Course hub</a>'
    else:
        prev = (
            f'<a class="course-page-nav__prev" href="{prefix}-week-{week - 1}.html">'
            f'<span aria-hidden="true">←</span> Week {week - 1}</a>'
        )
    if week == last:
        nxt = f'<a class="course-page-nav__next" href="{hub}">Course hub <span aria-hidden="true">→</span></a>'
    else:
        nxt = (
            f'<a class="course-page-nav__next" href="{prefix}-week-{week + 1}.html">'
            f"Week {week + 1} <span aria-hidden=\"true\">→</span></a>"
        )
    return (
        '                        <nav class="course-page-nav" aria-label="Page">\n'
        f"                            {prev}\n"
        f"                            {nxt}\n"
        "                        </nav>"
    )


def page_shell(title: str, article: str) -> str:
    return f"""<!doctype html>
<html lang="en" class="no-js">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>{title} - Ahmad Mousavi</title>
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
{SIDEBAR}

{article}
        </div>

        <div class="page__footer">
            <footer>
                <div class="page__footer-copyright">&copy; 2026 Ahmad Mousavi</div>
                <div class="page__footer-updated">Last updated: <time class="js-site-last-updated" datetime="{FOOTER_DT}">{FOOTER_LABEL}</time></div>
            </footer>
        </div>

        <script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token": "__CF_BEACON_TOKEN__"}}'></script>
        <script src="assets/js/site.js"></script>
    </body>
</html>
"""


def write_week_page(cfg: dict, week: int, last: int, inner: str) -> None:
    topic = cfg["topics"][week]
    title = f"Week {week}: {topic} - {cfg['code']}"
    article = f"""            <article class="page" itemscope itemtype="https://schema.org/LearningResource">
                <div class="page__inner-wrap">
                    <header>
                        <h1 id="page-title" class="page__title" itemprop="name">Week {week}: {topic}</h1>
                    </header>
                    <section class="page__content" itemprop="text">
                        <p class="lecture-meta">
                            <a href="{cfg['hub']}">{cfg['code']}</a> &middot; Week {week}
                        </p>
{inner}
{week_nav(cfg['prefix'], cfg['hub'], week, last)}
                    </section>
                </div>
            </article>"""
    path = ROOT / f"{cfg['prefix']}-week-{week}.html"
    path.write_text(page_shell(title, article), encoding="utf-8", newline="\n")


def weekly_table(cfg: dict) -> str:
    rows = []
    for week, topic in cfg["topics"].items():
        href = f"{cfg['prefix']}-week-{week}.html"
        rows.append(
            "                                <tr>\n"
            f'                                    <td><a href="{href}">{week}</a></td>\n'
            f'                                    <td><a href="{href}">{topic}</a></td>\n'
            "                                </tr>"
        )
    return (
        '                        <table class="course-schedule">\n'
        "                            <thead>\n"
        "                                <tr>\n"
        "                                    <th>Week</th>\n"
        "                                    <th>Topic</th>\n"
        "                                </tr>\n"
        "                            </thead>\n"
        "                            <tbody>\n"
        + "\n".join(rows)
        + "\n                            </tbody>\n"
        "                        </table>"
    )


def find_div_end(html: str, start: int) -> int:
    if not html.startswith("<div", start):
        raise SystemExit(f"Expected <div at {start}")
    i = start
    depth = 0
    while i < len(html):
        open_div = html.find("<div", i)
        close_div = html.find("</div>", i)
        if close_div == -1:
            raise SystemExit("Unclosed <div>")
        if open_div != -1 and open_div < close_div:
            depth += 1
            i = open_div + 4
        else:
            depth -= 1
            i = close_div + 6
            if depth == 0:
                return i
    raise SystemExit("Unclosed <div>")


DATA_641 = """                        <h2>Data</h2>
                        <table class="course-schedule">
                            <thead>
                                <tr>
                                    <th>Dataset</th>
                                    <th>Files</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>COVID-19 tweets</td>
                                    <td><a href="files/data-641/covid19_tweets.csv">covid19_tweets.csv</a></td>
                                </tr>
                                <tr>
                                    <td>Fake news</td>
                                    <td><a href="files/data-641/fakeNews.csv">fakeNews.csv</a></td>
                                </tr>
                                <tr>
                                    <td>Nemo</td>
                                    <td><a href="files/data-641/nemo.txt">nemo.txt</a></td>
                                </tr>
                                <tr>
                                    <td>Sample PDF</td>
                                    <td><a href="files/data-641/sample.pdf">sample.pdf</a></td>
                                </tr>
                                <tr>
                                    <td>Spam</td>
                                    <td><a href="files/data-641/spam.csv">spam.csv</a></td>
                                </tr>
                                <tr>
                                    <td>Train labels</td>
                                    <td><a href="files/data-641/TrainLabels.csv">TrainLabels.csv</a></td>
                                </tr>
                                <tr>
                                    <td>True news</td>
                                    <td><a href="files/data-641/trueNews.csv">trueNews.csv</a></td>
                                </tr>
                            </tbody>
                        </table>

                        <h2>Resources</h2>
                        <table class="course-schedule">
                            <thead>
                                <tr>
                                    <th>Resource</th>
                                    <th>What it is for</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td><a href="https://www.python.org/downloads/" target="_blank" rel="noopener">Python</a></td>
                                    <td>Install Python</td>
                                </tr>
                                <tr>
                                    <td><a href="https://jupyter.org/" target="_blank" rel="noopener">Jupyter</a></td>
                                    <td>Notebooks for labs</td>
                                </tr>
                                <tr>
                                    <td><a href="https://www.nltk.org/" target="_blank" rel="noopener">NLTK</a></td>
                                    <td>Classic NLP toolkit</td>
                                </tr>
                                <tr>
                                    <td><a href="https://www.oreilly.com/library/view/practical-natural-language/9781492054047/" target="_blank" rel="noopener">Practical Natural Language Processing</a></td>
                                    <td>Main textbook (Vajjala, Majumder, Gupta, Surana)</td>
                                </tr>
                                <tr>
                                    <td><a href="https://www.manning.com/books/deep-learning-with-python-second-edition" target="_blank" rel="noopener">Deep Learning with Python</a></td>
                                    <td>Neural nets (Chollet)</td>
                                </tr>
                            </tbody>
                        </table>
"""


def replace_span(html: str, start: int, end: int, replacement: str) -> str:
    return html[:start] + replacement + html[end:]


def rewrite_hub(key: str, cfg: dict) -> None:
    path = ROOT / cfg["hub"]
    html = path.read_text(encoding="utf-8")
    article_start = html.find('<article class="page"')
    if article_start == -1:
        raise SystemExit(f"No article in {cfg['hub']}")

    if '<div class="course-weeks">' in html:
        panels = extract_week_panels(html)
        last = max(panels)
        for week, inner in panels.items():
            write_week_page(cfg, week, last, inner)

        weekly_h2 = html.find("<h2>Weekly Materials</h2>", article_start)
        if weekly_h2 == -1:
            weekly_h2 = html.find("<h2>Weekly materials</h2>", article_start)
        if weekly_h2 == -1:
            raise SystemExit(f"No Weekly materials heading in {cfg['hub']}")
        weekly_h2 = html.rfind("\n", article_start, weekly_h2) + 1
        weeks_div = html.find('<div class="course-weeks">', weekly_h2)
        weeks_end = find_div_end(html, weeks_div)
        weekly = (
            "                        <h2>Weekly materials</h2>\n"
            '                        <p class="course-weeks-intro">\n'
            f"                            {cfg['weeks_intro']}\n"
            "                        </p>\n"
            f"{weekly_table(cfg)}"
        )
        html = replace_span(html, weekly_h2, weeks_end, weekly)

    meta = html.find('<p class="course-meta">American University</p>', article_start)
    if meta == -1:
        raise SystemExit(f"No course-meta in article of {cfg['hub']}")
    p_start = html.find("<p>", meta + 1)
    p_end = html.find("</p>", p_start) + 4
    html = replace_span(
        html,
        p_start,
        p_end,
        "<p>\n"
        f"                            {cfg['intro']}\n"
        "                        </p>",
    )

    if key == "641" and '<ul class="course-data-list">' in html:
        data_h2 = html.find("<h2>Data</h2>", article_start)
        resources_end = html.find("</section>", data_h2)
        html = replace_span(html, data_h2 - 24, resources_end, DATA_641 + "                    ")

    if 'class="author__bio"' not in html or 'id="page-title"' not in html:
        raise SystemExit(f"Rewrite damaged chrome in {cfg['hub']}")
    if "<h2>Syllabus" not in html:
        raise SystemExit(f"Rewrite dropped syllabus in {cfg['hub']}")

    html = html.replace(
        'datetime="2026-09-19T22:20:00-04:00">September 19, 2026, 10:20 PM EDT',
        f'datetime="{FOOTER_DT}">{FOOTER_LABEL}',
    )
    path.write_text(html, encoding="utf-8", newline="\n")


def link_lecture_weeks() -> None:
    for key, cfg in COURSES.items():
        prefix = cfg["prefix"]
        hub = cfg["hub"]
        for path in ROOT.glob(f"{prefix}-*.html"):
            if re.search(rf"{prefix}-week-\d+\.html$", path.name):
                continue
            if path.name == hub:
                continue
            text = path.read_text(encoding="utf-8")
            updated = re.sub(
                rf'(<a href="{re.escape(hub)}">{re.escape(cfg["code"])}</a> &middot; )Week (\d+)',
                rf'\1<a href="{prefix}-week-\2.html">Week \2</a>',
                text,
            )
            if updated != text:
                path.write_text(updated, encoding="utf-8", newline="\n")


def main() -> None:
    for key, cfg in COURSES.items():
        rewrite_hub(key, cfg)
        print(f"Rewrote {cfg['hub']} and week pages")
    link_lecture_weeks()
    print("Linked lecture breadcrumbs to week pages")


if __name__ == "__main__":
    main()
