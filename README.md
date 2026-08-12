# Hammersborg – OUW

Nabolags-onepager for **Hammersborgkvartalet** under Oslo Urban Week
(22. september, Storsalen på Tempelet). Målet er påmelding til de to arrangementene.

Eier: Höegh Eiendom · Publisert: https://hammersborg.netlify.app/

Netlify deployer automatisk fra `main`. Pusher du, går det rett ut.

## Innhold

| Sti | Hva |
|---|---|
| `src/Hammersborgkvartalet.dc.html` | **Kildefil — rediger her.** All inline-CSS per seksjon. |
| `src/support.js` | Runtime som kildefilen krever. Ikke rediger. |
| `assets/` | Originalbildene i full oppløsning. Kilde for bygget, serveres ikke. |
| `assets-web/` | Skalerte bilder som faktisk serveres. Skrives for hånd, se under. |
| `build.py` | Bygger begge utgavene. Kjøres etter hver endring. |
| `index.html` | **Bygget — rediger aldri.** Web-utgaven Netlify publiserer. ~270 KB. |
| `hammersborg-standalone.html` | **Bygget.** Alt i én fil, virker uten nett. Til deling som vedlegg. |
| `netlify.toml` | Skjermer interne filer, og setter mellomlagring på bildene. |
| `docs/HUBSPOT.md` | Implementeringsnotater for HubSpot: skjema, designtokens. |

## Gjøre endringer

1. Rediger `src/Hammersborgkvartalet.dc.html`.
2. Bygg:

   ```bash
   python3 build.py
   ```

   Skriver `index.html` og `hammersborg-standalone.html`. Bygget henter React —
   og fonter til den selvstendige utgaven — fra nett. `--web` bygger bare
   web-utgaven og går raskere.
3. Se resultatet: åpne `index.html` i nettleser.

## To utgaver, og hvorfor

`index.html` er **271 KB** og henter bildene som egne filer fra `assets-web/`.
Nettleseren kan da vise teksten før bildene er nede, laste dem etter hvert som
man scroller, og mellomlagre dem til neste besøk.

`hammersborg-standalone.html` er **5,9 MB** med alt inlinet. Den virker uten nett
og uten filer ved siden av, og er den du sender som vedlegg.

Tidligere var `index.html` selv 11,1 MB, fordi alle bildene lå base64-kodet i
HTML-en. Ingenting vistes før hele fila var lastet ned — på mobilnett 15–20
sekunder blank skjerm.

### Når bildene endres

`assets-web/` genereres ikke av `build.py`. Legger du til eller bytter et bilde,
må du skalere det manuelt:

```bash
cp assets/nytt.jpg assets-web/ && sips -Z 1400 -s formatOptions 60 assets-web/nytt.jpg
```

Hero-bildet tåler 2200 px; kortbilder klarer seg med 1400. Er originalen alt
mindre enn målet, la den være — re-koding gjør små filer større.

### Live forhåndsvisning mens du jobber

```bash
python3 -m http.server 8765
```

Åpne `http://localhost:8765/src/Hammersborgkvartalet.dc.html`. Da slipper du å
bygge for hver småendring — bare last siden på nytt. Symlinken `src/assets`
finnes bare for at bildene skal løses riktig i denne visningen.

To 404-er på `{{ ev.img }}` og `{{ ft.img }}` i konsollen er ufarlige: nettleseren
prøver å laste dem før runtime-en rekker å fylle inn malen.

## GitHub Pages

Settings → Pages → Source: `main` / mappe `/docs`. Siden blir liggende på
`https://hoegh-eiendom.github.io/hammersborg-ouw/`.

Merk: siden publiseres via Netlify fra `main`, ikke via GitHub Pages.
ikke har det, del `index.html` som fil i stedet — den virker frittstående, uten
nett og uten `assets/`-mappa ved siden av.

## Viktig om skjemaet

Påmeldingsskjemaet er et **ekte HubSpot-skjema** (portal 25006101, form-id
`6b0bdd6e-…`). Innsendinger havner i Höegh Eiendoms CRM. Åpner du siden og sender
inn, opprettes en reell kontakt.

To konsekvenser:

- **Skjemaet krever nettilgang.** Resten av siden virker uten nett, men
  skjemaseksjonen står tom uten tilkobling.
- **Utformingen av skjemaet settes i HubSpot,** ikke her. Det rendres i en
  kryssdomene-iframe, så CSS fra siden når ikke inn. Se `docs/hubspot-form.css`.

## Arbeidsflyt

Design itereres i prototypen. Utvikler gjør en engangs-oppbygging i HubSpot ut fra
`docs/HUBSPOT.md`. Etterpå gjøres små tekst-/bildeendringer i HubSpot; større
redesign prototypes her først. Dette repoet er ikke koblet til HubSpot — endringer
her oppdaterer ikke den publiserte siden automatisk.

## Bilderettigheter

**Avklart:** Höegh Eiendom eier bildene selv. De kan brukes offentlig.

Fotnoten krediterer dem som «Illustrasjonsfoto – Höegh Eiendom 2026».
«Illustrasjonsfoto» er med av en grunn: bildene viser et uoppført prosjekt, og
merkingen hindrer at de leses som foto av noe som står der i dag.
