// Taalkiezer met vlaggen + onthouden taalkeuze.
// Laadt synchroon in <head>: wie eerder een andere taal koos, wordt doorgestuurd
// vóór de Nederlandse pagina in beeld komt. Nederlands staat in de root, de
// vertalingen in /en/, /fr/, ... (gegenereerd door docs/build-i18n.py).
(function () {
  var LANGS = [
    { code: 'nl', name: 'Nederlands', flag: 'vl.png' },
    { code: 'en', name: 'English', flag: 'gb.svg' },
    { code: 'fr', name: 'Français', flag: 'fr.svg' },
    { code: 'de', name: 'Deutsch', flag: 'de.svg' },
    { code: 'es', name: 'Español', flag: 'es.svg' },
    { code: 'pt', name: 'Português', flag: 'pt.svg' },
    { code: 'it', name: 'Italiano', flag: 'it.svg' }
  ];
  var LABEL = {
    nl: 'Taal kiezen', en: 'Choose language', fr: 'Choisir la langue', de: 'Sprache wählen',
    es: 'Elegir idioma', pt: 'Escolher idioma', it: 'Scegli la lingua'
  };
  var STORE_KEY = 'th_lang';

  var current = document.documentElement.lang || 'nl';
  var match = location.pathname.match(/^\/(en|fr|de|es|pt|it)(\/.*)?$/);
  var rest = match ? (match[2] || '/') : location.pathname;
  var isKnown = function (code) { return LANGS.some(function (l) { return l.code === code; }); };
  var urlFor = function (code) { return (code === 'nl' ? '' : '/' + code) + rest + location.search + location.hash; };

  var saved = null;
  try { saved = localStorage.getItem(STORE_KEY); } catch (err) {}

  // Alleen vanaf de Nederlandse (standaard)pagina's doorsturen: een gedeelde
  // /fr/-link blijft gewoon Frans, ook als de bezoeker eerder iets anders koos.
  if (current === 'nl' && saved && saved !== 'nl' && isKnown(saved) && location.protocol !== 'file:') {
    location.replace(urlFor(saved));
    return;
  }

  function flagImg(l) {
    return '<img src="/assets/flags/' + l.flag + '" alt="" width="24" height="16" />';
  }

  function build() {
    var host = document.querySelector('.header-right');
    if (!host || document.querySelector('.lang-switch')) return;
    var active = LANGS.filter(function (l) { return l.code === current; })[0] || LANGS[0];

    var wrap = document.createElement('div');
    wrap.className = 'lang-switch';
    wrap.innerHTML =
      '<button class="lang-toggle" type="button" aria-haspopup="true" aria-expanded="false" aria-controls="lang-menu" aria-label="' +
        LABEL[current] + ': ' + active.name + '">' +
        flagImg(active) + '<span class="lang-code">' + active.code + '</span>' +
      '</button>' +
      '<ul class="lang-menu" id="lang-menu" hidden>' +
        LANGS.map(function (l) {
          return '<li><a href="' + urlFor(l.code) + '" hreflang="' + l.code + '" lang="' + l.code + '" data-lang="' + l.code + '"' +
            (l.code === current ? ' aria-current="true"' : '') + '>' + flagImg(l) + '<span>' + l.name + '</span></a></li>';
        }).join('') +
      '</ul>';
    host.insertBefore(wrap, host.firstChild);

    var btn = wrap.querySelector('.lang-toggle');
    var menu = wrap.querySelector('.lang-menu');
    var setOpen = function (open) {
      menu.hidden = !open;
      btn.setAttribute('aria-expanded', String(open));
    };
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      setOpen(menu.hidden);
      if (!menu.hidden) menu.querySelector('[aria-current]').focus();
    });
    menu.addEventListener('click', function (e) {
      var link = e.target.closest('a[data-lang]');
      if (!link) return;
      try { localStorage.setItem(STORE_KEY, link.dataset.lang); } catch (err) {}
    });
    document.addEventListener('click', function (e) { if (!wrap.contains(e.target)) setOpen(false); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !menu.hidden) { setOpen(false); btn.focus(); }
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', build);
  else build();
})();
