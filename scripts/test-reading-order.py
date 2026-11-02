#!/usr/bin/env python3
"""Checks that the four-perspectives module leads into the proposed actions."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "content" / "editions.json").read_text(encoding="utf-8"))
DIST = ROOT / "dist"

for edition in DATA["editions"]:
    route = DIST / "editions" / edition["id"] / "index.html"
    html = route.read_text(encoding="utf-8")
    assert html.count('class="facets-module container"') == 1, edition["id"]
    assert html.index('class="signals-section container"') < html.index('class="facets-module container"')
    assert html.index('class="facets-module container"') < html.index('class="actions-section container"')

home = (DIST / "index.html").read_text(encoding="utf-8")
assert home.count('class="facets-module container"') == 1
assert home.index('class="signals-section container"') < home.index('class="facets-module container"')
assert home.index('class="facets-module container"') < home.index('class="actions-section container"')
print("PASS: four perspectives follow the signals and precede the proposed actions.")
