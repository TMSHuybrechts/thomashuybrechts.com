// "FF snel vragen?": stuurt het contactformulier naar de n8n-workflow "Freelance | 01 Lead intake".
// Contract: POST { naam, email, bedrijf, bericht, website }  ->  { ok: true }   (website = honeypot, moet leeg blijven)
// n8n doet de rest: spamcheck (Groq), Notion, bevestigingsmail naar de klant, melding naar Thomas.
(function () {
  const LIVE_ENDPOINT = 'https://pve.tail5e2072.ts.net:8443/webhook/lead'; // Tailscale Funnel op pve: enkel /webhook staat open
  const LAN_ENDPOINT = 'http://192.168.0.246:5678/webhook/lead';
  const TIMEOUT_MS = 15000;
  const MAIL = 'hey@thomashuybrechts.com';

  const form = document.getElementById('ff-vragen');
  if (!form) return;

  const params = new URLSearchParams(location.search);
  const isLocal = ['localhost', '127.0.0.1', '[::1]', ''].includes(location.hostname);
  const mode = isLocal && params.has('mock') ? 'mock' : 'live'; // ?mock = lokaal doen alsof, er vertrekt niets
  const ENDPOINT = isLocal ? LAN_ENDPOINT : LIVE_ENDPOINT;

  // Openen vanuit de ballon aan het portret of de knop in het contactblok; sluiten met ×, Esc of klik naast de ballon
  const dialog = document.getElementById('ff-vragen-dialog');
  let opener = null;
  function openAsk(e) {
    opener = e.currentTarget;
    if (typeof dialog.showModal === 'function') dialog.showModal();
    else dialog.setAttribute('open', '');
    document.body.classList.add('ask-lock');
    (form.classList.contains('is-sent') ? form.querySelector('[data-ask-close]') : form.elements.naam).focus();
  }
  function closeAsk() {
    if (!dialog.open) return;
    if (typeof dialog.close === 'function') dialog.close();
    else { dialog.removeAttribute('open'); dialog.dispatchEvent(new Event('close')); }
  }
  document.querySelectorAll('[data-ask-open]').forEach(btn => btn.addEventListener('click', openAsk));
  form.querySelector('[data-ask-close]').addEventListener('click', closeAsk);
  dialog.addEventListener('click', e => { if (e.target === dialog) closeAsk(); });
  dialog.addEventListener('close', () => {
    document.body.classList.remove('ask-lock');
    if (opener) opener.focus();
  });

  const status = form.querySelector('.ask-status');
  const button = form.querySelector('.ask-send');
  const EMAIL_RE = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

  const RULES = {
    naam: v => v ? '' : 'Hoe mag ik je noemen?',
    email: v => !v ? 'Je e-mailadres, zodat ik kan antwoorden.' : EMAIL_RE.test(v) ? '' : 'Dit e-mailadres klopt niet helemaal.',
    bericht: v => v.length >= 10 ? '' : 'Vertel in een paar woorden wat je wil oplossen.',
  };

  function setError(field, message) {
    const label = field.closest('.ask-field');
    let error = label.querySelector('.ask-error');
    if (!message) {
      field.removeAttribute('aria-invalid');
      if (error) error.remove();
      return;
    }
    if (!error) {
      error = document.createElement('span');
      error.className = 'ask-error';
      error.id = 'err-' + field.name;
      label.appendChild(error);
    }
    error.textContent = message;
    field.setAttribute('aria-invalid', 'true');
    field.setAttribute('aria-describedby', error.id);
  }

  function validate() {
    let first = null;
    for (const [name, rule] of Object.entries(RULES)) {
      const field = form.elements[name];
      const message = rule(field.value.trim());
      setError(field, message);
      if (message && !first) first = field;
    }
    if (first) first.focus();
    return !first;
  }

  // Foutmelding verdwijnt zodra het veld goed is
  form.addEventListener('input', e => {
    const rule = RULES[e.target.name];
    if (rule && e.target.hasAttribute('aria-invalid')) setError(e.target, rule(e.target.value.trim()));
  });

  function showSent(naam) {
    form.classList.add('is-sent');
    status.textContent = `Top${naam ? ', ' + naam : ''}! Ik heb je vraag. Je krijgt binnen twee werkdagen antwoord, kijk ook even in je mailbox.`;
    status.focus();
  }

  function showFailed() {
    status.innerHTML = '';
    status.append('Dat lukte even niet. Mail me gerust op ');
    const link = document.createElement('a');
    link.href = 'mailto:' + MAIL;
    link.textContent = MAIL;
    status.append(link, '.');
  }

  form.addEventListener('submit', async e => {
    e.preventDefault();
    if (button.disabled || !validate()) return;

    const data = Object.fromEntries(['naam', 'email', 'bedrijf', 'bericht', 'website'].map(k => [k, form.elements[k].value.trim()]));
    button.disabled = true;
    status.textContent = 'Even versturen...';

    if (mode === 'mock') {
      setTimeout(() => showSent(data.naam.split(' ')[0]), 700);
      return;
    }

    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);
    try {
      const res = await fetch(ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
        signal: controller.signal,
      });
      if (!res.ok) throw new Error('HTTP ' + res.status);
      showSent(data.naam.split(' ')[0]);
    } catch (err) {
      console.warn('[ff-vragen] versturen mislukt:', err);
      button.disabled = false;
      showFailed();
    } finally {
      clearTimeout(timer);
    }
  });
})();
