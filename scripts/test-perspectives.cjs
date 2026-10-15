'use strict';
const assert = require('node:assert/strict');
const { createState, selectFacet, canRotate, setPanelInteractivity, ROTATION_DELAY } = require('../assets/perspectives.js');

const state = createState(false);
assert.equal(ROTATION_DELAY, 24000);
assert.equal(canRotate(state), false, 'No animation before the module enters view.');
state.visible = true;
assert.equal(canRotate(state), true);
for (const property of ['hovered', 'focused', 'pageHidden', 'userPaused', 'reduced']) {
  state[property] = true;
  assert.equal(canRotate(state), false, `${property} must stop automatic rotation.`);
  state[property] = false;
}
for (let step = 1; step <= 8; step++) {
  selectFacet(state, state.active + 1, false);
  assert.equal(state.active, step % 4);
  assert.equal(state.step, step, 'Rotation continues through 360° without a reverse jump.');
}
selectFacet(state, 2, true);
assert.equal(state.active, 2);
assert.equal(state.userPaused, true, 'A manual choice pauses autoplay.');
assert.equal(canRotate(state), false);
selectFacet(state, -1, true);
assert.equal(state.active, 3);
selectFacet(state, 4, true);
assert.equal(state.active, 0);
const reduced = createState(true);
reduced.visible = true;
assert.equal(canRotate(reduced), false);
reduced.userPaused = false;
assert.equal(canRotate(reduced), false, 'Reduced motion cannot accidentally enable autoplay.');
selectFacet(reduced, 1, true);
assert.equal(reduced.active, 1, 'Manual reading remains available with reduced motion.');
function link(initial) {
  const attrs = initial === null ? {} : { tabindex: initial };
  return {
    getAttribute: (name) => attrs[name] ?? null,
    setAttribute: (name, value) => { attrs[name] = value; },
    removeAttribute: (name) => { delete attrs[name]; }
  };
}
const normal = link(null), custom = link('2');
const panel = { querySelectorAll: () => [normal, custom] };
const remembered = new WeakMap();
setPanelInteractivity(panel, false, remembered);
assert.equal(normal.getAttribute('tabindex'), '-1');
assert.equal(custom.getAttribute('tabindex'), '-1');
setPanelInteractivity(panel, true, remembered);
assert.equal(normal.getAttribute('tabindex'), null);
assert.equal(custom.getAttribute('tabindex'), '2');
setPanelInteractivity(panel, false, remembered);
setPanelInteractivity(panel, true, remembered);
assert.equal(custom.getAttribute('tabindex'), '2', 'Original keyboard behavior survives repeated changes.');
console.log('PASS: four facets, continuous rotation, manual selection, visibility/focus/hover pause, reduced motion and keyboard fallback.');
