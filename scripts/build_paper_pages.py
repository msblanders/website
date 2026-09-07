"""Build static paper pages and editable sharing cards from papers/papers.json.

Run with Python 3 from any directory. Add --images to render the SVG cards to PNG;
that optional step needs CairoSVG and the site's Google Fonts installed locally
(Fraunces 9pt Soft Medium and IBM Plex Sans). Commit the generated HTML/SVG/PNG.
GitHub Pages serves the committed files directly, without running this script.
Sharing PNGs render from vector artwork at 2400 by 1260 pixels. A versioned
filename lets sharing services fetch a fresh asset when the artwork changes.
"""
from pathlib import Path
from html import escape
import argparse
import json

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://msblanders.github.io/website/"


def build(render_images=False):
    papers = json.loads((ROOT / "papers/papers.json").read_text())
    for p in papers:
        folder = ROOT / "papers" / p["slug"]
        folder.mkdir(parents=True, exist_ok=True)
        url = BASE + "papers/" + p["slug"] + "/"
        image_name = p["slug"] + "-preview-v2.png"
        image_url = url + image_name
        e = escape
        authors = " · ".join(p["authors"])
        venue = f'{p["journal"]} · {p["year"]}'
        equal = f'<p class="equal">{e(p["equal_authors"])}</p>' if p.get("equal_authors") else ""
        finding = f'<p>{e(p["finding"])}</p>' if p.get("finding") else ""
        note = f'<p class="note">{e(p["equal_authors"])}</p>' if p.get("equal_authors") else ""
        extra = f'<a href="{e(p["extra_url"])}">{e(p["extra_label"])}</a>' if p.get("extra_url") else ""
        pubmed = f'<a href="{e(p["pubmed"])}">PubMed record</a>' if p.get("pubmed") else ""
        related = "\n".join(f'<li><a href="../{q["slug"]}/">{e(q["heading"])}</a> — <i>{e(q["journal"])}</i>, {q["year"]}</li>' for q in papers if q != p)
        author_meta = "\n".join(f'<meta name="citation_author" content="{e(a)}">' for a in p["authors"])
        methods = "".join(f'<li>{e(m)}</li>' for m in p["methods"])
        html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(p["heading"])} | Mitchell Landers</title>
<meta name="description" content="{e(p["description"])}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Mitchell Landers, PhD">
<meta property="og:title" content="{e(p["heading"])}">
<meta property="og:description" content="{e(p["description"])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{image_url}">
<meta property="og:image:secure_url" content="{image_url}">
<meta property="og:image:type" content="image/png">
<meta property="og:image:width" content="2400">
<meta property="og:image:height" content="1260">
<meta property="og:image:alt" content="{e(p["heading"] + ' — ' + venue + '. ' + authors)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(p["heading"])}">
<meta name="twitter:description" content="{e(p["description"])}">
<meta name="twitter:image" content="{image_url}">
<meta name="twitter:image:alt" content="{e(p["heading"] + ' — ' + venue + '. ' + authors)}">
<meta name="citation_title" content="{e(p["title"])}">
{author_meta}
<meta name="citation_journal_title" content="{e(p["journal"])}">
<meta name="citation_publication_date" content="{p["year"]}">
<meta name="citation_doi" content="{p["doi"]}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght,SOFT@9..144,300..600,50&amp;family=IBM+Plex+Sans:wght@400;500;600&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="../paper.css">
</head>
<body>
<a class="skip" href="#main">Skip to overview</a>
<header class="topbar wrap">
  <a class="brand" href="../../">Mitchell Landers, PhD</a>
  <nav aria-label="Main navigation"><a href="../../#publications">Publications</a><a href="../../files/cv.pdf">CV</a></nav>
