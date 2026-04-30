(() => {
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
      const h = masthead.getBoundingClientRect().height;
      document.body.style.paddingTop = `${Math.ceil(h)}px`;
    };

    update();
    window.addEventListener('resize', update);
    if (screen.orientation && screen.orientation.addEventListener) {
      screen.orientation.addEventListener('change', update);
    }
  }

  function initGreedyNav() {
    const nav = document.getElementById('site-nav');
    if (!nav) return;

    const visible = nav.querySelector('.visible-links');
    const hidden = nav.querySelector('.hidden-links');
    const toggle = nav.querySelector('.greedy-nav__toggle');

    if (!visible || !hidden || !toggle) return;

    const ensureToggleState = () => {
      const hiddenCount = hidden.children.length;
      if (hiddenCount > 0) {
        toggle.classList.remove('hidden');
        toggle.setAttribute('count', String(hiddenCount));
      } else {
        toggle.classList.add('hidden');
        toggle.setAttribute('count', '');
        hidden.classList.add('hidden');
        toggle.classList.remove('close');
      }
    };

    const availableWidth = () => {
      // Width nav can use, minus toggle buttons.
      const navWidth = nav.getBoundingClientRect().width;
      const title = nav.querySelector('.site-title');
      const titleWidth = title ? title.getBoundingClientRect().width : 0;
      const toggleWidth = toggle.getBoundingClientRect().width;
      const themeToggle = nav.querySelector('#theme-toggle');
      const themeWidth = themeToggle ? themeToggle.getBoundingClientRect().width : 0;
      // Small buffer for padding/gaps.
      return navWidth - titleWidth - toggleWidth - themeWidth - 40;
    };

    const linksWidth = () => visible.getBoundingClientRect().width;

    const update = () => {
      // Reset: move everything back to visible first, preserving order.
      while (hidden.firstElementChild) {
        visible.appendChild(hidden.firstElementChild);
      }

      // If overflow, move from end to hidden until it fits.
      let tries = 0;
      while (linksWidth() > availableWidth() && visible.children.length > 0 && tries < 50) {
        hidden.insertBefore(visible.lastElementChild, hidden.firstElementChild);
        tries++;
      }

      ensureToggleState();
    };

    toggle.addEventListener('click', () => {
      hidden.classList.toggle('hidden');
      toggle.classList.toggle('close');
    });

    update();
    window.addEventListener('resize', update);
    if (screen.orientation && screen.orientation.addEventListener) {
      screen.orientation.addEventListener('change', update);
    }
  }

  // Run early.
  setHtmlJsClass();

  // DOM-dependent initializers.
  window.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initAuthorUrlsToggle();
    initMastheadSpacing();
    initGreedyNav();
  });
})();
