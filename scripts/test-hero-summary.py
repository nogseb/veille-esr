#!/usr/bin/env python3
"""Checks for the current edition hero and executive summary presentation."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "content" / "editions.json").read_text(encoding="utf-8"))
LATEST = max(DATA["editions"], key=lambda item: item["date"])
HTML = (ROOT / "dist" / "index.html").read_text(encoding="utf-8")
CSS = (ROOT / "dist" / "assets" / "styles.css").read_text(encoding="utf-8")

hero_meta = LATEST.get("heroMeta")
assert hero_meta, "Latest edition must provide a concise hero metadata line"
assert hero_meta in HTML, "Hero metadata is absent from the rendered home page"
assert "Brouillon consolidé" not in hero_meta and "non publié" not in hero_meta.lower()
assert "hero-ripple" in HTML and 'aria-hidden="true"' in HTML
assert "hero-ripple-expand" in CSS
assert "pointer-events:none" in CSS
assert "prefers-reduced-motion:reduce" in CSS
assert HTML.count('hero-ripple-instance') == 3
assert 'data-ambient="on"' in HTML
assert 'data-ambient-orbiter' in HTML
assert 'Désactiver la cartographie' in HTML

stake = LATEST.get("tbsStake")
if stake:
    assert "RÉSUMÉ DE LA SEMAINE" in HTML
    assert "ENJEUX POUR TBS EDUCATION" in HTML
    assert LATEST["intro"] in HTML
    assert stake in HTML
    assert "Cette consolidation retient" not in LATEST["intro"]

print("PASS: concise hero metadata, executive summary, three-point vector ripple and motion-safe orbital cartography.")
