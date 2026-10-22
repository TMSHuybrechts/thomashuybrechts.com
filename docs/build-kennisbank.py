"""Genereert de kennisbank (/kennisbank/) uit De praktische technologiegids.

Run: python docs/build-kennisbank.py
Bron: de gids-bron (Markdown per hoofdstuk), standaard
      D:/FREELANCE/03_MARKETING/technologiegids/bron/encyclopedie  (of env GIDS_BRON)
Schrijft kennisbank/index.html en kennisbank/<slug>/index.html, en vult de sitemap aan.

Bewust gefaseerd: alleen de onderwerpen in TOPICS worden gepubliceerd (Google waardeert
een groeiende site meer dan honderden pagina's ineens). Voeg er per week een paar toe.
"""
import datetime
import html
import json
import os
import re
import subprocess
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
BRON = Path(os.environ.get("GIDS_BRON", "D:/FREELANCE/03_MARKETING/technologiegids/bron/encyclopedie"))
# Eigen artikels (cases), zelfde opbouw als de gids, nummer 0.N
EIGEN = ROOT / "docs" / "kennisbank-artikels"
SITE = "https://thomashuybrechts.com/"
EMAIL = "hey@thomashuybrechts.com"
TODAY = datetime.date.today().isoformat()
MAANDEN = ['januari', 'februari', 'maart', 'april', 'mei', 'juni', 'juli', 'augustus', 'september', 'oktober', 'november', 'december']
STAND = f"{MAANDEN[datetime.date.today().month - 1]} {datetime.date.today().year}"

# Gepubliceerde onderwerpen (nummer uit de gids). Gekozen omdat ze aansluiten bij de diensten.
TOPICS = [
    "0.1",                                    # eigen project: AI Business OS
    "1.13", "1.16", "1.7", "1.6",            # AI-basis voor kmo's
    "2.1", "2.8", "2.17", "2.18",             # agents
    "4.1", "4.3", "4.6", "4.10", "4.11", "4.14", "4.16",  # automatisering
    "6.9", "6.10", "6.14", "6.15", "6.16",    # web
    "7.12",                                   # voice agents
    "9.8", "9.13",                            # beveiliging en privacy
    "10.1",                                   # SaaS
    "14.10",                                  # conversie
]
# Korte Nederlandse zoekterm per onderwerp: komt in titel en h1 (zo zoeken kmo's).
NL = {
    "0.1": "mijn eigen AI-systeem voor een freelancezaak", "10.1": "software als abonnement",
    "1.13": "AI die antwoordt uit je eigen documenten", "1.16": "goede instructies geven aan AI",
    "1.7": "AI lokaal draaien, zonder cloud", "1.6": "open AI-modellen die je zelf kunt draaien",
    "2.1": "AI-agents die zelf taken uitvoeren", "2.8": "AI koppelen aan je eigen software",
    "2.17": "de mens blijft aan het stuur", "2.18": "AI-stappen in je bedrijfsprocessen",
    "4.1": "processen automatiseren met n8n", "4.3": "bedrijfsprocessen automatiseren",
    "4.6": "systemen die elkaar automatisch verwittigen", "4.10": "je klantenbestand slim opbouwen",
    "4.11": "automatisch nieuwe klanten vinden", "4.14": "e-mails automatisch verwerken",
    "4.16": "facturen en documenten automatisch lezen", "6.9": "een website die werkt als app",
    "6.10": "een website die op elk scherm werkt", "6.14": "toegankelijke websites (WCAG)",
    "6.15": "een snellere website", "6.16": "een veilige website",
    "7.12": "AI die de telefoon opneemt", "9.8": "AI-chatbots misleiden en hoe je dat voorkomt",
    "9.13": "GDPR voor kmo's", "14.10": "meer aanvragen uit je website halen",
}
CHAPTERS = {0: "Eigen projecten", 1: "AI en taalmodellen", 2: "AI-agents", 4: "Automatisering", 6: "Websites en apps",
            7: "Spraak en beeld", 9: "Beveiliging en privacy", 10: "SaaS en software", 14: "Business en groei"}


