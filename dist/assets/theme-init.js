(() => {
  'use strict';
  let theme = 'dark';
  try {
    const saved = window.localStorage.getItem('veille-esr-theme');
    if (saved === 'light' || saved === 'dark') theme = saved;
  } catch {
    // Storage can be blocked: the default dark theme still works.
  }
  document.documentElement.dataset.theme = theme;
  const browserColor = document.querySelector('meta[name="theme-color"]');
  if (browserColor) browserColor.setAttribute('content', theme === 'dark' ? '#111410' : '#f5f5ef');
})();
