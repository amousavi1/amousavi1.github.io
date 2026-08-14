(() => {
  // Single source of truth for the site-wide "Last updated" footer stamp.
  // Bump this ISO datetime whenever website content is changed.
  const SITE_LAST_UPDATED = '2026-08-14T15:35:00-07:00';

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
    'cardinality-constrained structured optimization': 'Sparse Optimization',
    'sparse and structured quadratic surface support vector machines': 'QSVMs',
    'robust multi-scale and multi-modal learning': 'Multi-Modal Learning',
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

    const headings = Array.from(content.querySelectorAll('h2, h3'));
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
        link.textContent = shortTocTitle(fullTitle);
        link.title = toTitleCase(fullTitle);

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

  // Run early.
  setHtmlJsClass();

  // DOM-dependent initializers.
  window.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initAuthorUrlsToggle();
    initMastheadSpacing();
    initSiteLastUpdated();
    initPageToc();
  });
})();
