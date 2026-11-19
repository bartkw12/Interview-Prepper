"""Read and rewrite cards in content/cue_cards.md as plain text.

No markdown library is needed here, so run.py can load this module even when markdown-it-py is missing.
scripts/build_data.py uses the parsing half; run.py uses the editing half to save changes made in the app.
"""
import re

CARD_HEAD = re.compile(r"^### ([A-Z]\d\d) · (.*?) \*\*\((\d+)\)\*\*\s*(★?)\s*$", re.M)
SHEET_HEAD = re.compile(r"^# Sheet \d+ ·", re.M)
POINT = re.compile(r"^(- |\d+\. )")
TAG = re.compile(r"`\[(.*?)\]`")
# Optional answer time on the tag line:  ⏱ 90s (75–120s)   or just   ⏱ 90s
TIME = re.compile(r"⏱\s*(\d+)\s*s(?:\s*\(\s*(\d+)\s*s?\s*[–-]\s*(\d+)\s*s?\s*\))?")
BLOCK_END = re.compile(r"^---\s*$|^# ", re.M)


def split_cards_and_sheets(text):
    m = SHEET_HEAD.search(text)
    return (text[: m.start()], text[m.start():]) if m else (text, "")


def parse_time(s):
    m = TIME.search(s)
    if not m:
        return None, s.strip()
    t = {"target": int(m.group(1)), "min": None, "max": None}
    if m.group(2):
        t["min"], t["max"] = int(m.group(2)), int(m.group(3))
    return t, (s[: m.start()] + s[m.end():]).strip()


def format_time(t):
    if not t:
        return ""
    out = f"⏱ {int(t['target'])}s"
    if t.get("min") is not None and t.get("max") is not None:
        out += f" ({int(t['min'])}–{int(t['max'])}s)"
    return out


def parse_cards(text):
    """Return a list of dicts: id, prompt, n, star, tag, extra, time, back (markdown), start, end.

    start/end are offsets of the card's block (heading up to the next '---' or '# ' line) in `text`.
    """
    cards_text, _ = split_cards_and_sheets(text)
    heads = list(CARD_HEAD.finditer(cards_text))
    cards = []
    for i, m in enumerate(heads):
        nxt = heads[i + 1].start() if i + 1 < len(heads) else len(cards_text)
        sep = BLOCK_END.search(cards_text, m.end(), nxt)
        end = sep.start() if sep else nxt
        lines = cards_text[m.end(): end].strip("\n").splitlines()
        first = lines[0].strip() if lines else ""
        tag = TAG.match(first)
        if not tag:
            raise ValueError(f"{m.group(1)}: the line after the heading must be the tag, like `[CV fundamentals]`")
        time, extra = parse_time(first[tag.end():])
        cards.append(dict(id=m.group(1), prompt=m.group(2).strip(), n=int(m.group(3)), star=bool(m.group(4)),
                          tag=tag.group(1), extra=extra, time=time, back="\n".join(lines[1:]).strip(),
                          start=m.start(), end=end))
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


# ---------- editing ----------

def split_back(back):
    """Split a card back into (before, points, after, ordered, structured).

    `structured` is False when notes sit between points; the app then edits the back as one markdown box.
    """
    lines = back.splitlines()
    idx = [i for i, ln in enumerate(lines) if POINT.match(ln)]
    if not idx:
        return back.strip(), [], "", False, True
    first = idx[0]
    pts, cur, last = [], None, first
    for i in range(first, len(lines)):
        ln = lines[i]
        if POINT.match(ln):
            if cur is not None:
                pts.append(cur)
            cur, last = POINT.sub("", ln), i
        elif cur is not None and ln.startswith("  ") and ln.strip():
            cur, last = cur + "\n" + ln.strip(), i
        elif cur is not None and not ln.strip():
            pts.append(cur)
            cur = None
        elif ln.strip():
            if any(j > i for j in idx):
                return back.strip(), [], "", False, False
            break
    if cur is not None:
        pts.append(cur)
    ordered = bool(re.match(r"\d", lines[first]))
    before = "\n".join(lines[:first]).strip()
    after = "\n".join(lines[last + 1:]).strip()
    return before, pts, after, ordered, True


