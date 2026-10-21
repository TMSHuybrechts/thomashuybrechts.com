### 0.1 AI Business OS

**In één zin:** AI Business OS is mijn eigen besturingssysteem voor een freelancezaak: het zoekt bedrijven die hulp kunnen gebruiken, meet hun website, houdt de opvolging bij en verstuurt mails die de Belgische regels respecteren.

- **Wat is het?** Een webapplicatie die ik zelf bouwde om mijn freelancewerk te runnen. In plaats van tien losse tools (een lijstje in Excel, een CRM, een mailprogramma, een agenda vol herinneringen) zit alles in één scherm, verdeeld over "afdelingen": leads zoeken, verkoop, outreach, mail en opdrachten. Elke afdeling toont met een kleur hoe het ervoor staat, van "draait smooth" tot "hier moet je nu iets aan doen". Het is een SaaS in wording: vandaag gebruik ik het zelf, het is gebouwd om later ook voor anderen te draaien.
- **Hoe werkt het technisch?**
  - **Lead Hunter:** zoekt per gemeente en doelgroep bedrijven op via OpenStreetMap en vult ze aan met het ondernemingsnummer uit de KBO.
  - **Website-meting:** bezoekt de homepage en meet wat echt meetbaar is: is de site bereikbaar, beveiligd (https), snel, mobielvriendelijk, staan er contactgegevens op, kun je online een afspraak maken, werken de interne links. Niets wordt verzonnen: geen meting is geen punten.
  - **Kansscore 0-100:** hoe groter de concrete verbeterkans, hoe hoger de score. Filialen van ketens zakken weg, want die beslissen zelden zelf over hun website.
  - **Verkoop:** een bord met kolommen (nieuw, gecontacteerd, in gesprek, gewonnen) waar je leads naartoe sleept.
  - **Outreach met de Belgische regels ingebouwd:** alleen algemene adressen (info@, contact@) van vennootschappen, nooit een persoonlijk adres of een eenmanszaak zonder toestemming. Elke mail heeft een afmeldlink, er is een daglimiet en de opvolging stopt vanzelf bij een antwoord, een afmelding of een adres dat niet werkt.
  - **Mail Hub:** verstuurt via het eigen domein en leest de inbox mee om antwoorden en afmeldingen te herkennen.
  - **Opdrachtenradar:** scant openbare freelance-opdrachten (onder meer uit de n8n-community) en zet ze klaar om op te volgen.
  - Gebouwd in Node.js met een SQLite-database, zelf gehost en met tests voor elke regel die mis kan gaan (geen dubbele mail, nooit mailen na een afmelding).
- **Wat kun je ermee bouwen?**
  - Een vaste weekroutine: maandag scannen, dinsdag de beste leads overnemen, de rest van de week opvolgen.
  - Campagnes per doelgroep, bijvoorbeeld "kapsalons zonder online afspraken" of "bedrijven met een onbeveiligde site".
  - Een eerlijk eerste contact: elke mail noemt één gemeten probleem van die zaak, in gewone taal.
- **Commercieel gebruik:** voor mezelf scheelt het uren zoekwerk per week en zorgt het dat geen enkele lead tussen de plooien valt. Als product mikt het op freelancers en kleine bureaus die lokaal klanten zoeken: een abonnement per gebruiker, met de Belgische mailregels als verschil met buitenlandse tools die daar geen rekening mee houden.
- **Sterke combinaties:** automatisch nieuwe klanten vinden (4.11) + je klantenbestand slim opbouwen (4.10) + e-mails automatisch verwerken (4.14) + GDPR (9.13). Over het verdienmodel zelf: Software as a Service (10.1).
- **Belangrijkste 20%:**
  - **Meten, niet raden:** een lead zonder gemeten probleem is geen lead.
  - **Wettelijk by design:** de regels zitten in de software, niet in je geheugen.
  - **Kwaliteit boven volume:** tien goede mails per dag halen meer op dan honderd algemene, en houden je domein uit de spam.
  - **Altijd een mens aan de knop:** een campagne vertrekt pas na goedkeuring.
- **Praktijkvoorbeeld (echte meting):** een scan in Meerhout over vijf doelgroepen leverde in minder dan een minuut 20 kandidaten op. Acht daarvan hadden geen website bekend, vijf hadden een site die niet meer werkte (domein verlopen, server dood of foutpagina) en zeven een werkende site. Bij een test in Geel vond de e-mailzoeker bij 13 van de 18 bedrijven met een werkende site een algemeen adres. De les: de beste kansen (geen of een kapotte site) bel je, de rest mail je.
