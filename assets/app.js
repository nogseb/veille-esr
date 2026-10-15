(() => {
  'use strict';

  const themeButton = document.querySelector('[data-theme-toggle]');
  if (themeButton) {
    const themeLabel = themeButton.querySelector('.theme-label');
    const browserColor = document.querySelector('meta[name="theme-color"]');
    function updateTheme(theme) {
      const dark = theme !== 'light';
      document.documentElement.dataset.theme = dark ? 'dark' : 'light';
      themeButton.setAttribute('aria-pressed', String(dark));
      themeButton.setAttribute('aria-label', dark ? 'Activer le mode clair' : 'Activer le mode sombre');
      themeButton.setAttribute('title', dark ? 'Activer le mode clair' : 'Activer le mode sombre');
      if (themeLabel) themeLabel.textContent = dark ? 'Clair' : 'Sombre';
      if (browserColor) browserColor.setAttribute('content', dark ? '#111410' : '#f5f5ef');
    }
    updateTheme(document.documentElement.dataset.theme);
    themeButton.hidden = false;
    themeButton.addEventListener('click', () => {
      const theme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
      updateTheme(theme);
      try {
        window.localStorage.setItem('veille-esr-theme', theme);
      } catch {
        // The switch remains usable when local storage is unavailable.
      }
    });
  }

  const normalize = (value) => String(value ?? '').toLowerCase().trim();

  document.querySelectorAll('[data-filter-scope]').forEach((scope) => {
    const buttons = [...scope.querySelectorAll('[data-filter]')];
    const items = [...scope.querySelectorAll('[data-axis]')];
    const counter = scope.querySelector('[data-result-count]');
    const empty = scope.querySelector('.empty-state');
    const noun = scope.classList.contains('sources-section') ? 'source' : 'signal';

    function applyFilter(value) {
      const filter = normalize(value);
      let visibleCount = 0;
      items.forEach((item) => {
        const visible = filter === 'all' || normalize(item.dataset.axis) === filter;
        item.hidden = !visible;
        if (visible) visibleCount += 1;
      });
      buttons.forEach((button) => {
        const selected = normalize(button.dataset.filter) === filter;
        button.classList.toggle('is-active', selected);
        button.setAttribute('aria-pressed', String(selected));
      });
      if (counter) counter.textContent = `${visibleCount} ${noun}${visibleCount > 1 ? 's' : ''}`;
      if (empty) empty.hidden = visibleCount !== 0;
    }

    buttons.forEach((button) => {
      button.addEventListener('click', () => applyFilter(button.dataset.filter));
    });
  });

  const menuButton = document.querySelector('.menu-toggle');
  const navigation = document.getElementById('navigation');
  const closeMenu = () => {
    if (!menuButton || !navigation) return;
    navigation.classList.remove('is-open');
    menuButton.setAttribute('aria-expanded', 'false');
  };
  if (menuButton && navigation) {
    menuButton.addEventListener('click', () => {
      const isOpen = menuButton.getAttribute('aria-expanded') !== 'true';
      menuButton.setAttribute('aria-expanded', String(isOpen));
      navigation.classList.toggle('is-open', isOpen);
    });
    navigation.querySelectorAll('a').forEach((link) => link.addEventListener('click', closeMenu));
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') {
        closeMenu();
        menuButton.focus();
      }
    });
    window.matchMedia('(min-width: 761px)').addEventListener('change', closeMenu);
  }

  document.querySelectorAll('[data-print]').forEach((button) => {
    button.addEventListener('click', () => {
      document.querySelectorAll('[data-filter="all"]').forEach((filter) => filter.click());
      window.print();
    });
  });
})();
