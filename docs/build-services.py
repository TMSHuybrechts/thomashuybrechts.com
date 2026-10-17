"""Genereert de dienstpagina's (SEO-landingspagina's) uit de SERVICES-lijst.

Run: python docs/build-services.py
Schrijft <slug>/index.html in de root. Prijzen staan bovenaan in PRICES,
zodat homepage en dienstpagina's samen aangepast kunnen worden.
Bron van de prijzen: docs/marktonderzoek-prijzen.md
"""
import html
import json
import sys
from urllib.parse import quote
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
SITE = "https://thomashuybrechts.com/"
EMAIL = "hey@thomashuybrechts.com"
REGION = ["Meerhout", "Geel", "Mol", "Balen", "Laakdal", "Westerlo", "Herentals", "Kasterlee", "Retie", "Turnhout"]

PRICES = {
    "website": "1.250",
    "chatbot": "250",
    "chatbot_month": "129",
    "n8n": "750",
    "hourly": "75",
    "zorg_basis": "45",
    "zorg_plus": "110",
    "zorg_premium": "250",
}

SERVICES = [
    {
        "slug": "website-laten-maken",
        "key": "website",
        "title": "Website laten maken Kempen | vanaf €{website} | Thomas Huybrechts",
        "description": "Website laten maken voor je kmo of zaak in de Kempen (Meerhout, Geel, Mol, Balen). Snel, vindbaar in Google, vaste prijs vanaf €{website} excl. btw. Gratis kennismaking.",
        "eyebrow": "WEBSITE LATEN MAKEN · KEMPEN",
        "h1": "Een website die <em>klanten oplevert.</em>",
        "intro": "Ik maak snelle, verzorgde websites voor kmo's en zelfstandigen in de Kempen. Geen trage template, wel een site die gevonden wordt in Google en bezoekers omzet in aanvragen. Vaste prijs, vooraf afgesproken.",
        "service_type": "Webdesign",
        "blocks": [
            ("Waarom een nieuwe website?", [
                "De meeste klanten zoeken je eerst op hun gsm. Laadt je site traag, is hij niet leesbaar op een klein scherm of vinden ze je telefoonnummer niet, dan bellen ze de volgende in de lijst. Een goede website lost precies dat op: hij laadt snel, vertelt in een paar seconden wat je doet en maakt het makkelijk om contact op te nemen.",
                "Ik bouw je site met schone, eigen code in plaats van een zwaar WordPress-thema met tientallen plugins. Dat maakt hem snel, veilig en goedkoop om te onderhouden. Je betaalt geen maandelijkse abonnementen voor een websitebouwer en de site blijft volledig van jou.",
            ]),
            ("Vindbaar in Google, ook lokaal", [
                "Een mooie site waar niemand op terechtkomt, levert niets op. Daarom zit de basis van zoekmachineoptimalisatie (SEO) er standaard in: duidelijke titels en beschrijvingen per pagina, een logische opbouw, gestructureerde gegevens voor Google, een sitemap en koppeling met Google Search Console.",
                "Werk je vooral in de regio, dan richt ik de site op lokale zoekopdrachten, zoals \"loodgieter Geel\" of \"kapper Mol\". Samen met een Google Bedrijfsprofiel is dat de snelste weg naar meer telefoontjes uit je eigen buurt.",
            ]),
            ("Klaar om mee te groeien", [
                "Je website is vaak het eerste stuk van je digitale zaak. Wil je later vragen automatisch laten beantwoorden of aanvragen meteen in je agenda of CRM zetten, dan hang ik er een AI-chatbot of een n8n-automatisatie aan. Zonder alles opnieuw te moeten bouwen.",
            ]),
            ("Onderhoud voor een vast bedrag per maand", [
                "Een website is niet af na de oplevering. Er verschijnen updates, back-ups moeten kloppen en beveiliging vraagt opvolging. Wil je daar niet zelf mee bezig zijn, dan kan je een onderhoudspakket nemen voor een vast bedrag per maand, maandelijks opzegbaar met één maand opzeg. Je kiest uit drie opties:",
                "Zorg Basis, €{zorg_basis} per maand: hosting, back-ups, beveiligingsupdates en bewaking, zodat je site snel, veilig en online blijft.",
                "Zorg Plus, €{zorg_plus} per maand: alles van Basis, plus 1 uur kleine wijzigingen per maand en een maandrapport.",
                "Zorg Premium, €{zorg_premium} per maand: alles van Plus, plus 3 uur wijzigingen, een SEO-rapport en een antwoord binnen 1 werkdag.",
                "Betaal je liever per jaar vooraf, dan betaal je 10 maanden en krijg je er 2 gratis.",
                "Alle bedragen zijn exclusief btw.",
            ]),
        ],
        "includes": [
            "Ontwerp op maat, tot 5 pagina's",
            "Mobielvriendelijk en snel (gemeten met Google PageSpeed)",
            "Basis-SEO, sitemap en Google Search Console",
            "Contactformulier dat rechtstreeks in je mailbox toekomt",
            "Meertalig als je dat nodig hebt (meerprijs)",
            "Uitleg bij oplevering, de site is van jou",
            "Optioneel onderhoud vanaf €{zorg_basis} per maand, maandelijks opzegbaar",
        ],
        "faq": [
            ("Wat kost een website laten maken?", "Een website start bij mij vanaf €{website} excl. btw voor een site op maat tot 5 pagina's. Meer pagina's, meerdere talen of een webshop vragen een offerte op maat. Je krijgt altijd vooraf een vaste prijs."),
            ("Wat kost onderhoud van mijn website?", "Onderhoud is optioneel en kost €{zorg_basis}, €{zorg_plus} of €{zorg_premium} per maand (excl. btw), afhankelijk van hoeveel opvolging je wil. Het is maandelijks opzegbaar met één maand opzeg. Betaal je per jaar vooraf, dan betaal je 10 maanden en krijg je er 2 gratis."),
            ("Is onderhoud verplicht?", "Nee. De site is van jou en je kan hem ook zelf laten hosten en bijhouden. Een onderhoudspakket is voor wie liever niet zelf bezig is met updates, back-ups en beveiliging."),
            ("Hoe lang duurt het voor mijn website online staat?", "Voor een gewone kmo-site reken je op twee tot vier weken, afhankelijk van hoe snel teksten en foto's klaar zijn. De exacte planning staat in de offerte."),
            ("Kan ik zelf nog iets aanpassen?", "Kleine aanpassingen doe ik snel voor je. Wil je zelf regelmatig teksten wijzigen, dan bespreken we vooraf een oplossing waarmee dat makkelijk kan."),
            ("Werk je enkel in de Kempen?", "Nee. Ik woon in Meerhout, maar werk online voor klanten in heel België en daarbuiten. Alles verloopt op afstand: kennismaking per videogesprek, oplevering en uitleg, zodat je alles ook meteen digitaal hebt. Is een bezoek echt nodig, dan kom ik langs in de Kempen."),
        ],
        "related": ["ai-chatbot-laten-maken", "n8n-automatisatie"],
    },
    {
        "slug": "ai-chatbot-laten-maken",
        "key": "chatbot",
        "title": "AI-chatbot laten maken | €{chatbot_month}/maand | Thomas Huybrechts",
        "description": "AI-chatbot laten maken voor je website of webshop, getraind op je eigen documenten en FAQ. Leads naar je mailbox, in het Nederlands. €{chatbot_month}/maand + €{chatbot} opstart. Probeer de demo.",
        "eyebrow": "AI-CHATBOT LATEN MAKEN · BELGIË",
        "h1": "Een chatbot die je klanten <em>écht helpt.</em>",
        "intro": "Ik bouw AI-chatbots die vragen van je bezoekers beantwoorden op basis van jouw eigen informatie: je diensten, prijzen, openingsuren en voorwaarden. Dag en nacht, in het Nederlands, en als hij het niet weet, verwijst hij door naar jou.",
        "service_type": "AI-chatbot",
        "blocks": [
            ("Wat is een chatbot?", [
                "Een chatbot is een programma dat op je website, in een app of via berichten met bezoekers praat. De bezoeker typt een vraag en de chatbot antwoordt meteen. Zo krijgen klanten hulp zonder te wachten op een mail of een telefoontje.",
                "Er bestaan twee soorten chatbots, en het verschil bepaalt wat je er in de praktijk mee kan.",
            ]),
            ("Het verschil tussen een gewone chatbot en de nieuwe generatie", [
                "Een klassieke chatbot werkt met vaste scripts. De bezoeker kiest een knop of typt een trefwoord, en de bot volgt een voorgeprogrammeerd pad. Dat werkt voor eenvoudige vragen, maar zodra iemand het anders formuleert of iets onverwachts vraagt, loopt hij vast en zegt hij dat hij het niet begrijpt.",
                "De nieuwe generatie, een AI-chatbot, is gebouwd op een groot taalmodel. Die begrijpt gewone taal, ook met typfouten, omgangstaal of een vraag in twee delen, en formuleert zelf een antwoord. Daardoor voelt het als een gesprek in plaats van een keuzemenu.",
                "Een AI-chatbot kan ook fouten maken als je hem niet afbakent. Daarom laat ik hem enkel antwoorden uit jouw eigen informatie, en verwijst hij door naar jou als hij iets niet weet.",
                "Een stap verder zijn AI-agents, die niet alleen antwoorden maar ook acties uitvoeren, zoals een aanvraag doorsturen of een afspraak voorstellen. Dat bespreken we als het bij jouw zaak past.",
            ]),
            ("Hoe zijn we hier gekomen? Een korte geschiedenis", [
                "Chatbots zijn ouder dan je denkt. In 1966 bouwde Joseph Weizenbaum aan het MIT ELIZA, een programma dat een gesprekstherapeut nabootste door op trefwoorden te reageren. Het begreep niets, maar mensen praatten er toch mee. Zo ontstonden de eerste chatbots: regels en scripts.",
                "Decennialang bleven chatbots zo werken, met keuzemenu's en vaste antwoorden, op websites en later in berichtenapps en spraakassistenten.",
                "De omslag kwam in 2017, toen onderzoekers van Google de transformer-architectuur beschreven, de techniek waarop moderne taalmodellen draaien. Eind 2022 bracht OpenAI ChatGPT uit en kon iedereen zelf ervaren dat een computer gewone taal begrijpt en zinnige antwoorden schrijft. Sindsdien volgen de modellen elkaar snel op, ook open modellen die je op je eigen computer kan draaien.",
            ]),
            ("Waar komt AI vandaan en hoe werkt het?", [
                "Moderne AI komt uit machine learning: in plaats van een computer regels te geven, laat je hem patronen leren uit enorme hoeveelheden voorbeelden. Een taalmodel leert zo uit een gigantische hoeveelheid tekst.",
                "In de kern voorspelt het telkens welk stukje tekst er logisch volgt. Door dat miljarden keren te oefenen leert het model grammatica, feiten en schrijfstijlen. Het zoekt dus niets op, het schrijft een antwoord dat past. Daarom kan het soms ook zelfverzekerd iets verkeerds zeggen.",
                "Voor een bedrijf maak ik dat betrouwbaar door het model bij elke vraag eerst het juiste stuk uit jouw eigen documenten te laten opzoeken en daaruit te laten antwoorden. Vakmensen noemen dat retrieval-augmented generation, kortweg RAG. Voor jou betekent het: antwoorden uit je eigen prijslijst en voorwaarden, niet uit het internet.",
            ]),
            ("Wat doet een AI-chatbot voor je zaak?", [
                "Je krijgt elke week dezelfde vragen: zijn jullie open op zaterdag, wat kost dat ongeveer, leveren jullie ook in Geel? Een AI-chatbot vangt die vragen op, ook 's avonds en in het weekend. Bezoekers krijgen meteen een antwoord in plaats van te wachten op een mail, en jij krijgt tijd terug.",
                "Op de demopagina kan je zelf een klassieke bot en een AI-bot naast elkaar testen.",
            ]),
            ("Getraind op jouw informatie, niet op het hele internet", [
                "De bot antwoordt alleen uit wat jij aanlevert: je website, een prijslijst, een handleiding, veelgestelde vragen. Zo verzint hij geen dingen over je zaak. Voor hij live gaat, testen we hem samen met de moeilijkste vragen die je klanten stellen.",
                "Laat een bezoeker zijn e-mailadres of telefoonnummer achter, dan komt die aanvraag meteen in je mailbox terecht. Zo wordt een vraag om 23 uur 's avonds de volgende ochtend een nieuwe klant.",
            ]),
            ("In de cloud of volledig lokaal", [
                "Standaard draait de chatbot via een snelle, betaalbare AI-dienst. Werk je met gevoelige gegevens, zoals in een praktijk of advocatenkantoor, dan kan hij ook volledig lokaal draaien op een server bij jou, zodat geen enkele vraag je gebouw verlaat.",
            ]),
        ],
        "includes": [
            "Getraind op je eigen documenten, website en FAQ",
            "Chatwidget in je bestaande website of webshop",
            "Leads en vragen rechtstreeks in je mailbox",
            "Nederlands, Engels en andere talen",
            "Duidelijk gemeld als AI, zoals de Europese AI Act vraagt",
            "Hosting, AI-kosten en onderhoud inbegrepen",
            "Maandelijks opzegbaar, geen jaarcontract",
        ],
        "faq": [
            ("Wat is een chatbot?", "Een chatbot is een programma dat op een website of in een app met bezoekers praat en hun vragen meteen beantwoordt, dag en nacht. Een klassieke chatbot volgt een vast script, een AI-chatbot begrijpt gewone taal en formuleert zelf een antwoord."),
            ("Wat is het verschil tussen een gewone chatbot en een AI-chatbot?", "Een gewone chatbot werkt met knoppen en trefwoorden en loopt vast bij een onverwachte vraag. Een AI-chatbot begrijpt gewone taal, ook met typfouten, en antwoordt op basis van de informatie die jij aanlevert, waardoor het gesprek natuurlijker verloopt."),
            ("Hoe werkt een AI-chatbot?", "Een AI-chatbot is gebouwd op een taalmodel dat getraind is op enorme hoeveelheden tekst en telkens voorspelt welk stukje tekst logisch volgt. Om betrouwbaar te zijn, zoekt hij bij elke vraag eerst het juiste stuk uit jouw eigen documenten op en antwoordt hij daaruit."),
            ("Wat kost een AI-chatbot laten maken?", "€{chatbot_month} per maand, plus een eenmalige opstart van €{chatbot} (excl. btw). Daarin zit alles: opbouw, hosting, de AI-kosten en onderhoud. Maandelijks opzegbaar. Moet hij gekoppeld worden aan andere systemen, dan krijg je daar een offerte voor."),
            ("Werkt het ook op mijn bestaande website?", "Ja. De chatbot is een klein stukje code dat in bijna elke website past: WordPress, Wix, Shopify, Squarespace of een site op maat."),
            ("Wat als de bot een fout antwoord geeft?", "Hij antwoordt alleen uit wat jij aanlevert en zegt het als hij iets niet weet. Dan verwijst hij door naar jou. We testen hem samen voor hij live gaat, en onderhoud houdt hem bij."),
            ("Wat gebeurt er met de gegevens van mijn klanten?", "Je kiest zelf waar de chatbot draait. Gesprekken worden niet gebruikt om andere AI-modellen te trainen, en wil je zekerheid, dan draait alles lokaal."),
        ],
        "related": ["n8n-automatisatie", "website-laten-maken"],
        "demo": True,
    },
    {
        "slug": "n8n-automatisatie",
        "key": "n8n",
        "title": "n8n-automatisatie voor kmo's | vanaf €{n8n} | Thomas Huybrechts",
        "description": "Repetitief werk automatiseren met n8n: offertes opvolgen, mails sorteren, data tussen systemen overzetten. Freelance in België, vanaf €{n8n} excl. btw.",
        "eyebrow": "N8N-AUTOMATISATIE · KMO'S",
        "h1": "Het saaie werk <em>doet zichzelf.</em>",
        "intro": "Gegevens overtypen van je mail naar een Excel, offertes opvolgen, facturen doorsturen naar je boekhouder: werk dat elke week terugkomt en niemand graag doet. Ik bouw met n8n een workflow die het automatisch voor je regelt.",
        "service_type": "Workflowautomatisering",
        "blocks": [
            ("Wat kan je automatiseren?", [
                "Bijna alles wat een vaste regel volgt. Een nieuwe aanvraag via je website komt automatisch in je CRM of Google Sheet en je krijgt een melding op je gsm. Een offerte die na een week nog niet getekend is, krijgt vanzelf een vriendelijke herinnering. Bijlagen uit je mailbox belanden in de juiste map, en een nieuwe bestelling in je webshop zet meteen een verzendlabel klaar.",
                "Met AI erbij gaat het nog een stap verder: binnenkomende mails automatisch sorteren en samenvatten, een eerste antwoord voorstellen, of gegevens uit een pdf-factuur halen.",
            ]),
            ("Waarom n8n?", [
                "n8n is een open-source automatisatieplatform dat met honderden apps praat: Gmail, Outlook, Google Sheets, Excel, Teamleader, Odoo, Shopify, WooCommerce, Slack en vrijwel alles met een API. Anders dan Zapier of Make betaal je niet per stap, en het kan op je eigen server draaien. Dat houdt de kosten laag en je gegevens onder controle.",
                "Ik gebruik n8n zelf elke dag, onder andere voor de AI-chatbot op deze website, die vragen beantwoordt en aanvragen naar mijn mailbox stuurt.",
            ]),
            ("Hoe het verloopt", [
                "We starten met één taak die je echt tijd kost. Ik bouw de workflow, we testen hem met echte gegevens, en je krijgt uitleg over hoe hij werkt. De workflow is daarna van jou. Werkt het, dan pakken we de volgende taak aan.",
            ]),
        ],
        "includes": [
            "Eén workflow die een terugkerende taak overneemt",
            "Koppeling met je mail, agenda, CRM, sheets of webshop",
            "Foutmeldingen als er iets misloopt",
            "Op n8n Cloud of op je eigen server",
            "Uitleg en overdracht, de workflow is van jou",
            "Groter traject? Uurtarief €{hourly} excl. btw",
        ],
        "faq": [
            ("Wat kost een n8n-automatisatie?", "Eén afgebakende workflow start bij mij vanaf €{n8n} excl. btw. Grotere trajecten met meerdere koppelingen reken ik aan €{hourly} per uur, met vooraf een raming. Daarnaast betaal je eventueel n8n Cloud (vanaf ongeveer €20 per maand), of niets als het op je eigen server draait."),
            ("Moet ik technisch zijn om dit te gebruiken?", "Nee. Je merkt vooral dat het werk gedaan wordt. Ik leg uit wat de workflow doet en hoe je ziet of alles goed loopt."),
            ("Kan je ook een bestaande Zapier- of Make-flow overzetten?", "Ja. Vaak bespaart overzetten naar n8n maandelijkse kosten, zeker als je flows veel stappen hebben."),
            ("Welke programma's kan je koppelen?", "Alles met een API of een n8n-koppeling: Gmail, Outlook, Google Sheets, Excel, Teamleader, Odoo, Shopify, WooCommerce, Mollie, Slack, Telegram en nog honderden andere."),
        ],
        "related": ["ai-chatbot-laten-maken", "website-laten-maken"],
    },
]

