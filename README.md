# reBottled landing page

A single-page website for reBottled, a social enterprise that replaces bottled water with a home reverse-osmosis system on subscription. It explains the mission, makes the case for switching and ends with an email sign-up for the regional pilot (first month and installation free).

Plain HTML, CSS and JavaScript. No build step and no dependencies.

## Files

- `index.html`: the page
- `styles.css`: all styles, including the tablet and phone layouts
- `main.js`: header behaviour, the bar animation and the sign-up form
- `assets/`: logo, product image and icons

## Run it locally

Open `index.html` in a browser, or serve the folder:

```sh
python3 -m http.server 8000
```

then visit http://localhost:8000.

## Sign-up form

The form is front-end only for now. It validates the email, the region and the consent tick box, then shows a confirmation. Nothing is sent or stored. To connect a backend, replace `submitSignup()` in `main.js` with a real request. It receives `{ email, region, consent, signedUpAt }`.

## Deploying

Any static host works (GitHub Pages, Netlify, Cloudflare Pages). For GitHub Pages: Settings → Pages → deploy from the `main` branch, root folder.