def slugify(title):
    s = title.lower().replace("&", "en")
    s = re.sub(r"\(([^)]*)\)", r" \1 ", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return re.sub(r"-{2,}", "-", s)


def load_entries():
    """Alle onderwerpen uit de gids: nummer -> {title, md}."""
    out = {}
    for f in sorted(BRON.glob("ch*.md")) + sorted(EIGEN.glob("*.md")):
        text = f.read_text(encoding="utf-8")
        for m in re.finditer(r"^### (\d{1,2}\.\d{1,2}) (.+?)\n(.*?)(?=^### |\Z)", text, re.S | re.M):
            out[m.group(1)] = {"num": m.group(1), "title": m.group(2).strip(), "md": m.group(3).strip()}
    return out


def pandoc(md):
    r = subprocess.run(["pandoc", "-f", "markdown", "-t", "html", "--wrap=none"], input=md.encode("utf-8"), capture_output=True)
    if r.returncode:
        raise RuntimeError(r.stderr.decode("utf-8", "replace"))
    return r.stdout.decode("utf-8")


def to_sections(md, published):
    """Zet '- **Label** tekst'-blokken om in <section> met <h2>. Geeft (oneliner, sections_html)."""
    soup = BeautifulSoup(pandoc(md), "html.parser")
    oneliner = ""
    first = soup.find("p")
    if first and "In één zin" in first.get_text():
        first.strong.decompose() if first.strong else None
        oneliner = first.get_text(" ", strip=True)
        first.decompose()
    parts = []
    top = soup.find("ul")
    for li in (top.find_all("li", recursive=False) if top else []):
        strong = li.find("strong")
        label = strong.get_text(strip=True).rstrip(":") if strong else ""
        if strong:
            strong.decompose()
        inner = li.decode_contents().strip()
        inner = re.sub(r"^\s*:?\s*", "", inner)
        if label.lower() == "praktijkvoorbeeld":
            label = "Praktijkvoorbeeld (fictief)"
        parts.append((label, inner))
    body = "\n".join(
        f'        <section class="svc-block kb-block">\n          <h2>{html.escape(lab)}</h2>\n          <div class="kb-text">{link_refs(inner, published)}</div>\n        </section>'
        for lab, inner in parts)
    return oneliner, body


def link_refs(fragment, published):
    """Gidsverwijzingen '(4.11)' zijn op het web betekenisloos: het nummer verdwijnt en de
    omschrijving ervoor wordt een link als dat onderwerp gepubliceerd is."""
    def repl(m):
        lead, phrase, num = m.group(1), m.group(2), m.group(3)
        return f'{lead}<a href="../{published[num]}/">{phrase}</a>' if num in published else lead + phrase
    out = re.sub(r"(^|[+,;:>]\s*|\s)([^<>()+,;:]{2,80}?)\s*\((\d{1,2}\.\d{1,2})\)", repl, fragment)
    return re.sub(r"\s*\((?:zie\s+)?\d{1,2}\.\d{1,2}(?:\s*(?:,|en)\s*\d{1,2}\.\d{1,2})*\)", "", out)


HEAD = """<!doctype html>
<html lang="nl" data-root="{up}">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title}</title>
    <meta name="description" content="{desc}" />
    <meta name="theme-color" content="#f3f0e8" />
    <meta name="color-scheme" content="light" />
    <link rel="canonical" href="{url}" />
    <!-- Gegenereerd door docs/build-kennisbank.py, niet met de hand aanpassen -->
    <meta property="og:type" content="{ogtype}" />
    <meta property="og:locale" content="nl_BE" />
    <meta property="og:site_name" content="Thomas Huybrechts" />
    <meta property="og:title" content="{title}" />
    <meta property="og:description" content="{desc}" />
    <meta property="og:url" content="{url}" />
    <meta property="og:image" content="{site}assets/og.png" />
    <meta name="twitter:card" content="summary_large_image" />
    <link rel="icon" href="{up}favicon.svg" type="image/svg+xml" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Manrope:wght@400;500;600;700&family=Playfair+Display:ital,wght@1,600&display=swap" />
    <link rel="stylesheet" href="{up}styles.css" />
    <script src="{up}script.js" defer></script>
    <script type="application/ld+json">
{schema}
    </script>
  </head>
  <body class="svc-page kb-page">
    <a class="skip-link" href="#inhoud">Naar de inhoud</a>
    <header class="site-header" id="header">
      <a class="brand" href="{up}" aria-label="Thomas Huybrechts, naar de homepage">
        <span class="brand-mark">TH</span>
        <span>Thomas Huybrechts</span>
      </a>
      <nav id="nav" aria-label="Hoofdmenu">
        <a href="{up}website-laten-maken/">Websites</a>
        <a href="{up}n8n-automatisatie/">Automatisatie</a>
        <a href="{up}ai-chatbot-laten-maken/">AI-chatbot</a>
        <a class="is-active" aria-current="page" href="{up}kennisbank/">Kennisbank</a>
        <a class="nav-contact" href="#contact">Contact</a>
      </nav>
      <div class="header-right">
        <button class="menu-toggle" type="button" aria-controls="nav" aria-expanded="false" aria-label="Menu openen">
          <span></span><span></span>
        </button>
      </div>
    </header>
"""

FOOT = """      <section class="contact" id="contact">
        <div class="contact-copy reveal">
          <p class="eyebrow"><span class="status-dot"></span> Vrijblijvend</p>
          <h2>Wil je dit toepassen in je eigen zaak?</h2>
          <p class="contact-sub">Ik help kmo's en zelfstandigen met websites, AI-chatbots en automatisering. Vraag een gratis website-check aan of stel gewoon je vraag.</p>
          <div class="contact-actions">
            <a class="button button-light" href="mailto:{email}?subject={subject}">Stel je vraag <span aria-hidden="true">&nearr;</span></a>
            <button class="copy-email" type="button" data-email="{email}" aria-live="polite">
              <span class="copy-email-text">{email}</span>
              <span class="copy-email-hint">Klik om te kopiëren</span>
            </button>
          </div>
        </div>
        <div class="contact-disc reveal" aria-hidden="true">
          <span>HELLO &middot; BONJOUR &middot; HALLO &middot; HEY &middot; </span>
          <strong>TH</strong>
        </div>
      </section>
    </main>
    <footer>
      <a class="brand footer-brand" href="{up}"><span class="brand-mark">TH</span><span>Thomas Huybrechts</span></a>
      <nav class="footer-nav" aria-label="Voettekst">
        <a href="{up}website-laten-maken/">Website laten maken</a>
        <a href="{up}ai-chatbot-laten-maken/">AI-chatbot laten maken</a>
        <a href="{up}n8n-automatisatie/">n8n-automatisatie</a>
        <a href="{up}kennisbank/">Kennisbank</a>
        <a href="mailto:{email}">E-mail</a>
      </nav>
      <p>&copy; <span id="year"></span> Thomas Huybrechts &middot; Uit &ldquo;De praktische technologiegids&rdquo;</p>
    </footer>
  <script data-goatcounter="https://thomashuybrechts.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>
</body>
</html>
"""

AUTHOR = {"@id": SITE + "#thomas"}


def page_schema(e, url, desc):
    return json.dumps({"@context": "https://schema.org", "@graph": [
        {"@type": "TechArticle", "headline": f"{e['title']}: {NL[e['num']]}", "description": desc, "inLanguage": "nl-BE",
         "url": url, "mainEntityOfPage": url, "author": AUTHOR, "publisher": AUTHOR, "dateModified": TODAY,
         **({} if e["num"].startswith("0.") else {"isPartOf": {"@type": "Book", "name": "De praktische technologiegids", "author": AUTHOR}}),
         "about": {"@type": "DefinedTerm", "name": e["title"], "description": desc}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Thomas Huybrechts", "item": SITE},
            {"@type": "ListItem", "position": 2, "name": "Kennisbank", "item": SITE + "kennisbank/"},
            {"@type": "ListItem", "position": 3, "name": e["title"], "item": url}]},
    ]}, ensure_ascii=False, indent=2)


