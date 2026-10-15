(() => {
  'use strict';

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
