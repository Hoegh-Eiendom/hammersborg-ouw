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

   Skriver `index.html` og `hammersborg-standalone.html`. Tar under ett sekund
   og **krever ikke nett** — React og fontene ligger i `vendor/`.
3. Se resultatet: åpne `index.html` i nettleser.

### Kontroller før deploy

```bash
python3 build.py --check
```

Sier fra om filene på disk er bygget fra gjeldende kilde. Gir exitkode 1 hvis
noe er utdatert, så den kan brukes i et skript.

Bygget skriver en kildesignatur nederst i begge filene. `--check` sammenligner
den med en hash av kilden, support.js og innholdet i `assets-web/`.

### To ting som gjør bygget forutsigbart

**Begge utgavene bygges ferdig i minnet før noen skrives.** Feiler den ene,
skrives ingen. Tidligere kunne `index.html` bli oppdatert mens den selvstendige
utgaven ble liggende igjen på forrige versjon — det skjedde, uten at noe sa fra.

**Ingen nettverksavhengighet.** React og fontene lå tidligere bak 13
nedlastinger per bygg, og en enkelt 404 fra Google Fonts veltet hele
byggingen. Nå leses de fra `vendor/`, som er sjekket inn. Mangler en fil,
lastes den ned én gang og lagres — med fire forsøk. Slett `vendor/` for å
tvinge ny nedlasting.

`--web` bygger bare web-utgaven. Da blir den selvstendige utdatert, og både
byggingen og `--check` sier fra.

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

## Publisering

Netlify bygger fra `main` og serverer repo-rota. Push til `main` går rett ut på
https://hammersborg.netlify.app/ — ingen manuell publisering.

Fordi rota serveres, ville alt i repoet vært offentlig lesbart. `netlify.toml`
skjermer `docs/`, `src/`, `build.py`, `README.md` og `assets/`.

GitHub Pages er ikke i bruk.

## Viktig om skjemaet

Påmeldingen skjer på en **ekstern HubSpot-side**, ikke på denne siden.
Påmeldingsseksjonen inneholder en utgående lenke:

```
https://evytx.share-eu1.hsforms.com/2_PDcehZhRH6M8jWpA1CGFw
```

Skjemaet var tidligere bygget inn med HubSpots embed-skript. Det er tatt ut, så
siden avhenger ikke lenger av at et tredjepartsskript laster.

`docs/hubspot-form.css` er derfor **ikke i bruk**. Den er beholdt i tilfelle
skjemaet skal bygges inn igjen.

## Arbeidsflyt

Design itereres i kildefila her, bygges med `build.py`, og pushes. Netlify
deployer automatisk.

Skjemaet lever i HubSpot og redigeres der — se `docs/HUBSPOT.md` for
feltspesifikasjonen. Endringer i skjemaet påvirker ikke denne siden, og omvendt;
det eneste bindeleddet er lenka over.

## Bilderettigheter

**Avklart:** Höegh Eiendom eier bildene selv. De kan brukes offentlig.

Fotnoten krediterer dem som «Illustrasjonsfoto – Höegh Eiendom 2026».
«Illustrasjonsfoto» er med av en grunn: bildene viser et uoppført prosjekt, og
merkingen hindrer at de leses som foto av noe som står der i dag.
