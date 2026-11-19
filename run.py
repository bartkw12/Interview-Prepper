"""Start Interview Prepper: serve the app on this computer and open it in your browser.

Usage (from the repository root, any Python 3.8+, no packages needed to study):
    python run.py                  # opens http://127.0.0.1:8765
    python run.py --port 9000      # another port
    python run.py --no-browser     # don't open a browser tab
    python run.py --host 0.0.0.0   # also reachable from your phone on the same Wi-Fi (no password: home networks only)

Your Got it / Struggling / Memorized marks are saved to progress.json next to this file.
Editing cards in the app saves to content/cue_cards.md and rebuilds web/data/cards.js; that needs
markdown-it-py (pip install -r requirements.txt). Stop with Ctrl+C.
"""
import argparse
import json
import os
import re
import socket
import sys
import tempfile
import threading
import webbrowser
from functools import partial
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parent
WEB_DIR = ROOT / "web"
sys.path.insert(0, str(ROOT / "scripts"))
import cardfile  # noqa: E402

DEFAULT_PROGRESS = ROOT / "progress.json"
DEFAULT_CARDS = ROOT / "content" / "cue_cards.md"
DEFAULT_CONFIG = ROOT / "content" / "config.json"
MAX_BODY = 1_000_000  # bytes; the marks file and a card edit are a few KB
MAX_IMAGE = 10_000_000
NEED_BUILDER = "Editing needs markdown-it-py. Stop the app, run: pip install -r requirements.txt, then start it again."

_lock = threading.Lock()
_builder = []  # the build_data module, or None when markdown-it-py is missing; loaded on first use


def builder():
    if not _builder:
        try:
            import build_data
            _builder.append(build_data)
        except SystemExit:  # build_data exits when markdown-it-py is missing
            _builder.append(None)
    return _builder[0]


