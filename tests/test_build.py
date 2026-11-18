"""Tests for scripts/build_data.py. Run all tests with: python -m unittest"""
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

try:
    import build_data
except SystemExit:  # markdown-it-py not installed
    build_data = None

SAMPLE = """# Deck

---

### A01 · What is a **pixel**? **(2)** ★
`[Basics]`
- **Smallest unit** of an image.
- Holds an **intensity** or **RGB** value.
  continues here.
*Simply: a dot.*

---

### A02 · Name one filter **(1)**
`[Basics]`
1. A **Gaussian blur**: ![blur](figs/blur.png)

---

### B01 · Plain point **(1)**
`[Other]`
- no bold words in this point

---

# Sheet 1 · Project: the summary

| a | b |
|---|---|
| 1 | 2 |

---

# Sheet 2 · Second

Text.
"""


@unittest.skipIf(build_data is None, "markdown-it-py is not installed (pip install -r requirements.txt)")
class BuildTests(unittest.TestCase):
    def setUp(self):
        self.data = build_data.build(SAMPLE, {"brand": "Test"})
        self.cards = {c["id"]: c for c in self.data["cards"]}

    def test_cards_and_sections(self):
        self.assertEqual(list(self.cards), ["A01", "A02", "B01"])
        self.assertEqual(self.data["sections"], {"A": "Basics", "B": "Other"})
        self.assertTrue(self.cards["A01"]["star"])
        self.assertFalse(self.cards["A02"]["star"])
        self.assertEqual(self.data["config"], {"brand": "Test"})

    def test_prompt_keeps_inline_markdown(self):
        self.assertEqual(self.cards["A01"]["prompt"], "What is a <strong>pixel</strong>?")

    def test_hints(self):
        a01 = self.cards["A01"]
        self.assertEqual(a01["hint1"], ["Smallest unit", "intensity"])
        self.assertEqual(a01["hint2"], [["Smallest unit"], ["intensity", "RGB"]])
        self.assertEqual(self.cards["B01"]["hint1"], ["no bold words …"])
        self.assertEqual(self.cards["B01"]["hint2"], [[]])

    def test_figures_get_fig_class(self):
        self.assertIn('<img class="fig" src="figs/blur.png" alt="blur" loading="lazy">', self.cards["A02"]["answer"])

    def test_sheets(self):
        self.assertEqual([s["title"] for s in self.data["sheets"]], ["Sheet 1 · Project: the summary", "Sheet 2 · Second"])
        self.assertIn("<table>", self.data["sheets"][0]["html"])

    def test_wrong_point_count_fails(self):
        bad = SAMPLE.replace("Name one filter **(1)**", "Name one filter **(3)**")
        with self.assertRaisesRegex(ValueError, r"A02: heading says \(3\) points but the back has 1"):
            build_data.build(bad, {})

    def test_duplicate_ids_fail(self):
        bad = SAMPLE.replace("### B01 ·", "### A01 ·")
        with self.assertRaisesRegex(ValueError, "Duplicate card IDs: A01"):
            build_data.build(bad, {})

    def test_missing_tag_fails(self):
        bad = SAMPLE.replace("`[Other]`\n", "")
        with self.assertRaisesRegex(ValueError, "B01"):
            build_data.build(bad, {})

    def test_main_writes_loadable_js(self):
        with tempfile.TemporaryDirectory() as d:
            cards, cfg, out = Path(d, "c.md"), Path(d, "c.json"), Path(d, "out", "cards.js")
            cards.write_text(SAMPLE.replace("Text.", "a </script> tag"), encoding="utf-8")
            cfg.write_text('{"title": "T"}', encoding="utf-8")
            build_data.main(["--cards", str(cards), "--config", str(cfg), "--out", str(out)])
            js = out.read_text(encoding="utf-8")
            self.assertNotIn("</script>", js)
            payload = js.split("window.PREP_DATA = ", 1)[1].rstrip().rstrip(";")
            self.assertEqual(len(json.loads(payload)["cards"]), 3)

    def test_real_deck_builds(self):
        text = (ROOT / "content" / "cue_cards.md").read_text(encoding="utf-8")
        data = build_data.build(text, {})
        self.assertGreater(len(data["cards"]), 0)
        for c in data["cards"]:
            self.assertEqual(len(c["hint1"]), c["n"], c["id"])
        for src in {s for c in data["cards"] for s in re.findall(r'src="(figs/[^"]+)"', c["answer"])}:
            self.assertTrue((ROOT / "web" / src).exists(), f"missing figure {src}")


if __name__ == "__main__":
    unittest.main()
