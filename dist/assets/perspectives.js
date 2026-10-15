(function () {
  'use strict';

  const ROTATION_DELAY = 24000;

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

  function setPanelInteractivity(panel, current, remembered) {
    panel.inert = !current;
    panel.querySelectorAll('a[href],button,input,select,textarea,[tabindex],[contenteditable]').forEach((node) => {
      if (!remembered.has(node)) remembered.set(node, node.getAttribute('tabindex'));
      if (!current) node.setAttribute('tabindex', '-1');
      else if (remembered.get(node) === null) node.removeAttribute('tabindex');
      else node.setAttribute('tabindex', remembered.get(node));
    });
  }

  function mount(doc, win) {
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
    const ambient = root.querySelector('[data-ambient-toggle]');
    const proposal = root.querySelector('.ambient-proposal');
    const note = root.querySelector('[data-facet-note]');
    const reduced = win.matchMedia('(prefers-reduced-motion: reduce)');
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
      if (note) note.textContent = state.reduced ? 'Navigation manuelle · mouvements réduits respectés' : state.userPaused ? 'Navigation manuelle · rotation en pause' : 'Rotation lente · 24 secondes par facette';
      root.setAttribute('aria-roledescription', 'carrousel');
      if (manual && announce) {
        announce.textContent = `Facette ${state.active + 1} sur 4 : ${buttons[state.active].dataset.facetName}.`;
      }
      schedule();
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
      schedule();
    });
    reduced.addEventListener('change', (event) => {
      state.reduced = event.matches;
      if (state.reduced) state.userPaused = true;
      render(false);
    });
    if (ambient) ambient.addEventListener('click', () => {
      const on = doc.documentElement.dataset.ambient !== 'on';
      doc.documentElement.dataset.ambient = on ? 'on' : 'off';
      ambient.setAttribute('aria-pressed', String(on));
      ambient.textContent = on ? 'Désactiver le fond' : 'Essayer le fond animé';
    });

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
    module.exports = { createState, selectFacet, canRotate, setPanelInteractivity, ROTATION_DELAY };
  } else mount(document, window);
})();
