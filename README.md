# Interview Prepper

A flashcard app for interview prep that runs on your own computer. It reads the cue cards and project sheets
from one markdown file and shows them one card at a time, with hints, a full answer and large figures.
No printing, no account, and no internet needed once it is cloned.

## Run it

You need Python 3.8 or newer. Nothing else to install.

```bash
git clone https://github.com/bartkw12/Interview-Prepper.git
cd Interview-Prepper
python run.py        # on Linux or macOS: python3 run.py
```

Your browser opens at http://127.0.0.1:8765. Stop the app with Ctrl+C in the terminal.

**In VS Code:** open the folder, then press **F5** (or pick *Run Interview Prepper* in the Run and Debug panel).
The other entries there rebuild the card data, run the tests, or start the app for your phone.

**Without Python:** you can also double-click `web/index.html`. Everything works, but your marks are then
kept only in that browser instead of in `progress.json`.

**On your phone:** run `python run.py --host 0.0.0.0` and open the "On your phone" address it prints, on the
same Wi-Fi. There is no password, so only do this on a network you trust.

## How to study

| | |
|---|---|
| **Deck** | All cards, ★ Must-know, Struggling (cards you marked), or Not got yet |
| **Sections** | Pick one or more (for example CV fundamentals). None picked means all sections |
| **Shuffle** | Random order inside the current selection |
| **Hint** (`H`) | First press: the lead phrase of each point. Second press: all the key words |
| **Reveal answer** (`Space`) | The full answer with every point and figure |
| **Struggling** (`1`) / **Got it** (`2`) | Marks the card and moves on |
| `←` `→` | Previous and next card |
| Figures | Click to see full screen; `Esc` or a click closes it |

The **All cards** tab lists every card with its mark; click one to study it. The **Sheets** tab has the
project sheets. The header counts down to the interview date in `content/config.json`.

**Where marks are saved.** With `run.py`, in `progress.json` in the repo folder (and a copy in the browser).
`progress.json` is in `.gitignore`, so each computer keeps its own marks. To carry marks between your desktop
and laptop with git, delete the `progress.json` line from `.gitignore` and commit the file.

## Edit the cards

All content is in [`content/cue_cards.md`](content/cue_cards.md). The comment at the top of that file explains
the format. A card looks like this:

```markdown
### F03 · What does a convolution do? **(3)** ★
`[CV fundamentals]`
- **Slides a small kernel** over the image ...
- **Same weights everywhere**, so ...
- **Output = feature map** ...
```

- `F03` is the ID; the letter is the section, named after the card's tag.
- `**(3)**` is the number of points. Each top-level `- ` or `1. ` line is one point.
- `★` marks a must-know card.
- **Bold** words become the hints. Italic lines and plain paragraphs are extras and are not counted.
- Figures go in `web/figs/` and are used as `![](figs/name.png)`.

After editing, rebuild the data the app loads, then reload the page:

```bash
pip install -r requirements.txt     # once: installs markdown-it-py
python scripts/build_data.py        # writes web/data/cards.js
```

The build stops with a clear message if a card's point count doesn't match its heading, a tag line is missing,
or two cards share an ID. To change the title, the header name or the interview date, edit `content/config.json`
and rebuild.

## Tests

```bash
python -m unittest -v
```

The build tests are skipped if markdown-it-py is not installed; the server tests need nothing extra.

## Project layout

```
content/cue_cards.md     the cards and sheets (edit this)
content/config.json      title, header name, interview date
scripts/build_data.py    markdown -> web/data/cards.js
web/index.html           the app page
web/css/style.css        styles (light and dark)
web/js/app.js            study logic: decks, filters, hints, marks
web/data/cards.js        generated card data (committed, so the app runs without rebuilding)
web/figs/                figures
run.py                   local server: serves web/, saves marks to progress.json
tests/                   unit tests (python -m unittest)
.vscode/                 run configs (F5) and tasks
```

`web/data/cards.js` is a script (`window.PREP_DATA = ...`) rather than JSON so that the page also works when
opened straight from disk, where browsers block loading JSON files.
