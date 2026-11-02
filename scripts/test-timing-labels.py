#!/usr/bin/env python3
"""Checks that temporal qualification remains visible only when it adds a reservation."""
import json
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "content" / "editions.json").read_text(encoding="utf-8"))
DIST = ROOT / "dist"

for edition in DATA["editions"]:
    page = DIST / "editions" / edition["id"] / "index.html"
    soup = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
    for signal in edition["signals"]:
        card = soup.select_one(f'#signal-{signal["id"]}')
        assert card is not None, signal["id"]
        badge = card.select_one(".timing-badge")
        assert signal["dateLabel"] in card.get_text(" ", strip=True)
        if signal["timing"] == "week":
            assert badge is None, f'{signal["id"]} must not display a week-status badge'
        elif signal["timing"] == "context":
            assert badge is not None and badge.get_text(" ", strip=True) == "Actu hors période"
        else:
            assert badge is not None and badge.get_text(" ", strip=True) == "Dispositif observé"

home = (DIST / "index.html").read_text(encoding="utf-8")
assert "Actualité de la fenêtre" not in home
assert "LE SIGNAL À RETENIR ·" not in home
assert "Actu hors période" in home
print("PASS: dates preserved, week badges hidden and out-of-period signals clearly qualified.")
