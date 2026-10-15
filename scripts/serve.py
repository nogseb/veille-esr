#!/usr/bin/env python3
"""Preview the generated static site, including its production subdirectory."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

DIST = Path(__file__).resolve().parents[1] / "dist"


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIST), **kwargs)

    def do_GET(self):
        if self.path == "/veille-esr":
            self.send_response(301)
            self.send_header("Location", "/veille-esr/")
            self.end_headers()
            return
        if self.path.startswith("/veille-esr/"):
            self.path = self.path[len("/veille-esr"):]
        if Path(self.translate_path(urlsplit(self.path).path)).name.startswith("."):
            self.send_error(404)
            return
        super().do_GET()

    def send_error(self, code, message=None, explain=None):
        if code == 404 and (DIST / "404.html").is_file():
            body = (DIST / "404.html").read_bytes()
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(body)
            return
        super().send_error(code, message, explain)


if __name__ == "__main__":
    print("Aperçu statique prêt sur 0.0.0.0:3000", flush=True)
    ThreadingHTTPServer(("0.0.0.0", 3000), Handler).serve_forever()
