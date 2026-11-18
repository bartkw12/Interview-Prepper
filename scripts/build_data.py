"""Turn content/cue_cards.md into web/data/cards.js, the data file the app loads.

Usage (from the repository root):
    python scripts/build_data.py
    python scripts/build_data.py --cards content/cue_cards.md --config content/config.json --out web/data/cards.js

Needs markdown-it-py (pip install -r requirements.txt). Only needed when you edit the cards;
the app itself runs on the committed cards.js with plain Python.

The output is a small JavaScript file (window.PREP_DATA = {...}) rather than JSON, so the app also works
when index.html is opened straight from disk, where browsers block fetch().
"""
import argparse
import json
import re
import sys
from pathlib import Path

try:
    from markdown_it import MarkdownIt
except ImportError:  # pragma: no cover - message for a missing dependency
    sys.exit("markdown-it-py is missing. Install it with: pip install -r requirements.txt")

ROOT = Path(__file__).resolve().parent.parent

CARD_HEAD = re.compile(r"^### ([A-Z]\d\d) · (.*?) \*\*\((\d+)\)\*\*\s*(★?)\s*$", re.M)
SHEET_HEAD = re.compile(r"^# Sheet \d+ ·", re.M)
POINT = re.compile(r"^(- |\d+\. )")

_md = MarkdownIt("commonmark", {"typographer": True}).enable(["table", "replacements", "smartquotes"])


def render(md_text):
    """Markdown to HTML. Figures get the class the app uses for click-to-enlarge."""
    html = _md.render(md_text)

    def fig(m):
        attrs = m.group(1)
        src = re.search(r'src="([^"]*)"', attrs).group(1)
        alt = re.search(r'alt="([^"]*)"', attrs)
        alt = alt.group(1) if alt and alt.group(1) else "figure"
        return f'<img class="fig" src="{src}" alt="{alt}" loading="lazy">'

    return re.sub(r"<img([^>]*)>", fig, html)


def render_inline(md_text):
    return _md.renderInline(md_text.strip())


def split_cards_and_sheets(text):
    m = SHEET_HEAD.search(text)
    return (text[: m.start()], text[m.start():]) if m else (text, "")


def parse_cards(text):
    """Return a list of dicts: id, prompt, n, star, tag, back (markdown)."""
    cards_text, _ = split_cards_and_sheets(text)
    heads = list(CARD_HEAD.finditer(cards_text))
    cards = []
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(cards_text)
        block = cards_text[m.end(): end]
        block = re.split(r"^---\s*$|^# ", block, maxsplit=1, flags=re.M)[0]
        lines = block.strip("\n").splitlines()
        tag = re.match(r"`\[(.*?)\]`", lines[0].strip()) if lines else None
        if not tag:
            raise ValueError(f"{m.group(1)}: the line after the heading must be the tag, like `[CV fundamentals]`")
        cards.append(dict(id=m.group(1), prompt=m.group(2).strip(), n=int(m.group(3)), star=bool(m.group(4)),
                          tag=tag.group(1), back="\n".join(lines[1:]).strip()))
    return cards


def points(back):
    """Top-level points: '- ' or 'n. ' lines, with indented continuation lines joined on."""
    pts, cur = [], None
    for line in back.splitlines():
        if POINT.match(line):
            if cur is not None:
                pts.append(cur)
            cur = POINT.sub("", line)
        elif cur is not None and line.startswith("  ") and line.strip():
            cur += " " + line.strip()
        elif cur is not None:
            pts.append(cur)
            cur = None
    if cur is not None:
        pts.append(cur)
    return pts


def lead(point):
    """First hint: the point's first bold phrase, or its first three words."""
    bolds = re.findall(r"\*\*(.+?)\*\*", point)
    if bolds:
        return bolds[0].rstrip(":").strip()
    words = re.sub(r"[*`]", "", point).split()
    return " ".join(words[:3]) + " …"


def keywords(point):
    """Second hint: every bold phrase in the point."""
    return [re.sub(r"[*`]", "", b).rstrip(":").strip() for b in re.findall(r"\*\*(.+?)\*\*", point)]


def parse_sheets(text):
    _, sheets_text = split_cards_and_sheets(text)
    sheets = []
    for part in re.split(r"^(?=# )", sheets_text, flags=re.M):
        part = part.strip()
        if not SHEET_HEAD.match(part):
            continue
        title, _, body = part.partition("\n")
        body = re.sub(r"^---\s*$", "", body, flags=re.M)
        sheets.append({"title": title.lstrip("# ").strip(), "html": render(body)})
    return sheets


def build(text, config):
    cards, sections, problems = [], {}, []
    for c in parse_cards(text):
        pts = points(c["back"])
        if len(pts) != c["n"]:
            problems.append(f'{c["id"]}: heading says ({c["n"]}) points but the back has {len(pts)}')
        sec = c["id"][0]
        sections.setdefault(sec, c["tag"])
        cards.append({
            "id": c["id"], "sec": sec, "tag": c["tag"], "prompt": render_inline(c["prompt"]),
            "n": c["n"], "star": c["star"],
            "hint1": [render_inline(lead(p)) for p in pts],
            "hint2": [[render_inline(k) for k in keywords(p)] for p in pts],
            "answer": render(c["back"]),
        })
    if problems:
        raise ValueError("Point counts do not match:\n  " + "\n  ".join(problems))
    ids = [c["id"] for c in cards]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        raise ValueError("Duplicate card IDs: " + ", ".join(dupes))
    return {"config": config, "sections": sections, "cards": cards, "sheets": parse_sheets(text)}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--cards", type=Path, default=ROOT / "content" / "cue_cards.md")
    ap.add_argument("--config", type=Path, default=ROOT / "content" / "config.json")
    ap.add_argument("--out", type=Path, default=ROOT / "web" / "data" / "cards.js")
    args = ap.parse_args(argv)

    text = args.cards.read_text(encoding="utf-8")
    config = json.loads(args.config.read_text(encoding="utf-8")) if args.config.exists() else {}
    try:
        data = build(text, config)
    except ValueError as e:
        sys.exit(f"Build failed. {e}")

    payload = json.dumps(data, ensure_ascii=False, indent=None).replace("</", "<\\/")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("// Generated by scripts/build_data.py from content/cue_cards.md. Do not edit by hand.\n"
                        f"window.PREP_DATA = {payload};\n", encoding="utf-8")
    stars = sum(c["star"] for c in data["cards"])
    print(f'{len(data["cards"])} cards ({stars} starred), {len(data["sections"])} sections, '
          f'{len(data["sheets"])} sheets -> {args.out} ({args.out.stat().st_size // 1024} KB)')


if __name__ == "__main__":
    main()