def read_progress(path):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def atomic_write(path, data):
    """Write text (as UTF-8 with LF endings) or bytes atomically, so a crash mid-write never leaves a broken file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(data, str):
        data = data.encode("utf-8")
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix="." + path.stem + "-", suffix=path.suffix)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


def write_progress(path, data):
    atomic_write(path, json.dumps(data, indent=1, sort_keys=True))


IMAGE_TYPES = ((b"\x89PNG\r\n\x1a\n", ".png"), (b"\xff\xd8\xff", ".jpg"), (b"GIF87a", ".gif"), (b"GIF89a", ".gif"))


def image_ext(data):
    """The file extension for PNG, JPEG, GIF or WebP bytes, or None for anything else."""
    for sig, ext in IMAGE_TYPES:
        if data.startswith(sig):
            return ext
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return ".webp"
    return None


def safe_stem(name):
    """A plain file name from whatever the browser sent: no folders, lowercase letters, digits, - and _."""
    base = re.split(r"[\\/]", name or "")[-1]
    base = base.rsplit(".", 1)[0] if "." in base else base
    stem = re.sub(r"[^a-z0-9_-]+", "-", base.lower()).strip("-_")[:60]
    return stem or "figure"


def save_figure(figs_dir, name, data):
    """Save image bytes into figs_dir under a new name (never overwrites). Returns the file name."""
    ext = image_ext(data)
    if not ext:
        raise ValueError("That file is not a PNG, JPEG, GIF or WebP image")
    figs_dir = Path(figs_dir)
    figs_dir.mkdir(parents=True, exist_ok=True)
    stem = safe_stem(name)
    for i in range(1, 1000):
        fname = stem + ("" if i == 1 else f"-{i}") + ext
        try:
            with open(figs_dir / fname, "xb") as f:
                f.write(data)
            return fname
        except FileExistsError:
            continue
    raise ValueError("Too many figures with that name")


class Handler(SimpleHTTPRequestHandler):
    """Static files from web/, plus the app's API:

    GET/PUT /api/progress     your marks
    GET/PUT /api/card/<ID>    one card's editable fields; PUT saves to cue_cards.md and rebuilds cards.js
    POST    /api/figure       upload an image into web/figs/
    """

    # Windows can map .js to text/plain through the registry; pin the types the app needs.
    extensions_map = {
        **SimpleHTTPRequestHandler.extensions_map,
        ".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8",
        ".css": "text/css; charset=utf-8", ".json": "application/json", ".png": "image/png",
        ".jpg": "image/jpeg", ".gif": "image/gif", ".webp": "image/webp", ".svg": "image/svg+xml",
    }

    def __init__(self, *args, progress_path=DEFAULT_PROGRESS, cards_path=DEFAULT_CARDS, config_path=DEFAULT_CONFIG,
                 out_path=WEB_DIR / "data" / "cards.js", figs_dir=WEB_DIR / "figs", **kwargs):
        self.progress_path = progress_path
        self.cards_path, self.config_path, self.out_path, self.figs_dir = cards_path, config_path, out_path, figs_dir
        super().__init__(*args, **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")  # always show the latest rebuilt cards
        super().end_headers()

    def _json(self, status, obj):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _route(self):
        """('progress', None), ('card', 'H05'), ('figure', None) or (None, None)."""
        path = urlsplit(self.path).path.rstrip("/")
        if path == "/api/progress":
            return "progress", None
        if path == "/api/figure":
            return "figure", None
        m = re.fullmatch(r"/api/card/([A-Z]\d\d)", path)
        return ("card", m.group(1)) if m else (None, None)

    def _body(self, limit):
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0 or length > limit:
            self._json(HTTPStatus.BAD_REQUEST, {"error": "empty or too large"})
            return None
        return self.rfile.read(length)

    def _json_body(self):
        raw = self._body(MAX_BODY)
        if raw is None:
            return None
        try:
            data = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            data = None
        if not isinstance(data, dict):
            self._json(HTTPStatus.BAD_REQUEST, {"error": "expected a JSON object"})
            return None
        return data

    def do_GET(self):
        route, card_id = self._route()
        if route == "progress":
            with _lock:
                return self._json(HTTPStatus.OK, read_progress(self.progress_path))
        if route == "card":
            with _lock:
                text = Path(self.cards_path).read_text(encoding="utf-8")
            try:
                fields = cardfile.card_fields(text, card_id)
            except KeyError:
                return self._json(HTTPStatus.NOT_FOUND, {"error": f"No card {card_id} in {Path(self.cards_path).name}"})
            except ValueError as e:
                return self._json(HTTPStatus.BAD_REQUEST, {"error": str(e)})
            ok = builder() is not None
            return self._json(HTTPStatus.OK, {"fields": fields, "editable": ok, "reason": "" if ok else NEED_BUILDER})
        if route == "figure":
            return self._json(HTTPStatus.METHOD_NOT_ALLOWED, {"error": "POST an image here"})
        return super().do_GET()

    def do_PUT(self):
        route, card_id = self._route()
        if route == "progress":
            data = self._json_body()
            if data is None:
                return
            with _lock:
                write_progress(self.progress_path, data)
            return self._json(HTTPStatus.OK, {"ok": True})
        if route == "card":
            return self._save_card(card_id)
        if route == "figure":
            return self._save_figure()
        return self._json(HTTPStatus.NOT_FOUND, {"error": "not found"})

    do_POST = do_PUT

    def _save_card(self, card_id):
        build = builder()
        if build is None:
            return self._json(HTTPStatus.SERVICE_UNAVAILABLE, {"error": NEED_BUILDER})
        data = self._json_body()
        if data is None:
            return
        with _lock:
            text = Path(self.cards_path).read_text(encoding="utf-8")
            try:
                new_text = cardfile.update_card(text, card_id, data)
                config_path = Path(self.config_path)
                config = json.loads(config_path.read_text(encoding="utf-8")) if config_path.exists() else {}
                built = build.build(new_text, config)
            except KeyError:
                return self._json(HTTPStatus.NOT_FOUND, {"error": f"No card {card_id}"})
            except ValueError as e:
                return self._json(HTTPStatus.BAD_REQUEST, {"error": f"Not saved. {e}"})
            atomic_write(self.cards_path, new_text)
            atomic_write(self.out_path, build.to_js(built))
        card = next(c for c in built["cards"] if c["id"] == card_id)
        return self._json(HTTPStatus.OK, {"card": card, "fields": cardfile.card_fields(new_text, card_id)})

    def _save_figure(self):
        raw = self._body(MAX_IMAGE)
        if raw is None:
            return
        name = (parse_qs(urlsplit(self.path).query).get("name") or ["figure"])[0]
        try:
            with _lock:
                fname = save_figure(self.figs_dir, name, raw)
        except ValueError as e:
            return self._json(HTTPStatus.BAD_REQUEST, {"error": str(e)})
        return self._json(HTTPStatus.OK, {"src": "figs/" + fname})

    def log_request(self, code="-", size="-"):  # keep the terminal quiet apart from errors
        if str(getattr(code, "value", code)).startswith(("4", "5")):
            super().log_request(code, size)


def make_server(host, port, progress_path=DEFAULT_PROGRESS, web_dir=WEB_DIR, tries=20, cards_path=DEFAULT_CARDS,
                config_path=DEFAULT_CONFIG, out_path=None, figs_dir=None):
    """Bind to the first free port from `port` upward (port 0 picks any free port)."""
    web_dir = Path(web_dir)
    handler = partial(Handler, directory=str(web_dir), progress_path=Path(progress_path), cards_path=Path(cards_path),
                      config_path=Path(config_path), out_path=Path(out_path or web_dir / "data" / "cards.js"),
                      figs_dir=Path(figs_dir or web_dir / "figs"))
    last_err = None
    for p in ([0] if port == 0 else range(port, port + tries)):
        try:
            return ThreadingHTTPServer((host, p), handler)
        except OSError as e:
            last_err = e
    raise SystemExit(f"No free port from {port} to {port + tries - 1}: {last_err}")


def lan_address():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("10.255.255.255", 1))
            return s.getsockname()[0]
    except OSError:
        return None


def main(argv=None):
    ap = argparse.ArgumentParser(description="Serve Interview Prepper and open it in your browser.")
    ap.add_argument("--host", default="127.0.0.1", help="127.0.0.1 (this computer only, default) or 0.0.0.0 (your network)")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--no-browser", action="store_true", help="don't open a browser tab")
    ap.add_argument("--progress", type=Path, default=DEFAULT_PROGRESS, help="where to save your marks")
    args = ap.parse_args(argv)

    if not (WEB_DIR / "data" / "cards.js").exists():
        sys.exit("web/data/cards.js is missing. Build it first: python scripts/build_data.py")

    server = make_server(args.host, args.port, args.progress)
    port = server.server_address[1]
    url = f"http://127.0.0.1:{port}/"
    print(f"Interview Prepper is running at {url}")
    if args.host == "0.0.0.0":
        ip = lan_address()
        if ip:
            print(f"On your phone (same Wi-Fi): http://{ip}:{port}/  (anyone on this network can also edit your cards)")
    print(f"Marks are saved to {args.progress}")
    if builder() is not None:
        print("Card edits are saved to content/cue_cards.md")
    else:
        print("Card editing is off: run  pip install -r requirements.txt  and restart to turn it on")
    print("Press Ctrl+C to stop.")
    if not args.no_browser:
        threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