GUIDE_CARD = """          <article class="price-card price-card-accent kb-card">
            <p class="price-name">Uit de gids</p>
            <p class="kb-card-title">De praktische technologiegids</p>
            <p class="kb-card-text">219 onderwerpen over AI, automatisering, websites en beveiliging, uitgelegd voor wie er mee aan de slag wil. Elk onderwerp op één pagina.</p>
            <ul>
              <li>Voor ondernemers, makers en nieuwsgierigen</li>
              <li>Belgische regels (stand {stand})</li>
              <li>Samengesteld door Thomas Huybrechts</li>
            </ul>
            <a class="button button-light kb-card-btn" href="#contact">Vraag hulp bij je project <span aria-hidden="true">&rarr;</span></a>
          </article>"""
OWN_CARD = """          <article class="price-card price-card-accent kb-card">
            <p class="price-name">Eigen project</p>
            <p class="kb-card-title">In ontwikkeling</p>
            <p class="kb-card-text">Vandaag gebruik ik dit zelf voor mijn freelancezaak. Wil je het ook gebruiken of mee testen zodra het als dienst beschikbaar is?</p>
            <ul>
              <li>Gebouwd en getest door Thomas Huybrechts</li>
              <li>Belgische mailregels ingebouwd</li>
              <li>Zelf gehost, jouw gegevens blijven van jou</li>
            </ul>
            <a class="button button-light kb-card-btn" href="#contact">Interesse? Laat het weten <span aria-hidden="true">&rarr;</span></a>
          </article>"""


