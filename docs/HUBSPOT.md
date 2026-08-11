# Utviklerpakke: Hammersborgkvartalet – nabolags-onepager (HubSpot)

## Formål
Én landingsside som får naboer og lokale brukere til å melde seg på Hammersborgkvartalets
to arrangementer under Oslo Urban Week (22. september, Storsalen på Tempelet).

## Omfang — les dette først
**Besluttet: siden bygges ikke opp på nytt i HubSpot.** Prototypen i dette repoet
er selve leveransen, og `index.html` er den publiserbare fila.

Det eneste som skal inn i HubSpot er **påmeldingsskjemaet**, slik at påmeldingene
havner i CRM-et. Se «Påmeldingsskjema» under.

Avsnittene om moduloppbygging, kart og designtokens lenger ned er beholdt som
referanse om siden senere likevel skal porteres til HubSpot. De er ikke oppgaven nå.

## Om filene i denne pakken
Filene her er en **designreferanse laget i HTML** – en prototype som viser ønsket utseende og
oppførsel. Det er **ikke** produksjonskode som skal limes rett inn. Oppgaven er å **gjenskape
dette designet i HubSpot** med CMS-moduler (HubL) og et ekte HubSpot-skjema, slik at
markedsteamet kan redigere innhold selv.

- `index.html` – hele siden som én selvstendig fil (åpne i nettleser for å se ferdig
  design, alle bilder/fonter inkludert). Bruk denne som «fasit» på utseende.
  Bygget fra kilden med `python3 build.py` — rediger den aldri direkte.
- `src/Hammersborgkvartalet.dc.html` – kildemarkup med all inline-CSS per seksjon. Herfra
  henter du eksakte farger, spacing, fontstørrelser og struktur.
- `assets/` – alle bilder (hentet fra prosjektets presentasjons-PDF) og HE-logo.

## Fidelity
**Høy (hi-fi).** Endelige farger, typografi, spacing og interaksjoner. Gjenskap pikselnært.

## Anbefalt HubSpot-oppbygging
Bygg siden som en template med selvstendige moduler, i denne rekkefølgen (topp → bunn). Hver
modul bør ha redigerbare felt (tekst/bilde/lenke) så teamet kan oppdatere uten utvikler.

1. **Hero** – fullflate bakgrunnsbilde (`img00.jpg`), mørk gradient-overlay, HE-logo oppe til
   venstre, nav-lenker + «Meld deg på»-knapp, stor tittel (Newsreader serif), ingress og to CTA-er.
   Felt: bakgrunnsbilde, eyebrow-tekst, tittel, ingress, knappetekster.
2. **Arrangementer** – to kort (bilde, tag-badge, tid/sted, tittel, beskrivelse, CTA).
   Bygg som en **repeterbar modul** (HubL `{% for %}` eller gjentakbar gruppe).
3. **Påmelding** – teglrød seksjon. **Her plasseres HubSpot-skjemaet** (se eget avsnitt under).
4. **Prosjektet** – tekst + stort bilde (`img04.jpg`) + faktastripe (6 nøkkeltall).
5. **Hva skjer** – 4 bildekort (passasjen, torget, gateplan, grønne møteplasser).
6. **Nabolaget** – tekst + bilde (`img03.jpg`) + **Google Maps-innbygging** (iframe, se under).
7. **Bærekraft** – lys salvie-grønn seksjon: innrammet bilde (`img13.jpg`) + 3 punktkort.
8. **Footer** – mørk. HE-logo, avsluttende CTA, kontakt-/arrangementsinfo.

## Påmeldingsskjema (VIKTIG)

**Status: opprettet og bygget inn.** Form-id `6b0bdd6e-28e1-4ea9-b6cf-c3553dcf5fdc`,
portal 25006101, region eu1. Embed-en ligger i påmeldingsseksjonen i kildefila, og
skjemaet rendres i en kryssdomene-iframe — utformingen settes derfor i HubSpots
skjema-editor, ikke i CSS på siden.

### Avvik som gjenstår å rette i HubSpot
Verifisert i nettleser 11. august 2026:

1. **«Jeg ønsker å delta på» er ikke påkrevd.** Skal være påkrevd — ingen skal
   kunne melde seg på uten å velge arrangement.
2. **Navn er ikke påkrevd.** Skal være påkrevd.
3. **«Antall personer» er en nedtrekksliste uten standardverdi.** Skal være et
   tallfelt med standardverdi 1 og minimum 1.
4. **Samtykketeksten avviker.** Står som «Jeg godtar å motta annen kommunikasjon
   fra Höegh Eiendom». Skal være: «Jeg samtykker til å bli kontaktet om
   arrangementet og relatert informasjon fra Hammersborgkvartalet.»
5. **Alternativ 2 heter «Ungdom først og minikonsert».** Arrangementskortet på
   siden sier «Ungdom først». Velg én skrivemåte og bruk den begge steder.
6. **Fonten i skjemaet er en generisk sans,** ikke Hanken Grotesk.

Avkrysningene står korrekt umerket, og knappen heter «Send påmelding».

### Opprinnelig spesifikasjon
Beholdt som fasit for punktene over.
- Lag et **HubSpot Form** med feltene: Navn, E-post, Antall personer,
  Avkrysning «ønsker å delta på» (Nabolagstreffet / Ungdom først),
  Samtykke (påkrevd avkrysning). Prototypen har ikke noe kommentarfelt.
