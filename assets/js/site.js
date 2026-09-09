(() => {
  // Single source of truth for the site-wide "Last updated" footer stamp.
  // Bump this ISO datetime whenever website content is changed.
  const SITE_LAST_UPDATED = '2026-09-09T15:36:00-04:00';

  function formatSiteLastUpdated(isoDateTime) {
    const date = new Date(isoDateTime);
    if (Number.isNaN(date.getTime())) return isoDateTime;
    return date.toLocaleString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: 'numeric',
      minute: '2-digit',
      timeZoneName: 'short',
    });
  }

  function initSiteLastUpdated() {
    const label = formatSiteLastUpdated(SITE_LAST_UPDATED);
    document.querySelectorAll('.js-site-last-updated').forEach((el) => {
      el.setAttribute('datetime', SITE_LAST_UPDATED);
      el.textContent = label;
    });
  }

  function setHtmlJsClass() {
    const html = document.documentElement;
    html.className = (html.className || '').replace(/\bno-js\b/g, '').trim();
    if (!html.classList.contains('js')) html.classList.add('js');
  }

  function getThemeSetting() {
    const t = localStorage.getItem('theme');
    return t === 'dark' || t === 'light' ? t : null;
  }

  function getPreferredTheme() {
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
      ? 'dark'
      : 'light';
  }

  function applyTheme(theme) {
    const html = document.documentElement;
    const icon = document.getElementById('theme-icon');

    if (theme === 'dark') {
      html.setAttribute('data-theme', 'dark');
      if (icon) {
        icon.classList.remove('fa-sun');
        icon.classList.add('fa-moon');
      }
    } else {
      html.removeAttribute('data-theme');
      if (icon) {
        icon.classList.remove('fa-moon');
        icon.classList.add('fa-sun');
      }
    }
  }

  function initTheme() {
    const toggle = document.getElementById('theme-toggle');
    const media = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;

    const initial = getThemeSetting() || getPreferredTheme();
    applyTheme(initial);

    if (media && media.addEventListener) {
      media.addEventListener('change', (e) => {
        if (getThemeSetting()) return;
        applyTheme(e.matches ? 'dark' : 'light');
      });
    }

    if (!toggle) return;
    toggle.addEventListener('click', (e) => {
      if (e && typeof e.preventDefault === 'function') e.preventDefault();
      const current = document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
      const next = current === 'dark' ? 'light' : 'dark';
      localStorage.setItem('theme', next);
      applyTheme(next);
    });
  }

  function initAuthorUrlsToggle() {
    const wrapper = document.querySelector('.author__urls-wrapper');
    if (!wrapper) return;

    const button = wrapper.querySelector('button');
    const urls = wrapper.querySelector('.author__urls');
    if (!button || !urls) return;

    button.addEventListener('click', () => {
      const isOpen = button.classList.toggle('open');
      urls.style.display = isOpen ? 'block' : '';
    });
  }

  function initMastheadSpacing() {
    const masthead = document.querySelector('.masthead');
    if (!masthead) return;

    const update = () => {
      const h = Math.ceil(masthead.getBoundingClientRect().height);
      document.body.style.paddingTop = `${h}px`;
      document.documentElement.style.setProperty('--masthead-height', `${h}px`);
    };

    update();
    window.addEventListener('resize', update);
    if (screen.orientation && screen.orientation.addEventListener) {
      screen.orientation.addEventListener('change', update);
    }
  }

  const TOC_SHORT_TITLES = {
    'working with students': 'For Students',
    'cardinality-constrained structured optimization': 'Sparse Optimization',
    'sparse and structured quadratic surface support vector machines': 'QSVMs',
    'robust multi-scale and multi-modal learning': 'Multi-Modal Learning',
    'a. what `c()` actually builds': 'A. What c() Builds',
    'c. indexing is a language': 'C. Indexing',
    'd. packages, names, and what r is searching': 'D. Packages and Names',
    'e. arithmetic that is not the arithmetic you learned in school': 'E. Arithmetic',
    'f. files, data frames, and silent shape changes': 'F. Files and Data Frames',
    'g. optional: the questions that are meant to bother you': 'G. Optional',
    '4. what happens when types are mixed?': '4. Coercion',
    '11. the seq() function': '11. seq()',
    '12. special values: na, nan, inf, and null': '12. Special Values',
    '13. detecting special values: the is.*() family': '13. Detecting Special Values',
    '16. useful is.*() functions': '16. is.*() Functions',
    '17. useful as.*() functions': '17. as.*() Functions',
    '18. a useful family of functions to remember': '18. Function Families',
    '1. read the pipe as "then"': '1. Then',
    '2. three ways to compute a geometric mean': '2. Geometric Mean',
    '3. extra arguments stay in the function that needs them': '3. Extra Arguments',
    '4. `subset()` keeps the rows you want': '4. subset()',
    '4. other magrittr pipes (aside)': '4. Other Pipes',
    '5. other magrittr pipes (aside)': '5. Other Pipes',
    '6. practice': '6. Practice',
    '2. duplication is a reason to stop and wrap': '2. Duplication',
    '3. `if` needs one `true` or `false`': '3. if',
    '4. names, arguments, and scope': '4. Names and Scope',
    '5. comments and roxygen': '5. Documentation',
    '1. a script is code you keep': '1. Scripts',
    '2. write the function once': '2. Write Once',
    '3. `source()` makes the function available': '3. source()',
    '5. this week, in one place': '5. Week Recap',
    '7. this week, in one place': '7. Week Recap',
    '1. why we plot': '1. Why Plot',
    '2. the grammar, in four pieces': '2. Grammar',
    '3. which variable is `x`': '3. x and y',
    '4. a third variable: categorical': '4. Categorical',
    '5. a third variable: quantitative': '5. Quantitative',
    '1. smoothing: `geom_smooth()`': '1. Smooth',
    '2. where the mapping lives': '2. Mapping Scope',
    '3. overplotting': '3. Overplotting',
    '4. one quantitative variable: histograms and densities': '4. Histograms',
    '5. one categorical and one quantitative: boxplots': '5. Boxplots',
    '2. a fixed color is not a mapping': '2. Fixed Color',
    '4. scales and colorblind palettes': '4. Scales',
    '6. saving a plot': '6. ggsave()',
    '1. mappings': '1. Mappings',
    '2. smooths and overplotting': '2. Smooths',
    '3. distributions and boxplots': '3. Distributions',
    '4. facets, theme, and save': '4. Facets',
    '2. write `add_half()`': '2. add_half()',
    '3. check the inputs': '3. Input Checks',
    '1. why dplyr': '1. Why dplyr',
    '2. `filter()` keeps rows by value': '2. filter()',
    '3. `slice()` keeps rows by position': '3. slice()',
    '4. `arrange()` sorts rows': '4. arrange()',
    '1. `select()` keeps columns': '1. select()',
    '2. `rename()`': '2. rename()',
    '3. `mutate()` and `transmute()`': '3. mutate()',
    '4. `relocate()`': '4. relocate()',
    '1. `summarize()` collapses rows': '1. summarize()',
    '2. `group_by()` makes virtual groups': '2. group_by()',
    '3. this week, in one place': '3. Week Recap',
    '1. filter and slice': '1. Filter and Slice',
    '2. arrange, select, mutate': '2. Arrange and Mutate',
    '3. summarize and group': '3. Summarize',
    '1. `rowwise()` is a group of one': '1. rowwise()',
    '2. `across()` repeats a function on columns': '2. across()',
    '1. `case_when()`': '1. case_when()',
    '2. row names and `distinct()`': '2. Distinct',
    '3. programming note (aside)': '3. Programming',
    '4. this week, in one place': '4. Week Recap',
    '1. row-wise and across': '1. Row-wise',
    '2. case_when and row names': '2. case_when',
    '1. paths, once more': '1. Paths',
    '2. `readr` reads flat files into tibbles': '2. readr',
    '3. check the import immediately': '3. Check Import',
    '4. write files back out': '4. Write Out',
    '1. parse after the file is in': '1. Parse',
    '2. dates and times': '2. Dates',
    '3. numbers, logicals, factors': '3. Numbers',
    '4. `col_types` at import': '4. col_types',
    '1. a working order': '1. Working Order',
    '2. one variable': '2. One Variable',
    '3. two variables': '3. Two Variables',
    '4. missingness, patterns, outliers': '4. Missingness',
    '5. this week, in one place': '5. Week Recap',
    '1. import': '1. Import',
    '2. parsers': '2. Parsers',
    '3. eda': '3. EDA',
    '1. tidy data': '1. Tidy Data',
    '2. `table1` is tidy; `table4a` is not': '2. table1 vs table4a',
    '3. `pivot_longer()` makes columns into rows': '3. pivot_longer()',
    '4. numeric-looking names need backticks': '4. Backticks',
    '1. `pivot_wider()` is the inverse': '1. pivot_wider()',
    '2. duplicate keys fail': '2. Duplicate Keys',
    '3. `separate()` splits one column': '3. separate()',
    '4. `unite()` pastes columns': '4. unite()',
    '5. tidy, then join': '5. Then Join',
    '2. wider, separate, unite': '2. Wider',
    '1. several tables, one system': '1. Several Tables',
    '2. check the keys': '2. Keys',
    '3. mutating joins add columns': '3. Mutating Joins',
    '1. `semi_join()` and `anti_join()`': '1. Filtering Joins',
    '2. duplicate keys and many-to-many': '2. Many-to-Many',
    '3. worst delay days, then those flights': '3. Worst Days',
    '4. plane age and delay': '4. Plane Age',
    '1. when a data frame is not enough': '1. Why a Database',
    '2. connect, copy, `tbl()`': '2. Connect',
    '3. lazy verbs, then `collect()`': '3. collect()',
    '4. close the connection': '4. Disconnect',
    '1. the five tables': '1. Five Tables',
    '2. destinations and airports': '2. Destinations',
    '3. delay by timezone': '3. Timezone',
    '5. plane age and delay': '5. Plane Age',
    '1. a string is text in quotes': '1. Strings',
    '2. length and pieces': '2. Length',
    '3. `str_sub()` extracts and replaces': '3. str_sub()',
    '5. a first replacement': '5. Replace',
    '1. a pattern is a regular expression': '1. Regex',
    '2. the language, in pieces': '2. Pieces',
    '3. detect, count, extract, split, replace': '3. stringr Verbs',
    '4. `separate()` with a regex': '4. separate()',
    '1. pieces and replacement': '1. Pieces',
    '2. regular expressions': '2. Regex',
    '1. a factor is an integer plus labels': '1. Factors',
    '3. reorder levels': '3. Reorder',
    '4. recode, collapse, lump': '4. Recode',
    '5. add, drop, and missing levels': '5. Add and Drop',
    '1. load lubridate and look at the class': '1. Classes',
    '2. parsers and constructors': '2. Parsers',
    '3. pull pieces out': '3. Extract',
    '4. durations, periods, and intervals': '4. Spans',
    '5. time zones': '5. Time Zones',
    '1. question, then evidence': '1. Evidence',
    '2. two-sample `t.test()`': '2. t.test()',
    '3. h0 and the p-value': '3. p-value',
    '4. anova and nested models': '4. ANOVA',
    '1. fit a linear model': '1. lm()',
    '2. read the fit': '2. Read the Fit',
    '3. residual plots': '3. Residuals',
    '4. numerical summaries': '4. Summaries',
    '1. two-sample t-test': '1. t-test',
    '4. column summaries': '4. Summaries',
    '1. why knit slides from code': '1. Why Knit',
    '3. yaml and slide breaks': '3. YAML',
    '4. what to show': '4. What to Show',
    '5. one idea per slide': '5. One Idea',
    '2. mean arrival delay by day': '2. Daily Delay',
    '3. the line plot, no code': '3. Plot',
    '1. label every chunk': '1. Labels',
    '2. options that hide or skip work': '2. Options',
    '3. defaults in a setup chunk': '3. Setup',
    '4. tables with `kable()`': '4. kable()',
    '5. folding code in the yaml': '5. Folding',
    '6. child documents': '6. Child Docs',
    '7. load a package only if it is missing': '7. Conditional Load',
    '1. numbered figures and tables': '1. Numbers',
    '2. cross-references': '2. Cross-Refs',
    '3. a `.bib` file': '3. Bib',
    '4. cite in the text': '4. Cite',
    '5. style with csl': '5. CSL',
    '6. the same idea in quarto': '6. Quarto',
    '2. a table and a plot': '2. Table and Plot',
    '3. a citation and folding': '3. Cite',
    '1. two kinds of vectors': '1. Two Kinds',
    '2. `[` keeps structure; `[[` extracts one': '2. [ and [[',
    '3. recycling and names': '3. Recycling',
    '4. lists hold mixed types': '4. Lists',
    '5. a data frame is a list of columns': '5. Data Frames',
    '1. a for-loop, pre-allocated': '1. for',
    '2. `while` when `n` is unknown': '2. while',
    '3. `across()` often replaces a column loop': '3. across()',
    '4. `purrr::map`': '4. map()',
    '5. `map2` and `pmap`': '5. map2',
    '6. `keep` / `discard` and split-plus-map': '6. keep',
    '1. the lifecycle': '1. Lifecycle',
    '2. tools you have now': '2. Tools',
    '3. last lesson': '3. Iterate',
    '1. a sampling distribution': '1. Sampling',
  };

  function toTitleCase(text) {
    return String(text || '')
      .replace(/\s+/g, ' ')
      .trim()
      .split(' ')
      .filter(Boolean)
      .map((word) =>
        word
          .split('-')
          .map((part) => (part ? part.charAt(0).toUpperCase() + part.slice(1) : part))
          .join('-')
      )
      .join(' ');
  }

  function shortTocTitle(fullTitle) {
    const full = String(fullTitle || '').replace(/\s+/g, ' ').trim();
    const mapped = TOC_SHORT_TITLES[full.toLowerCase()];
    return toTitleCase(mapped || full);
  }

  function slugifyHeading(text) {
    const slug = String(text || '')
      .toLowerCase()
      .replace(/&/g, 'and')
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-+|-+$/g, '');
    return slug || 'section';
  }

  function ensureHeadingId(heading) {
    if (heading.id) return heading.id;
    const base = slugifyHeading(heading.textContent);
    let id = base;
    let n = 2;
    while (document.getElementById(id)) {
      id = `${base}-${n}`;
      n += 1;
    }
    heading.id = id;
    return id;
  }

  function initTocSpy(nav, headings) {
    const links = Array.from(nav.querySelectorAll('a[href^="#"]'));
    if (!links.length || !('IntersectionObserver' in window)) return;

    const linkById = new Map(links.map((link) => [link.getAttribute('href').slice(1), link]));
    let currentId = '';

    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((entry) => entry.isIntersecting)
          .sort((a, b) => b.intersectionRatio - a.intersectionRatio);
        if (!visible.length) return;
        const id = visible[0].target.id;
        if (!id || id === currentId) return;
        currentId = id;
        links.forEach((link) => {
          const active = linkById.get(id) === link;
          link.classList.toggle('is-active', active);
          if (active) link.setAttribute('aria-current', 'location');
          else link.removeAttribute('aria-current');
        });
      },
      { rootMargin: '-20% 0px -65% 0px', threshold: [0, 0.25, 1] }
    );

    headings.forEach((heading) => observer.observe(heading));
  }

  function initPageToc() {
    const main = document.getElementById('main');
    const content = document.querySelector('#main > .page .page__content');
    if (!main || !content) return;

    const headingSelector = document.body.classList.contains('page-lecture') ? 'h2' : 'h2, h3';
    const headings = Array.from(content.querySelectorAll(headingSelector));
    const aside = document.createElement('aside');
    aside.className = 'sidebar-right';
    aside.setAttribute('aria-label', 'On this page');

    if (headings.length) {
      const nav = document.createElement('nav');
      nav.className = 'page-toc';

      const title = document.createElement('p');
      title.className = 'page-toc__title';
        title.textContent = 'Contents';
      nav.appendChild(title);

      const list = document.createElement('ul');
      list.className = 'page-toc__list';

      let currentH2Item = null;
      let h3List = null;

      headings.forEach((heading) => {
        const id = ensureHeadingId(heading);
        const fullTitle = heading.textContent.replace(/\s+/g, ' ').trim();
        const link = document.createElement('a');
        link.href = `#${id}`;
        const lecturePage = document.body.classList.contains('page-lecture');
        if (lecturePage) {
          const mapped = TOC_SHORT_TITLES[fullTitle.toLowerCase()];
          link.textContent = mapped || fullTitle;
          link.title = fullTitle;
        } else {
          link.textContent = shortTocTitle(fullTitle);
          link.title = toTitleCase(fullTitle);
        }

        if (heading.tagName === 'H3' && currentH2Item) {
          if (!h3List) {
            h3List = document.createElement('ul');
            h3List.className = 'page-toc__sublist';
            currentH2Item.appendChild(h3List);
          }
          const item = document.createElement('li');
          item.appendChild(link);
          h3List.appendChild(item);
          return;
        }

        const item = document.createElement('li');
        item.appendChild(link);
        list.appendChild(item);
        currentH2Item = item;
        h3List = null;
      });

      nav.appendChild(list);
      aside.appendChild(nav);
      initTocSpy(nav, headings);
    }

    const page = main.querySelector(':scope > .page');
    if (page) page.insertAdjacentElement('afterend', aside);
    else main.appendChild(aside);
  }

  function initCourseWeekTabs() {
    const root = document.querySelector('.course-weeks');
    if (!root) return;

    const tabs = Array.from(root.querySelectorAll('[role="tab"]'));
    const panels = Array.from(root.querySelectorAll('[role="tabpanel"]'));
    if (!tabs.length || !panels.length) return;

    const selectTab = (tab) => {
      const panelId = tab.getAttribute('aria-controls');
      tabs.forEach((item) => {
        const selected = item === tab;
        item.setAttribute('aria-selected', selected ? 'true' : 'false');
        item.tabIndex = selected ? 0 : -1;
      });
      panels.forEach((panel) => {
        panel.hidden = panel.id !== panelId;
      });
    };

    tabs.forEach((tab) => {
      tab.addEventListener('click', () => selectTab(tab));
    });

    const hash = window.location.hash.replace('#', '');
    const fromHash = hash ? tabs.find((tab) => tab.getAttribute('aria-controls') === hash) : null;
    selectTab(fromHash || tabs[0]);
  }

  // Run early.
  setHtmlJsClass();

  // DOM-dependent initializers.
  window.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initAuthorUrlsToggle();
    initMastheadSpacing();
    initSiteLastUpdated();
    initPageToc();
    initCourseWeekTabs();
  });
})();
