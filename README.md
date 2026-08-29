# mitchelllanders.com — site source

One static page, no build step. `index.html` contains all HTML, CSS, and the small
publication-filter script. Fonts load from Google Fonts (Fraunces, IBM Plex Sans, IBM Plex Mono).

## Files
- `index.html` — the site
- `files/cv.pdf` — linked from the nav and the CV button (replace with the final CV)
- `files/avatar.jpg` — headshot (700×700 crop of the UCSD department photo). To swap it, drop in
  any square image with the same filename.
- `files/photo_ucsd_full.jpeg` — the uncropped original, in case you want a different crop.

## Before publishing
- Email is currently `m1landers@ucsd.edu`; swap for a personal address when the UCSD one lapses.

## Deploy on GitHub Pages (free, ~10 minutes)
1. Create a public repo named `USERNAME.github.io` (or any name, e.g. `site`).
2. Upload `index.html`, `README.md`, and the `files/` folder.
3. Settings → Pages → Source: "Deploy from a branch" → `main` / root → Save.
4. The site is live at `https://USERNAME.github.io/` within a minute or two.
5. Custom domain (optional): buy `mitchelllanders.com` (Namecheap/Cloudflare, ~$12/yr),
   add it under Settings → Pages → Custom domain, and add the four GitHub Pages A records
   plus a `www` CNAME at the registrar. Tick "Enforce HTTPS" once it validates.

Netlify Drop (`app.netlify.com/drop`) also works: drag the folder in, done.

## Editing
- Add a publication: copy any `<article class="pub">` block into the right year group.
  `data-tags` controls which filter buttons show it (space-separated: envy, shame, anger,
  forgiveness, status, methods).
- Add a year group: copy a `<div class="pubgroup" data-group>` block.
- Colors and fonts are the CSS variables at the top of `<style>`.
