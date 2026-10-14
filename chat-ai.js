// AI-chat: praat met de n8n-webhook. Geen sleutels in de frontend — die zitten in n8n.
// Contract: POST { brand, sessionId, message, history: [{ role, text }] }  ->  { reply: "..." }
// brand = data-brand op <html> (merksites); n8n kiest daarmee het juiste kennisdocument.
(function () {
  const LIVE_ENDPOINT = 'https://pve.tail5e2072.ts.net:8443/webhook/chat'; // Tailscale Funnel op pve: enkel /webhook staat open, het n8n-beheer niet
  const LAN_ENDPOINT = 'http://192.168.0.246:5678/webhook/chat'; // n8n op pve, enkel bereikbaar op het thuisnetwerk
  const TIMEOUT_MS = 20000;
  const MAX_MESSAGES = 20; // per sessie; n8n dwingt dezelfde grens af
  const MAX_HISTORY = 12;
  const FALLBACK = 'Dat lukt nu even niet. Mail me op hey@thomashuybrechts.com, dan antwoord ik zelf.';
  const LIMIT_REACHED = 'We zitten aan de limiet van deze demo. Mail me op hey@thomashuybrechts.com voor de rest van je vragen.';

  const isLocal = ['localhost', '127.0.0.1', '[::1]', ''].includes(location.hostname);
  const wantMock = new URLSearchParams(location.search).has('mock'); // ?mock = vaste voorbeeldantwoorden, enkel lokaal
  const ENDPOINT = isLocal ? LAN_ENDPOINT : LIVE_ENDPOINT;
  const mode = isLocal && wantMock ? 'mock' : ENDPOINT ? 'live' : 'offline';

  let sessionId = '';
  try {
    sessionId = sessionStorage.getItem('th_chat_sid') || '';
    if (!sessionId) {
      sessionId = (crypto.randomUUID && crypto.randomUUID()) || String(Date.now()) + Math.random().toString(16).slice(2);
      sessionStorage.setItem('th_chat_sid', sessionId);
    }
  } catch { sessionId = String(Date.now()); }

  let sent = 0;

  // Enkel voor lokale preview zolang de backend niet bestaat: vaste voorbeeldantwoorden, nooit op de live site.
  const MOCK = [
    [['kost', 'prijs', 'tarief', 'price'], 'Dat hangt af van wat de bot moet kunnen: enkel vragen beantwoorden, of ook afspraken inplannen en leads doorsturen? Een prijs geef ik niet zelf, die bespreken we persoonlijk. Wat verkoop je in je webshop, en welke vragen krijg je het vaakst?'],
    [['english', 'do you', 'can you'], 'Yes, I answer in English as well. We work in Dutch and English. What would you like the chatbot to do for your business?'],
    [['data', 'privacy', 'amerika', 'lokaal', 'gdpr'], 'Dat kan. De bot kan volledig lokaal draaien, op een server bij jou of in België. Dan verlaat geen enkele vraag je gebouw. Dat is iets trager dan de cloud, maar voor dokters, boekhouders of advocaten vaak de juiste keuze.'],
    [['garage', 'telefoon', 'bellen', 'afspraak'], 'Ja. Een bot op je site kan de vragen opvangen waarvoor mensen nu bellen: openingsuren, of je een bepaald merk doet, wanneer er plaats is. Bij een afspraakvraag stuurt hij naam en nummer naar je mailbox. Welke vragen krijg je het vaakst aan de telefoon?'],
    [['producten', 'documenten', 'hoe lang', 'bouwen'], 'Twee antwoorden. Eén: ja, de bot leest je eigen productinfo en documenten en antwoordt daaruit. Twee: een eerste werkende versie staat er meestal binnen een week of twee, afhankelijk van hoe verspreid je informatie zit. Waar staat je productinfo nu?'],
  ];
  const mockReply = text => {
    const q = text.toLowerCase();
    const hit = MOCK.find(([kws]) => kws.some(k => q.includes(k)));
    return hit ? hit[1] : 'Ik ben de AI-assistent van deze site. Vertel eens: wat vragen je klanten of collega\'s het vaakst, en waar verlies je daar nu tijd mee?';
  };

  async function send(message, history) {
    if (sent >= MAX_MESSAGES) return { reply: LIMIT_REACHED, ok: false };
    sent += 1;

    if (mode === 'offline') return { reply: FALLBACK, ok: false };
    if (mode === 'mock') {
      await new Promise(r => setTimeout(r, 900));
      return { reply: mockReply(message), ok: true };
    }

    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), TIMEOUT_MS);
    try {
      const res = await fetch(ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ brand: document.documentElement.dataset.brand || 'thomas', sessionId, message, history: (history || []).slice(-MAX_HISTORY) }),
        signal: ctrl.signal,
      });
      if (!res.ok) throw new Error('HTTP ' + res.status);
      const data = await res.json();
      const reply = typeof data.reply === 'string' ? data.reply.trim() : '';
      if (!reply) throw new Error('leeg antwoord');
      return { reply, ok: true };
    } catch (err) {
      console.warn('[chat-ai]', err);
      return { reply: FALLBACK, ok: false };
    } finally {
      clearTimeout(timer);
    }
  }

  window.TH_AI = { send, mode };
})();