- Telefon er bevisst utelatt. Ikke legg det inn.
- «Ønsker å delta på» skal stå **uten** forhåndsavkrysning. Påmelderen velger selv.
- **Validering må bygges i HubSpot.** Kildefilen setter `required` på Navn, E-post
  og Samtykke, men x-dc-runtimen fjerner attributtet — i prototypen validerer
  skjemaet ingenting (`form.checkValidity()` gir `true` på et tomt skjema).
  Samtykke må være påkrevd i HubSpot-skjemaet.
- **Minst én av «ønsker å delta på» skal være påkrevd.** Ingen skal kunne melde
  seg på uten å velge arrangement. I HubSpot settes dette ved å gjøre
  avkrysningsgruppa til et påkrevd felt.

- Legg skjemaet inn i påmeldingsseksjonen via HubSpots skjema-modul.
- «Meld deg på»-knappene i hero/arrangementer/footer skal scrolle til skjemaseksjonen
  (anker-lenke til seksjonens id).

### Ferdig brief og styling
`docs/hubspot-brief.md` er en ferdig tekst å lime rett inn i HubSpots
AI-assistent: felt, rekkefølge, påkrevd-regler, ordrett samtykketekst,
knappetekst og bekreftelsesmelding.

`docs/hubspot-form.css` gir skjemaet samme utseende som prototypen — grid med tre
felt på én linje, pillene for arrangementsvalg, knapp og feilmeldinger. Verdiene
er hentet fra kildefila; endres designet der, må CSS-en oppdateres tilsvarende.

CSS-en er testet mot HubSpots standard-markup på 1332px og 375px. Klassenavnene er
HubSpots vanlige (`.hs-form`, `.hs-input`, `.hs-form-checkbox`, `.hs-button`),
men markup varierer mellom HubSpot-versjoner — stemmer ikke en selektor, inspiser
det faktiske skjemaet og juster.

Rendres skjemaet i en `<iframe>`, når CSS fra siden det ikke. Sjekk det først om
stilen ikke slår inn.

`docs/hubspot-form-api.md` er et alternativ til begge: ferdige API-kall som
oppretter de to kontaktegenskapene og skjemaet direkte. Krever et private app
token med scopene `forms` og `crm.schemas.contacts.write`.

## Kart
Google Maps-innbygging (iframe med `/maps/embed?pb=…`, adresse Akersgata 73, 0180 Oslo).
Ligger i Nabolaget-seksjonen. Kopier iframe-src fra kildefilen. Merk: den enkle
`output=embed`-varianten blokkeres i noen sandkasser – bruk `/maps/embed?pb=`-formen.

## Designtokens
Farger:
- Krem bakgrunn: `#F1E7D6` · lys kort: `#FBF5EA` · sekundær flate: `#EADCC5`
- Primær teglrød: `#7C3226` · aksent kobber/oransje: `#C97A4A` · lenke-hover: `#B56349`
- Tekst mørk: `#2A211B` · tekst dempet: `#5C4E43` / `#6B5D50`
- Salvie-grønn seksjon: bakgrunn `#DCE1D2`, kort `#F3F5EC`, kant `#CDD3BE`, aksent `#5E6B4C`
- Grønn event-badge: `#71806A`
- Footer/mørk: `#2A211B`

Typografi:
- Overskrifter: **Newsreader** (serif), weight 400–500, negativ letter-spacing ~-0.01em
- Brødtekst/UI: **Hanken Grotesk**, weight 400–700
- Eyebrow: 0.8rem, uppercase, letter-spacing 0.16em, weight 600

Form:
- Border-radius: kort 18–22px, knapper/pills 999px, felt 12px
- Kort-kant: `1px solid #E4D6C0`
- Seksjons-padding: `clamp(64px,9vw,116px)` vertikalt

## Responsivt
- Alle rutenett bruker `auto-fit`/flex og stabler til én kolonne på mobil.
- Nav-lenkene skjules på mobil (kun logo + «Meld deg på» vises).
- Egen fast «Meld deg på»-linje nederst på mobil (sticky bar).

## Assets
Alle bilder ligger i `assets/` (hentet fra `Hammersborgkvartalet_generell_v2.pdf`):
- `img00.jpg` hero · `img03.jpg` nabolag · `img04.jpg` prosjekt-aksonometri
- `img06/07/09.jpg` gateplan/passasje/torg · `img13.jpg` Sirkelhagen · `img29.jpg` nabolagstreff
- `he-logo-hvit.png` Höegh Eiendom-logo (hvit, én linje)

Bekreft med Höegh Eiendom at bildene kan brukes offentlig på publisert side.

## Ansvarsfordeling / arbeidsflyt
- Design godkjennes i prototypen (rask iterasjon).
- Utvikler gjør **engangs-oppbygging** i HubSpot ut fra denne pakken.
- Etterpå: små tekst-/bildeendringer gjøres i HubSpot. Større redesign prototypes her først,
  deretter porteres til HubSpot. Denne filen er ikke koblet til HubSpot – endringer her
  oppdaterer ikke den publiserte siden automatisk.
