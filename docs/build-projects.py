#!/usr/bin/env python3
"""Genereert de projectpagina's in /projecten/ vanuit één template.
Pas de PROJECTS-data hieronder aan en run: python3 docs/build-projects.py

Optionele velden per project:
- "images": lijst (src, caption). Leeg = geen gallery.
- "extra_partial": bestandsnaam in docs/partials/ die als los HTML-blok
  ná de gallery wordt ingevoegd (bv. de interactieve OpenClaw-wheel).
"""
import html, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PARTIALS = pathlib.Path(__file__).resolve().parent / "partials"
EMAIL = "hey@thomashuybrechts.com"

PROJECTS = [
    {
        "slug": "orbit-display",
        "num": "01",
        "tag": "LOKALE AI · ORCHESTRATIE · COMMAND CENTER",
        "title": "Orbit Display",
        "intro": "Eén visueel commandocentrum dat mijn lokale AI-tools, automatiseringen, beveiligingsutility's, skill-ontdekking en projectlaunchers samenbrengt in één navigeerbaar ecosysteem — met een draaiend wiel als navigatie.",
        "meta": [("Type", "Lokaal web-commandocentrum"), ("Status", "Actief in gebruik"), ("Rol", "Concept, ontwerp & ontwikkeling"), ("Stack", "Lokale AI · OpenClaw · n8n · Ollama · security tooling")],
        "images": [],
        "extra_partial": "openclaw-wheel.html",
        "problem": "Wie lokaal met AI werkt, verzamelt snel tientallen losse tools: modellen, automatiseringen, security-scanners, skill-collecties en dashboards. Ze staan verspreid over mappen, poorten en terminals. Je verliest het overzicht — wat draait er, wat sluimert, en hoe hangt alles samen?",
        "features": [
            ("Wiel-navigatie", "Elke tool is een node op een draaiend wiel; de centrale kaart toont meteen status, cijfers en acties. Eén beweging brengt je bij de juiste module."),
            ("Tool- & modulestatus", "In één oogopslag zien wat online is, wat sluimert en waar aandacht nodig is — met een operationeel rooster naast het wiel."),
            ("Lokale skill-ontdekking", "Doorzoek een index van duizenden lokale AI-skills, met categorieën en tags, zonder dat er iets naar de cloud gaat."),
            ("Audit- & security-views", "Bevindingen uit lokale audits worden visueel en read-only samengevat, zodat je snel ziet wat opvolging vraagt."),
            ("Projectlaunchers", "Start onderliggende tools en dashboards rechtstreeks vanuit één interface, in plaats van losse snelkoppelingen en terminals."),
            ("Verbonden ecosysteem", "Koppelingen naar de Thomas Cluster-modules en n8n-automatiseringen maken van losse tools één samenhangend geheel."),
        ],
        "learned": "De grootste winst zat niet in nóg een tool, maar in de laag eromheen: één plek die alles zichtbaar en bereikbaar maakt. Zodra status en navigatie samenvielen, ging een losse verzameling over in een echt ecosysteem.",
        "next": "Victus Control",
        "next_slug": "victus-control",
    },
    {
        "slug": "victus-control",
        "num": "02",
        "tag": "LOCAL-FIRST · OPERATIONS · REACT/TS",
        "title": "Victus Control",
        "intro": "Een local-first operations-platform om een AI-werkstation te begrijpen, structureren en beheren: live runtime-ontdekking, inventaris, resource-monitoring, security-review en een intent-map die je gewenste opstelling vergelijkt met de werkelijkheid.",
        "meta": [("Type", "Local-first ops-platform"), ("Status", "Actief in ontwikkeling"), ("Rol", "Concept, ontwerp & ontwikkeling"), ("Stack", "React · TypeScript · Vite · SQLite · Playwright")],
        "images": [("victus-control.png", "Victus Control — live services, resource-monitor en netwerkkaart (voorbeeldweergave met demodata)")],
        "problem": "Een lokaal AI-werkstation groeit snel uit tot een kluwen: modellen, automatiseringen, dashboards en tools verspreid over processen en poorten. Wat draait er echt, wat hoort er te draaien, en waar wijkt de werkelijkheid af van je bedoeling?",
        "features": [
            ("Live runtime-ontdekking", "Scant draaiende diensten en tools en toont status, health en resource-kost per lokale AI-tool — in plaats van losse terminals en giswerk."),
            ("Intent Map — bedoeld vs. waargenomen", "Teken hoe je werkstation hóórt te zijn en laat Victus dat vergelijken met wat er live draait: OK, ontbrekend, blootgesteld of onverwacht. Dát verschil is de kern van het project."),
            ("Resource-monitor", "CPU, RAM, GPU en VRAM in één oogopslag, zodat je meteen ziet waar de druk zit tijdens zwaar AI-werk."),
            ("Persistente inventaris", "Onthoudt bekende tools met notities en statuslabels, ook als ze net niet draaien — een levende catalogus in plaats van een kerkhof."),
            ("Security-review", "Onbekende luisteraars belanden in een review-flow in plaats van stil open te staan; je beslist wat vertrouwd is."),
            ("Agents & MCP-diagnostiek", "Zicht op gekoppelde agents en MCP-servers, bovenop een testbare React/TypeScript-architectuur met SQLite-state."),
        ],
        "learned": "De interessante vraag was niet ‘nog een dashboard’, maar: laat de gebruiker de bedóelde opstelling definiëren en vergelijk die met de live werkelijkheid. Dat verschil — desired vs. observed — is waar het echte inzicht zit.",
        "next": "Thomas Cluster Dashboard",
        "next_slug": "thomas-cluster",
    },
    {
        "slug": "thomas-cluster",
        "tag": "INFRASTRUCTUUR · DOCKER · n8n · OLLAMA",
        "title": "Thomas Cluster Dashboard",
        "intro": "Eén zelf-gehost controleplatform voor mijn lokale AI- en automatiseringscluster: een master command center met Docker-, n8n-, Ollama/OpenClaw- en ComfyUI-modules onder één dak.",
        "meta": [("Type", "Cluster-orkestratie"), ("Status", "Actief in gebruik"), ("Rol", "Concept, ontwerp & ontwikkeling"), ("Stack", "Docker · n8n · Ollama · OpenClaw · ComfyUI")],
        "images": [("thomas-cluster.png", "Master Cluster Command Center — start-flow, AI-mode/travel-mode en de module-HQ's (voorbeeldweergave)")],
        "problem": "Een groeiend lokaal AI-lab is al snel een verzameling losse diensten: containers, automatiseringen, modelservers en GPU-workflows, elk met hun eigen venster. Alles apart opstarten en controleren kost tijd en gaat mis.",
        "features": [
            ("Master command center", "Eén moederdashboard om het hele cluster te wekken, valideren en controleren — met een start-flow die stap voor stap netwerk, infra-node, AI-node, Ollama en OpenClaw nakijkt."),
            ("AI-mode & travel-mode", "De primaire AI-node blijft bereikbaar, ook wanneer de machine fysiek niet thuis staat, via een overlay-netwerk en reconnect-logica."),
            ("Docker-module", "Containers overzien en beheren vanuit het dashboard in plaats van losse terminals."),
            ("n8n-automatisering", "De automatiseringsmotor als eigen module, naast de rest van het cluster."),
            ("Lokale modellen", "Ollama en OpenClaw gekoppeld: modellen starten en verbinden met de rest van de stack."),
            ("ComfyUI / GPU-workflows", "Een aparte view voor beeldgeneratie en GPU-werk, als module van hetzelfde geheel."),
        ],
        "learned": "De modules — Docker, n8n, Ollama, ComfyUI — zijn geen losse projecten maar vensters op één systeem. De echte waarde zat in de start-flow en reconnect-logica die van losse diensten één betrouwbaar cluster maken.",
        "next": "Repo Notebook",
        "next_slug": "repo-notebook",
    },
    {
        "slug": "repo-notebook",
        "num": "03",
        "tag": "ELECTRON · LOKALE AI · KENNIS",
        "title": "Repo Notebook",
        "hero_bg": "repo-notebook-bg.jpg",
        "intro": "Een visuele kennisomgeving die GitHub-repositories verzamelt, analyseert en als verbonden informatie presenteert — met Oogst, lokale AI en slimme suggesties.",
        "meta": [("Type", "Desktop-app (Electron)"), ("Status", "Actief in ontwikkeling"), ("Rol", "Concept, ontwerp & ontwikkeling"), ("Stack", "Electron · lokale LLM · MCP · GitHub API")],
        "images": [("repo-notebook-2.webp", "Oogst: plak een GitHub-account, toolnamen of een pagina-URL en Repo Notebook haalt alle repositories op"), ("repo-notebook-1.webp", "De lijstweergave met 127 opgeslagen repositories, README, statistieken en notities per repo")],
        "problem": "Wie veel met open source werkt, verzamelt honderden repositories: in browsertabs, sterretjes, notities en losse mapjes. Daar gaat kennis verloren. Waarom sloeg je iets op? Werkt het nog? Wat hangt ermee samen?",
        "features": [
            ("Verzamelen zonder wrijving", "Plak een repo-URL en hij wordt opgeslagen met README, sterren, forks, taal en licentie. Zoeken, filteren op categorie en status, en een A–Z-index voor grote verzamelingen."),
            ("Oogst", "Plak een GitHub-account, een lijst toolnamen of een pagina-URL (blog, Medium, linktree). Oogst haalt de pagina op, trekt alle GitHub-links eruit en laat je kiezen wat naar de notebook gaat. Niets wordt bewaard tot jij het aanvinkt."),
            ("Lokale AI", "Categorieën, samenvattingen en suggesties komen van een lokaal draaiend taalmodel. Geen data naar de cloud, geen API-kosten, werkt ook offline."),
            ("Notities & status", "Per repo een eigen notitie (‘waarom sloeg je dit op?’) en een status: te proberen, geïnstalleerd, bevalt, archief. Zo blijft de verzameling levend in plaats van een kerkhof."),
            ("Kaart & Snelstart", "Repositories als verbonden kaart bekijken, en met één klik klonen of openen op GitHub."),
            ("MCP-koppeling", "Via het Model Context Protocol kunnen AI-assistenten rechtstreeks in de notebook zoeken en lezen — de basis voor de Obsidian-plugin."),
        ],
        "learned": "Lokale AI is snel genoeg voor dit soort werk als je de taken klein houdt: categoriseren, samenvatten, suggereren. De grootste winst zat niet in het model, maar in de workflow eromheen — Oogst en de statusknoppen maakten het verschil tussen ‘handig’ en ‘dagelijks gebruiken’.",
        "next": "Repo Notebook voor Obsidian",
        "next_slug": "repo-notebook-obsidian",
    },
    {
        "slug": "repo-notebook-obsidian",
        "num": "04",
        "tag": "OBSIDIAN · PLUGIN · MCP",
        "title": "Repo Notebook voor Obsidian",
        "intro": "Een Obsidian-plugin die Repo Notebook naar je eigen vault brengt, met BRAT-releases en een MCP-koppeling zodat AI-assistenten rechtstreeks met je notities kunnen werken.",
        "meta": [("Type", "Obsidian-plugin"), ("Status", "Actief in ontwikkeling"), ("Rol", "Ontwerp & ontwikkeling"), ("Stack", "TypeScript · Obsidian API · BRAT · MCP")],
        "images": [("repo-graph.jpg", "De kennisgraaf in Obsidian — elke opgeslagen repo wordt een notitie, met wikilinks die alles verbinden (uitgezoomde voorbeeldweergave)")],
        "problem": "Veel makers leven in Obsidian. Een aparte desktop-app is dan één plek te veel. De kennis over repositories hoort naast je andere notities te staan — doorzoekbaar, linkbaar en van jou.",
        "features": [
            ("Alles in je vault", "Repositories worden gewone Markdown-notities met frontmatter. Ze werken met je bestaande tags, links en graph view."),
            ("BRAT-releases", "Installeren en updaten via BRAT, zonder wachten op de officiële community-store. Snelle iteratie met echte gebruikers."),
            ("MCP-koppeling", "Een MCP-server maakt de vault bereikbaar voor AI-assistenten zoals Claude: zoeken in je repo-notities, samenvattingen opvragen, suggesties laten toevoegen."),
            ("Zelfde brein als Repo Notebook", "De analyse- en suggestielogica wordt gedeeld met de desktop-app, zodat beide dezelfde kwaliteit leveren."),
        ],
        "learned": "Een plugin bouwen dwingt je om je kern klein en overdraagbaar te maken. Wat in de desktop-app ‘vanzelf’ ging, moest hier expliciet en testbaar worden — en daar werd de desktop-app ook beter van.",
        "next": "CyberDash",
        "next_slug": "cyberdash",
    },
    {
        "slug": "cyberdash",
        "tag": "SECURITY · PYTHON · DOCKER · LOKALE AI",
        "title": "CyberDash",
        "intro": "Een modulair security-dashboard dat lokale AI, netwerk- en security-tools, OSINT-utility's en containerbeheer achter één webinterface samenbrengt — gebouwd als oefening in architectuur en integratie.",
        "meta": [("Type", "Security-dashboard"), ("Status", "Eerder project"), ("Rol", "Concept, ontwerp & ontwikkeling"), ("Stack", "Python · Flask · JavaScript · Docker · Ollama")],
        "images": [("cyberdash.jpg", "CyberDash — dashboard-overzicht met security-score, dreigingen, recente activiteit en systeemstatus (voorbeeldweergave met demodata)")],
        "problem": "Security-werk verspreidt zich over tientallen losse command-line-tools met elk hun eigen output. Ik wilde één plek die scanners, OSINT en een geïsoleerd oefenlab samenbrengt — en meteen een oefening in architectuur en integratie.",
        "features": [
            ("Eén webinterface", "Scanners, OSINT-tools en labbeheer achter één modulair dashboard in plaats van losse terminals."),
            ("Lokale AI-assistent", "Een lokaal taalmodel als assistent in de interface, zodat er geen data naar de cloud gaat."),
            ("Tool-wrappers", "Nette wrappers rond bekende security-tools, met de resultaten netjes in de interface."),
            ("OSINT-module", "Open-source-intelligence-hulpmiddelen gebundeld op één plek."),
            ("Geïsoleerd oefenlab", "Een containergebaseerd lab om veilig en afgeschermd te experimenteren."),
        ],
        "learned": "De uitdaging zat niet in de losse tools maar in de architectuur eromheen: modules netjes koppelen, output uniform tonen en alles veilig en geïsoleerd houden. Publiek toon ik dit als integratie- en ontwerpwerk, niet als live security-tooling.",
        "next": "LLM Wiki",
        "next_slug": "llm-wiki",
    },
    {
        "slug": "llm-wiki",
        "tag": "LOKALE AI · KENNISGRAAF · AUTO-INGEST",
        "title": "LLM Wiki",
        "intro": "Een zelf-onderhoudende kennisbank: bronnen worden automatisch ingelezen, entiteiten en concepten geëxtraheerd, en alles verbonden in een doorzoekbare kennisgraaf.",
        "meta": [("Type", "Kennisbank + kennisgraaf"), ("Status", "Actief in gebruik"), ("Rol", "Concept, ontwerp & ontwikkeling"), ("Stack", "Lokale AI · Python · Markdown · graafvisualisatie")],
        "images": [("llm-wiki-graph.webp", "De kennisgraaf: bronnen, entiteiten, concepten en syntheses verbonden via honderden relaties (label-vrije weergave)")],
        "problem": "Kennis raakt versnipperd over notities, documenten en gesprekken. Ik wilde een systeem dat bronnen automatisch inleest, samenvat en verbindt — zodat het overzicht meegroeit in plaats van te verwateren.",
        "features": [
            ("Automatische ingest", "Drop een bron in de inbox en de wiki leest hem in: samenvatting, kernclaims, entiteiten en concepten worden er automatisch uit gehaald."),
            ("Kennisgraaf", "Alles wordt verbonden in een doorzoekbare graaf met honderden nodes en relaties, met aparte types voor bronnen, entiteiten, concepten en syntheses."),
            ("Levende synthese", "Een overzichtspagina wordt bij elke ingest herschreven, zodat de rode draad over alle bronnen actueel blijft."),
            ("Lokaal & privaat", "Draait op lokale AI; de volledige kennisbank blijft op je eigen machine."),
            ("Gezond gehouden", "Ingebouwde controles op wees-pagina's, gebroken links en tegenstrijdigheden houden de kennisbank consistent."),
        ],
        "learned": "De waarde zat niet in nóg meer notities, maar in de verbindingen ertussen. Zodra ingest, graaf en synthese samenwerkten, werd een losse verzameling documenten een echt kennissysteem.",
        "next": "Jarvis",
        "next_slug": "jarvis",
    },
    {
        "slug": "jarvis",
        "tag": "AGENTS · SPRAAK · GEBAREN",
        "title": "Jarvis",
        "intro": "Een handsfree AI-command center: een visuele agent-architectuur die aanvoelt als een tactical game, bestuurd met klappen, stem en handgebaren.",
        "meta": [("Type", "AI-command center"), ("Status", "Actief in ontwikkeling"), ("Rol", "Concept, ontwerp & ontwikkeling"), ("Stack", "Lokale AI · agents · spraak (STT) · gebarenherkenning")],
        "images": [("jarvis-nexus.jpg", "Jarvis Nexus — het agent command center: elke agent heeft een eigen lane, load en input/output (voorbeeldweergave)")],
        "problem": "Een chatvenster is passief. Ik wilde een assistent die je zíét werken — welke agents actief zijn, hoe ze samenwerken en waar de volgende actie ontstaat — en die je handsfree bestuurt.",
        "features": [
            ("Agent command center", "Een Nexus-Core orkestreert gespecialiseerde agents (research, briefing, geheugen, risico) — elk met een eigen lane, load en duidelijke input/output. Meer mission control dan admin-paneel."),
            ("Klapbesturing", "2× kort klappen opent je dashboards, muziek en editor; 3× klappen stelt een gesproken vraag aan je kennisbank. Volledig handsfree."),
            ("Stem in het Vlaams", "Spraakinvoer en gesproken antwoorden in het Nederlands van hier."),
            ("Handgebaren", "Een aparte versie bestuurt de interface met handgebaren via de camera."),
            ("Lokaal brein", "Draait op lokale AI, zodat je gesprekken en data op je eigen machine blijven."),
        ],
        "learned": "Handsfree bediening dwingt je om intentie simpel te maken: een klap, een gebaar, een zin. De echte uitdaging zat niet in de features maar in betrouwbaar herkennen en meteen duidelijke feedback geven.",
        "next": "Sirena",
        "next_slug": "sirena",
    },
    {
        "slug": "sirena",
        "num": "05",
        "tag": "ASSISTENT · STEM · AVATAR",
        "title": "Sirena",
        "intro": "Een zichtbare Vlaamse desktopassistent met een lokaal AI-brein, stem en avatar — die niet alleen antwoordt, maar echte acties op je computer uitvoert.",
        "meta": [("Type", "Desktopassistent"), ("Status", "Actief in ontwikkeling"), ("Rol", "Concept, ontwerp & ontwikkeling"), ("Stack", "Lokale LLM · spraakherkenning & -synthese · avatar · systeemkoppelingen")],
        "images": [("sirena-app.jpg", "Sirena — chatvenster met modelkeuze, avatar en spraakbesturing (voorbeeldweergave)")],
        "problem": "AI-assistenten zitten meestal in een chatvenster en blijven bij praten. Sirena is een experiment in de andere richting: een assistent die je ziet en hoort, in het Nederlands van hier, en die dingen kan dóén op je computer.",
        "features": [
            ("Zichtbaar en hoorbaar", "Een avatar op je bureaublad, met stem in het Vlaams. Je praat ertegen, ze praat terug."),
            ("Lokaal brein", "Het taalmodel draait op je eigen machine. Je gesprekken en bestanden verlaten je computer niet."),
            ("Echte acties", "Koppelingen om bestanden te openen, programma's te starten, informatie op te zoeken en taken uit te voeren — met bevestiging waar dat hoort."),
            ("Uitbreidbaar", "Nieuwe vaardigheden toevoegen als modules, zodat Sirena meegroeit met wat je nodig hebt."),
        ],
        "learned": "Spraak en avatar maken een assistent meteen ‘echter’ — en dus ook strenger beoordeeld. Latency, betrouwbaarheid en duidelijke bevestigingen wegen zwaarder dan nog een feature.",
        "next": "Embedded experimenten",
        "next_slug": "embedded",
    },
    {
        "slug": "embedded",
        "num": "06",
        "tag": "ESP32 · FIRMWARE · HARDWARE",
        "title": "Embedded experimenten",
        "intro": "Eigen firmware, displays en microcontrollers samenbrengen in tastbare apparaten — van ESP32-prototypes tot interactieve interfaces die met je software praten.",
        "meta": [("Type", "Hardware & firmware"), ("Status", "Doorlopend"), ("Rol", "Ontwerp, firmware & bouw"), ("Stack", "ESP32 · C/C++ · displays & sensoren · Wi-Fi/Bluetooth · LoRa")],
        "images": [],
        "problem": "Software wordt pas echt interessant als ze de fysieke wereld raakt. Deze experimenten verkennen hoe kleine, goedkope microcontrollers een brug slaan tussen sensoren, schermen en de AI-tools die ik bouw.",
        "features": [
            ("ESP32-prototypes", "Eigen firmware voor microcontrollers met Wi-Fi en Bluetooth: meten, tonen, sturen."),
            ("Displays & interfaces", "Kleine schermen en bedieningselementen die een apparaat begrijpelijk maken zonder handleiding."),
            ("Koppeling met software", "Apparaten die praten met de desktop-tools en assistenten die ik bouw — hardware als verlengstuk van de software."),
            ("Off-grid communicatie", "Experimenten met LoRa-mesh voor communicatie zonder internet of netwerkdekking."),
        ],
        "learned": "Hardware is onvergeeflijk: een verkeerde weerstand of een timing-fout laat zich niet wegrefactoren. Dat dwingt tot klein beginnen, alles meten en pas dan uitbreiden — precies de werkwijze die ik ook in software hanteer.",
        "next": "Generatieve AI",
        "next_slug": "generative-ai",
    },
    {
        "slug": "generative-ai",
        "tag": "GENERATIEVE AI · BEELD & VIDEO",
        "title": "Generatieve AI",
        "intro": "Fotorealistische beelden en video genereren met lokale AI — van prompt en model tot afgewerkt resultaat, volledig op mijn eigen GPU.",
        "meta": [("Type", "Beeld- & videogeneratie"), ("Status", "Doorlopend"), ("Rol", "Prompting, LoRA-training & post-productie"), ("Stack", "ComfyUI · Stable Diffusion / Flux · LoRA · lokale RTX 4070")],
        "images": [("genai-gladiator.jpg", "Cinematische gladiator — fotorealistische AI-generatie, lokaal gerenderd"), ("genai-bust.jpg", "Marmeren buste — dezelfde generatie die je ook ziet als avatar van Agent Thomas op deze site")],
        "problem": "Goede AI-beelden en video zijn geen kwestie van één knop. Het zit in prompting, de juiste modellen kiezen, eigen LoRA's trainen en netjes afwerken. Ik wilde die hele pijplijn lokaal beheersen — zonder cloud-abonnement, met volledige controle over stijl, kwaliteit en privacy.",
        "features": [
            ("Fotorealistische beelden", "Van portretten en sculpturen tot cinematische scènes, met aandacht voor licht, compositie en detail."),
            ("Eigen LoRA-training", "Modellen fijn-afstemmen op een specifieke stijl of personage, getraind op mijn eigen RTX 4070."),
            ("ComfyUI-workflows", "Node-gebaseerde pijplijnen voor herhaalbare, controleerbare resultaten in plaats van willekeurige output."),
            ("Ook video", "Dezelfde workflow uitgebreid naar korte, bewegende beelden — van stilstaand naar clip."),
            ("Volledig lokaal", "Alles draait op mijn eigen machine: geen cloud, geen abonnement, volle controle en privacy."),
        ],
        "learned": "Het verschil tussen ‘een plaatje’ en een bruikbaar resultaat zit in de workflow: prompten, itereren, trainen en afwerken. Lokaal werken dwong me de hele pijplijn te begrijpen in plaats van te leunen op een externe dienst.",
        "next": "Orbit Display",
        "next_slug": "orbit-display",
    },
]

