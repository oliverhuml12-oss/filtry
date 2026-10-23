# reBottled landing page

A single-page website for reBottled, a social enterprise that replaces bottled water with a home reverse-osmosis system on subscription. It explains the mission, makes the case for switching and ends with an email sign-up for the regional pilot (first month and installation free).

Plain HTML, CSS and JavaScript. No build step and no dependencies.

## Files

- `index.html`: the page
- `styles.css`: all styles, including the tablet and phone layouts
- `main.js`: the bar animation and the sign-up forms
- `assets/`: logo, product image and icons

## Run it locally

Open `index.html` in a browser, or serve the folder:

```sh
python3 -m http.server 8000
```

then visit http://localhost:8000.

## Sign-up form

There are two identical sign-up fields, one in the hero and one at the bottom of the page. Each takes an email address, validates it and then asks which island the person lives on, so we know where to tell them about the pilot.

It is front-end only for now. Nothing is sent or stored. To connect a backend, replace `submitSignup()` (receives `{ email, signedUpAt }`) and `saveRegion()` (receives `{ email, region }`) in `main.js` with real requests.

## Deploying

Any static host works (GitHub Pages, Netlify, Cloudflare Pages). For GitHub Pages: Settings → Pages → deploy from the `main` branch, root folder.
