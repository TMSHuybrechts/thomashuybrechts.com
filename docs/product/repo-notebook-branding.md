# Repo Notebook — Thomas Huybrechts merkfamilie

## Product en afbakening
De bestaande Engelstalige Repo Notebook-productsite presenteert de desktop-app aan ontwikkelaars en onderzoekers. De persoonlijke hoofdsite blijft ongewijzigd. De productsite behoudt haar inhoud, routes, app-screenshots en downloadbestemming.

## Visuele identiteit
- Warme papierkleur `#f3f0e8`, inkt `#171816`, accent `#d7ff43`, tekstgrijs `#676861`.
- Manrope voor lopende tekst en titels, Playfair Display cursief voor nadruk, DM Mono voor labels; dezelfde fonts als de hoofdsite, met systeemfallbacks.
- Merknaam met een eigen RN-monogram en zichtbare vermelding van Thomas Huybrechts.
- Editorial opbouw: grote koppen, dunne scheidingslijnen, veel ademruimte en een productbeeld op een contrasterende ondergrond. Geen blauwe gradients of neon-gloed.
- Screenshots blijven echte productbeelden; hun donkere app-interface wordt niet herkleurd.

## Technische afspraken
Statische HTML en CSS, zonder nieuwe runtime-afhankelijkheden. Navigatie blijft op mobiel bereikbaar. Focusindicatoren, skiplink, reduced-motion en lazy loading blijven ondersteund. Voorbeeldcijfers worden als screenshotvoorbeelden aangeduid, niet als actuele gebruikersstatistieken.

## Controle
Controleer desktop en smalle mobiele weergave op overloop, afgebroken tekst, beeldladen, ankerlinks en terugnavigatie. Publiceren is gescheiden van lokaal ontwikkelen en controleren.

## Geverifieerde eigenschappen
Desktop (1280 px) en mobiel (390 px) hebben geen horizontale documentoverloop. De zeven afbeeldingen laden, alle interne ankerdoelen bestaan en de Run-link is met een echte klik getest. Geen browserconsolefouten waargenomen. De smallere 320px-controle werd onderbroken door een browser-time-out en is niet als geslaagd geregistreerd. De bronwijzigingen beperken zich tot de productsite en de bijbehorende documentatie.
