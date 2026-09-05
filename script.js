// Toon inhoud pas verbergen wanneer JS draait (anders blijft .reveal onzichtbaar
// als je index.html gewoon opent zonder werkende JavaScript).
document.documentElement.classList.add('js');

// Jaar in de footer
const year = document.getElementById('year');
if (year) year.textContent = new Date().getFullYear();

// Scroll-onthulling (met fallback voor oude browsers)
const reveals = document.querySelectorAll('.reveal');
if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver(
    entries => entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }),
    { threshold: 0.12 }
  );
  reveals.forEach(el => observer.observe(el));
} else {
  reveals.forEach(el => el.classList.add('visible'));
}

// Header: compacter na scrollen
const header = document.getElementById('header');
const onScroll = () => header.classList.toggle('is-scrolled', window.scrollY > 40);
onScroll();
window.addEventListener('scroll', onScroll, { passive: true });

// Mobiel menu
const nav = document.getElementById('nav');
const toggle = document.querySelector('.menu-toggle');
const closeMenu = () => {
  nav.classList.remove('is-open');
  toggle.setAttribute('aria-expanded', 'false');
  toggle.setAttribute('aria-label', 'Menu openen');
};
toggle.addEventListener('click', () => {
  const open = !nav.classList.contains('is-open');
  nav.classList.toggle('is-open', open);
  toggle.setAttribute('aria-expanded', String(open));
  toggle.setAttribute('aria-label', open ? 'Menu sluiten' : 'Menu openen');
});
nav.addEventListener('click', e => e.target.closest('a') && closeMenu());
document.addEventListener('keydown', e => e.key === 'Escape' && closeMenu());

// Actieve sectie in de navigatie
const navLinks = [...nav.querySelectorAll('a[href^="#"]')];
const sections = navLinks.map(a => document.querySelector(a.getAttribute('href'))).filter(Boolean);
if ('IntersectionObserver' in window && sections.length) {
  const spy = new IntersectionObserver(
    entries => entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      navLinks.forEach(a => a.classList.toggle('is-active', a.getAttribute('href') === '#' + entry.target.id));
    }),
    { rootMargin: '-40% 0px -55% 0px' }
  );
  sections.forEach(s => spy.observe(s));
}

// Hero-object: lichte 3D-reactie op de muis (niet op touch of bij reduced motion)
const object = document.querySelector('.hero-object');
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (object && !reduceMotion && window.matchMedia('(hover: hover)').matches) {
  object.addEventListener('pointermove', ({ clientX, clientY }) => {
    const { left, top, width, height } = object.getBoundingClientRect();
    object.style.transform = `perspective(900px) rotateX(${(clientY - top - height / 2) / -45}deg) rotateY(${(clientX - left - width / 2) / 45}deg)`;
  });
  object.addEventListener('pointerleave', () => (object.style.transform = ''));
}

// E-mailadres kopiëren
const copyBtn = document.querySelector('.copy-email');
if (copyBtn) {
  const hint = copyBtn.querySelector('.copy-email-hint');
  copyBtn.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(copyBtn.dataset.email);
      copyBtn.classList.add('is-copied');
      hint.textContent = 'gekopieerd';
      setTimeout(() => { copyBtn.classList.remove('is-copied'); hint.textContent = 'kopieer'; }, 2000);
    } catch {
      window.location.href = 'mailto:' + copyBtn.dataset.email;
    }
  });
}

// Achtergrondmuziek: uit tot de bezoeker zelf op de knop drukt
const bgm = document.getElementById('bgm');
const soundBtn = document.querySelector('.sound-toggle');
if (bgm && soundBtn) {
  bgm.volume = 0.35;
  soundBtn.addEventListener('click', async () => {
    if (bgm.paused) {
      try { await bgm.play(); soundBtn.setAttribute('aria-pressed', 'true'); soundBtn.setAttribute('aria-label', 'Muziek pauzeren'); } catch {}
    } else {
      bgm.pause(); soundBtn.setAttribute('aria-pressed', 'false'); soundBtn.setAttribute('aria-label', 'Muziek afspelen');
    }
  });
}

