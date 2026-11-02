#!/usr/bin/env python3
"""Checks that the ambient-background control is explicitly placed in the site footer."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"

for path in DIST.rglob("*.html"):
    html = path.read_text(encoding="utf-8")
    is_error = path.name == "404.html" or "404" in path.parts
    if is_error:
        assert "data-ambient-toggle" not in html, path
        continue
    assert html.count('data-ambient-toggle') == 1, path
    assert "Fond animé de la veille" in html, path
    assert "Cartographie des signaux." not in html, path
    footer_at = html.index('<footer class="site-footer">')
    control_at = html.index('data-ambient-toggle')
    assert control_at > footer_at, path
    if 'class="facets-module container"' in html:
        assert control_at > html.index('class="facets-module container"'), path

print("PASS: the ambient-background setting is explicit, unique and placed in every site footer.")
