"""Tests for run.py's server. Run all tests with: python -m unittest"""
import json
import shutil
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

PNG = b"\x89PNG\r\n\x1a\n" + b"\x00" * 32


class ServerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        d = Path(self.tmp.name)
        self.progress = d / "progress.json"
        # Edits go to copies, never to the real deck.
        self.cards, self.config = d / "cue_cards.md", d / "config.json"
        shutil.copy(ROOT / "content" / "cue_cards.md", self.cards)
        shutil.copy(ROOT / "content" / "config.json", self.config)
        self.out, self.figs = d / "cards.js", d / "figs"
        self.server = run.make_server("127.0.0.1", 0, self.progress, cards_path=self.cards, config_path=self.config,
                                      out_path=self.out, figs_dir=self.figs)
        self.base = f"http://127.0.0.1:{self.server.server_address[1]}"
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.tmp.cleanup()

    def request(self, path, method="GET", body=None, ctype="application/json"):
        req = urllib.request.Request(self.base + path, data=body, method=method, headers={"Content-Type": ctype})
        try:
            with urllib.request.urlopen(req, timeout=5) as r:
                return r.status, r.headers, r.read()
        except urllib.error.HTTPError as e:
            with e:
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

    # ---------- card editing ----------
    def card(self, cid):
        status, _, body = self.request("/api/card/" + cid)
        return status, json.loads(body)

    def test_get_card_fields(self):
        status, res = self.card("H05")
        self.assertEqual(status, 200)
        f = res["fields"]
        self.assertEqual(f["id"], "H05")
        self.assertEqual(len(f["points"]), 2)
        self.assertEqual(f["time"]["target"], 60)
        self.assertEqual(self.card("Z99")[0], 404)

    @unittest.skipIf(run.builder() is None, "markdown-it-py is not installed (pip install -r requirements.txt)")
    def test_save_card_rewrites_markdown_and_rebuilds(self):
        f = self.card("H05")[1]["fields"]
        body = {"prompt": f["prompt"], "star": True, "time": f["time"], "before": f["before"],
                "points": f["points"] + ["**New point:** added in the app"], "after": f["after"], "ordered": f["ordered"]}
        status, _, raw = self.request("/api/card/H05", "PUT", json.dumps(body).encode())
        self.assertEqual(status, 200, raw)
        card = json.loads(raw)["card"]
        self.assertEqual((card["n"], card["star"]), (3, True))
        self.assertIn("New point", card["hint1"][2])
        md = self.cards.read_text(encoding="utf-8")
        self.assertIn("### H05 · What is your greatest weakness? **(3)** ★", md)
        self.assertIn("- **New point:** added in the app", md)
        js = self.out.read_text(encoding="utf-8")
        self.assertIn("added in the app", js)
        self.assertNotIn("\r\n", js)

    @unittest.skipIf(run.builder() is None, "markdown-it-py is not installed (pip install -r requirements.txt)")
    def test_bad_save_changes_nothing(self):
        before = self.cards.read_text(encoding="utf-8")
        f = self.card("H05")[1]["fields"]
        status, _, raw = self.request("/api/card/H05", "PUT", json.dumps({"prompt": f["prompt"], "points": []}).encode())
        self.assertEqual(status, 400)
        self.assertIn("at least one point", json.loads(raw)["error"])
        self.assertEqual(self.request("/api/card/Z99", "PUT", b'{"points": ["x"]}')[0], 404)
        self.assertEqual(self.cards.read_text(encoding="utf-8"), before)
        self.assertFalse(self.out.exists())

    def test_figure_upload(self):
        status, _, raw = self.request("/api/figure?name=..%2F..%2FMy%20Shot.PNG", "POST", PNG, "image/png")
        self.assertEqual(status, 200, raw)
        self.assertEqual(json.loads(raw)["src"], "figs/my-shot.png")
        self.assertEqual((self.figs / "my-shot.png").read_bytes(), PNG)
        # Same name again: a new file, never an overwrite.
        status, _, raw = self.request("/api/figure?name=my-shot.png", "POST", PNG, "image/png")
        self.assertEqual(json.loads(raw)["src"], "figs/my-shot-2.png")
        # Not an image.
        status, _, _ = self.request("/api/figure?name=x.png", "POST", b"<script>alert(1)</script>", "image/png")
        self.assertEqual(status, 400)
        self.assertEqual(sorted(p.name for p in self.figs.iterdir()), ["my-shot-2.png", "my-shot.png"])


if __name__ == "__main__":
    unittest.main()
