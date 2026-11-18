"""Start Interview Prepper: serve the app on this computer and open it in your browser.

Usage (from the repository root, any Python 3.8+, no packages needed):
    python run.py                  # opens http://127.0.0.1:8765
    python run.py --port 9000      # another port
    python run.py --no-browser     # don't open a browser tab
    python run.py --host 0.0.0.0   # also reachable from your phone on the same Wi-Fi (no password: home networks only)

Your Got it / Struggling marks are saved to progress.json next to this file. Stop with Ctrl+C.
"""
import argparse
import json
import os
import socket
import sys
import tempfile
import threading
import webbrowser
from functools import partial
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WEB_DIR = ROOT / "web"
DEFAULT_PROGRESS = ROOT / "progress.json"
MAX_BODY = 1_000_000  # bytes; the marks file is a few KB

_lock = threading.Lock()


def read_progress(path):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def write_progress(path, data):
    """Write atomically, so a crash mid-write never leaves a broken file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".progress-", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=1, sort_keys=True)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


class Handler(SimpleHTTPRequestHandler):
    """Static files from web/, plus GET/PUT /api/progress."""

    # Windows can map .js to text/plain through the registry; pin the types the app needs.
    extensions_map = {
        **SimpleHTTPRequestHandler.extensions_map,
        ".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8",
        ".css": "text/css; charset=utf-8", ".json": "application/json", ".png": "image/png",
        ".jpg": "image/jpeg", ".svg": "image/svg+xml",
    }

    def __init__(self, *args, progress_path=DEFAULT_PROGRESS, **kwargs):
        self.progress_path = progress_path
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

    def _is_api(self):
        return self.path.split("?", 1)[0].rstrip("/") == "/api/progress"

    def do_GET(self):
        if self._is_api():
            with _lock:
                return self._json(HTTPStatus.OK, read_progress(self.progress_path))
        return super().do_GET()

    def do_PUT(self):
        if not self._is_api():
            return self._json(HTTPStatus.NOT_FOUND, {"error": "not found"})
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0 or length > MAX_BODY:
            return self._json(HTTPStatus.BAD_REQUEST, {"error": "empty or too large"})
        try:
            data = json.loads(self.rfile.read(length).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return self._json(HTTPStatus.BAD_REQUEST, {"error": "not JSON"})
        if not isinstance(data, dict):
            return self._json(HTTPStatus.BAD_REQUEST, {"error": "expected a JSON object"})
        with _lock:
            write_progress(self.progress_path, data)
        return self._json(HTTPStatus.OK, {"ok": True})

    do_POST = do_PUT

    def log_request(self, code="-", size="-"):  # keep the terminal quiet apart from errors
        if str(getattr(code, "value", code)).startswith(("4", "5")):
            super().log_request(code, size)


def make_server(host, port, progress_path=DEFAULT_PROGRESS, web_dir=WEB_DIR, tries=20):
    """Bind to the first free port from `port` upward (port 0 picks any free port)."""
    handler = partial(Handler, directory=str(web_dir), progress_path=Path(progress_path))
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
            print(f"On your phone (same Wi-Fi): http://{ip}:{port}/")
    print(f"Marks are saved to {args.progress}")
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
