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
    python3 build.py --web      # bare web-utgaven
    python3 build.py --check    # bygg ingenting, bare kontroller at filene
                                # på disk stemmer med kilden

To egenskaper er verdt å kjenne:

1. Begge utgavene bygges ferdig i minnet før noen av dem skrives. Feiler den ene,
   skrives ingen. Tidligere kunne index.html bli oppdatert mens den selvstendige
   utgaven ble liggende igjen på forrige versjon — uten at noe sa fra.

2. React og fontene ligger i vendor/ og hentes fra disk. Bygget krever derfor
   ikke nett. Mangler en fil, lastes den ned én gang og lagres, med gjentatte
   forsøk. Slett vendor/ for å tvinge ny nedlasting.
"""

import base64
import hashlib
import json
import mimetypes
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src" / "Hammersborgkvartalet.dc.html"
SUPPORT = ROOT / "src" / "support.js"
ASSETS_WEB = ROOT / "assets-web"
VENDOR = ROOT / "vendor"

WEB_UT = ROOT / "index.html"
STANDALONE_UT = ROOT / "hammersborg-standalone.html"

BASE_URL = "https://hammersborgkvartalet.no"
TITLE = "Hammersborgkvartalet – Oslo Urban Week"
BESKRIVELSE = ("Bli med på nabolagstreff og foredrag i Hammersborgkvartalet under "
               "Oslo Urban Week, tirsdag 22. september. Gratis, med mulighet for "
               "mat og drikke.")

IKKE_LAT = ("img00.jpg", "he-logo-hvit.png")

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# Skrives inn i begge utgavene, slik at --check kan se om de er utdaterte.
STEMPEL = "<!-- kildesignatur: {} -->"


# ---------------------------------------------------------------- nedlasting

def hent(url, forsok=4):
    """Hent en URL med gjentatte forsøk.

    Google Fonts og unpkg svarer av og til 404 eller kobler ned midt i. Ett
    enkeltforsøk gjorde bygget uforutsigbart.
    """
    sist = None
    for n in range(1, forsok + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read()
        except (urllib.error.URLError, urllib.error.HTTPError, OSError) as e:
            sist = e
            if n < forsok:
                pause = 1.5 * n
                print(f"    forsøk {n}/{forsok} feilet ({e}) — nytt om {pause:.0f}s")
                time.sleep(pause)
    raise RuntimeError(f"ga opp etter {forsok} forsøk: {url}\n  siste feil: {sist}")


def vendorfil(navn, url):
    """Les fra vendor/, eller last ned og lagre der første gang."""
    sti = VENDOR / navn
    if sti.exists():
        return sti.read_bytes()
    VENDOR.mkdir(exist_ok=True)
    print(f"  ↓ henter {navn}")
    data = hent(url)
    sti.write_bytes(data)
    return data


def data_uri(raw, mime):
    return f"data:{mime};base64," + base64.b64encode(raw).decode("ascii")


# ------------------------------------------------------------------- felles

def signatur():
    """Hash av alt som påvirker resultatet."""
    h = hashlib.sha256()
    # build.py er med fordi verdier her — BASE_URL, TITLE, BESKRIVELSE — havner
    # i resultatet. Uten den ville en endret BASE_URL gitt uendret signatur, og
    # --check ville meldt OK på filer bygget med gammel adresse.
    for f in (SRC, SUPPORT, Path(__file__)):
        h.update(f.read_bytes())
    for f in sorted(ASSETS_WEB.iterdir()):
        if not f.name.startswith("."):
            h.update(f.name.encode())
            h.update(str(f.stat().st_size).encode())
    return h.hexdigest()[:16]


def hode_tagger():
    """Metadata som må stå i den statiske HTML-en.

    Delingstjenester kjører ikke JavaScript. Ligger disse i <helmet> inne i
    <x-dc>, injiseres de av runtimen og crawlerne ser dem aldri.
    """
    return "\n".join([
        f'<title>{TITLE}</title>',
        f'<meta name="description" content="{BESKRIVELSE}">',
        '<meta property="og:type" content="website">',
        '<meta property="og:site_name" content="Höegh Eiendom">',
        f'<meta property="og:title" content="{TITLE}">',
        f'<meta property="og:description" content="{BESKRIVELSE}">',
        f'<meta property="og:url" content="{BASE_URL}/">',
        f'<meta property="og:image" content="{BASE_URL}/og-image.jpg">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<meta property="og:locale" content="nb_NO">',
        '<meta name="twitter:card" content="summary_large_image">',
        '<link rel="icon" href="/favicon.svg" type="image/svg+xml">',
        # Runtimen utleder rotkomponentens navn fra filnavnet (dcNameFromPath).
        # Uten dette blir navnet "index", <x-dc> finnes aldri, og siden rendrer
        # rå kildekode.
        f'<base href="{SRC.name}">',
    ])


def resources_script(support_src):
    """window.__resources — må være satt uansett utgave.

    Uten den re-fetcher runtimen sin egen side og kjører parseDcText på rå
    tekst. Regexen treffer da strengen "<x-dc>" som står i en feilmelding inne
    i den inlinede support.js, før det ekte elementet, og siden rendrer rå
    JS-kildekode. Verdiene mapper React-URL-ene til inlinede kopier.
    """
    mapping = {}
    for url in re.findall(r'var REACT(?:_DOM)?_URL = "([^"]+)"', support_src):
        navn = url.rsplit("/", 1)[-1]
        mapping[url] = data_uri(vendorfil(navn, url), "text/javascript")
    payload = json.dumps(mapping).replace("</", "<\\/")
    return f"<script>window.__resources = {payload};</script>"


def grunnlag():
    html = SRC.read_text(encoding="utf-8")
    html = re.sub(r'\s*<meta name="ext-resource-dependency"[^>]*>', "", html)
    html = html.replace("<html>", '<html lang="no">', 1)
    html = html.replace('<meta charset="utf-8">',
                        f'<meta charset="utf-8">\n{hode_tagger()}', 1)

    tag = '<script src="./support.js"></script>'
    if tag not in html:
        sys.exit(f"FEIL: fant ikke {tag} i kilden — er den endret?")
    support_src = SUPPORT.read_text(encoding="utf-8")
    html = html.replace(tag, resources_script(support_src)
                        + f"\n<script>\n{support_src}\n</script>")
    return html + "\n" + STEMPEL.format(signatur()) + "\n"


# ------------------------------------------------------------------ utgaver

def bygg_web(html):
    html = html.replace("assets/", "assets-web/")

    def lat(m):
        tag = m.group(0)
        if any(n in tag for n in IKKE_LAT) or "loading=" in tag:
            return tag
        return tag[:4] + ' loading="lazy" decoding="async"' + tag[4:]
    html = re.sub(r"<img\b[^>]*>", lat, html)

    if "data:image" in html:
        sys.exit("FEIL: web-utgaven skal ikke inneholde inlinede bilder")
    return html


def bygg_standalone(html):
    for path in sorted(ASSETS_WEB.iterdir(), key=lambda p: -len(p.name)):
        if path.name.startswith("."):
            continue
        ref = f"assets/{path.name}"
        if ref not in html:
            continue
        mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        html = html.replace(ref, data_uri(path.read_bytes(), mime))

    m = re.search(r'<link\s+href="(https://fonts\.googleapis\.com/css2[^"]+)"[^>]*>', html)
    if m:
        css = vendorfil("fonts.css", m.group(1).replace("&amp;", "&")).decode("utf-8")
        for url in sorted(set(re.findall(r"url\((https://fonts\.gstatic\.com/[^)]+)\)", css))):
            navn = "font-" + hashlib.sha1(url.encode()).hexdigest()[:12] + ".woff2"
            css = css.replace(url, data_uri(vendorfil(navn, url), "font/woff2"))
        html = html.replace(m.group(0), f"<style>\n{css}\n</style>")

    rest = sorted(set(re.findall(r"assets/[A-Za-z0-9_.-]+", html)))
    if rest:
        sys.exit(f"FEIL: uinlinede referanser igjen: {rest}")
    return html


# -------------------------------------------------------------------- kjør

def kontroller():
    sig = signatur()
    stempel = STEMPEL.format(sig)
    avvik = []
    for f in (WEB_UT, STANDALONE_UT):
        if not f.exists():
            avvik.append(f"{f.name}: finnes ikke")
        elif stempel not in f.read_text(encoding="utf-8"):
            avvik.append(f"{f.name}: bygget fra en eldre kilde")
    if avvik:
        print("UTDATERT:")
        for a in avvik:
            print("  -", a)
        print("\nKjør: python3 build.py")
        sys.exit(1)
    print(f"OK — begge utgavene er bygget fra kilden ({sig})")


def main():
    if "--check" in sys.argv:
        return kontroller()

    bare_web = "--web" in sys.argv
    felles = grunnlag()

    # Bygg ferdig i minnet før noe skrives, så utgavene aldri spriker.
    web = bygg_web(felles)
    standalone = None if bare_web else bygg_standalone(felles)

    WEB_UT.write_text(web, encoding="utf-8")
    print(f"Skrev {WEB_UT.name} ({len(web.encode()) // 1024} KB)")
    if standalone is not None:
        STANDALONE_UT.write_text(standalone, encoding="utf-8")
        print(f"Skrev {STANDALONE_UT.name} ({len(standalone.encode()) // 1024} KB)")
    elif STANDALONE_UT.exists():
        print(f"MERK: {STANDALONE_UT.name} er nå utdatert (--web). "
              f"Kjør uten --web før deling.")


if __name__ == "__main__":
    main()
