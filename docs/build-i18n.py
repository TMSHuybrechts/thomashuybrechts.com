#!/usr/bin/env python3
"""Meertaligheid voor thomashuybrechts.com.

Nederlands is de bron (root). Per taal komt er een kopie in /<taal>/ met
vertaalde teksten, aangepaste paden, hreflang-links en een eigen canonical.

Gebruik (na `python docs/build-projects.py`):
  python docs/build-i18n.py extract   # verzamelt alle teksten -> docs/i18n/strings.json
                                      # en meldt per taal wat nog niet vertaald is
  python docs/build-i18n.py build     # schrijft /<taal>/..., /i18n/<taal>.js, sitemap.xml
                                      # en het hreflang-blok in de Nederlandse pagina's

Vertalingen staan in docs/i18n/<taal>.json:
  {"strings": {"<Nederlandse tekst>": "<vertaling>"}, "kw": {"<intent>": ["trefwoord", ...]}}
De sleutel is de Nederlandse tekst met witruimte samengevouwen en HTML-entiteiten
uitgepakt. Ontbreekt een vertaling, dan blijft de Nederlandse tekst staan (met waarschuwing).
JavaScript-teksten worden gevonden als t('...') in script.js en T('...') in inline scripts.
"""
import html, json, pathlib, posixpath, re, sys
from urllib.parse import quote, unquote

ROOT = pathlib.Path(__file__).resolve().parent.parent
I18N = ROOT / "docs" / "i18n"
SITE = "https://thomashuybrechts.com/"

# code, hreflang, og:locale, eigen naam (voor de taalkiezer staat dit in lang.js)
LANGS = [
    ("en", "en", "en_GB"),
    ("fr", "fr", "fr_FR"),
    ("de", "de", "de_DE"),
    ("es", "es", "es_ES"),
    ("pt", "pt", "pt_PT"),
    ("it", "it", "it_IT"),
]
SOURCE_HREFLANG = "nl-BE"

TRANSLATABLE_ATTRS = ("alt", "title", "aria-label", "placeholder")
TRANSLATABLE_META = {"description", "twitter:title", "twitter:description", "og:title", "og:description"}
URL_ATTRS = ("href", "src")

TOKEN_RE = re.compile(r"<!--.*?-->|<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>|<[^>]+>", re.S | re.I)
ATTR_RE = re.compile(r'([\w:-]+)\s*=\s*"([^"]*)"')
JS_CALL_RE = re.compile(r"\b[tT]\('((?:[^'\\]|\\.)*)'\)")
BLOCK_RE = re.compile(r"\n?[ \t]*<!-- i18n:start.*?<!-- i18n:end -->", re.S)


def pages():
    """Te vertalen pagina's, relatief t.o.v. de root (posix)."""
    out = ["index.html"]
    out += sorted(f"projecten/{p.name}" for p in (ROOT / "projecten").glob("*.html"))
    return out


def norm(s):
    return " ".join(html.unescape(s).split())


def has_letters(s):
    return any(ch.isalpha() for ch in s)


def page_url(lang, page):
    path = "" if page == "index.html" else page
    return SITE + (f"{lang}/" if lang else "") + path


# ---------- extract ----------

def segments_of(src):
    """Alle vertaalbare teksten van één HTML-pagina, in volgorde."""
    found = []
    pos = 0
    for m in TOKEN_RE.finditer(src):
        found += text_segment(src[pos:m.start()])
        tok = m.group(0)
        low = tok[:20].lower()
        if low.startswith("<script"):
            if "application/ld+json" in tok[:80]:
                found += [norm(v) for v in jsonld_strings(tok) if has_letters(v)]
            else:
                found += [js_unescape(v) for v in JS_CALL_RE.findall(tok)]
        elif low.startswith("<!--") or low.startswith("<style"):
            pass
        else:
            found += [v for _, v in tag_texts(tok)]
        pos = m.end()
    found += text_segment(src[pos:])
    return [s for s in found if s and has_letters(s)]


def text_segment(raw):
    key = norm(raw)
    return [key] if key and has_letters(key) else []