</header>
<div class="hero"><div class="wrap">
  <p class="eyebrow">Published research · {e(venue)}</p>
  <h1>{e(p["heading"])}</h1>
  <p class="subtitle">{e(p["subtitle"])}</p>
  <p class="authors">{e(authors)}</p>
  {equal}
  <div class="actions">
    <a class="button" href="{e(p["primary_url"])}">{e(p["primary_label"])}</a>
    <a class="button secondary" href="{e(p["secondary_url"])}">{e(p["secondary_label"])}</a>
  </div>
</div></div>
<main class="wrap" id="main" tabindex="-1">
  <section class="overview" aria-labelledby="overview-title">
    <h2 id="overview-title">Overview</h2>
    <p>{e(p["summary"])}</p>
    {finding}
    <ul class="methods" aria-label="Research methods and scope">{methods}</ul>
  </section>
  <section class="citation" aria-labelledby="citation-title">
    <h2 id="citation-title">Publication</h2>
    <p>{e(p["citation_authors"])} ({p["year"]}). {e(p["title"])}. <i>{e(p["journal"])}, {p["volume"]}</i>{f'({p["issue"]})' if p.get("issue") else ''}, {p["pages"]}. <a href="https://doi.org/{p["doi"]}">https://doi.org/{p["doi"]}</a></p>
    {note}
    <div class="resources">{pubmed}{extra}<a href="../../#publications">All publications</a></div>
  </section>
  <nav class="related" aria-label="Related papers"><h2>Related research</h2><ul>{related}</ul></nav>
</main>
<footer><div class="wrap"><span>Mitchell Landers · Behavioral scientist</span><a href="../../">Research and projects</a></div></footer>
</body>
</html>
'''
        (folder / "index.html").write_text(html)
        title_lines = "\n".join(f'<text x="78" y="{234+i*89}" fill="#EAF1F2" font-family="Fraunces 9pt Soft" font-size="74" font-weight="500">{e(line)}</text>' for i, line in enumerate(p["card_lines"]))
        card_subtitle = f'<text x="82" y="323" fill="#EAF1F2" font-family="IBM Plex Sans" font-size="35" font-weight="500">{e(p["card_subtitle"])}</text>' if p.get("card_subtitle") else ""
        if card_subtitle:
            title_lines += "\n" + card_subtitle
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="2400" height="1260" viewBox="0 0 1200 630" role="img" aria-labelledby="title description">
<title id="title">{e(p["heading"])}</title>
<desc id="description">{e(venue + '. ' + authors + '. ' + p["card_detail"])}</desc>
<!-- Editable sharing card; typography and colors match the main website. -->
<defs><linearGradient id="background" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#15343E"/><stop offset="1" stop-color="#1E4B57"/></linearGradient><clipPath id="canvas"><rect width="1200" height="630"/></clipPath></defs>
<g clip-path="url(#canvas)">
<rect width="1200" height="630" fill="url(#background)"/>
<g fill="none" stroke="#A9C2C6" stroke-width="1.5" opacity=".12"><circle cx="1138" cy="98" r="228"/><circle cx="1138" cy="98" r="306"/><circle cx="1138" cy="98" r="384"/></g>
<text x="82" y="96" fill="#EAF1F2" font-family="IBM Plex Sans" font-size="27" font-weight="500">{e(venue.upper())}</text>
<rect x="82" y="131" width="64" height="5" rx="2.5" fill="#C98B1F"/>
{title_lines}
<text x="82" y="409" fill="#EAF1F2" font-family="IBM Plex Sans" font-size="30" font-weight="500">{e(p["card_detail"])}</text>
<path d="M82 478 H1118" stroke="#A9C2C6" stroke-opacity=".25"/>
<text x="82" y="543" fill="#EAF1F2" font-family="IBM Plex Sans" font-size="29" font-weight="500">{e(authors)}</text>
</g></svg>
'''
        (folder / "preview.svg").write_text(svg)
        if render_images:
            import cairosvg
            cairosvg.svg2png(bytestring=svg.encode(), write_to=str(folder / image_name))
        print(p["slug"], "built")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--images", action="store_true")
    build(parser.parse_args().images)
