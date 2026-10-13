// Vergelijkingspagina: één vraag gaat naar de gescripte gids (window.TH_SCRIPTED uit script.js)
// én naar de AI-chat (window.TH_AI uit chat-ai.js).
(function () {
  const scripted = window.TH_SCRIPTED;
  const ai = window.TH_AI;
  const form = document.getElementById('duel-form');
  if (!scripted || !ai || !form) return;

  const input = document.getElementById('duel-q');
  const submit = form.querySelector('button');
  const tries = [...document.querySelectorAll('.try')];
  const logClassic = document.getElementById('log-classic');
  const logAi = document.getElementById('log-ai');
  const chipsEl = document.getElementById('chips-classic');
  const aiNote = document.getElementById('ai-note');
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const history = [];

  const NOTES = {
    mock: 'Lokale preview · voorbeeldantwoorden, de AI-backend is nog niet aangesloten',
    offline: 'De AI-backend wordt nog aangesloten · binnenkort live',
  };
  if (NOTES[ai.mode]) aiNote.textContent = NOTES[ai.mode];

  const add = (log, cls, text) => {
    const el = document.createElement('div');
    el.className = 'at-msg ' + cls;
    el.textContent = text;
    log.appendChild(el);
    log.scrollTop = log.scrollHeight;
    return el;
  };
  const typing = log => {
    const el = document.createElement('div');
    el.className = 'at-typing';
    el.innerHTML = '<i></i><i></i><i></i>';
    log.appendChild(el);
    log.scrollTop = log.scrollHeight;
    return el;
  };
  const wait = ms => new Promise(r => setTimeout(r, ms));

  function setChips(ids) {
    chipsEl.innerHTML = '';
    (ids || []).forEach(id => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'at-chip';
      b.textContent = scripted.labels[id] || id;
      b.dataset.intent = id;
      chipsEl.appendChild(b);
    });
  }

  function renderScripted(ans) {
    const el = document.createElement('div');
    el.className = 'at-msg at-bot';
    el.innerHTML = ans.text.replace(/\n/g, '<br>'); // eigen, vertrouwde tekst uit script.js
    if (ans.actions && ans.actions.length) {
      const box = document.createElement('div');
      box.className = 'at-actions';
      ans.actions.forEach(a => {
        const link = document.createElement('a');
        link.textContent = a.label;
        link.href = a.href;
        if (a.dl) link.setAttribute('download', '');
        if (a.ext) { link.target = '_blank'; link.rel = 'noopener'; }
        box.appendChild(link);
      });
      el.appendChild(box);
    }
    logClassic.appendChild(el);
    logClassic.scrollTop = logClassic.scrollHeight;
    setChips(ans.chips);
  }

  // Eerlijke teller: de klassieke bot scoort wanneer hij een trefwoord herkent, de AI wanneer er een echt antwoord kwam
  const score = { classic: [0, 0], ai: [0, 0] };
  const tally = (key, hit) => {
    score[key][1] += 1;
    if (hit) score[key][0] += 1;
    const el = document.getElementById('score-' + key);
    el.textContent = score[key][0] + ' / ' + score[key][1];
    el.hidden = false;
  };
  const metaLine = (log, text) => {
    const meta = document.createElement('span');
    meta.className = 'msg-meta';
    meta.textContent = text;
    log.appendChild(meta);
    log.scrollTop = log.scrollHeight;
  };

  async function askClassic(text, intent) {
    add(logClassic, 'at-user', text);
    setChips([]);
    const dots = typing(logClassic);
    const id = intent || scripted.classify(text);
    const ans = scripted.answer(id);
    await wait(reduced ? 140 : 480 + Math.min(900, ans.text.length * 11));
    dots.remove();
    renderScripted(ans);
    const understood = id !== 'fallback';
    if (!understood) metaLine(logClassic, 'GEEN TREFWOORD HERKEND');
    tally('classic', understood);
  }

  async function askAi(text) {
    add(logAi, 'at-user', text);
    const dots = typing(logAi);
    const started = performance.now();
    const { reply, ok } = await ai.send(text, history);
    dots.remove();
    add(logAi, 'at-bot', reply); // textContent: antwoord van het model wordt nooit als HTML ingevoegd
    if (ok) {
      history.push({ role: 'user', text }, { role: 'assistant', text: reply });
      metaLine(logAi, 'ANTWOORD IN ' + ((performance.now() - started) / 1000).toFixed(1).replace('.', ',') + ' S');
    }
    tally('ai', ok);
  }

  let busy = false;
  const setBusy = state => {
    busy = state;
    submit.disabled = state;
    tries.forEach(b => { b.disabled = state; });
  };

  async function ask(text, intent) {
    text = (text || '').trim();
    if (!text || busy) return;
    setBusy(true);
    try {
      await Promise.all([askClassic(text, intent), askAi(text)]);
    } finally {
      setBusy(false);
    }
  }

  form.addEventListener('submit', e => {
    e.preventDefault();
    const v = input.value;
    input.value = '';
    ask(v);
  });
  tries.forEach(b => b.addEventListener('click', () => ask(b.textContent)));
  chipsEl.addEventListener('click', e => {
    const b = e.target.closest('.at-chip');
    if (b) ask(b.textContent, b.dataset.intent);
  });

  renderScripted(scripted.answer('greeting'));
  add(logAi, 'at-bot', 'Hallo! Ik ben de AI-assistent van deze site. Stel je vraag in je eigen woorden, of klik hierboven op een voorbeeld.');
})();
