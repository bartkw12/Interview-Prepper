"""Tests for run.py's server. Run all tests with: python -m unittest"""
import json
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import run  # noqa: E402


class ServerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.progress = Path(self.tmp.name, "progress.json")
        self.server = run.make_server("127.0.0.1", 0, self.progress)
        self.base = f"http://127.0.0.1:{self.server.server_address[1]}"
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.tmp.cleanup()

    def request(self, path, method="GET", body=None):
        req = urllib.request.Request(self.base + path, data=body, method=method,
                                     headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=5) as r:
                return r.status, r.headers, r.read()
        except urllib.error.HTTPError as e:
            return e.code, e.headers, e.read()

    def test_serves_the_app(self):
        status, headers, body = self.request("/")
        self.assertEqual(status, 200)
        self.assertIn(b'<script src="js/app.js">', body)
        status, headers, _ = self.request("/js/app.js")
        self.assertEqual(status, 200)
        self.assertTrue(headers["Content-Type"].startswith("text/javascript"))
        self.assertEqual(headers["Cache-Control"], "no-store")

    def test_progress_starts_empty_then_round_trips(self):
        self.assertEqual(json.loads(self.request("/api/progress")[2]), {})
        marks = {"marks": {"F01": "hard", "H01": "got"}, "deck": "hard"}
        status, _, _ = self.request("/api/progress", "PUT", json.dumps(marks).encode())
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(self.request("/api/progress")[2]), marks)
        self.assertEqual(json.loads(self.progress.read_text(encoding="utf-8")), marks)

    def test_rejects_bad_bodies(self):
        self.assertEqual(self.request("/api/progress", "PUT", b"not json")[0], 400)
        self.assertEqual(self.request("/api/progress", "PUT", b"[1, 2]")[0], 400)
        self.assertFalse(self.progress.exists())

    def test_broken_progress_file_reads_as_empty(self):
        self.progress.write_text("{oops", encoding="utf-8")
        self.assertEqual(json.loads(self.request("/api/progress")[2]), {})

    def test_unknown_put_path_is_404(self):
        self.assertEqual(self.request("/api/other", "PUT", b"{}")[0], 404)


if __name__ == "__main__":
    unittest.main()
