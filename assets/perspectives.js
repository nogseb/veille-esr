(function () {
  'use strict';

  const ROTATION_DELAY = 24000;
  const MAX_HERO_RIPPLES = 3;
  const HERO_RIPPLE_REFRESH = 5600;

  function createState(reduced) {
    return {
      active: 0, step: 0, count: 4,
      userPaused: Boolean(reduced), reduced: Boolean(reduced),
      hovered: false, focused: false, visible: false, pageHidden: false
    };
  }

  function selectFacet(state, index, manual) {
    const next = ((index % state.count) + state.count) % state.count;
    let delta = (next - state.active + state.count) % state.count;
    if (delta > state.count / 2) delta -= state.count;
    state.step += delta;
    state.active = next;
    if (manual) state.userPaused = true;
    return state;
  }

  function canRotate(state) {
    return !state.userPaused && !state.reduced && !state.hovered &&
      !state.focused && state.visible && !state.pageHidden;
  }

  function createRipplePositions(random, count) {
    const generator = typeof random === 'function' ? random : Math.random;
    const target = Math.max(1, Math.min(MAX_HERO_RIPPLES, Number(count) || MAX_HERO_RIPPLES));
    const positions = [];
    for (let index = 0; index < target; index += 1) {
      let candidate = null;
      for (let attempt = 0; attempt < 14; attempt += 1) {
        candidate = {
          x: Math.round((12 + generator() * 72) * 10) / 10,
          y: Math.round((17 + generator() * 64) * 10) / 10
        };
        const apart = positions.every((point) => Math.hypot(point.x - candidate.x, point.y - candidate.y) > 19);
        if (apart || attempt === 13) break;
      }
      positions.push(candidate);
    }
    return positions;
  }

  function createSatelliteMotions(random, count) {
    const generator = typeof random === 'function' ? random : Math.random;
    const target = Math.max(0, Number(count) || 0);
    return Array.from({ length: target }, () => ({
      speed: Math.round((0.0024 + generator() * 0.0066) * 1000000) / 1000000,
      direction: generator() < 0.5 ? -1 : 1,
      phase: Math.round(generator() * 3600) / 10
    }));
  }

  function shouldAnimateAmbient(enabled, reduced, pageHidden) {
    return Boolean(enabled) && !Boolean(reduced) && !Boolean(pageHidden);
  }

  function setPanelInteractivity(panel, current, remembered) {
    panel.inert = !current;
    panel.querySelectorAll('a[href],button,input,select,textarea,[tabindex],[contenteditable]').forEach((node) => {
      if (!remembered.has(node)) remembered.set(node, node.getAttribute('tabindex'));
      if (!current) node.setAttribute('tabindex', '-1');
      else if (remembered.get(node) === null) node.removeAttribute('tabindex');
      else node.setAttribute('tabindex', remembered.get(node));
    });
  }

  function mountHeroRipples(doc, win, reduced) {
    const root = doc.querySelector('[data-hero-ripple]');
    if (!root) return;
    const points = Array.from(root.querySelectorAll('.hero-ripple-instance')).slice(0, MAX_HERO_RIPPLES);
    if (!points.length) return;

    function position(point, next) {
      point.style.setProperty('--ripple-x', `${next.x}%`);
      point.style.setProperty('--ripple-y', `${next.y}%`);
    }

    function seed() {
      createRipplePositions(Math.random, points.length).forEach((next, index) => position(points[index], next));
    }

    seed();
    if (reduced.matches) return;
    let cursor = 0;
    win.setInterval(() => {
      if (doc.hidden || reduced.matches) return;
      const next = createRipplePositions(Math.random, points.length)[cursor];
      position(points[cursor], next);
      cursor = (cursor + 1) % points.length;
    }, HERO_RIPPLE_REFRESH);
  }

  function createAmbientController(doc, win, reduced) {
    const background = doc.querySelector('.ambient-background');
    if (!background) return { setEnabled: () => {}, refresh: () => {} };
    const paths = new Map(Array.from(background.querySelectorAll('[data-orbit-path]')).map((path) => [path.dataset.orbitPath, path]));
    const orbiters = Array.from(background.querySelectorAll('[data-ambient-orbiter]')).map((orbiter) => ({
      node: orbiter,
      path: paths.get(orbiter.dataset.ambientOrbiter),
      duration: Number(orbiter.dataset.duration) || 50000,
      phase: Number(orbiter.dataset.phase) || 0
    })).filter((item) => item.path && typeof item.path.getTotalLength === 'function');
    const satellites = Array.from(background.querySelectorAll('[data-satellite-orbit]')).map((node, index) => ({
      node,
      ...createSatelliteMotions(Math.random, 1)[0],
      index
    }));
    let frame = null;

    function enabled() {
      return doc.documentElement.dataset.ambient !== 'off';
    }

    function draw(timestamp) {
      frame = null;
      if (!shouldAnimateAmbient(enabled(), reduced.matches, doc.hidden)) return;
      orbiters.forEach((item) => {
        const length = item.path.getTotalLength();
        const progress = ((timestamp / item.duration) + item.phase) % 1;
        const point = item.path.getPointAtLength(length * progress);
        item.node.setAttribute('transform', `translate(${point.x.toFixed(1)} ${point.y.toFixed(1)})`);
      });
      satellites.forEach((item) => {
        const angle = ((timestamp * item.speed * item.direction) + item.phase) % 360;
        item.node.setAttribute('transform', `rotate(${angle.toFixed(2)})`);
      });
      frame = win.requestAnimationFrame(draw);
    }

    function refresh() {
      if (frame !== null) win.cancelAnimationFrame(frame);
      frame = null;
      if (shouldAnimateAmbient(enabled(), reduced.matches, doc.hidden)) {
        frame = win.requestAnimationFrame(draw);
      }
    }

    function setEnabled(on) {
      doc.documentElement.dataset.ambient = on ? 'on' : 'off';
      refresh();
    }

    refresh();
    return { setEnabled, refresh };
  }

  function mount(doc, win) {
    const reduced = win.matchMedia('(prefers-reduced-motion: reduce)');
    mountHeroRipples(doc, win, reduced);
    const ambientController = createAmbientController(doc, win, reduced);
    const root = doc.querySelector('[data-facets]');
    if (!root) return;
    const panels = Array.from(root.querySelectorAll('[data-facet-panel]'));
    const buttons = Array.from(root.querySelectorAll('[data-facet-select]'));
    const cube = root.querySelector('.facet-cube');
    const nav = root.querySelector('.facets-nav');
    const toolbar = root.querySelector('.facets-toolbar');
    const playback = root.querySelector('[data-facet-playback]');
    const counter = root.querySelector('[data-facet-count]');
    const announce = root.querySelector('[data-facet-announcement]');
    const ambient = doc.querySelector('[data-ambient-toggle]');
    const proposal = doc.querySelector('.ambient-proposal');
    const note = root.querySelector('[data-facet-note]');
    if (panels.length !== 4 || buttons.length !== 4 || !cube || !nav || !toolbar) return;
    const state = createState(reduced.matches);
    state.pageHidden = Boolean(doc.hidden);
    let timer = null;
    let observer = null;
    const rememberedTabindex = new WeakMap();

    function measure() {
      root.style.setProperty('--facet-depth', `${cube.clientWidth / 2}px`);
    }

    function schedule() {
      if (timer !== null) win.clearTimeout(timer);
      timer = null;
      if (canRotate(state)) {
        timer = win.setTimeout(() => {
          selectFacet(state, state.active + 1, false);
          render(false);
        }, ROTATION_DELAY);
      }
    }

    function render(manual) {
      root.style.setProperty('--facet-rotation', `${-state.step * 90}deg`);
      panels.forEach((panel, index) => {
        const current = index === state.active;
        panel.classList.toggle('is-active', current);
        panel.setAttribute('aria-hidden', String(!current));
        setPanelInteractivity(panel, current, rememberedTabindex);
      });
      buttons.forEach((button, index) => {
        button.classList.toggle('is-active', index === state.active);
        button.setAttribute('aria-pressed', String(index === state.active));
      });
      if (counter) counter.textContent = `${String(state.active + 1).padStart(2, '0')} / 04`;
      if (playback) {
        playback.textContent = state.userPaused ? 'Reprendre la rotation' : 'Mettre en pause';
        playback.setAttribute('aria-pressed', String(state.userPaused));
        playback.hidden = state.reduced;
      }
      if (note) {
        const message = state.reduced ? 'Mouvements réduits respectés' : state.userPaused ? '' : 'Rotation lente · 24 secondes par facette';
        note.textContent = message;
        note.hidden = !message;
      }
      root.setAttribute('aria-roledescription', 'carrousel');
      if (manual && announce) {
        announce.textContent = `Facette ${state.active + 1} sur 4 : ${buttons[state.active].dataset.facetName}.`;
      }
      schedule();
    }

    function setAmbient(on) {
      ambientController.setEnabled(on);
      if (!ambient) return;
      ambient.setAttribute('aria-pressed', String(on));
      ambient.textContent = on ? 'Désactiver le fond animé' : 'Activer le fond animé';
    }

    buttons.forEach((button, index) => {
      button.addEventListener('click', () => {
        selectFacet(state, index, true);
        render(true);
      });
      button.addEventListener('keydown', (event) => {
        let target;
        if (event.key === 'ArrowRight' || event.key === 'ArrowDown') target = (index + 1) % 4;
        else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') target = (index + 3) % 4;
        else if (event.key === 'Home') target = 0;
        else if (event.key === 'End') target = 3;
        else return;
        event.preventDefault();
        buttons[target].focus();
        selectFacet(state, target, true);
        render(true);
      });
    });

    if (playback) playback.addEventListener('click', () => {
      state.userPaused = !state.userPaused;
      render(false);
    });
    root.addEventListener('mouseenter', () => { state.hovered = true; schedule(); });
    root.addEventListener('mouseleave', () => { state.hovered = false; schedule(); });
    root.addEventListener('focusin', () => { state.focused = true; schedule(); });
    root.addEventListener('focusout', (event) => {
      state.focused = Boolean(event.relatedTarget && root.contains(event.relatedTarget));
      schedule();
    });
    doc.addEventListener('visibilitychange', () => {
      state.pageHidden = Boolean(doc.hidden);
      doc.documentElement.dataset.pageHidden = String(state.pageHidden);
      ambientController.refresh();
      schedule();
    });
    reduced.addEventListener('change', (event) => {
      state.reduced = event.matches;
      if (state.reduced) state.userPaused = true;
      ambientController.refresh();
      render(false);
    });
    if (ambient) {
      setAmbient(doc.documentElement.dataset.ambient !== 'off');
      ambient.addEventListener('click', () => setAmbient(doc.documentElement.dataset.ambient !== 'on'));
    }

    root.classList.add('is-enhanced');
    nav.hidden = false;
    toolbar.hidden = false;
    if (proposal) proposal.hidden = false;
    measure();
    render(false);
    if (win.ResizeObserver) {
      observer = new win.ResizeObserver(measure);
      observer.observe(cube);
    } else win.addEventListener('resize', measure);
    if (win.IntersectionObserver) {
      const intersection = new win.IntersectionObserver((entries) => {
        state.visible = entries.some((entry) => entry.isIntersecting);
        schedule();
      }, { threshold: 0.2 });
      intersection.observe(root);
    } else {
      state.visible = true;
      schedule();
    }
    win.requestAnimationFrame(() => root.classList.add('is-ready'));
  }

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
      createState, selectFacet, canRotate, setPanelInteractivity, createRipplePositions,
      shouldAnimateAmbient, createSatelliteMotions, ROTATION_DELAY, MAX_HERO_RIPPLES, HERO_RIPPLE_REFRESH
    };
  } else mount(document, window);
})();