RESULTS = {
    "orbit-display": "Al mijn lokale AI-tools, automatiseringen en security in één navigeerbaar overzicht — volledig lokaal, geen cloud.",
    "victus-control": "Toont in één oogopslag het verschil tussen je bedóelde en je live opstelling — zonder cloud-afhankelijkheid.",
    "thomas-cluster": "4 systemen — Docker, n8n, Ollama en ComfyUI — onder één command center met start- en reconnect-logica.",
    "repo-notebook": "127 repositories beheerd en gecategoriseerd door lokale AI — geen cloud-API, geen abonnement.",
    "repo-notebook-obsidian": "Repo-kennis én een AI-koppeling (MCP) rechtstreeks in je Obsidian-vault, met BRAT-releases.",
    "cyberdash": "Meerdere security-, OSINT- en labtools achter één interface, met een lokale AI-assistent.",
    "llm-wiki": "Bronnen automatisch ingelezen en verbonden in een kennisgraaf met honderden nodes — volledig lokaal.",
    "jarvis": "3 handsfree besturingswijzen — klap, stem én handgebaren — op een lokaal brein.",
    "sirena": "Praat, luistert én voert echte computeracties uit — met een lokaal AI-brein, geen cloud.",
    "embedded": "Eigen firmware, displays en sensoren die rechtstreeks met mijn software praten.",
    "generative-ai": "Fotorealistische beelden en video, met eigen LoRA's getraind op één RTX 4070 — volledig lokaal.",
}

