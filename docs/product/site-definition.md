# Websitedefinitie

## Doel

`thomashuybrechts.com` presenteert Thomas als een nieuwsgierige digitale maker. De site combineert een compact online cv met een actueel overzicht van onderwerpen en projecten waar hij mee bezig is.

## Doelgroep

- Mensen die Thomas professioneel of creatief leren kennen
- Potentiële samenwerkingspartners
- Werkgevers, opdrachtgevers en andere makers

## Inhoudsarchitectuur

1. **Introductie:** naam, positionering, drie bewijspunten en kernboodschap.
2. **Over:** portret, motivatie, manier van denken en operationele/leidinggevende achtergrond (chef en teamlead).
3. **Wat ik doe:** drie inzetbare domeinen (AI-agents & automatisering, producten & prototypes, hardware & embedded) met concrete voorbeelden.
4. **Waar ik mee bezig ben:** vier concrete projecten: Repo Notebook, de bijbehorende Obsidian-plugin, Sirena en embedded experimenten — elk met een eigen detailpagina (screenshots, probleem, functies, geleerde lessen, demo-knop).
5. **Arena-manifest:** een visueel statement over bouwen, testen en verbeteren.
6. **Hoe ik werk:** vier stappen (begrijpen, bouwen, testen, verbeteren).
7. **Profiel:** focus, sterktes, gereedschap, welk werk Thomas zoekt, basisinformatie, cv-download en GitHub/LinkedIn.
8. **Contact:** directe e-maillink, kopieerbaar adres en verwachtingsmanagement.

## Ontwerpbeslissingen

- **Richting:** redactioneel-technisch; warm papier als basis met zwarte typografie en scherpe kleuraccenten.
- **Herkenbaar element:** een interactieve, orbitale illustratie die ideeën, AI, code en apparaten rond de stap van idee naar werkend product plaatst.
- **Cinematisch statement:** het aangeleverde gladiatorbeeld wordt als redactionele metafoor gebruikt en expliciet gekoppeld aan de werkprincipes bouwen, testen en verbeteren. Het beeld wordt niet als portret gepresenteerd.
- **Typografie:** Manrope voor heldere moderne tekst, DM Mono voor technische labels en Playfair Display Italic voor een persoonlijk accent.
- **Gedrag:** subtiele scroll-onthulling, een horizontale ticker en een lichte pointerreactie in de hero.
- **Toegankelijkheid:** semantische secties, toetsenbordfocus, skiplink, voldoende contrast en ondersteuning voor `prefers-reduced-motion`.
- **Techniek:** dependencyvrije statische HTML, CSS en JavaScript voor snelle hosting en eenvoudig onderhoud.
- **Navigatie:** sticky header met blur, actieve sectie-indicator en een volwaardig mobiel menu.
- **Vindbaarheid & delen:** canonical, Open Graph/Twitter-tags met eigen social preview (`assets/og.png`), JSON-LD (Person + WebSite), `robots.txt`, `sitemap.xml` en een 404-pagina.

## Contentbeleid

De site vermijdt onbevestigde werkgevers, opleidingen, jaartallen en functietitels. Feitelijke loopbaangegevens kunnen later als aparte ervaringssectie worden toegevoegd zodra de definitieve cv-inhoud beschikbaar is.

## Uitgelichte projecten

- **Repo Notebook:** een visuele kennisomgeving voor het verzamelen en verbinden van GitHub-repositories, met lokale AI, Oogst en suggesties.
- **Repo Notebook voor Obsidian:** een gekoppelde Obsidian-plugin, verspreid via BRAT en voorzien van MCP-integratie.
- **Sirena:** een lokale Vlaamse desktopassistent met stem, avatar en computeracties.
- **Embedded experimenten:** firmware en interactieve hardware rond ESP32, schermen en microcontrollers.