def render_topic(e, published, entries):
    slug = published[e["num"]]
    url = f"{SITE}kennisbank/{slug}/"
    oneliner, body = to_sections(e["md"], published)
    desc = (oneliner[:155].rsplit(" ", 1)[0] + "…") if len(oneliner) > 158 else oneliner
    title = f"{e['title']}: {NL[e['num']]} | Kennisbank Thomas Huybrechts"
    chap = int(e["num"].split(".")[0])
    siblings = [n for n in TOPICS if n != e["num"] and int(n.split(".")[0]) == chap][:4]
    related = siblings or [n for n in TOPICS if n != e["num"]][:3]
    related_html = "\n".join(f'          <a class="svc-related-link" href="../{published[n]}/">{html.escape(entries[n]["title"])} <span aria-hidden="true">&rarr;</span></a>' for n in related)
    up = "../../"
    own = e["num"].startswith("0.")
    aside = OWN_CARD if own else GUIDE_CARD.format(stand=STAND)
    return HEAD.format(up=up, title=html.escape(title), desc=html.escape(desc), url=url, ogtype="article", site=SITE,
                       schema=page_schema(e, url, desc)) + f"""
    <main id="inhoud">
      <nav class="svc-crumbs" aria-label="Kruimelpad"><a href="{up}">Home</a> <span aria-hidden="true">/</span> <a href="../">Kennisbank</a> <span aria-hidden="true">/</span> <span>{html.escape(e['title'])}</span></nav>
      <section class="svc-hero kb-hero">
        <p class="eyebrow"><span class="status-dot"></span> KENNISBANK &middot; {html.escape(CHAPTERS.get(chap, '').upper())}</p>
        <h1>{html.escape(e['title'])}</h1>
        <p class="kb-sub">{html.escape(NL[e['num']][0].upper() + NL[e['num']][1:])}</p>
        <p class="hero-intro">{html.escape(oneliner)}</p>
      </section>

      <div class="svc-layout">
        <article class="svc-body kb-body">
{body}
        </article>
        <aside class="svc-aside reveal" aria-label="Over deze uitleg">
{aside}
        </aside>
      </div>

      <section class="svc-related reveal" aria-label="Verwante onderwerpen">
        <p class="eyebrow">VERWANTE ONDERWERPEN</p>
{related_html}
        <a class="svc-related-link" href="../">Alle onderwerpen <span aria-hidden="true">&rarr;</span></a>
      </section>
""" + FOOT.format(up=up, email=EMAIL, subject=html.escape(e["title"]))


# Teasers: eigen projecten die nog niet beschikbaar zijn. Nieuwsgierig maken, niet alles uitleggen.
TEASERS = {
    "0.1": {
        "title": "AI Business OS: je hele freelancezaak in één scherm (binnenkort) | Thomas Huybrechts",
        "desc": "Een eigen AI-systeem dat klanten zoekt, websites doorlicht, opvolgt en mailt volgens de Belgische regels. Binnenkort beschikbaar: zet je op de wachtlijst.",
        "h1": "AI Business OS. <em>Je zaak, op één scherm.</em>",
        "intro": "Ik bouwde het voor mezelf: één systeem dat klanten zoekt, hun website doorlicht, de opvolging bewaakt en mailt zonder de Belgische regels te breken. Vandaag draait mijn eigen freelancezaak erop. Binnenkort misschien de jouwe.",
        "hooks": [("20 bedrijven", "doorgelicht in minder dan een minuut (echte scan in Meerhout)"),
                  ("0 dubbele mails", "en nooit nog mailen naar wie zich afmeldde"),
                  ("Made in België", "met de Belgische mailregels ingebouwd, niet als bijzaak")],
        "shots": [("bos-command-center", "Command Center", "Elke afdeling in één oogopslag. Groen draait. Wat aandacht vraagt, zie je meteen."),
                  ("bos-lead-hunter", "Lead Hunter", "Het zoekt, het meet, en het zegt je bij wie je eerst moet aankloppen."),
                  ("bos-crm", "CRM & Sales", "Van eerste contact tot klant. Slepen in plaats van Excel."),
                  ("bos-outreach", "Cold Outreach", "Mails die de regels kennen. Ook op de dagen dat jij ze vergeet.")],
    },
}


