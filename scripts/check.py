#!/usr/bin/env python3
"""Dependency-free structural checks for the generated watch website."""
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
DATA = json.loads((ROOT / "content/editions.json").read_text(encoding="utf-8"))


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = []
        self.h1s = 0
        self.canonical = None
        self.has_description = False
        self.noindex = False
        self.sources = 0
        self.signals = 0

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "h1":
            self.h1s += 1
        if "id" in values:
            self.ids.append(values["id"])
        if tag == "link" and values.get("rel") == "canonical":
            self.canonical = values.get("href")
        if tag == "meta":
            self.has_description |= values.get("name") == "description" and bool(values.get("content"))
            self.noindex |= values.get("name") == "robots" and "noindex" in (values.get("content") or "")
        for attribute in ("href", "src"):
            if values.get(attribute):
                self.links.append(values[attribute])
        classes = (values.get("class") or "").split()
        self.signals += "signal-card" in classes
        self.sources += "source-card" in classes


def resolve_file(page, raw):
    path = unquote(urlsplit(raw).path)
    if not path:
        return page
    if path.startswith("/veille-esr/"):
        candidate = DIST / path[len("/veille-esr/"):]
    elif path.startswith("/"):
        candidate = DIST / path.lstrip("/")
    else:
        candidate = page.parent / path
    candidate = candidate.resolve()
    if candidate.is_dir():
        candidate /= "index.html"
    return candidate


def main():
    axes = DATA["axes"]
    editions = DATA["editions"]
    assert len(axes) == 8
    assert len({axis["id"] for axis in axes}) == 8
    assert len({item["id"] for item in editions}) == len(editions)
    assert len({item["date"] for item in editions}) == len(editions)
    latest = max(editions, key=lambda item: item["date"])
    for edition in editions:
        assert 1 <= len(edition["signals"]) <= 5
        assert len(edition["actions"]) <= 3
        for signal in edition["signals"]:
            assert signal["axis"] in {axis["id"] for axis in axes}
            assert signal["sources"]
            assert all(source["url"].startswith("https://") for source in signal["sources"])
    errors = []
    pages = list(DIST.rglob("*.html"))
    for path in pages:
        page = Page()
        page.feed(path.read_text(encoding="utf-8"))
        relative = path.relative_to(DIST)
        if page.h1s != 1:
            errors.append(f"{relative}: expected one h1, found {page.h1s}")
        if len(page.ids) != len(set(page.ids)):
            errors.append(f"{relative}: duplicate element IDs")
        if not page.has_description:
            errors.append(f"{relative}: missing description")
        is_error = relative == Path("404.html") or relative.parts[0] == "404"
        if is_error and not page.noindex:
            errors.append(f"{relative}: error page is indexable")
        if not is_error and not str(page.canonical).startswith(DATA["site"]["url"]):
            errors.append(f"{relative}: invalid canonical URL")
        if path == DIST / "index.html" and page.signals != len(latest["signals"]):
            errors.append("Homepage signal count differs from the latest edition")
        for raw in page.links:
            parsed = urlsplit(raw)
            if parsed.scheme or parsed.netloc:
                continue
            target = resolve_file(path, raw)
            if not target.is_file():
                errors.append(f"{relative}: missing local file {raw}")
            elif parsed.fragment and target.suffix == ".html":
                other = Page()
                other.feed(target.read_text(encoding="utf-8"))
                if unquote(parsed.fragment) not in other.ids:
                    errors.append(f"{relative}: missing anchor {raw}")
    css = (DIST / "assets/styles.css").read_text(encoding="utf-8")
    for raw in re.findall(r"url\(['\"]?([^)'\"]+)", css):
        if not (DIST / "assets" / raw).resolve().is_file():
            errors.append(f"Missing CSS asset: {raw}")
    manifest = json.loads((DIST / "manus-routes.json").read_text())
    for route in manifest["routes"]:
        assert (DIST / route["path"].lstrip("/") / "index.html").is_file()
    assert (DIST / "assets/social.png").is_file()
    assert (DIST / "assets/manrope.woff2").read_bytes()[:4] == b"wOF2"
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"PASS: {len(pages)} HTML pages, {len(manifest['routes'])} public routes, eight axes, editorial caps, local links, metadata and assets.")


if __name__ == "__main__":
    main()