def tag_texts(tok):
    """(attribuut, genormaliseerde tekst) voor vertaalbare attributen van een tag."""
    attrs = dict((k.lower(), v) for k, v in ATTR_RE.findall(tok))
    out = []
    for a in TRANSLATABLE_ATTRS:
        if a in attrs and has_letters(attrs[a]):
            out.append((a, norm(attrs[a])))
    if tok[:5].lower() == "<meta":
        kind = attrs.get("name") or attrs.get("property") or ""
        if kind in TRANSLATABLE_META and "content" in attrs:
            out.append(("content", norm(attrs["content"])))
    subject = mail_subject(attrs.get("href", ""))
    if subject:
        out.append(("href", subject))
    return out


SUBJECT_RE = re.compile(r"([?&]subject=)([^&]*)")


def mail_subject(href):
    """Onderwerp van een mailto-link, of None."""
    if not href.startswith("mailto:"):
        return None
    m = SUBJECT_RE.search(html.unescape(href))
    return norm(unquote(m.group(2))) if m else None


def translate_mailto(href, tr):
    return SUBJECT_RE.sub(lambda m: m.group(1) + quote(tr(norm(unquote(m.group(2))))), href)


SKIP_JSONLD_KEYS = {"@context", "@type", "@id", "url", "email", "sameAs", "inLanguage", "addressCountry"}


def jsonld_strings(tok):
    body = tok[tok.index(">") + 1: tok.rindex("<")]
    data = json.loads(body)
    out = []

    def walk(node, key=None):
        if isinstance(node, dict):
            for k, v in node.items():
                walk(v, k)
        elif isinstance(node, list):
            for v in node:
                walk(v, key)
        elif isinstance(node, str) and key not in SKIP_JSONLD_KEYS:
            out.append(node)
    walk(data)
    return out


def js_unescape(s):
    return s.replace("\\'", "'").replace("\\n", "\n").replace("\\\\", "\\")


def js_escape(s):
    return s.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n")


def js_keys():
    keys = [js_unescape(v) for v in JS_CALL_RE.findall((ROOT / "script.js").read_text(encoding="utf-8"))]
    for page in pages():
        src = (ROOT / page).read_text(encoding="utf-8")
        for m in re.finditer(r"<script\b(?![^>]*ld\+json)[^>]*>(.*?)</script>", src, re.S | re.I):
            keys += [js_unescape(v) for v in JS_CALL_RE.findall(m.group(1))]
    return [k for k in dict.fromkeys(keys) if has_letters(k)]


def load_lang(code):
    f = I18N / f"{code}.json"
    if not f.exists():
        return {"strings": {}, "kw": {}}
    return json.loads(f.read_text(encoding="utf-8"))


def extract():
    I18N.mkdir(parents=True, exist_ok=True)
    seen = {}
    for page in pages():
        for s in segments_of((ROOT / page).read_text(encoding="utf-8")):
            seen.setdefault(s, []).append(page)
    for k in js_keys():
        seen.setdefault(k, []).append("script.js")
    items = [{"nl": k, "pages": sorted(set(v))} for k, v in seen.items()]
    (I18N / "strings.json").write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(items)} unieke teksten -> docs/i18n/strings.json")
    for code, *_ in LANGS:
        have = load_lang(code)["strings"]
        missing = [k for k in seen if k not in have]
        print(f"  {code}: {len(seen) - len(missing)} vertaald, {len(missing)} ontbreken")


# ---------- build ----------

class Translator:
    def __init__(self, code):
        self.code = code
        self.strings = load_lang(code)["strings"]
        self.missing = set()

    def __call__(self, key):
        if key in self.strings:
            return self.strings[key]
        self.missing.add(key)
        return key


def translate_text(raw, tr):
    key = norm(raw)
    if not key or not has_letters(key):
        return raw
    lead = raw[: len(raw) - len(raw.lstrip())]
    trail = raw[len(raw.rstrip()):]
    return lead + html.escape(tr(key), quote=False) + trail