def join_back(before, pts, after, ordered=False):
    parts = []
    if before and before.strip():
        parts.append(before.strip())
    out = []
    for i, p in enumerate(pts):
        lines = [ln.strip() for ln in str(p).splitlines() if ln.strip()]
        if not lines:
            continue
        out.append((f"{i + 1}. " if ordered else "- ") + "\n  ".join(lines))
    if out:
        parts.append("\n".join(out))
    if after and after.strip():
        parts.append(after.strip())
    return "\n\n".join(parts)


def find_card(text, card_id):
    for c in parse_cards(text):
        if c["id"] == card_id:
            return c
    raise KeyError(card_id)


def card_fields(text, card_id):
    """The editable fields of one card, for the app's editor."""
    c = find_card(text, card_id)
    before, pts, after, ordered, structured = split_back(c["back"])
    return {"id": c["id"], "prompt": c["prompt"], "star": c["star"], "tag": c["tag"], "extra": c["extra"],
            "time": c["time"], "back": c["back"], "before": before, "points": pts, "after": after,
            "ordered": ordered, "structured": structured}


def format_card(card_id, prompt, star, tag, back, extra="", time=None):
    """One card as markdown. The heading's point count is taken from the back, so it is always right."""
    n = len(points(back))
    head = f"### {card_id} · {prompt} **({n})**" + (" ★" if star else "")
    tagline = " ".join(x for x in (f"`[{tag}]`", format_time(time), extra) if x)
    return f"{head}\n{tagline}\n\n{back.strip()}\n"


def _clean_time(t):
    if t in (None, "", {}):
        return None
    if not isinstance(t, dict):
        raise ValueError("time must be an object with target, min and max seconds")
    try:
        target = int(t.get("target"))
        lo = None if t.get("min") in (None, "") else int(t["min"])
        hi = None if t.get("max") in (None, "") else int(t["max"])
    except (TypeError, ValueError):
        raise ValueError("Answer times must be whole seconds")
    if target <= 0:
        raise ValueError("The target time must be more than 0 seconds")
    if (lo is None) != (hi is None):
        raise ValueError("Give both a minimum and a maximum time, or neither")
    if lo is not None and not (0 < lo <= target <= hi):
        raise ValueError("Times must be minimum ≤ target ≤ maximum")
    return {"target": target, "min": lo, "max": hi}


def update_card(text, card_id, data):
    """Return `text` with one card rewritten from the editor's fields.

    `data` has prompt, star, time and either `back` (raw markdown) or before / points / after / ordered.
    Raises KeyError for an unknown card and ValueError for bad input. Everything outside the card is unchanged.
    """
    c = find_card(text, card_id)
    if not isinstance(data, dict):
        raise ValueError("expected a JSON object")
    prompt = " ".join(str(data.get("prompt", c["prompt"])).split())
    if not prompt:
        raise ValueError("The question can't be empty")
    if "back" in data:
        back = str(data["back"]).replace("\r\n", "\n").strip()
    else:
        pts = data.get("points")
        if not isinstance(pts, list):
            raise ValueError("points must be a list")
        back = join_back(str(data.get("before") or ""), [str(p) for p in pts], str(data.get("after") or ""),
                         bool(data.get("ordered")))
    if not points(back):
        raise ValueError("A card needs at least one point")
    time = _clean_time(data["time"]) if "time" in data else c["time"]
    block = format_card(card_id, prompt, bool(data.get("star", c["star"])), c["tag"], back, c["extra"], time)
    new_text = text[: c["start"]] + block + "\n" + text[c["end"]:]
    check = find_card(new_text, card_id)
    if check["prompt"] != prompt or check["back"] != back:
        raise ValueError("That question text breaks the card heading; avoid '**(' in it")
    return new_text
