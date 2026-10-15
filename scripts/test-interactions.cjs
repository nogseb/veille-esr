const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');

class Element {
  constructor(dataset = {}, classes = []) {
    this.dataset = dataset;
    this.hidden = false;
    this.attributes = {};
    this.events = {};
    const set = new Set(classes);
    this.classList = {
      contains: (name) => set.has(name),
      remove: (name) => set.delete(name),
      toggle: (name, value) => value ? set.add(name) : set.delete(name),
    };
  }
  setAttribute(name, value) { this.attributes[name] = value; }
  getAttribute(name) { return this.attributes[name]; }
  addEventListener(name, callback) { this.events[name] = callback; }
  click() { this.events.click?.(); }
  focus() { this.focused = true; }
}

function scopeFor(axes, sources = false) {
  const scope = new Element({}, sources ? ['sources-section'] : ['signals-section']);
  scope.items = axes.map((axis) => new Element({ axis }));
  scope.buttons = [...new Set(['all', ...axes, 'marque'])].map((filter) => new Element({ filter }));
  scope.counter = new Element();
  scope.empty = new Element();
  scope.empty.hidden = true;
  scope.querySelectorAll = (selector) => selector === '[data-axis]' ? scope.items : scope.buttons;
  scope.querySelector = (selector) => selector === '.empty-state' ? scope.empty : scope.counter;
  scope.select = (filter) => scope.buttons.find((button) => button.dataset.filter === filter).click();
  return scope;
}

const edition = scopeFor(['marche', 'offre', 'recherche', 'reputation', 'horschamp']);
const sources = scopeFor([...Array(6).fill('marque'), ...Array(7).fill('acquisition'), ...Array(6).fill('international')], true);
const menu = new Element();
menu.setAttribute('aria-expanded', 'false');
const navigation = new Element();
navigation.querySelectorAll = () => [];
const printButton = new Element();
const themeButton = new Element();
const themeLabel = new Element();
themeButton.querySelector = () => themeLabel;
const browserColor = new Element();
const html = new Element({ theme: 'dark' });
const store = new Map();
const documentEvents = {};
let printed = false;
const document = {
  documentElement: html,
  querySelectorAll(selector) {
    if (selector === '[data-filter-scope]') return [edition, sources];
    if (selector === '[data-print]') return [printButton];
    if (selector === '[data-filter="all"]') return [edition, sources].flatMap((scope) => scope.buttons.filter((button) => button.dataset.filter === 'all'));
    return [];
  },
  querySelector(selector) {
    if (selector === '[data-theme-toggle]') return themeButton;
    if (selector === 'meta[name="theme-color"]') return browserColor;
    return menu;
  },
  getElementById: () => navigation,
  addEventListener: (name, callback) => { documentEvents[name] = callback; },
};
const window = {
  print: () => { printed = true; },
  matchMedia: () => ({ addEventListener() {} }),
  localStorage: { getItem: (key) => store.get(key), setItem: (key, value) => store.set(key, value) },
};
const initializeTheme = fs.readFileSync(path.join(__dirname, '../assets/theme-init.js'), 'utf8');
for (const [saved, expected] of [[undefined, 'dark'], ['light', 'light'], ['dark', 'dark'], ['unexpected', 'dark']]) {
  store.clear();
  if (saved !== undefined) store.set('veille-esr-theme', saved);
  vm.runInNewContext(initializeTheme, { document, window });
  assert.equal(html.dataset.theme, expected);
}
store.clear();
vm.runInNewContext(fs.readFileSync(path.join(__dirname, '../assets/app.js'), 'utf8'), { document, window });
assert.equal(html.dataset.theme, 'dark');
assert.equal(themeButton.getAttribute('aria-label'), 'Activer le mode clair');
assert.equal(themeButton.hidden, false);
themeButton.click();
assert.equal(html.dataset.theme, 'light');
assert.equal(store.get('veille-esr-theme'), 'light');
assert.equal(themeLabel.textContent, 'Sombre');
assert.equal(themeButton.getAttribute('aria-pressed'), 'false');
vm.runInNewContext(initializeTheme, { document, window });
assert.equal(html.dataset.theme, 'light');
themeButton.click();
assert.equal(html.dataset.theme, 'dark');
window.localStorage = { getItem() { throw new Error('blocked'); }, setItem() { throw new Error('blocked'); } };
vm.runInNewContext(initializeTheme, { document, window });
assert.equal(html.dataset.theme, 'dark');
themeButton.click();
assert.equal(html.dataset.theme, 'light');
themeButton.click();
assert.equal(html.dataset.theme, 'dark');

edition.select('marque');
assert.equal(edition.counter.textContent, '0 signal');
assert.equal(edition.empty.hidden, false);
assert.ok(edition.items.every((item) => item.hidden));
edition.select('horschamp');
assert.equal(edition.counter.textContent, '1 signal');
assert.equal(edition.items.filter((item) => !item.hidden).length, 1);
assert.equal(edition.empty.hidden, true);
sources.select('acquisition');
assert.equal(sources.counter.textContent, '7 sources');
assert.equal(sources.items.filter((item) => !item.hidden).length, 7);
assert.equal(sources.buttons.filter((button) => button.attributes['aria-pressed'] === 'true').length, 1);
menu.click();
assert.equal(menu.getAttribute('aria-expanded'), 'true');
assert.equal(navigation.classList.contains('is-open'), true);
documentEvents.keydown({ key: 'Escape' });
assert.equal(menu.getAttribute('aria-expanded'), 'false');
assert.equal(navigation.classList.contains('is-open'), false);
printButton.click();
assert.equal(edition.items.filter((item) => !item.hidden).length, 5);
assert.equal(sources.items.filter((item) => !item.hidden).length, 19);
assert.ok(printed);
console.log('PASS: dark default, saved choice, accessible theme toggle, blocked storage, filters, empty state, mobile menu, Escape and print reset.');