def rewrite_url(url, page, lang):
    """Pad vanuit /<lang>/<page> naar hetzelfde doel. Vertaalde pagina's blijven binnen de taal."""
    if not url or url.startswith(("#", "/", "http:", "https:", "mailto:", "tel:", "data:", "javascript:")):
        return url
    m = re.match(r"([^?#]*)(.*)", url)
    path, suffix = m.group(1), m.group(2)
    if not path:
        return url
    pagedir = posixpath.dirname(page)
    target = posixpath.normpath(posixpath.join(pagedir, path))
    is_dir = path.endswith("/") or target == "."
    target_file = "index.html" if target == "." else target
    translated = set(pages())
    if target_file in translated or (is_dir and posixpath.join(target, "index.html").lstrip("./") in translated):
        return url  # zelfde structuur binnen de taalmap
    new = posixpath.relpath(target, posixpath.join(lang, pagedir) if pagedir else lang)
    if is_dir and not new.endswith("/"):
        new += "/"
    return new + suffix


def rewrite_tag(tok, page, lang, tr):
    attrs = ATTR_RE.findall(tok)
    meta_kind = ""
    if tok[:5].lower() == "<meta":
        d = dict((k.lower(), v) for k, v in attrs)
        meta_kind = d.get("name") or d.get("property") or ""

    def repl(m):
        name, val = m.group(1), m.group(2)
        low = name.lower()
        if low in TRANSLATABLE_ATTRS and has_letters(val):
            val = html.escape(tr(norm(val)), quote=True)
        elif low == "content" and meta_kind in TRANSLATABLE_META:
            val = html.escape(tr(norm(val)), quote=True)
        elif low == "content" and meta_kind == "og:locale":
            val = dict((c, o) for c, _, o in LANGS)[lang]
        elif low == "content" and meta_kind == "og:url":
            val = page_url(lang, page)
        elif low == "href" and mail_subject(val):
            val = html.escape(translate_mailto(html.unescape(val), tr), quote=True)
        elif low in URL_ATTRS:
            if low == "href" and 'rel="canonical"' in tok:
                val = page_url(lang, page)
            else:
                val = html.escape(rewrite_url(html.unescape(val), page, lang), quote=True)
        elif low == "srcset":
            val = ", ".join(
                " ".join([rewrite_url(part.split()[0], page, lang)] + part.split()[1:])
                for part in val.split(",")
            )
        elif low == "style" and "url(" in val:
            val = re.sub(r"url\(([^)]+)\)", lambda u: f"url({rewrite_url(u.group(1), page, lang)})", val)
        elif low == "lang" and tok[:5].lower() == "<html":
            val = lang
        return f'{name}="{val}"'

    out = ATTR_RE.sub(repl, tok)
    if tok[:5].lower() == "<html":
        depth = page.count("/") + 1
        out = out[:-1].rstrip() + f' data-root="{"../" * depth}">'
    return out


def rewrite_jsonld(tok, lang, page, tr):
    start, end = tok.index(">") + 1, tok.rindex("<")
    data = json.loads(tok[start:end])

    def walk(node, key=None):
        if isinstance(node, dict):
            return {k: walk(v, k) for k, v in node.items()}
        if isinstance(node, list):
            return [walk(v, key) for v in node]
        if isinstance(node, str):
            if key == "inLanguage":
                return lang
            if key == "url" and node.startswith(SITE) and node != SITE:
                rest = node[len(SITE):]
                return SITE + f"{lang}/" + rest if rest in pages() else node
            if key in SKIP_JSONLD_KEYS or not has_letters(node):
                return node
            return tr(norm(node))
        return node
    body = json.dumps(walk(data), ensure_ascii=False, indent=2)
    body = "\n".join("    " + line for line in body.splitlines())
    return tok[:start] + "\n" + body + "\n    " + tok[end:]


