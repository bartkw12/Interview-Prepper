"""Tests for scripts/cardfile.py, the card reader/rewriter behind in-app editing. Run all tests with: python -m unittest"""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import cardfile  # noqa: E402

try:
    import build_data
except SystemExit:  # markdown-it-py not installed
    build_data = None

SAMPLE = """# Deck

---

### A01 · What is a **pixel**? **(2)** ★
`[Basics]` ⏱ 90s (75–120s)

*Mnemonic:* P for pixel.

- **Smallest unit** of an image.
- Holds an **intensity** or **RGB** value.
  continues here.

*Simply: a dot.*

---

### A02 · Name one filter **(1)**
`[Basics]` *(small font)* ⏱ 30s
1. A **Gaussian blur**

---

### B01 · Odd layout **(2)**
`[Other]`
- first
A note between points.
- second

---

# Sheet 1 · Project

Text.
"""


class ParseTests(unittest.TestCase):
    def test_time_and_extra_on_the_tag_line(self):
        cards = {c["id"]: c for c in cardfile.parse_cards(SAMPLE)}
        self.assertEqual(cards["A01"]["time"], {"target": 90, "min": 75, "max": 120})
        self.assertEqual(cards["A01"]["extra"], "")
        self.assertEqual(cards["A02"]["time"], {"target": 30, "min": None, "max": None})
        self.assertEqual(cards["A02"]["extra"], "*(small font)*")
        self.assertIsNone(cards["B01"]["time"])
        self.assertEqual(cards["A01"]["tag"], "Basics")

    def test_fields_split_the_back(self):
        f = cardfile.card_fields(SAMPLE, "A01")
        self.assertTrue(f["structured"])
        self.assertEqual(f["before"], "*Mnemonic:* P for pixel.")
        self.assertEqual(f["points"], ["**Smallest unit** of an image.", "Holds an **intensity** or **RGB** value.\ncontinues here."])
        self.assertEqual(f["after"], "*Simply: a dot.*")
        self.assertFalse(f["ordered"])
        self.assertTrue(cardfile.card_fields(SAMPLE, "A02")["ordered"])
        self.assertFalse(cardfile.card_fields(SAMPLE, "B01")["structured"])

    def test_unknown_card(self):
        with self.assertRaises(KeyError):
            cardfile.card_fields(SAMPLE, "Z99")


class UpdateTests(unittest.TestCase):
    def fields(self, cid):
        f = cardfile.card_fields(SAMPLE, cid)
        return {k: f[k] for k in ("prompt", "star", "time", "before", "points", "after", "ordered")}

    def test_add_a_point_updates_the_count_and_nothing_else(self):
        f = self.fields("A01")
        f["points"].append("A **third** point")
        new = cardfile.update_card(SAMPLE, "A01", f)
        self.assertIn("### A01 · What is a **pixel**? **(3)** ★\n`[Basics]` ⏱ 90s (75–120s)\n", new)
        self.assertIn("- A **third** point\n\n*Simply: a dot.*", new)
        start = new.index("### A02")
        self.assertEqual(new[start:], SAMPLE[SAMPLE.index("### A02"):])
        self.assertEqual(new[: new.index("### A01")], SAMPLE[: SAMPLE.index("### A01")])

    def test_remove_point_star_and_time(self):
        f = self.fields("A01")
        f.update(points=f["points"][:1], star=False, time=None)
        new = cardfile.update_card(SAMPLE, "A01", f)
        c = cardfile.find_card(new, "A01")
        self.assertEqual((c["n"], c["star"], c["time"]), (1, False, None))

    def test_ordered_points_keep_numbers_and_extra_text(self):
        f = self.fields("A02")
        f["points"].append("A **median** filter")
        new = cardfile.update_card(SAMPLE, "A02", f)
        self.assertIn("`[Basics]` ⏱ 30s *(small font)*\n\n1. A **Gaussian blur**\n2. A **median** filter\n", new)

    def test_raw_back_from_markdown_view(self):
        new = cardfile.update_card(SAMPLE, "B01", {"prompt": "Odd layout", "back": "- first\nA note.\n- second\n- third"})
        self.assertEqual(cardfile.find_card(new, "B01")["n"], 3)

    def test_bad_input(self):
        f = self.fields("A01")
        for bad in ({**f, "points": []}, {**f, "prompt": "  "}, {**f, "time": {"target": 90, "min": 100, "max": 120}},
                    {**f, "time": {"target": 90, "min": 60}}, {**f, "time": {"target": "abc"}}):
            with self.assertRaises(ValueError, msg=bad):
                cardfile.update_card(SAMPLE, "A01", bad)
        with self.assertRaises(KeyError):
            cardfile.update_card(SAMPLE, "Z99", f)

    @unittest.skipIf(build_data is None, "markdown-it-py is not installed (pip install -r requirements.txt)")
    def test_every_real_card_survives_an_unchanged_save(self):
        text = (ROOT / "content" / "cue_cards.md").read_text(encoding="utf-8")
        before = build_data.build(text, {})
        out = text
        for c in cardfile.parse_cards(text):
            f = cardfile.card_fields(out, c["id"])
            self.assertTrue(f["structured"], c["id"])
            out = cardfile.update_card(out, c["id"], {k: f[k] for k in ("prompt", "star", "time", "before", "points", "after", "ordered")})
        self.assertEqual(build_data.build(out, {}), before)


if __name__ == "__main__":
    unittest.main()
