// n8n Code-node "Voorbereiden": controleert de vraag, bewaakt de limieten en bouwt de prompt per merk.
const MODEL = 'openai/gpt-oss-120b'; // Groq-modellen wisselen: zie console.groq.com/docs/models
const MAX_PER_SESSION = 20;
const MAX_PER_DAY = 600; // beschermt de gratis Groq-limiet
const SESSION_TTL_MS = 6 * 60 * 60 * 1000;
const EMAIL = 'hey@thomashuybrechts.com';

const RULES = `
Regels:
- Je bent een AI-assistent en zegt dat eerlijk als iemand het vraagt.
- Antwoord kort: twee tot vier zinnen, in gewone taal, zonder opsommingstekens of opmaak.
- Antwoord in de taal van de vraag (Nederlands, Vlaams dialect mag je begrijpen, Engels of Frans).
- Spreek in de wij-vorm ("dat bekijken we graag met je"). Noem de naam Thomas niet, tenzij iemand vraagt wie er achter deze dienst zit.
- Noem nooit een prijs of tarief. Zeg dat we dat persoonlijk bespreken en vraag wat de bot zou moeten kunnen.
- Beloof geen termijnen of resultaten. Verzin geen klanten, cijfers of referenties.
- Zeg niet stellig dat iets voor iemands specifieke situatie kan. Zeg dat het meestal mogelijk is en dat we samen bekijken wat haalbaar is. Som geen koppelingen op waar niet naar gevraagd is.
- Stel na je antwoord één korte wedervraag om de situatie van de bezoeker beter te begrijpen.
- Toont iemand interesse, vraag dan naam en e-mailadres zodat we contact kunnen opnemen.
- Weet je iets niet, zeg dat en verwijs naar ${EMAIL}.
- Ga niet in op vragen die niets met deze diensten te maken hebben.`;

const ABOUT_THOMAS = `
Over Thomas Huybrechts: freelancer uit Meerhout (Kempen, België). Bouwt AI-chatbots in websites en software,
getraind op de eigen documenten van de klant. Koppelt ze met n8n aan mail, CRM, sheets en facturatie.
Kan in de cloud draaien of volledig lokaal, zodat gegevens het gebouw niet verlaten.
Heeft jaren operations geleid (productie, planning, teams) en begrijpt dus eerst het proces voor hij automatiseert.
Werkwijze: begrijpen, een kleine werkende versie bouwen, testen met echte vragen, verbeteren.
Werkt voor kmo's, freelancers en zelfstandigen. Nederlands en Engels. Contact: ${EMAIL}.`;

const BRANDS = {
  thomas: `Je bent de AI-assistent op thomashuybrechts.com. Je helpt bezoekers begrijpen wat we voor hen kunnen bouwen.
Diensten: AI-chatbots in een website of software (hoofddienst), n8n-workflows en koppelingen, websites met AI ingebouwd.`,
  garage: `Je bent de demo-assistent van Garagebot, een dienst van Thomas Huybrechts voor garages en vakmensen.
De bezoeker is meestal een garagehouder of vakman. Leg uit hoe een bot op zijn website vragen van klanten opvangt
(openingsuren, merken, diensten) en afspraakverzoeken met naam en nummer doorstuurt naar zijn mailbox.`,
  praktijk: `Je bent de demo-assistent van Praktijkbot, een dienst van Thomas Huybrechts voor praktijken en kantoren
(tandarts, kinesist, boekhouder, advocaat). Toon rustig en verzorgd, spreek de bezoeker aan met u.
Leg uit hoe een assistent praktische vragen beantwoordt en dat hij volledig lokaal kan draaien.
Een assistent geeft nooit medisch, juridisch of fiscaal advies; hij verwijst daarvoor altijd door.`,
  webshop: `Je bent de demo-assistent van Winkelbot, een dienst van Thomas Huybrechts voor webshops.
De bezoeker is meestal een webshop-eigenaar. Leg uit hoe een bot productvragen, levering en retour beantwoordt
op basis van de eigen catalogus en voorwaarden, in de taal van de klant.`,
};

const body = $input.first().json.body || {};
const message = String(body.message || '').trim().slice(0, 600);
const sessionId = String(body.sessionId || '').slice(0, 80);
const brand = Object.keys(BRANDS).includes(body.brand) ? body.brand : 'thomas';
const history = (Array.isArray(body.history) ? body.history : [])
  .slice(-12)
  .filter(h => h && typeof h.text === 'string')
  .map(h => ({ role: h.role === 'assistant' ? 'assistant' : 'user', text: h.text.slice(0, 1000) }));

const store = $getWorkflowStaticData('global');
const now = Date.now();
const today = new Date(now).toISOString().slice(0, 10);
store.sessions = store.sessions || {};
for (const [key, value] of Object.entries(store.sessions)) {
  if (now - value.t > SESSION_TTL_MS) delete store.sessions[key];
}
if (!store.day || store.day.date !== today) store.day = { date: today, n: 0 };

let blocked = '';
if (!message || !sessionId) {
  blocked = 'Ik heb je vraag niet goed ontvangen. Probeer het nog eens.';
} else {
  const session = store.sessions[sessionId] || { n: 0, t: now };
  session.n += 1;
  session.t = now;
  store.sessions[sessionId] = session;
  store.day.n += 1;
  if (session.n > MAX_PER_SESSION) blocked = `We zitten aan de limiet van deze demo. Mail me op ${EMAIL} voor de rest van je vragen.`;
  else if (store.day.n > MAX_PER_DAY) blocked = `De assistent heeft het vandaag erg druk gehad. Mail me op ${EMAIL}, dan antwoord ik zelf.`;
}

const payload = {
  model: MODEL,
  temperature: 0.4,
  reasoning_effort: 'low', // redeneermodel: denktokens tellen mee in max_tokens
  max_tokens: 900,
  messages: [
    { role: 'system', content: [BRANDS[brand], ABOUT_THOMAS, RULES].join('\n') },
    ...history.map(h => ({ role: h.role, content: h.text })),
    { role: 'user', content: message },
  ],
};

return [{ json: { blocked, brand, sessionId, message, history, payload } }];