def i18n_block(page, lang):
    # Paden relatief t.o.v. de Nederlandse pagina; translate_page herschrijft ze voor /<lang>/
    rel = "../" * page.count("/") or "./"
    lines = ["<!-- i18n:start · gegenereerd door docs/build-i18n.py, niet met de hand aanpassen -->"]
    lines.append(f'<link rel="alternate" hreflang="{SOURCE_HREFLANG}" href="{page_url("", page)}" />')
    for code, hreflang, _ in LANGS:
        lines.append(f'<link rel="alternate" hreflang="{hreflang}" href="{page_url(code, page)}" />')
    lines.append(f'<link rel="alternate" hreflang="x-default" href="{page_url("", page)}" />')
    if lang:
        lines.append(f'<script src="{rel}i18n/{lang}.js"></script>')
    lines.append(f'<script src="{rel}lang.js"></script>')
    lines.append("<!-- i18n:end -->")
    return "\n".join("    " + line for line in lines)


def with_block(src, page, lang):
    src = BLOCK_RE.sub("", src)
    m = re.search(r'[ \t]*<link rel="canonical"[^>]*>', src)
    assert m, f"geen canonical in {page}"
    return src[: m.end()] + "\n" + i18n_block(page, lang) + src[m.end():]


def translate_page(src, page, lang, tr):
    out = []
    pos = 0
    for m in TOKEN_RE.finditer(src):
        out.append(translate_text(src[pos:m.start()], tr))
        tok = m.group(0)
        low = tok[:20].lower()
        if low.startswith("<script") and "application/ld+json" in tok[:80]:
            out.append(rewrite_jsonld(tok, lang, page, tr))
        elif low.startswith("<script"):
            open_tag = tok[: tok.index(">") + 1]
            out.append(rewrite_tag(open_tag, page, lang, tr) + tok[len(open_tag):])
        elif low.startswith("<!--") or low.startswith("<style"):
            out.append(tok)
        else:
            out.append(rewrite_tag(tok, page, lang, tr))
        pos = m.end()
    out.append(translate_text(src[pos:], tr))
    return "".join(out)


def write_js_dict(code, tr):
    data = load_lang(code)
    strings = {k: tr(k) for k in js_keys()}
    js = ("// Gegenereerd door docs/build-i18n.py — niet met de hand aanpassen\n"
          f"window.TH_I18N = {json.dumps(strings, ensure_ascii=False, indent=1)};\n"
          f"window.TH_I18N_KW = {json.dumps(data.get('kw', {}), ensure_ascii=False)};\n")
    out = ROOT / "i18n" / f"{code}.js"
    out.parent.mkdir(exist_ok=True)
    out.write_text(js, encoding="utf-8", newline="\n")


def write_sitemap():
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    alts = [("", SOURCE_HREFLANG)] + [(c, h) for c, h, _ in LANGS]

    def entry(loc, prio, page=None):
        lines.append(f"  <url><loc>{loc}</loc><changefreq>monthly</changefreq><priority>{prio}</priority>")
        if page:
            for code, hreflang in alts:
                lines.append(f'    <xhtml:link rel="alternate" hreflang="{hreflang}" href="{page_url(code, page)}" />')
        lines.append("  </url>")
    for code in [""] + [c for c, *_ in LANGS]:
        for page in pages():
            entry(page_url(code, page), "1.0" if page == "index.html" else "0.8", page)
    entry(SITE + "repo-notebook/", "0.9")
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def build():
    for page in pages():
        path = ROOT / page
        path.write_text(with_block(path.read_text(encoding="utf-8"), page, ""), encoding="utf-8", newline="\n")
    for code, *_ in LANGS:
        tr = Translator(code)
        for page in pages():
            src = with_block((ROOT / page).read_text(encoding="utf-8"), page, code)
            out = ROOT / code / page
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(translate_page(src, page, code, tr), encoding="utf-8", newline="\n")
        write_js_dict(code, tr)
        status = f"{len(tr.missing)} ontbrekende vertalingen" if tr.missing else "volledig"
        print(f"{code}: {len(pages())} pagina's · {status}")
        for k in sorted(tr.missing)[:8]:
            print("   -", k[:90])
    write_sitemap()
    print("sitemap.xml bijgewerkt")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "extract":
        extract()
    elif cmd == "build":
        build()
    else:
        print(__doc__)
        sys.exit(1)
