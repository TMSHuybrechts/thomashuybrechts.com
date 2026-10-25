// Business OS-productsite: verschijnen bij scrollen, demo-tabs en de wachtlijst.
// De wachtlijst gebruikt dezelfde n8n-webhook als "FF snel vragen?" (Freelance | 01 Lead intake),
// met "Wachtlijst Business OS" vooraan in het bericht zodat het in Notion herkenbaar is.
document.documentElement.classList.add('js');

(function reveal() {
  const items = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window)) { items.forEach(el => el.classList.add('visible')); return; }
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -8% 0px' });
  items.forEach(el => io.observe(el));
})();

(function tabs() {
  const list = document.querySelector('.demo-tabs');
  if (!list) return;
  const tabs = [...list.querySelectorAll('[role="tab"]')];
  function select(tab) {
    tabs.forEach(t => {
      const on = t === tab;
      t.setAttribute('aria-selected', on);
      t.tabIndex = on ? 0 : -1;
      document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
    });
  }
  tabs.forEach((t, i) => {
    t.addEventListener('click', () => select(t));
    t.addEventListener('keydown', e => {
      const step = { ArrowRight: 1, ArrowLeft: -1 }[e.key];
      if (!step) return;
      e.preventDefault();
      const next = tabs[(i + step + tabs.length) % tabs.length];
      select(next);
      next.focus();
    });
  });
})();

(function waitlist() {
  const LIVE_ENDPOINT = 'https://pve.tail5e2072.ts.net:8443/webhook/lead'; // Tailscale Funnel op pve: enkel /webhook staat open
  const LAN_ENDPOINT = 'http://192.168.0.246:5678/webhook/lead';
  const TIMEOUT_MS = 15000;
  const MAIL = 'hey@thomashuybrechts.com';
  const EMAIL_RE = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

  const form = document.getElementById('wl-form');
  if (!form) return;
  const isLocal = ['localhost', '127.0.0.1', '[::1]', ''].includes(location.hostname);
  const mock = isLocal && new URLSearchParams(location.search).has('mock'); // ?mock = lokaal doen alsof, er vertrekt niets
  const ENDPOINT = isLocal ? LAN_ENDPOINT : LIVE_ENDPOINT;
  const status = form.querySelector('.wl-status');
  const button = form.querySelector('button[type="submit"]');

  // "Kies Pro" e.d. vult meteen het pakket in
  document.querySelectorAll('[data-plan]').forEach(a => a.addEventListener('click', () => { form.elements.pakket.value = a.dataset.plan; }));

  const RULES = {
    naam: v => v ? '' : 'Hoe mag ik je noemen?',
    email: v => !v ? 'Je e-mailadres, zodat ik je kan verwittigen.' : EMAIL_RE.test(v) ? '' : 'Dit e-mailadres klopt niet helemaal.',
  };

  function setError(field, message) {
    const label = field.closest('.wl-field');
    let error = label.querySelector('.wl-error');
    if (!message) { field.removeAttribute('aria-invalid'); if (error) error.remove(); return; }
    if (!error) {
      error = document.createElement('span');
      error.className = 'wl-error';
      error.id = 'wl-err-' + field.name;
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

  form.addEventListener('input', e => {
    const rule = RULES[e.target.name];
    if (rule && e.target.hasAttribute('aria-invalid')) setError(e.target, rule(e.target.value.trim()));
  });

  function done(naam) {
    form.classList.add('is-sent');
    status.textContent = `Je staat op de lijst${naam ? ', ' + naam : ''}. Je hoort het als eerste zodra Business OS opengaat.`;
    status.focus();
  }

  function failed() {
    status.innerHTML = '';
    status.append('Dat lukte even niet. Mail me gerust op ');
    const link = document.createElement('a');
    link.href = 'mailto:' + MAIL + '?subject=Wachtlijst%20Business%20OS';
    link.textContent = MAIL;
    status.append(link, '.');
  }

  form.addEventListener('submit', async e => {
    e.preventDefault();
    if (button.disabled || !validate()) return;
    const v = k => form.elements[k].value.trim();
    const note = v('bericht');
    const data = {
      naam: v('naam'),
      email: v('email'),
      bedrijf: v('bedrijf'),
      bericht: `Wachtlijst Business OS. Ik wil graag toegang zodra het beschikbaar is. Pakket: ${v('pakket')}.${note ? ' ' + note : ''}`,
      website: v('website'),
    };
    button.disabled = true;
    status.textContent = 'Even versturen...';
    const first = data.naam.split(' ')[0];
    if (mock) { setTimeout(() => done(first), 600); return; }

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
      done(first);
    } catch (err) {
      console.warn('[wachtlijst] versturen mislukt:', err);
      button.disabled = false;
      failed();
    } finally {
      clearTimeout(timer);
    }
  });
})();
