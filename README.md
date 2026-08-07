# Hammersborg – OUW

Nabolags-onepager for **Hammersborgkvartalet** under Oslo Urban Week
(22. september, Storsalen på Tempelet). Målet er påmelding til de to arrangementene.

Eier: Höegh Eiendom · Status: designprototype, klar for HubSpot-oppbygging

## Innhold

| Sti | Hva |
|---|---|
| `index.html` | Hele siden som én selvstendig fil. Åpne i nettleser — ingen bygg, ingen avhengigheter. |
| `src/Hammersborgkvartalet.dc.html` | Kildefil med all inline-CSS per seksjon. Rediger her. |
| `src/support.js` | Runtime som kildefilen krever. |
| `assets/` | Bilder (hentet fra prosjekt-PDF) og Höegh Eiendom-logo. |
| `docs/HUBSPOT.md` | Implementeringsnotater for HubSpot: modul-kartlegging, skjema, designtokens. |
| `docs/index.html` | Kopi for GitHub Pages. |

## Se siden

Åpne `index.html` direkte i en nettleser.

## GitHub Pages

Settings → Pages → Source: `main` / mappe `/docs`. Siden blir liggende på
`https://hoegh-eiendom.github.io/hammersborg-ouw/`.

Merk: på privat repo krever Pages betalt GitHub-plan. Er repoet privat og dere
ikke har det, del `index.html` som fil i stedet.

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

Bildene er hentet fra prosjektets presentasjon. Bekreft internt at de kan brukes
offentlig før publisering.
