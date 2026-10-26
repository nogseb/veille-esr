const fs = require('fs');
const assert = require('assert');

const build = fs.readFileSync('scripts/build.py', 'utf8');
const css = fs.readFileSync('assets/featured-source.css', 'utf8');
assert(build.includes('featured_source(source)'));
assert(build.includes('class="featured-label"'));
assert(build.includes('class="featured-source"'));
assert(build.includes('class="featured-source-link"'));
assert(build.includes("asset(p, 'featured-source.css')"));
assert(css.includes('grid-template-columns:minmax(0,1fr)'));
assert(css.includes('overflow-wrap:anywhere'));
assert(css.includes('flex:1 1 auto'));
assert(!css.includes('white-space:nowrap'));
console.log('PASS: source de la carte vedette séparée, fluide et sans retour forcé.');