def e(s): return html.escape(s, quote=True)

TEMPLATE = """<!doctype html>
<html lang="nl">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title} — project van Thomas Huybrechts</title>
    <meta name="description" content="{intro}" />
    <meta name="theme-color" content="#f3f0e8" />
    <link rel="canonical" href="https://thomashuybrechts.com/projecten/{slug}.html" />
    <meta property="og:type" content="article" />
    <meta property="og:locale" content="nl_BE" />
    <meta property="og:site_name" content="Thomas Huybrechts" />
    <meta property="og:title" content="{title} — Thomas Huybrechts" />
    <meta property="og:description" content="{intro}" />
    <meta property="og:url" content="https://thomashuybrechts.com/projecten/{slug}.html" />
    <meta property="og:image" content="https://thomashuybrechts.com/assets/og.png" />
    <meta name="twitter:card" content="summary_large_image" />
    <link rel="icon" href="../favicon.svg" type="image/svg+xml" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Manrope:wght@400;500;600;700&family=Playfair+Display:ital,wght@1,600&display=swap" />
    <link rel="stylesheet" href="../styles.css" />
    <script src="../script.js" defer></script>
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "CreativeWork",
      "name": "{title}",
      "description": "{intro}",
      "url": "https://thomashuybrechts.com/projecten/{slug}.html",
      "author": {{ "@type": "Person", "name": "Thomas Huybrechts", "url": "https://thomashuybrechts.com/" }},
      "inLanguage": "nl-BE"
    }}
    </script>
  </head>
  <body class="project-page">
    <a class="skip-link" href="#inhoud">Ga naar de inhoud</a>

    <header class="site-header" id="header">
      <a class="brand" href="../" aria-label="Thomas Huybrechts, naar de startpagina">
        <span class="brand-mark">TH</span>
        <span>Thomas Huybrechts</span>
      </a>
      <nav id="nav" aria-label="Hoofdnavigatie">
        <a href="../#over">Over</a>
        <a href="../#doen">Wat ik doe</a>
        <a href="../#projecten">Projecten</a>
        <a href="../#profiel">Profiel</a>
        <a class="nav-contact" href="../#contact">Contact</a>
      </nav>
      <div class="header-right">
        <button class="sound-toggle" type="button" aria-pressed="false" aria-label="Muziek afspelen">
          <span class="sound-bars" aria-hidden="true"><i></i><i></i><i></i></span>
          <span class="sound-label">Geluid</span>
        </button>
        <audio id="bgm" src="../assets/audio/lemons.mp3" loop preload="none"></audio>
        <button class="menu-toggle" type="button" aria-controls="nav" aria-expanded="false" aria-label="Menu openen">
          <span></span><span></span>
        </button>
      </div>
    </header>

    <main id="inhoud">
      <article>
        <section class="section project-hero{hero_cls}"{hero_style}>
          <a class="back-link" href="../#projecten"><span aria-hidden="true">←</span> Alle projecten</a>
          <p class="work-tag">{tag}</p>
          <h1>{title}</h1>
          <p class="project-intro">{intro}</p>
          <dl class="project-meta">
{meta}
          </dl>
{result_html}          <div class="hero-actions">
            <a class="button button-dark" href="mailto:{email}?subject=Over%20{title_q}">Praat met mij hierover <span aria-hidden="true">↗</span></a>
            <a class="text-link" href="#details">Lees hoe het werkt <span aria-hidden="true">↓</span></a>
          </div>
        </section>
{gallery}{extra}
        <section class="section project-details" id="details">
          <div class="project-columns">
            <div class="reveal">
              <div class="section-label"><span>01</span> HET PROBLEEM</div>
              <p class="project-text">{problem}</p>
            </div>
            <div class="reveal">
              <div class="section-label"><span>02</span> WAT HET DOET</div>
              <dl class="feature-list">
{features}
              </dl>
            </div>
          </div>
          <div class="project-learned reveal">
            <div class="section-label"><span>03</span> WAT IK ERVAN LEERDE</div>
            <blockquote class="learned">{learned}</blockquote>
          </div>
        </section>

        <section class="contact contact-compact" id="contact">
          <div class="contact-copy reveal">
            <p class="eyebrow">INTERESSE?</p>
            <h2>Laten we <em>praten</em>.</h2>
            <p class="contact-sub">Vertel me wat je ervan vindt — of wat je ermee zou willen doen.</p>
            <div class="contact-actions">
              <a class="button button-light" href="mailto:{email}?subject=Over%20{title_q}">Contacteer mij <span aria-hidden="true">↗</span></a>
              <a class="next-project" href="./{next_slug}.html">Volgend project: <b>{next}</b> <span aria-hidden="true">→</span></a>
            </div>
          </div>
        </section>
      </article>
    </main>

    <footer>
      <a class="brand footer-brand" href="../"><span class="brand-mark">TH</span><span>Thomas Huybrechts</span></a>
      <nav class="footer-nav" aria-label="Voetnavigatie">
        <a href="../#over">Over</a>
        <a href="../#doen">Wat ik doe</a>
        <a href="../#projecten">Projecten</a>
        <a href="../#profiel">Profiel</a>
        <a href="https://github.com/TMSHuybrechts" rel="me noopener" target="_blank">GitHub</a>
        <a href="https://www.linkedin.com/in/thomashuybrechts" rel="me noopener" target="_blank">LinkedIn</a>
        <a href="mailto:{email}">E-mail</a>
      </nav>
      <p>© <span id="year"></span> Thomas Huybrechts · Digitaal maker, België · Met nieuwsgierigheid gebouwd.</p>
    </footer>
  </body>
</html>
"""