def render_teaser(e, published, entries):
    t = TEASERS[e["num"]]
    slug = published[e["num"]]
    url = f"{SITE}kennisbank/{slug}/"
    up = "../../"
    schema = json.dumps({"@context": "https://schema.org", "@graph": [
        {"@type": "SoftwareApplication", "name": e["title"], "applicationCategory": "BusinessApplication", "operatingSystem": "Web",
         "description": t["desc"], "url": url, "author": AUTHOR, "creator": AUTHOR, "inLanguage": "nl-BE",
         "image": [f"{SITE}assets/kennisbank/{s}.webp" for s, *_ in t["shots"]]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Thomas Huybrechts", "item": SITE},
            {"@type": "ListItem", "position": 2, "name": "Kennisbank", "item": SITE + "kennisbank/"},
            {"@type": "ListItem", "position": 3, "name": e["title"], "item": url}]},
    ]}, ensure_ascii=False, indent=2)
    hooks = "\n".join(f"        <div><b>{html.escape(a)}</b><span>{html.escape(b)}</span></div>" for a, b in t["hooks"])
    shots = "\n".join(
        f'        <figure class="kb-shot reveal"><img src="{up}assets/kennisbank/{s}.webp" width="1600" height="1000" loading="{("eager", "lazy")[i > 0]}" decoding="async" alt="Screenshot van {html.escape(name)} in AI Business OS">'
        f'<figcaption><b>{html.escape(name)}</b>{html.escape(cap)}</figcaption></figure>'
        for i, (s, name, cap) in enumerate(t["shots"]))
    head = HEAD.format(up=up, title=html.escape(t["title"]), desc=html.escape(t["desc"]), url=url, ogtype="website", site=SITE, schema=schema)
    head = head.replace(f'<meta property="og:image" content="{SITE}assets/og.png" />', f'<meta property="og:image" content="{SITE}assets/kennisbank/{t["shots"][0][0]}.webp" />')
    foot = FOOT.format(up=up, email=EMAIL, subject="Wachtlijst AI Business OS")
    foot = foot.replace("Wil je dit toepassen in je eigen zaak?", "Als eerste weten wanneer het klaar is?").replace("Stel je vraag <span", "Zet me op de wachtlijst <span")
    return head.replace('<body class="svc-page kb-page">', '<body class="svc-page kb-page kb-teaser">') + f"""
    <main id="inhoud">
      <div class="kb-soon" role="note"><strong>Coming soon</strong><span>In ontwikkeling &middot; zet je op de wachtlijst</span></div>
      <nav class="svc-crumbs" aria-label="Kruimelpad"><a href="{up}">Home</a> <span aria-hidden="true">/</span> <a href="../">Kennisbank</a> <span aria-hidden="true">/</span> <span>{html.escape(e['title'])}</span></nav>
      <section class="svc-hero kb-hero">
        <p class="eyebrow"><span class="status-dot"></span> EIGEN PROJECT &middot; SAAS IN WORDING</p>
        <h1>{t['h1']}</h1>
        <p class="hero-intro">{html.escape(t['intro'])}</p>
        <div class="hero-actions">
          <a class="button button-dark" href="mailto:{EMAIL}?subject=Wachtlijst%20AI%20Business%20OS">Zet me op de wachtlijst <span aria-hidden="true">&rarr;</span></a>
        </div>
      </section>
      <div class="kb-hooks reveal">
{hooks}
      </div>
      <div class="kb-gallery">
{shots}
      </div>
      <p class="kb-note">Screenshots met verzonnen demogegevens. Hoe het precies werkt? Dat vertel ik graag persoonlijk.</p>
      <section class="svc-related reveal" aria-label="Lees ook">
        <p class="eyebrow">LEES OOK</p>
        <a class="svc-related-link" href="../{published['10.1']}/">Wat is SaaS? <span aria-hidden="true">&rarr;</span></a>
        <a class="svc-related-link" href="../{published['4.11']}/">Automatisch nieuwe klanten vinden <span aria-hidden="true">&rarr;</span></a>
        <a class="svc-related-link" href="../">Alle onderwerpen <span aria-hidden="true">&rarr;</span></a>
      </section>
""" + foot


