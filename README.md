# reBottled landing page

A single-page website for reBottled, a social enterprise that replaces bottled water with a home reverse-osmosis system on subscription. It explains the mission, makes the case for switching and ends with an email sign-up for the regional pilot (first month and installation free).

Plain HTML, CSS and JavaScript. No build step and no dependencies.

## Files

- `index.html`: the English page (served at `/`)
- `es/`, `cy/`, `mt/`: Spanish (Canary Islands), Greek (Cyprus) and Maltese pages
- `styles.css`: all styles, including the tablet and phone layouts
- `main.js`: the bar animation and the sign-up forms
- `assets/`: logo, product image and icons
- `tools/build_locales.py`: generates the three local pages from the English one

## Run it locally

Open `index.html` in a browser, or serve the folder:

```sh
python3 -m http.server 8000
```

then visit http://localhost:8000.

## Sign-up form

There are two identical sign-up fields, one in the hero and one at the bottom of the page. Each takes an email address, validates it and then asks which island the person lives on, so we know where to tell them about the pilot.

It is front-end only for now. Nothing is sent or stored. To connect a backend, replace `submitSignup()` (receives `{ email, signedUpAt }`) and `saveRegion()` (receives `{ email, region }`) in `main.js` with real requests.

## Languages

| Path | Market | Language |
| --- | --- | --- |
| `/` | All | English |
| `/es/` | Canary Islands | Spanish |
| `/cy/` | Cyprus | Greek |
| `/mt/` | Malta | Maltese |

The local pages keep the same structure and share `styles.css`, `main.js` and `assets/`. Their copy is adapted per market: the visitor's own island is highlighted in the chart, the bottle count uses local figures (about 450 bottles a year per home in Malta, 390 in Cyprus, 240 in the Canary Islands), and in Cyprus and the Canaries the cost row is replaced with a storage row, because bottled water there costs less than the subscription.

Each page carries its interface text for the sign-up form in a `<script type="application/json" id="i18n">` block that `main.js` reads. The Greek page uses Literata and Noto Sans, because Newsreader and Libre Franklin have no Greek glyphs.

Don't edit the local pages by hand. Change the English page, update the strings in `tools/build_locales.py`, then run `python3 tools/build_locales.py`. The script stops if an English string it expects is missing.

## Deploying

Any static host works (GitHub Pages, Netlify, Cloudflare Pages). For GitHub Pages: Settings → Pages → deploy from the `main` branch, root folder.
