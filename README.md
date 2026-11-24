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
| **Deck** | All cards, ★ Must-know, Struggling (cards you marked), Not got yet, or Memorized (cards you retired) |
| **Sections** | Pick one or more (for example CV fundamentals). None picked means all sections |
| **Shuffle** | Random order inside the current selection |
| **Hint** (`H`) | First press: the lead phrase of each point. Second press: all the key words |
| **Reveal answer** (`Space`) | The full answer with every point and figure |
| **Struggling** (`1`) / **Got it** (`2`) | Marks the card and moves on |
| **Memorized** (`3`) | Retires a card you always get right: it leaves every deck and waits in the **Memorized** deck. A notice offers **Undo**; in the Memorized deck the button becomes **Bring back** |
| **Edit** (`E`) | Edit the card in place (see below) |
| `←` `→` | Previous and next card |
| Figures | Click to see full screen; `Esc` or a click closes it |

The **All cards** tab lists every card with its mark; click one to study it. The **Sheets** tab has the
project sheets. The header counts down to the interview date in `content/config.json`.

**Stopwatch.** Beside the card on a wide screen, or pinned to the bottom on a smaller one. `T` starts and pauses
it, `R` resets it. Cards with a recommended answer time (the Hatch interview cards) show it as `⏱ 1:30 (1:15–2:00)`.
The green band on the stopwatch is that range and the tick is the target. The time turns green inside the range
and red past it. Revealing the answer pauses the stopwatch, so you see how long you took. Under *Settings*:
reset on a new card, a chime past the maximum, and the target for cards without one (90 s).

**Where marks are saved.** With `run.py`, in `progress.json` in the repo folder (and a copy in the browser).
Memorized cards and stopwatch settings are saved there too. *Clear my marks* clears Got it and Struggling only.
`progress.json` is in `.gitignore`, so each computer keeps its own marks. To carry marks between your desktop
and laptop with git, delete the `progress.json` line from `.gitignore` and commit the file.

## Edit the cards

### In the app

With the app running from `python run.py`, press **Edit** (or `E`) on any card. You can:

- change the question, the ★ must-know flag and the answer time,
- edit, add (**+ Add point**), reorder (↑ ↓) or remove (✕) points,
- edit the notes before the points (a mnemonic, say) and after them (*Simply:* lines, backup stories),
- add an image with **Add image**, or **paste a screenshot** into any box. It is saved in `web/figs/` and goes
  in at the cursor,
- switch to **Markdown** to edit the back of the card as plain text.

**Save** (`Ctrl+S`) writes the card back into `content/cue_cards.md` and rebuilds `web/data/cards.js`. The point
count in the heading is updated for you. **Cancel** (`Esc`) leaves the card as it was. The edits are ordinary
changes to `cue_cards.md`, so `git diff` shows them and git can undo them.

Editing needs markdown-it-py (`pip install -r requirements.txt`). Without it, studying still works and run.py
says that editing is off. With `--host 0.0.0.0`, anyone on your Wi-Fi can edit your cards too.

### In the file

All content is in [`content/cue_cards.md`](content/cue_cards.md). The comment at the top of that file explains
the format. A card looks like this:

```markdown
### F03 · What does a convolution do? **(3)** ★
`[CV fundamentals]` ⏱ 60s (45–90s)
- **Slides a small kernel** over the image ...
- **Same weights everywhere**, so ...
- **Output = feature map** ...
```

- `F03` is the ID; the letter is the section, named after the card's tag.
- `**(3)**` is the number of points. Each top-level `- ` or `1. ` line is one point.
- `★` marks a must-know card.
- `⏱ 60s (45–90s)` after the tag is optional: the stopwatch target and the recommended range. `⏱ 60s` alone works too.
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
scripts/cardfile.py      reads and rewrites single cards (used by the build and by in-app editing)
web/index.html           the app page
web/css/style.css        styles (light and dark)
web/js/app.js            study logic: decks, filters, hints, marks, Memorized
web/js/editor.js         the in-app card editor
web/js/timer.js          the answer stopwatch
web/data/cards.js        generated card data (committed, so the app runs without rebuilding)
web/figs/                figures
run.py                   local server: serves web/, saves marks, saves card edits and uploaded images
tests/                   unit tests (python -m unittest)
.vscode/                 run configs (F5) and tasks
```

`web/data/cards.js` is a script (`window.PREP_DATA = ...`) rather than JSON so that the page also works when
opened straight from disk, where browsers block loading JSON files.


## To add

Will add compatibility with new interviews and projects, will have a default template any and all interviews can build into. No hard coded Hatch.