// ===== Agent Thomas — gescripte, client-side AI-gids (geen backend, geen data verlaat het toestel) =====
(function () {
  if (document.getElementById('agent-thomas')) return;
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const isProj = location.pathname.includes('/projecten/');
  const rel = isProj ? '../' : '';
  const URLS = {
    cv: rel + 'assets/thomas-huybrechts-cv.pdf',
    ava: rel + 'assets/agent-thomas.jpg',
    mail: 'mailto:hey@thomashuybrechts.com?subject=Contact%20via%20thomashuybrechts.com',
    github: 'https://github.com/TMSHuybrechts',
    linkedin: 'https://www.linkedin.com/in/thomashuybrechts',
    sec: id => rel + '#' + id,
    project: slug => (isProj ? '' : 'projecten/') + slug + '.html',
  };

  const PROJECTS = {
    'orbit-display': ['Orbit Display', 'één draaiend command-wiel dat al mijn lokale AI-tools, automatiseringen en beveiliging samenbrengt'],
    'victus-control': ['Victus Control', 'een local-first ops-platform met een intent-map: wat je wílt draaien vs. wat er écht draait'],
    'thomas-cluster': ['Thomas Cluster', 'één master command center voor mijn hele lokale AI-cluster (Docker, n8n, Ollama, ComfyUI)'],
    'repo-notebook': ['Repo Notebook', 'een Electron-app die GitHub-repos verzamelt, analyseert en verbindt — met lokale AI'],
    'repo-notebook-obsidian': ['Repo Notebook voor Obsidian', 'dezelfde kennisomgeving als plugin in je eigen Obsidian-vault, met MCP'],
    'cyberdash': ['CyberDash', 'een modulair security-dashboard — mijn oefening in architectuur & integratie'],
    'llm-wiki': ['LLM Wiki', 'een zelf-onderhoudende kennisbank die bronnen inleest en verbindt in een kennisgraaf'],
    'jarvis': ['Jarvis', 'een handsfree AI-command center: bestuurd met klappen, stem én handgebaren'],
    'sirena': ['Sirena', 'een Vlaamse desktopassistent met stem, avatar en échte computeracties'],
    'embedded': ['Embedded experimenten', 'eigen ESP32-firmware, displays en microcontrollers in tastbare toestellen'],
  };

  const LABELS = {
    cv: '📄 Bekijk cv', projects: '🚀 Toon projecten', skills: '🤔 Wat doe je?',
    contact: '✉️ Contact', tools: '🧰 Gereedschap', about: '👋 Wie ben je?',
  };
  Object.keys(PROJECTS).forEach(s => { LABELS[s] = PROJECTS[s][0]; });

  const A = (label, href, opts) => ({ label, href, dl: !!(opts && opts.dl), ext: !!(opts && opts.ext) });

  function projectAnswer(slug) {
    const p = PROJECTS[slug];
    return {
      text: '<b>' + p[0] + '</b> — ' + p[1] + '.',
      actions: [A('Bekijk project →', URLS.project(slug))],
      chips: ['projects', 'contact'],
    };
  }

  const ANSWERS = {
    greeting: () => ({
      text: 'Hoi! Welkom op mijn pagina 👋\nIk ben Agent Thomas — een AI-gids. Wil je mijn cv zien, of kijk je liever wat rond?',
      chips: ['cv', 'projects', 'skills', 'contact'],
    }),
    cv: () => ({
      text: 'Mijn cv staat klaar als PDF — meteen te downloaden 👇\nKort: digitale maker uit Meerhout, teamlead Production & Operations, met een brede tech-gereedschapskist — AI-agents, software én hardware.',
      actions: [A('📄 Download cv (PDF)', URLS.cv, { dl: true }), A('Bekijk profiel', URLS.sec('profiel'))],
      chips: ['skills', 'projects', 'contact'],
    }),
    projects: () => ({
      text: 'Ik bouw lokale AI, dashboards, tools én hardware. Mijn uitgelichte projecten:',
      actions: [A('Orbit Display', URLS.project('orbit-display')), A('Victus Control', URLS.project('victus-control')), A('Thomas Cluster', URLS.project('thomas-cluster')), A('Alle projecten →', URLS.sec('projecten'))],
      chips: ['repo-notebook', 'jarvis', 'llm-wiki', 'cyberdash'],
    }),
    skills: () => ({
      text: 'Drie dingen waar je mij voor inschakelt:\n① AI-agents & automatisering — lokale LLM’s, MCP, n8n\n② Producten & prototypes — Electron-apps, plugins, tools\n③ Hardware & embedded — ESP32, firmware, sensoren\nVaak combineer ik ze.',
      chips: ['tools', 'projects', 'contact'],
    }),
    tools: () => ({
      text: 'Mijn gereedschapskist:\n• AI: n8n, Ollama & lokale LLM’s, MCP, agents\n• Software: Python, JavaScript, Electron, Git\n• Systemen: Linux, Windows, Proxmox, Tailscale\n• Hardware: ESP32, Arduino, sensoren, 3D-printing',
      chips: ['projects', 'about', 'contact'],
    }),
    contact: () => ({
      text: 'Zeker! Ik ben beschikbaar voor projecten — vast of freelance, hybride of remote vanuit België 🇧🇪',
      actions: [A('✉️ Stuur een bericht', URLS.mail), A('LinkedIn ↗', URLS.linkedin, { ext: true }), A('GitHub ↗', URLS.github, { ext: true })],
      chips: ['cv', 'projects'],
    }),
    about: () => ({
      text: 'Ik ben Thomas — nieuwsgierig genoeg om het uit te zoeken, praktisch genoeg om het te bouwen. Mijn achtergrond loopt van keukens en automotive tot operations en IT, nu als teamlead Production & Operations. Geen slides, wel werkende dingen.',
      actions: [A('Lees meer over mij', URLS.sec('over'))],
      chips: ['skills', 'projects', 'contact'],
    }),
    localai: () => ({
      text: 'Ik werk graag local-first: AI die op je eigen machine draait (Ollama, lokale LLM’s). Geen cloud nodig, geen API-kosten, en je data blijft bij jou.',
      chips: ['projects', 'tools', 'contact'],
    }),
    meta: () => ({
      text: 'Eerlijk? 😄 Ik ben een lichte, gescripte gids — geen zware AI in de cloud. Thomas bóúwt wél échte lokale AI-agents; die zie je terug in zijn projecten.',
      chips: ['projects', 'contact'],
    }),
    thanks: () => ({ text: 'Graag gedaan! 🙌 Nog iets dat je wilt weten?', chips: ['projects', 'cv', 'contact'] }),
    bye: () => ({ text: 'Tot ziens! 👋 Kom gerust nog eens langs.', chips: ['projects', 'contact'] }),
    fallback: () => ({
      text: 'Daar heb ik zo geen kant-en-klaar antwoord op — maar Thomas wel. Bekijk zijn projecten of stuur hem een berichtje.',
      chips: ['projects', 'skills', 'contact'],
    }),
  };
  Object.keys(PROJECTS).forEach(s => { ANSWERS[s] = () => projectAnswer(s); });

  const MATCH = [
    { id: 'repo-notebook-obsidian', kw: ['obsidian', 'plugin', 'brat', 'vault'] },
    { id: 'orbit-display', kw: ['orbit', 'wiel', 'wheel', 'openclaw', 'draaiend'] },
    { id: 'victus-control', kw: ['victus', 'intent map', 'intent-map', 'praetor', 'imperator'] },
    { id: 'thomas-cluster', kw: ['cluster', 'docker', 'n8n', 'comfyui', 'infrastruct'] },
    { id: 'repo-notebook', kw: ['repo notebook', 'repo-notebook', 'oogst', 'repositor', 'github repo', 'electron'] },
    { id: 'cyberdash', kw: ['cyberdash', 'security', 'osint', 'hack', 'pentest', 'cyber'] },
    { id: 'llm-wiki', kw: ['llm wiki', 'wiki', 'kennisbank', 'kennisgraaf', 'ingest', 'graaf'] },
    { id: 'jarvis', kw: ['jarvis', 'klap', 'gebaren', 'gebaar', 'handsfree', 'nexus'] },
    { id: 'sirena', kw: ['sirena', 'avatar', 'desktopassistent', 'bureaublad'] },
    { id: 'embedded', kw: ['embedded', 'esp32', 'esp8266', 'firmware', 'arduino', 'microcontroller', 'hardware'] },
    { id: 'cv', kw: ['cv', 'curriculum', 'resume', 'werkervaring'] },
    { id: 'contact', kw: ['contact', 'mail', 'e-mail', 'email', 'inhuren', 'aanwerven', 'beschikbaar', 'hire', 'freelance', 'vacature', 'bereiken'] },
    { id: 'tools', kw: ['gereedschap', 'stack', 'technolog', 'welke tools', 'talen', 'programmeer', 'python', 'framework'] },
    { id: 'localai', kw: ['lokaal', 'lokale', 'ollama', 'privacy', 'cloud', 'local-first'] },
    { id: 'skills', kw: ['wat doe', 'wat kan', 'wat maak', 'diensten', 'skills', 'waarmee'] },
    { id: 'about', kw: ['wie ben', 'wie is', 'over thomas', 'over jou', 'jezelf', 'voorstellen'] },
    { id: 'projects', kw: ['project', 'werk', 'portfolio', 'gemaakt', 'gebouwd', 'laten zien', 'tonen', 'demo'] },
    { id: 'meta', kw: ['ben je echt', 'echte ai', 'ben je ai', 'ben je een bot', 'bot', 'werkt dit', 'fake', 'nep', 'chatgpt'] },
    { id: 'thanks', kw: ['bedankt', 'dank', 'merci', 'thanks', 'thx'] },
    { id: 'bye', kw: ['doei', 'tot ziens', 'ciao', 'bye', 'later'] },
    { id: 'greeting', kw: ['hallo', 'hoi', 'hey', 'goeiedag', 'goedendag'] },
  ];

  function classify(text) {
    const t = ' ' + text.toLowerCase().trim() + ' ';
    let best = null, score = 0;
    for (const m of MATCH) {
      let s = 0;
      for (const kw of m.kw) if (t.indexOf(kw) !== -1) s += 1 + kw.length / 20;
      if (s > score) { score = s; best = m.id; }
    }
    return score > 0 ? best : 'fallback';
  }

  const wrap = document.createElement('div');
  wrap.id = 'agent-thomas';
  wrap.className = 'agent-thomas';
  wrap.setAttribute('data-open', 'false');
  wrap.innerHTML =
    '<div class="at-teaser" hidden><span class="at-teaser-txt"></span><button class="at-teaser-x" type="button" aria-label="Sluiten">×</button></div>' +
    '<button class="at-launcher" type="button" aria-haspopup="dialog" aria-expanded="false" aria-controls="at-panel" aria-label="Praat met Agent Thomas">' +
      '<span class="at-ring" aria-hidden="true"></span>' +
      '<img src="' + URLS.ava + '" alt="" width="64" height="64" />' +
    '</button>' +
    '<section id="at-panel" class="at-panel" role="dialog" aria-label="Agent Thomas — digitale gids" hidden>' +
      '<header class="at-head">' +
        '<img src="' + URLS.ava + '" alt="" width="40" height="40" />' +
        '<div class="at-id"><b>Agent Thomas</b><span class="at-status"><i></i> AI-gids · demo</span></div>' +
        '<button class="at-close" type="button" aria-label="Chat sluiten">×</button>' +
      '</header>' +
      '<div class="at-log" role="log" aria-live="polite"></div>' +
      '<div class="at-chips"></div>' +
      '<form class="at-input" autocomplete="off">' +
        '<input type="text" name="q" placeholder="Stel gerust een vraag…" aria-label="Typ een bericht aan Agent Thomas" maxlength="200" />' +
        '<button type="submit" aria-label="Verstuur bericht">→</button>' +
      '</form>' +
      '<p class="at-fineprint">Gescripte demo-gids · geen data verlaat je toestel</p>' +
    '</section>';
  document.body.appendChild(wrap);

  const panel = wrap.querySelector('.at-panel');
  const launcher = wrap.querySelector('.at-launcher');
  const closeBtn = wrap.querySelector('.at-close');
  const log = wrap.querySelector('.at-log');
  const chipsEl = wrap.querySelector('.at-chips');
  const form = wrap.querySelector('.at-input');
  const input = form.querySelector('input');
  const teaser = wrap.querySelector('.at-teaser');
  const teaserTxt = teaser.querySelector('.at-teaser-txt');

  const scrollDown = () => { log.scrollTop = log.scrollHeight; };

  function addUser(text) {
    const el = document.createElement('div');
    el.className = 'at-msg at-user';
    el.textContent = text; // gebruikerstekst als textContent — veilig tegen HTML-injectie
    log.appendChild(el); scrollDown();
  }

  function addBot(ans) {
    const el = document.createElement('div');
    el.className = 'at-msg at-bot';
    el.innerHTML = ans.text.replace(/\n/g, '<br>'); // ans.text is eigen, vertrouwde tekst
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
    log.appendChild(el); scrollDown();
  }

  function setChips(ids) {
    chipsEl.innerHTML = '';
    (ids || []).forEach(id => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'at-chip';
      b.textContent = LABELS[id] || id;
      b.dataset.intent = id;
      chipsEl.appendChild(b);
    });
  }

  let typingEl = null;
  function showTyping() {
    typingEl = document.createElement('div');
    typingEl.className = 'at-typing';
    typingEl.innerHTML = '<i></i><i></i><i></i>';
    log.appendChild(typingEl); scrollDown();
  }
  function hideTyping() { if (typingEl) { typingEl.remove(); typingEl = null; } }

  let busy = false;
  function respond(id) {
    const ans = (ANSWERS[id] || ANSWERS.fallback)();
    setChips([]);
    showTyping();
    busy = true;
    const delay = prefersReduced ? 140 : 480 + Math.min(900, ans.text.length * 11);
    setTimeout(() => {
      hideTyping();
      addBot(ans);
      setChips(ans.chips);
      busy = false;
    }, delay);
  }

  function send(text) {
    text = (text || '').trim();
    if (!text || busy) return;
    addUser(text);
    respond(classify(text));
  }

  chipsEl.addEventListener('click', e => {
    const b = e.target.closest('.at-chip');
    if (!b || busy) return;
    const id = b.dataset.intent;
    addUser(LABELS[id] || id);
    respond(id);
  });

  form.addEventListener('submit', e => {
    e.preventDefault();
    const v = input.value;
    input.value = '';
    send(v);
  });

  let greeted = false;
  function open() {
    wrap.setAttribute('data-open', 'true');
    panel.hidden = false;
    launcher.setAttribute('aria-expanded', 'true');
    hideTeaser();
    if (!greeted) {
      greeted = true;
      showTyping();
      setTimeout(() => {
        hideTyping();
        const g = ANSWERS.greeting();
        addBot(g);
        setChips(g.chips);
      }, prefersReduced ? 120 : 450);
    }
    setTimeout(() => input.focus(), 80);
  }
  function close() {
    wrap.setAttribute('data-open', 'false');
    panel.hidden = true;
    launcher.setAttribute('aria-expanded', 'false');
    launcher.focus();
  }
  launcher.addEventListener('click', () => (panel.hidden ? open() : close()));
  closeBtn.addEventListener('click', close);
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && !panel.hidden) close(); });

  function hideTeaser() { teaser.hidden = true; }
  teaser.querySelector('.at-teaser-x').addEventListener('click', e => {
    e.stopPropagation();
    hideTeaser();
    try { sessionStorage.setItem('at_teaser', '1'); } catch (err) {}
  });
  teaser.addEventListener('click', open);

  let seen = false;
  try { seen = sessionStorage.getItem('at_teaser') === '1'; } catch (err) {}
  if (!seen) {
    setTimeout(() => {
      if (!panel.hidden) return;
      teaserTxt.textContent = 'Hoi! 👋 Vragen? Ik gids je even rond.';
      teaser.hidden = false;
      try { sessionStorage.setItem('at_teaser', '1'); } catch (err) {}
    }, 1600);
  }
})();