NAMES = {
    "website-laten-maken": "Website laten maken",
    "ai-chatbot-laten-maken": "AI-chatbot laten maken",
    "n8n-automatisatie": "n8n-automatisatie",
}


from services_en import NAMES_EN, SERVICES_EN, SLUG_EN, UI  # noqa: E402

SLUG_NL = {"website": "website-laten-maken", "chatbot": "ai-chatbot-laten-maken", "n8n": "n8n-automatisatie"}
SLUGS = {"nl": SLUG_NL, "en": SLUG_EN}
# in het Engels een komma als duizendtal (1,250)
PRICES_BY_LANG = {"nl": PRICES, "en": {k: v.replace(".", ",") for k, v in PRICES.items()}}


def names_of(lang):
    return NAMES if lang == "nl" else NAMES_EN


def page_url(key, lang):
    slug = SLUGS[lang][key]
    return f"{SITE}{slug}/" if lang == "nl" else f"{SITE}en/{slug}/"


def fill(s, lang="nl"):
    return s.format(**PRICES_BY_LANG[lang])


def esc(s, lang="nl"):
    return html.escape(fill(s, lang), quote=True)


def schema(svc, lang="nl"):
    url = page_url(svc["key"], lang)
    names = names_of(lang)
    price = PRICES[svc["key"]].replace(".", "")
    graph = [
        {
            "@type": "Service",
            "@id": f"{url}#dienst",
            "name": names[svc["slug"]],
            "serviceType": svc["service_type"],
            "description": fill(svc["description"], lang),
            "url": url,
            "inLanguage": lang,
            "provider": {"@id": f"{SITE}#zaak"},
            "areaServed": [{"@type": "City", "name": c} for c in REGION] + [{"@type": "Country", "name": UI[lang]["country"]}],
            "offers": {
                "@type": "Offer",
                "priceCurrency": "EUR",
                "price": price,
                "priceSpecification": {"@type": "PriceSpecification", "minPrice": price, "priceCurrency": "EUR", "valueAddedTaxIncluded": False},
            },
        },
        {
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": fill(q, lang), "acceptedAnswer": {"@type": "Answer", "text": fill(a, lang)}}
                for q, a in svc["faq"]
            ],
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Thomas Huybrechts", "item": SITE if lang == "nl" else SITE + "en/"},
                {"@type": "ListItem", "position": 2, "name": names[svc["slug"]], "item": url},
            ],
        },
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)


