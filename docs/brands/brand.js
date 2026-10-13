// Chatpaneel op een merksite: praat met dezelfde motor (window.TH_AI uit chat-ai.js).
(function () {
  const ai = window.TH_AI;
  const form = document.getElementById('chat-form');
  const log = document.getElementById('chat-log');
  if (!ai || !form || !log) return;

  const input = document.getElementById('chat-q');
  const submit = form.querySelector('button');
  const tries = [...document.querySelectorAll('.try')];
  const note = document.getElementById('chat-note');
  const history = [];

  const NOTES = {
    mock: 'Lokale preview · voorbeeldantwoorden, de AI-backend is nog niet aangesloten',
    offline: 'De assistent wordt nog aangesloten · binnenkort live',
  };
  if (NOTES[ai.mode]) note.textContent = NOTES[ai.mode];

  const add = (cls, text) => {
    const el = document.createElement('div');
    el.className = 'msg ' + cls;
    el.textContent = text; // nooit als HTML: tekst komt van de bezoeker of van het model
    log.appendChild(el);
    log.scrollTop = log.scrollHeight;
  };

  let busy = false;
  const setBusy = state => {
    busy = state;
    submit.disabled = state;
    tries.forEach(b => { b.disabled = state; });
  };

  async function ask(text) {
    text = (text || '').trim();
    if (!text || busy) return;
    setBusy(true);
    add('msg-user', text);
    const dots = document.createElement('div');
    dots.className = 'typing';
    dots.innerHTML = '<i></i><i></i><i></i>';
    log.appendChild(dots);
    log.scrollTop = log.scrollHeight;
    try {
      const { reply, ok } = await ai.send(text, history);
      add('msg-bot', reply);
      if (ok) history.push({ role: 'user', text }, { role: 'assistant', text: reply });
    } finally {
      dots.remove();
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

  add('msg-bot', log.dataset.greeting);
})();
