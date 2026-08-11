# Hammersborg – OUW

Nabolags-onepager for **Hammersborgkvartalet** under Oslo Urban Week
(22. september, Storsalen på Tempelet). Målet er påmelding til de to arrangementene.

Eier: Höegh Eiendom · Status: designprototype, klar for HubSpot-oppbygging

## Innhold

| Sti | Hva |
|---|---|
| `src/Hammersborgkvartalet.dc.html` | **Kildefil — rediger her.** All inline-CSS per seksjon. |
| `src/support.js` | Runtime som kildefilen krever. Ikke rediger. |
| `assets/` | Bilder (hentet fra prosjekt-PDF) og Höegh Eiendom-logo. |
| `build.py` | Bygger `index.html` fra kilden. Kjøres etter hver endring. |
| `index.html` | **Bygget fil — rediger aldri direkte.** Hele siden i én fil, virker uten nett. |
| `docs/index.html` | Identisk kopi for GitHub Pages, skrives av samme bygg. |
| `docs/HUBSPOT.md` | Implementeringsnotater for HubSpot: modul-kartlegging, skjema, designtokens. |

## Gjøre endringer

1. Rediger `src/Hammersborgkvartalet.dc.html`.
2. Bygg:

   ```bash
   python3 build.py
   ```

   Skriver både `index.html` og `docs/index.html`. Bygget henter fonter og React
   fra nett; `python3 build.py --no-fonts` hopper over det, men da krever den
   ferdige fila nettilgang for typografi.
3. Se resultatet: åpne `index.html` i nettleser.

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

Merk: på privat repo krever Pages betalt GitHub-plan. Er repoet privat og dere
ikke har det, del `index.html` som fil i stedet — den virker frittstående, uten
nett og uten `assets/`-mappa ved siden av.

## Viktig om skjemaet

Påmeldingsskjemaet i prototypen er **kun visuelt og lagrer ingen data**. Ved
oppbygging i HubSpot må det erstattes med et ekte HubSpot Form — se
`docs/HUBSPOT.md`.

## Arbeidsflyt

Design itereres i prototypen. Utvikler gjør en engangs-oppbygging i HubSpot ut fra
`docs/HUBSPOT.md`. Etterpå gjøres små tekst-/bildeendringer i HubSpot; større
redesign prototypes her først. Dette repoet er ikke koblet til HubSpot — endringer
her oppdaterer ikke den publiserte siden automatisk.

## Bilderettigheter

Bildene er hentet fra prosjektets presentasjon. Fotnoten krediterer dem som
«Illustrasjonsfoto – Höegh Eiendom 2026».

Krediteringen er en merking, ikke en klarering: den sier hvem bildene tilhører og
at de viser et uoppført prosjekt, men den bekrefter ikke i seg selv at de kan
brukes offentlig. Er noen av illustrasjonene laget av eksternt arkitekt- eller
visualiseringsbyrå, kan byrået ha rett på egen kreditering. Sjekk internt før
siden publiseres.