def render(svc, lang="nl"):
    T = UI[lang]
    names = names_of(lang)
    key = svc["key"]
    url = page_url(key, lang)
    up = "../" if lang == "nl" else "../../"  # naar de root van de site
    other = "en" if lang == "nl" else "nl"
    blocks = "\n".join(
        f"""        <section class="svc-block reveal">
          <h2>{html.escape(h)}</h2>
{chr(10).join(f'          <p>{esc(p, lang)}</p>' for p in ps)}
        </section>"""
        for h, ps in svc["blocks"]
    )
    includes = "\n".join(f"              <li>{esc(i, lang)}</li>" for i in svc["includes"])
    faq = "\n".join(
        f"""          <details>
            <summary>{esc(q, lang)} <span class="growth-toggle" aria-hidden="true">+</span></summary>
            <p>{esc(a, lang)}</p>
          </details>"""
        for q, a in svc["faq"]
    )
    related = "\n".join(
        f'          <a class="svc-related-link" href="../{r}/">{names[r]} <span aria-hidden="true">&rarr;</span></a>'
        for r in svc["related"]
    )
    demo_btn = f'\n            <a class="text-link" href="{up}demo/">{T["try_demo"]} <span aria-hidden="true">&rarr;</span></a>' if svc.get("demo") else ""
    active = ' class="is-active" aria-current="page"'
    nav = "\n".join(
        f'        <a{active if SLUGS[lang][k] == svc["slug"] else ""} href="../{SLUGS[lang][k]}/">{T["nav"][k]}</a>'
        for k in ("website", "n8n", "chatbot")
    )
    footer_links = "\n".join(
        f'        <a href="../{SLUGS[lang][k]}/">{T["footer_names"][k]}</a>' for k in ("website", "chatbot", "n8n")
    )
    price = PRICES_BY_LANG[lang][key]
    if key == "chatbot":
        price_html = f'<p class="price-amount"><small>+ &euro;{price} {T["setup"]}</small> &euro;{PRICES_BY_LANG[lang]["chatbot_month"]}<small>{T["per_month"]}</small></p>'
    else:
        price_html = f'<p class="price-amount"><small>{T["from"]}</small> &euro;{price}</p>'
    # taalversies van dezelfde dienst voor Google, en een zichtbare link naar de andere taal
    alternates = (
        f'    <link rel="alternate" hreflang="nl-BE" href="{page_url(key, "nl")}" />\n'
        f'    <link rel="alternate" hreflang="en" href="{page_url(key, "en")}" />\n'
        f'    <link rel="alternate" hreflang="x-default" href="{page_url(key, "nl")}" />'
    )
    i18n_scripts = f'    <script src="{up}i18n/en.js"></script>\n' if lang == "en" else ""
    other_href = f"../../{SLUGS[other][key]}/" if lang == "en" else f"../en/{SLUGS[other][key]}/"
    other_hreflang = "nl-BE" if other == "nl" else "en"
    return f"""<!doctype html>
<html lang="{lang}" data-root="{up}">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{esc(svc['title'], lang)}</title>
    <meta name="description" content="{esc(svc['description'], lang)}" />
    <meta name="theme-color" content="#f3f0e8" />
    <meta name="color-scheme" content="light" />
    <link rel="canonical" href="{url}" />
{alternates}
    <!-- Gegenereerd door docs/build-services.py, niet met de hand aanpassen -->

    <meta property="og:type" content="website" />
    <meta property="og:locale" content="{T['locale']}" />
    <meta property="og:site_name" content="Thomas Huybrechts" />
    <meta property="og:title" content="{esc(svc['title'], lang)}" />
    <meta property="og:description" content="{esc(svc['description'], lang)}" />
    <meta property="og:url" content="{url}" />
    <meta property="og:image" content="{SITE}assets/og.png" />
    <meta name="twitter:card" content="summary_large_image" />

    <link rel="icon" href="{up}favicon.svg" type="image/svg+xml" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Manrope:wght@400;500;600;700&family=Playfair+Display:ital,wght@1,600&display=swap" />
    <link rel="stylesheet" href="{up}styles.css" />
{i18n_scripts}    <script src="{up}script.js" defer></script>
    <script type="application/ld+json">
{schema(svc, lang)}
    </script>
  </head>
  <body class="svc-page">
    <a class="skip-link" href="#inhoud">{T['skip']}</a>

    <header class="site-header" id="header">
      <a class="brand" href="{'../' if lang == 'nl' else '../../en/'}" aria-label="{T['brand_aria']}">
        <span class="brand-mark">TH</span>
        <span>Thomas Huybrechts</span>
      </a>
      <nav id="nav" aria-label="{T['nav_aria']}">
{nav}
        <a href="{up}demo/">{T['demo']}</a>
        <a href="{up if lang == 'nl' else '../../en/'}#prijzen">{T['pricing']}</a>
        <a class="nav-contact" href="#contact">{T['contact']}</a>
      </nav>
      <div class="header-right">
        <button class="menu-toggle" type="button" aria-controls="nav" aria-expanded="false" aria-label="{T['menu_aria']}">
          <span></span><span></span>
        </button>
      </div>
    </header>

    <main id="inhoud">
      <nav class="svc-crumbs" aria-label="{T['crumbs_aria']}"><a href="{'../' if lang == 'nl' else '../../en/'}">{T['home']}</a> <span aria-hidden="true">/</span> <span>{names[svc['slug']]}</span></nav>
      <section class="svc-hero">
        <p class="eyebrow"><span class="status-dot"></span> {svc['eyebrow']}</p>
        <h1>{svc['h1']}</h1>
        <p class="hero-intro">{esc(svc['intro'], lang)}</p>
        <div class="hero-actions">
          <a class="button button-dark" href="#contact">{T['cta']} <span aria-hidden="true">&rarr;</span></a>{demo_btn}
        </div>
      </section>

      <div class="svc-layout">
        <div class="svc-body">
{blocks}
        </div>
        <aside class="svc-aside reveal" aria-label="{T['aside_aria']}">
          <article class="price-card price-card-accent">
            <p class="price-name">{names[svc['slug']]}</p>
            {price_html}
            <ul>
{includes}
            </ul>
            <p class="svc-vat">{T['vat']}</p>
          </article>
        </aside>
      </div>

      <section class="section faq svc-faq" id="vragen">
        <div class="section-label reveal"><span>?</span> {T['faq_label']}</div>
        <div class="faq-list reveal">
{faq}
        </div>
      </section>

      <section class="svc-related reveal" aria-label="{T['related_aria']}">
        <p class="eyebrow">{T['related_label']}</p>
{related}
      </section>

      <section class="contact" id="contact">
        <div class="contact-copy reveal">
          <p class="eyebrow"><span class="status-dot"></span> {T['avail']}</p>
          <h2>{T['contact_h2']}</h2>
          <p class="contact-sub">{T['contact_sub']}</p>
          <div class="contact-actions">
            <a class="button button-light" href="mailto:{EMAIL}?subject={quote(names[svc['slug']])}">{T['cta']} <span aria-hidden="true">&nearr;</span></a>
            <button class="copy-email" type="button" data-email="{EMAIL}" aria-live="polite">
              <span class="copy-email-text">{EMAIL}</span>
              <span class="copy-email-hint">{T['copy']}</span>
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
      <a class="brand footer-brand" href="{'../' if lang == 'nl' else '../../en/'}"><span class="brand-mark">TH</span><span>Thomas Huybrechts</span></a>
      <nav class="footer-nav" aria-label="{T['footer_nav_aria']}">
{footer_links}
        <a href="{up}demo/">{T['demo']}</a>
        <a href="mailto:{EMAIL}">{T['email']}</a>
        <a href="{other_href}" hreflang="{other_hreflang}" lang="{other}">{T['other_lang']}</a>
      </nav>
      <p>&copy; <span id="year"></span> Thomas Huybrechts &middot; {T['footer_line']}</p>
    </footer>
  <script data-goatcounter="https://thomashuybrechts.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>
</body>
</html>
"""


def main():
    for lang, services in (("nl", SERVICES), ("en", SERVICES_EN)):
        for svc in services:
            out = ROOT / svc["slug"] / "index.html" if lang == "nl" else ROOT / "en" / svc["slug"] / "index.html"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(render(svc, lang), encoding="utf-8", newline="\n")
            print(f"  {out.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
