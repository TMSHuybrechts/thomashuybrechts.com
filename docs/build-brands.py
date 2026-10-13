#!/usr/bin/env python3
"""Zelfde motor, andere carrosserie: bouwt één losse site per merk uit één template.

Per merk:
- docs/brands/<slug>.json          inhoud (teksten, testvragen, lettertypes)
- docs/brands/themes/<slug>.css    carrosserie (kleuren, lettertypes, vormen)

Gedeeld: docs/brands/base.css, docs/brands/brand.js en /chat-ai.js (de chat-motor).
Run: python docs/build-brands.py   ->   dist-merken/<slug>/ (zelfstandig te hosten)
"""
import html, json, pathlib, shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = pathlib.Path(__file__).resolve().parent / "brands"
OUT = ROOT / "dist-merken"
EMAIL = "hey@thomashuybrechts.com"
MAIN_SITE = "https://thomashuybrechts.com/"
REQUIRED = ("name", "sector", "title", "description", "eyebrow", "h1", "intro", "cta", "fonts_url", "pains_title", "pains", "steps_title", "steps", "tries", "greeting", "cta_title", "cta_text")

e = html.escape


def cards(items, tag="article"):
    return "\n".join(
        f'          <{tag} class="card"><b>{i:02d}</b><h3>{e(t)}</h3><p>{e(p)}</p></{tag}>'
        for i, (t, p) in enumerate(items, 1)
    )


def render(slug, b):
    robots = "" if b.get("live") else '\n    <meta name="robots" content="noindex" />'
    mailto = f"mailto:{EMAIL}?subject={e(b['name'])}%20-%20kennismaking"
    tries = "\n".join(f'            <button type="button" class="try">{e(q)}</button>' for q in b["tries"])
    return f"""<!doctype html>
<html lang="nl" data-brand="{e(slug)}">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{e(b['title'])}</title>
    <meta name="description" content="{e(b['description'])}" />{robots}
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link rel="stylesheet" href="{e(b['fonts_url'])}" />
    <link rel="stylesheet" href="./style.css" />
    <script src="./chat-ai.js" defer></script>
    <script src="./brand.js" defer></script>
  </head>
  <body>
    <header class="top">
      <a class="logo" href="./">{e(b['name'])}</a>
      <a class="btn btn-small" href="#contact">{e(b['cta'])}</a>
    </header>

    <main>
      <section class="hero">
        <div class="hero-copy">
          <p class="eyebrow">{e(b['eyebrow'])}</p>
          <h1>{e(b['h1'])}</h1>
          <p class="lead">{e(b['intro'])}</p>
          <a class="btn" href="#contact">{e(b['cta'])}</a>
        </div>

        <div class="chat" aria-label="Probeer de assistent">
          <div class="chat-head"><i aria-hidden="true"></i><span>Probeer het zelf</span><small>dit is een AI</small></div>
          <div class="chat-log" id="chat-log" role="log" aria-live="polite" data-greeting="{e(b['greeting'])}"></div>
          <div class="chat-tries">
{tries}
          </div>
          <form class="chat-form" id="chat-form" autocomplete="off">
            <label class="sr-only" for="chat-q">Jouw vraag</label>
            <input id="chat-q" type="text" maxlength="300" placeholder="Typ een vraag zoals je klant dat zou doen…" />
            <button type="submit" aria-label="Verstuur">→</button>
          </form>
          <p class="chat-note" id="chat-note">Prijzen en afspraken bevestigen we persoonlijk.</p>
        </div>
      </section>

      <section class="block">
        <h2>{e(b['pains_title'])}</h2>
        <div class="grid">
{cards(b['pains'])}
        </div>
      </section>

      <section class="block block-alt">
        <h2>{e(b['steps_title'])}</h2>
        <div class="grid">
{cards(b['steps'])}
        </div>
      </section>

      <section class="cta" id="contact">
        <h2>{e(b['cta_title'])}</h2>
        <p>{e(b['cta_text'])}</p>
        <a class="btn" href="{mailto}">{e(b['cta'])}</a>
        <p class="cta-mail">{EMAIL}</p>
      </section>
    </main>

    <footer>
      <p>{e(b['name'])} is een dienst van <a href="{MAIN_SITE}">Thomas Huybrechts</a>, freelance AI-chatbots &amp; automatisering, België.</p>
    </footer>
  </body>
</html>
"""


def build():
    base_css = (SRC / "base.css").read_text(encoding="utf-8")
    built = []
    for path in sorted(SRC.glob("*.json")):
        slug = path.stem
        brand = json.loads(path.read_text(encoding="utf-8"))
        missing = [k for k in REQUIRED if not brand.get(k)]
        if missing:
            raise SystemExit(f"{path.name}: ontbrekende velden: {', '.join(missing)}")
        theme = SRC / "themes" / f"{slug}.css"
        if not theme.exists():
            raise SystemExit(f"{slug}: geen carrosserie gevonden ({theme.relative_to(ROOT)})")

        out = OUT / slug
        out.mkdir(parents=True, exist_ok=True)
        (out / "index.html").write_text(render(slug, brand), encoding="utf-8", newline="\n")
        (out / "style.css").write_text(theme.read_text(encoding="utf-8") + "\n" + base_css, encoding="utf-8", newline="\n")
        shutil.copyfile(SRC / "brand.js", out / "brand.js")
        shutil.copyfile(ROOT / "chat-ai.js", out / "chat-ai.js")
        built.append(slug)
    print(f"{len(built)} merken gebouwd in {OUT.relative_to(ROOT)}/: {', '.join(built)}")


if __name__ == "__main__":
    build()
