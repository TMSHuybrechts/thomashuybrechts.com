# thomashuybrechts.com

Een lichte, responsieve persoonlijke website voor Thomas Huybrechts: positionering, diensten, projecten, werkwijze, profiel en contact.

## Lokaal bekijken

Open `index.html` rechtstreeks in een browser, of start vanuit deze map een lokale server:

```powershell
python -m http.server 8080
```

Bezoek daarna `http://localhost:8080`.

## Nog aan te vullen (placeholders)

Deze bestanden zijn nu tijdelijke placeholders — vervang ze door echte beelden/bestanden met **exact dezelfde bestandsnaam** (of pas de verwijzing in de HTML aan):

| Bestand | Wat | Waar gebruikt |
|---|---|---|
| `assets/projects/obsidian-1.svg`, `obsidian-2.svg` | Screenshots Obsidian-plugin | `projecten/repo-notebook-obsidian.html` |
| `assets/projects/sirena-1.svg`, `sirena-2.svg` | Screenshots Sirena | `projecten/sirena.html` |
| `assets/projects/embedded-1.svg`, `embedded-2.svg` | Foto's ESP32-prototypes | `projecten/embedded.html` |
| LinkedIn-URL | Nu `linkedin.com/in/thomas-huybrechts-a14277105` (gok) — vervang door je echte profiel-URL in `index.html`, `docs/build-projects.py` (daarna `python3 docs/build-projects.py`) en de JSON-LD (`sameAs`). GitHub (`github.com/TMSHuybrechts`) klopt al. | profiel, contact, footer |

De Repo Notebook-screenshots (`assets/projects/repo-notebook-1.webp` en `-2.webp`) het portret (`assets/thomas.jpg`, uitsnede van je composietbeeld; het volledige beeld staat in `assets/thomas-composite.jpg`) en het cv (`assets/thomas-huybrechts-cv.pdf`, bron: `docs/cv/cv.html`) zijn echt.

## Structuur

- `index.html` — alle teksten, secties en structured data (JSON-LD onderaan `<head>`)
- `styles.css` — kleuren, typografie, layout, mobiel menu
- `script.js` — scroll-onthulling, sticky header, mobiel menu, actieve navigatie, e-mail kopiëren
- `projecten/*.html` — vier projectpagina's, gegenereerd met `python3 docs/build-projects.py` (teksten, meta en beelden staan in dat script)
- `404.html` — foutpagina (Cloudflare Pages/Netlify/Vercel pikken deze automatisch op; GitHub Pages ook)
- `robots.txt`, `sitemap.xml` — zoekmachines
- `assets/audio/lemons.mp3` — achtergrondmuziek achter de knop "Geluid" in de header (staat uit tot de bezoeker klikt; volume 35 %, loopt)
- `assets/og.png` — social preview (1200×630) voor LinkedIn, WhatsApp, X, …
- `assets/arena.webp` + `assets/arena-640.webp` — arena-beeld (desktop + mobiel); `arena.png` is het origineel en wordt niet geladen

## Aanpassen

- Contactadres: zoek in `index.html` naar `hey@thomashuybrechts.com` (komt ook voor in de JSON-LD en de demo-knoppen bij projecten)
- Projecten: sectie `#projecten`; de knop per project opent een e-mail met vooraf ingevuld onderwerp
- Diensten: sectie `#doen`
- Werkwijze: sectie `#werkwijze`
- Sociale links (GitHub, LinkedIn): voeg toe in `.footer-nav` en in de JSON-LD onder `"sameAs": [...]`

## Publiceren (GitHub Pages, gratis)

1. Maak op GitHub een nieuwe **publieke** repository, bv. `thomashuybrechts.com`.
2. Zet de inhoud van deze map in de root van de repo (niet in een submap) en push naar `main`. `CNAME` en `.nojekyll` zitten er al bij.
3. Repo → **Settings → Pages** → Source: *Deploy from a branch* → Branch `main` / `/ (root)` → Save.
4. Bij **Custom domain** staat `thomashuybrechts.com` (uit `CNAME`). Vink **Enforce HTTPS** aan zodra het certificaat er is (kan tot een uur duren).
5. Bij je domeinregistrar (DNS-beheer van thomashuybrechts.com):
   - 4 × **A**-record voor `@` → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - **CNAME** voor `www` → `tmshuybrechts.github.io`
   - Verwijder eventuele oude A/AAAA-records voor `@` en `www` (bv. een parkeerpagina van de registrar).
6. Wacht op DNS (meestal 10–60 min). Controleer op https://thomashuybrechts.com en https://www.thomashuybrechts.com.

Updaten = bestanden aanpassen en pushen; binnen een minuut staat het live.

Alternatieven: Cloudflare Pages of Netlify (map slepen, gratis), of de webhosting van je registrar (bestanden via FTP/bestandsbeheer in de `www`-map zetten). Controleer na publicatie de social preview via bv. opengraph.xyz en de structured data via de Rich Results Test van Google.

## Repo Notebook branding
De productsite in `repo-notebook/` deelt de papier-, inkt- en limoenkleuren en typografie van de hoofdsite. Zie [merkafspraken](docs/product/repo-notebook-branding.md). De hoofdsite en desktop-app behouden hun bestaande gedrag.