def render_index(published, entries):
    url = SITE + "kennisbank/"
    desc = "Heldere uitleg over AI, chatbots, automatisering, websites en beveiliging voor ondernemers, makers en iedereen die mee wil met technologie. Uit De praktische technologiegids van Thomas Huybrechts."
    groups = []
    for chap, name in CHAPTERS.items():
        items = [n for n in TOPICS if int(n.split(".")[0]) == chap]
        if not items:
            continue
        lis = "\n".join(
            f'            <li><a href="{published[n]}/"><strong>{html.escape(entries[n]["title"])}</strong><span>{html.escape(NL[n])}</span></a></li>'
            for n in items)
        groups.append(f'        <section class="kb-group reveal">\n          <h2>{html.escape(name)}</h2>\n          <ul class="kb-list">\n{lis}\n          </ul>\n        </section>')
    schema = json.dumps({"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "name": "Kennisbank", "description": desc, "url": url, "inLanguage": "nl-BE", "author": AUTHOR,
         "hasPart": [{"@type": "TechArticle", "headline": entries[n]["title"], "url": f"{url}{published[n]}/"} for n in TOPICS]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Thomas Huybrechts", "item": SITE},
            {"@type": "ListItem", "position": 2, "name": "Kennisbank", "item": url}]},
    ]}, ensure_ascii=False, indent=2)
    up = "../"
    return HEAD.format(up=up, title="Kennisbank: AI, automatisering en websites gewoon uitgelegd | Thomas Huybrechts",
                       desc=html.escape(desc), url=url, ogtype="website", site=SITE, schema=schema) + f"""
    <main id="inhoud">
      <nav class="svc-crumbs" aria-label="Kruimelpad"><a href="{up}">Home</a> <span aria-hidden="true">/</span> <span>Kennisbank</span></nav>
      <section class="svc-hero kb-hero">
        <p class="eyebrow"><span class="status-dot"></span> KENNISBANK</p>
        <h1>Technologie, <em>gewoon uitgelegd.</em></h1>
        <p class="hero-intro">AI, chatbots, automatisering, websites en beveiliging: wat is het, wat kun je ermee en waar moet je op letten? Korte, eerlijke uitleg voor ondernemers, makers en iedereen die mee wil met technologie, uit De praktische technologiegids. Elke week komen er onderwerpen bij.</p>
      </section>
      <div class="kb-groups">
{chr(10).join(groups)}
      </div>
""" + FOOT.format(up=up, email=EMAIL, subject="Vraag via de kennisbank")


def update_sitemap(published):
    path = ROOT / "sitemap.xml"
    xml = path.read_text(encoding="utf-8")
    xml = re.sub(r"  <!-- kennisbank -->.*?<!-- /kennisbank -->\n", "", xml, flags=re.S)
    locs = [SITE + "kennisbank/"] + [f"{SITE}kennisbank/{published[n]}/" for n in TOPICS]
    block = "  <!-- kennisbank -->\n" + "".join(
        f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>{'0.8' if u.endswith('kennisbank/') else '0.6'}</priority></url>\n"
        for u in locs) + "  <!-- /kennisbank -->\n"
    path.write_text(xml.replace("</urlset>", block + "</urlset>"), encoding="utf-8", newline="\n")


def main():
    entries = load_entries()
    missing = [n for n in TOPICS if n not in entries or n not in NL]
    assert not missing, f"onbekende onderwerpen: {missing}"
    published = {n: slugify(entries[n]["title"]) for n in TOPICS}
    base = ROOT / "kennisbank"
    for n in TOPICS:
        out = base / published[n] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        render = render_teaser if n in TEASERS else render_topic
        out.write_text(render(entries[n], published, entries), encoding="utf-8", newline="\n")
    (base / "index.html").write_text(render_index(published, entries), encoding="utf-8", newline="\n")
    update_sitemap(published)
    print(f"kennisbank: {len(TOPICS)} onderwerpen + overzicht, sitemap bijgewerkt")


if __name__ == "__main__":
    main()
