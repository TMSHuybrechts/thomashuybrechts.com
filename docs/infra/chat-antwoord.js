// n8n Code-node "Antwoord": haalt het antwoord uit de Groq-respons en herkent een lead (e-mailadres in het gesprek).
const FALLBACK = 'Dat lukt nu even niet. Mail me op hey@thomashuybrechts.com, dan antwoord ik zelf.';
const prep = $('Voorbereiden').first().json;
const res = $input.first().json || {};

const blocked = prep.blocked || '';
const fromModel = ((res.choices && res.choices[0] && res.choices[0].message && res.choices[0].message.content) || '').trim();
const reply = blocked || fromModel || FALLBACK;

const email = (prep.message.match(/[\w.+-]+@[\w-]+(\.[\w-]+)+/) || [])[0] || '';
const transcript = [
  ...prep.history.map(h => (h.role === 'assistant' ? 'Bot: ' : 'Bezoeker: ') + h.text),
  'Bezoeker: ' + prep.message,
  'Bot: ' + reply,
].join('\n\n');

return [{ json: { reply, lead: Boolean(email), email, brand: prep.brand, transcript } }];
