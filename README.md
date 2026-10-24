# reBottled landing page

A single-page website for reBottled, a social enterprise that replaces bottled water with a home reverse-osmosis system on subscription. It explains the mission, makes the case for switching and ends with an email sign-up for the regional pilot (first month and installation free).

Plain HTML, CSS and JavaScript. No build step and no dependencies.

## Files

- `index.html`: the English page (served at `/`)
- `es/`, `cy/`, `mt/`: Spanish (Canary Islands), Greek (Cyprus) and Maltese pages
- `styles.css`: all styles, including the tablet and phone layouts
- `main.js`: the bar animation and the sign-up forms
- `config.js`: Supabase URL and publishable key
- `supabase/schema.sql`: the table and function for sign-ups
- `assets/`: logo, product image and icons
- `tools/build_locales.py`: generates the three local pages from the English one

## Run it locally

Open `index.html` in a browser, or serve the folder:

```sh
python3 -m http.server 8000
```

then visit http://localhost:8000.

## Sign-up form and Supabase

There are two identical sign-up fields, one in the hero and one at the bottom of the page. Each takes an email address, saves it, then asks which island the person lives on and saves that too.

Sign-ups go to a Supabase table called `signups` through the `upsert_signup()` database function. The browser only uses the publishable key. Row Level Security keeps the table closed to the public, so nobody can read the list from the website.

The live project is **Filtry** (`iswibgplfxicvrcxrhpk`, EU West). The schema in `supabase/schema.sql` is applied there and `config.js` points to it.

To set up a new project from scratch:

1. Create a project at [supabase.com](https://supabase.com). Pick an EU region, for example Frankfurt.
2. Open **SQL Editor**, paste the contents of `supabase/schema.sql` and run it.
3. In **Project Settings**, copy the Project URL and the **publishable key** (`sb_publishable_…`) into `config.js`. Never use the secret key here.
4. Commit and push. New sign-ups appear in **Table Editor → signups**, and you can export them as CSV.

While `config.js` is empty, the form still works for previews but saves nothing, and logs a warning in the browser console.

## Languages

| Path | Market | Language |
| --- | --- | --- |
| `/` | All | English |
| `/es/` | Canary Islands | Spanish |
| `/cy/` | Cyprus | Greek |
| `/mt/` | Malta | Maltese |

The local pages keep the same structure and share `styles.css`, `main.js` and `assets/`. Their copy is adapted per market: the visitor's own island is highlighted in the chart, every page uses the highest figure, about 450 bottles a year per home (Malta), worded as "up to" on the Cyprus and Canary pages, and in Cyprus and the Canaries the cost row is replaced with a storage row, because bottled water there costs less than the subscription.

Each page carries its interface text for the sign-up form in a `<script type="application/json" id="i18n">` block that `main.js` reads. The Greek page uses Literata and Noto Sans, because Newsreader and Libre Franklin have no Greek glyphs.

Don't edit the local pages by hand. Change the English page, update the strings in `tools/build_locales.py`, then run `python3 tools/build_locales.py`. The script stops if an English string it expects is missing.

## Deploying

Any static host works (GitHub Pages, Netlify, Cloudflare Pages). For GitHub Pages: Settings → Pages → deploy from the `main` branch, root folder.
