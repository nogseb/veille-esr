'use strict';
const assert = require('node:assert/strict');
const {
  createState, selectFacet, canRotate, setPanelInteractivity, createRipplePositions,
  shouldAnimateAmbient, createSatelliteMotions, ROTATION_DELAY, MAX_HERO_RIPPLES, HERO_RIPPLE_REFRESH
} = require('../assets/perspectives.js');

const state = createState(false);
assert.equal(ROTATION_DELAY, 24000);
assert.equal(MAX_HERO_RIPPLES, 3);
assert.equal(HERO_RIPPLE_REFRESH, 5600);
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

const sequence = [0.02, 0.98, 0.76, 0.21, 0.44, 0.66, 0.13, 0.84, 0.58, 0.35];
let pointer = 0;
const points = createRipplePositions(() => sequence[pointer++ % sequence.length], 5);
assert.equal(points.length, 3, 'Hero never renders more than three simultaneous points.');
for (const point of points) {
  assert.ok(point.x >= 12 && point.x <= 84);
  assert.ok(point.y >= 17 && point.y <= 81);
}
assert.equal(new Set(points.map((point) => `${point.x}:${point.y}`)).size, 3, 'Random hero points retain distinct positions.');
assert.equal(shouldAnimateAmbient(true, false, false), true);
assert.equal(shouldAnimateAmbient(false, false, false), false);
assert.equal(shouldAnimateAmbient(true, true, false), false, 'Reduced motion stops orbital movement.');
assert.equal(shouldAnimateAmbient(true, false, true), false, 'A hidden tab stops orbital movement.');
const satelliteSequence = [0.04, 0.1, 0.16, 0.81, 0.9, 0.28, 0.42, 0.38, 0.73];
let satellitePointer = 0;
const satellites = createSatelliteMotions(() => satelliteSequence[satellitePointer++ % satelliteSequence.length], 3);
assert.equal(satellites.length, 3);
assert.ok(satellites.every((item) => item.speed >= 0.0024 && item.speed <= 0.009));
assert.ok(satellites.every((item) => [-1, 1].includes(item.direction)));
assert.equal(new Set(satellites.map((item) => item.speed)).size, 3, 'Each satellite receives a distinct sampled orbital speed.');
assert.ok(new Set(satellites.map((item) => item.phase)).size > 1, 'Satellite phases are not synchronized.');
console.log('PASS: four facets, controlled rotation, three-point hero, randomized satellite orbits, reduced motion and keyboard fallback.');