for p in PROJECTS:
    meta = "\n".join(f'            <div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in p["meta"])
    if p.get("images"):
        imgs = []
        for i, (src, cap) in enumerate(p["images"]):
            imgs.append(f'          <figure class="reveal{" gallery-main" if i == 0 else ""}">\n            <img src="../assets/projects/{src}" alt="{e(cap)}" loading="{"eager" if i == 0 else "lazy"}" decoding="async" />\n            <figcaption>{e(cap)}</figcaption>\n          </figure>')
        gallery = f'\n        <section class="project-gallery" aria-label="Beelden van {e(p["title"])}">\n' + "\n".join(imgs) + "\n        </section>\n"
    else:
        gallery = ""
    extra = ""
    if p.get("extra_partial"):
        extra = "\n" + (PARTIALS / p["extra_partial"]).read_text(encoding="utf-8") + "\n"
    feats = "\n".join(f'                <div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in p["features"])
    _res = RESULTS.get(p["slug"], "")
    result_html = f'          <div class="project-result"><span class="lbl">RESULTAAT</span><p>{e(_res)}</p></div>\n' if _res else ""
    hero_bg = p.get("hero_bg")
    hero_cls = " has-bg" if hero_bg else ""
    hero_style = f' style="--hero-bg:url(../assets/projects/{hero_bg})"' if hero_bg else ""
    out = TEMPLATE.format(
        hero_cls=hero_cls, hero_style=hero_style, result_html=result_html,
        title=e(p["title"]), title_q=p["title"].replace(" ", "%20"), intro=e(p["intro"]), slug=p["slug"], tag=e(p["tag"]),
        email=EMAIL, meta=meta, gallery=gallery, extra=extra, problem=e(p["problem"]), features=feats, learned=e(p["learned"]),
        next=e(p["next"]), next_slug=p["next_slug"],
    )
    (ROOT / "projecten" / f"{p['slug']}.html").write_text(out, encoding="utf-8")
    print("wrote", p["slug"])
