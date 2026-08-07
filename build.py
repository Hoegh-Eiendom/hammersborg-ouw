#!/usr/bin/env python3
"""Bygger den selvstendige index.html fra src/.

Inliner support.js, alle bilder i assets/ og webfontene fra Google Fonts som
data-URI-er, slik at resultatet er én fil som virker uten nett og uten server.

Bruk:
    python3 build.py            # bygg index.html + docs/index.html
    python3 build.py --no-fonts # hopp over fontnedlasting (krever ikke nett)
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
ASSETS = ROOT / "assets"
OUTPUTS = [ROOT / "index.html", ROOT / "docs" / "index.html"]

TITLE = "Hammersborgkvartalet – Oslo Urban Week"

# Google serverer woff2 kun til nettlesere som annonserer støtte for det.
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def data_uri(raw, mime):
    return f"data:{mime};base64," + base64.b64encode(raw).decode("ascii")


def inline_assets(html):
    """Bytt hver assets/… -referanse mot en data-URI.

    Gjelder både img-src i markup og filstier inne i JS-datastrukturene
    ({{ ev.img }} / {{ ft.img }}) — sistnevnte var ikke inlinet i den gamle
    bundlede fila, som derfor viste brutte bilder utenfor repo-rota.
    """
    # Lengste navn først, så et kortere navn aldri treffer inni et lengre.
    for path in sorted(ASSETS.iterdir(), key=lambda p: -len(p.name)):
        if path.name.startswith("."):
            continue
        ref = f"assets/{path.name}"
        if ref not in html:
            print(f"  ! {ref} brukes ikke i kilden — hoppet over")
            continue
        mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        html = html.replace(ref, data_uri(path.read_bytes(), mime))
        print(f"  + {ref} ({path.stat().st_size // 1024} KB)")
    return html


def inline_fonts(html):
    """Erstatt Google Fonts-<link> med en <style> der woff2 er inlinet."""
    match = re.search(r'<link\s+href="(https://fonts\.googleapis\.com/css2[^"]+)"[^>]*>', html)
    if not match:
        print("  ! fant ingen Google Fonts-link")
        return html

    css = fetch(match.group(1).replace("&amp;", "&")).decode("utf-8")
    urls = sorted(set(re.findall(r"url\((https://fonts\.gstatic\.com/[^)]+)\)", css)))
    for url in urls:
        css = css.replace(url, data_uri(fetch(url), "font/woff2"))
    print(f"  + {len(urls)} fontfiler inlinet")

    return html.replace(match.group(0), f"<style>\n{css}\n</style>")


def resources_script(support_src, offline):
    """Bygg <script>window.__resources = …</script>.

    To grunner til at den må være der:

    1. Uten den re-fetcher runtime-en sin egen side og kjører parseDcText på rå
       tekst (support.js linje 158). Den regexen treffer da strengen "<x-dc>" som
       står i en feilmelding inne i den inlinede support.js — før det ekte
       <x-dc>-elementet — og siden rendrer rå JS-kildekode.
    2. cdnScriptFor() slår opp React-URL-ene her. Mappes de til data-URI-er,
       slipper fila å hente React fra unpkg og virker uten nett.
    """
    urls = re.findall(r'var REACT(?:_DOM)?_URL = "([^"]+)"', support_src)
    mapping = {}
    if not offline:
        for url in urls:
            mapping[url] = data_uri(fetch(url), "text/javascript")
            print(f"  + {url.rsplit('/', 1)[-1]}")
    else:
        print("  · React hentes fra unpkg ved visning (--offline) — krever nett")

    payload = json.dumps(mapping).replace("</", "<\\/")
    return f"<script>window.__resources = {payload};</script>"


def main():
    html = SRC.read_text(encoding="utf-8")

    print("Bygger fra", SRC.relative_to(ROOT))

    # Bundler-hint som ikke har noen funksjon i den ferdige fila.
    html = re.sub(r'\s*<meta name="ext-resource-dependency"[^>]*>', "", html)

    # x-dc-runtimen utleder rotkomponentens navn fra filnavnet (dcNameFromPath i
    # support.js): faller pathname ikke på .dc.html, brukes document.baseURI.
    # Uten dette blir navnet "index" og <x-dc>-blokken finnes aldri — siden
    # rendrer da rå kildekode. Alle øvrige URL-er i fila er absolutte
    # (data:/https:), så <base> påvirker ikke noe annet.
    head_extra = (f'<title>{TITLE}</title>\n'
                  f'<base href="{SRC.name}">')
    html = html.replace('<meta charset="utf-8">',
                        f'<meta charset="utf-8">\n{head_extra}', 1)

    script_tag = '<script src="./support.js"></script>'
    if script_tag not in html:
        sys.exit(f"FEIL: fant ikke {script_tag} i kilden — er den endret?")
    support_src = SUPPORT.read_text(encoding="utf-8")
    offline = "--no-fonts" in sys.argv
    html = html.replace(
        script_tag,
        resources_script(support_src, offline) + f"\n<script>\n{support_src}\n</script>",
    )
    print(f"  + support.js ({SUPPORT.stat().st_size // 1024} KB)")

    html = inline_assets(html)

    if "--no-fonts" in sys.argv:
        print("  · hopper over fonter (--no-fonts) — fila krever da nett for typografi")
    else:
        html = inline_fonts(html)

    if "assets/" in html:
        rest = sorted(set(re.findall(r"assets/[A-Za-z0-9_.-]+", html)))
        sys.exit(f"FEIL: uinlinede referanser igjen: {rest}")

    for out in OUTPUTS:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding="utf-8")
        print(f"Skrev {out.relative_to(ROOT)} ({len(html.encode()) // 1024} KB)")


if __name__ == "__main__":
    main()
