#!/usr/bin/env python3
"""Bygger de to utgavene av siden fra src/.

  index.html                    Web-utgaven. Bildene ligger som egne filer i
                                assets-web/, fonter hentes fra Google Fonts.
                                Dette er fila Netlify publiserer.

  hammersborg-standalone.html   Selvstendig utgave. Alt inlinet som data-URI-er,
                                virker uten nett og uten filer ved siden av.
                                Til deling som vedlegg.

Bruk:
    python3 build.py            # bygg begge
    python3 build.py --web      # bare web-utgaven (rask, ingen nedlasting)
"""

import base64
import json
import mimetypes
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src" / "Hammersborgkvartalet.dc.html"
SUPPORT = ROOT / "src" / "support.js"
ASSETS_WEB = ROOT / "assets-web"

WEB_UT = ROOT / "index.html"
STANDALONE_UT = ROOT / "hammersborg-standalone.html"

BASE_URL = "https://hammersborg.netlify.app"
TITLE = "Hammersborgkvartalet – Oslo Urban Week"
BESKRIVELSE = ("Bli med på nabolagstreff og foredrag i Hammersborgkvartalet under "
               "Oslo Urban Week, tirsdag 22. september. Gratis, med mulighet for "
               "mat og drikke.")

# Bildet i hero lastes med en gang; resten kan vente til de nærmer seg skjermen.
IKKE_LAT = ("img00.jpg", "he-logo-hvit.png")

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def data_uri(raw, mime):
    return f"data:{mime};base64," + base64.b64encode(raw).decode("ascii")


def hode_tagger():
    """Metadata som må stå i den statiske HTML-en.

    Delingstjenester (Slack, Teams, Facebook, LinkedIn) kjører ikke JavaScript.
    Ligger disse i <helmet> inne i <x-dc>, blir de injisert av runtimen og
    crawlerne ser dem aldri. Derfor skrives de rett i <head>.
    """
    return "\n".join([
        f'<title>{TITLE}</title>',
        f'<meta name="description" content="{BESKRIVELSE}">',
        '<meta property="og:type" content="website">',
        f'<meta property="og:site_name" content="Höegh Eiendom">',
        f'<meta property="og:title" content="{TITLE}">',
        f'<meta property="og:description" content="{BESKRIVELSE}">',
        f'<meta property="og:url" content="{BASE_URL}/">',
        f'<meta property="og:image" content="{BASE_URL}/og-image.jpg">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<meta property="og:locale" content="nb_NO">',
        '<meta name="twitter:card" content="summary_large_image">',
        '<link rel="icon" href="/favicon.svg" type="image/svg+xml">',
        # Runtimen utleder rotkomponentens navn fra filnavnet (dcNameFromPath i
        # support.js). Uten dette blir navnet "index", <x-dc>-blokken finnes
        # aldri, og siden rendrer rå kildekode.
        f'<base href="{SRC.name}">',
    ])


def resources_script(support_src, react_inline):
    """<script>window.__resources = …</script>

    Må være satt uansett utgave: uten den re-fetcher runtimen sin egen side og
    kjører parseDcText på rå tekst. Den regexen treffer strengen "<x-dc>" som
    står i en feilmelding inne i den inlinede support.js — før det ekte
    elementet — og siden rendrer rå JS-kildekode.

    Verdiene mapper React-URL-ene. Inlinet slipper siden å hente React fra
    unpkg; uten inlining faller cdnScriptFor tilbake på unpkg med SRI.
    """
    urls = re.findall(r'var REACT(?:_DOM)?_URL = "([^"]+)"', support_src)
    mapping = {}
    if react_inline:
        for url in urls:
            mapping[url] = data_uri(fetch(url), "text/javascript")
            print(f"  + {url.rsplit('/', 1)[-1]}")
    payload = json.dumps(mapping).replace("</", "<\\/")
    return f"<script>window.__resources = {payload};</script>"


def felles(html):
    """Steg som er like for begge utgavene."""
    html = re.sub(r'\s*<meta name="ext-resource-dependency"[^>]*>', "", html)
    html = html.replace("<html>", '<html lang="no">', 1)
    html = html.replace('<meta charset="utf-8">',
                        f'<meta charset="utf-8">\n{hode_tagger()}', 1)
    return html


def sett_inn_support(html, react_inline):
    tag = '<script src="./support.js"></script>'
    if tag not in html:
        sys.exit(f"FEIL: fant ikke {tag} i kilden — er den endret?")
    src = SUPPORT.read_text(encoding="utf-8")
    return html.replace(tag, resources_script(src, react_inline)
                        + f"\n<script>\n{src}\n</script>")


def lat_lasting(html):
    """Legg loading=lazy på bilder under første skjermflate."""
    def sub(m):
        tag = m.group(0)
        if any(n in tag for n in IKKE_LAT) or "loading=" in tag:
            return tag
        return tag[:4] + ' loading="lazy" decoding="async"' + tag[4:]
    return re.sub(r"<img\b[^>]*>", sub, html)


def bygg_web():
    print("Bygger web-utgaven")
    html = felles(SRC.read_text(encoding="utf-8"))
    html = sett_inn_support(html, react_inline=True)
    # Bildene serveres som egne filer — nettleseren kan da mellomlagre dem,
    # laste dem etter behov, og vise teksten før de er nede.
    html = html.replace("assets/", "assets-web/")
    html = lat_lasting(html)
    if "data:image" in html:
        sys.exit("FEIL: web-utgaven skal ikke inneholde inlinede bilder")
    WEB_UT.write_text(html, encoding="utf-8")
    print(f"Skrev {WEB_UT.name} ({len(html.encode()) // 1024} KB)")


def bygg_standalone():
    print("Bygger selvstendig utgave")
    html = felles(SRC.read_text(encoding="utf-8"))
    html = sett_inn_support(html, react_inline=True)

    for path in sorted(ASSETS_WEB.iterdir(), key=lambda p: -len(p.name)):
        if path.name.startswith("."):
            continue
        ref = f"assets/{path.name}"
        if ref not in html:
            continue
        mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        html = html.replace(ref, data_uri(path.read_bytes(), mime))

    match = re.search(r'<link\s+href="(https://fonts\.googleapis\.com/css2[^"]+)"[^>]*>', html)
    if match:
        css = fetch(match.group(1).replace("&amp;", "&")).decode("utf-8")
        for url in sorted(set(re.findall(r"url\((https://fonts\.gstatic\.com/[^)]+)\)", css))):
            css = css.replace(url, data_uri(fetch(url), "font/woff2"))
        html = html.replace(match.group(0), f"<style>\n{css}\n</style>")
        print("  + fonter inlinet")

    if "assets/" in html:
        sys.exit(f"FEIL: uinlinede referanser igjen: "
                 f"{sorted(set(re.findall(r'assets/[A-Za-z0-9_.-]+', html)))}")
    STANDALONE_UT.write_text(html, encoding="utf-8")
    print(f"Skrev {STANDALONE_UT.name} ({len(html.encode()) // 1024} KB)")


if __name__ == "__main__":
    bygg_web()
    if "--web" not in sys.argv:
        bygg_standalone()
