#!/usr/bin/env python3
"""Checks that temporal qualification remains visible only when it adds a reservation."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "content" / "editions.json").read_text(encoding="utf-8"))
DIST = ROOT / "dist"


def card_html(html, signal_id):
    pattern = rf'<article class="signal-card[^>]* id="signal-{re.escape(signal_id)}">(.*?)</article>'
    match = re.search(pattern, html, flags=re.DOTALL)
    assert match is not None, signal_id
    return match.group(1)


for edition in DATA["editions"]:
    page = DIST / "editions" / edition["id"] / "index.html"
    html = page.read_text(encoding="utf-8")
    for signal in edition["signals"]:
        card = card_html(html, signal["id"])
        assert signal["dateLabel"] in card
        badge = re.search(r'<span class="timing-badge [^"]+">(.*?)</span>', card)
        if signal["timing"] == "week":
            assert badge is None, f'{signal["id"]} must not display a week-status badge'
        elif signal["timing"] == "context":
            assert badge is not None and badge.group(1) == "Actu hors période"
        else:
            assert badge is not None and badge.group(1) == "Dispositif observé"

home = (DIST / "index.html").read_text(encoding="utf-8")
assert "Actualité de la fenêtre" not in home
assert "LE SIGNAL À RETENIR ·" not in home
assert "Actu hors période" in home
print("PASS: dates preserved, week badges hidden and out-of-period signals clearly qualified.")
