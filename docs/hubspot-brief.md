# Brief til HubSpot AI

Teksten under limes rett inn i HubSpots AI-assistent. Den er skrevet for å bli
lest av en AI, ikke av et menneske — derfor er den kommanderende og eksplisitt.

Alle verdier er hentet fra `src/Hammersborgkvartalet.dc.html`. Endres skjemaet i
prototypen, må denne briefen oppdateres.

---

Lag et påmeldingsskjema i HubSpot etter spesifikasjonen under. Følg den helt ut,
og legg ikke til felt, tekster eller elementer som ikke står her.

**Navn på skjema:** Påmelding – Hammersborgkvartalet, Oslo Urban Week 2026

**Formål:** Påmelding til to nabolagsarrangementer under Oslo Urban Week,
tirsdag 22. september 2026, i Storsalen på Tempelet, Kommandør T. I. Øgrims
plass 4. Arrangement 1: nabolagstreff kl. 16:00–18:00. Arrangement 2: «Ungdom
først», samtale og konsert kl. 18:00–19:30. Målgruppen er naboer og lokale
aktører i Hammersborg.

## Felt, i denne rekkefølgen

1. **Navn** — enkeltlinje tekst — påkrevd — plassholder: `Ditt navn`
2. **E-post** — e-post — påkrevd — plassholder: `navn@epost.no`
3. **Antall personer** — tall — ikke påkrevd — standardverdi `1` — minimum `1`
4. **Jeg ønsker å delta på** — flervalg med avkrysningsbokser — påkrevd, minst
   ett valg må gjøres. To alternativer, i denne rekkefølgen:
   - `Nabolagstreffet`
   - `Ungdom først`

   **Ingen av dem skal være forhåndsavkrysset.** Påmelderen skal velge selv.
5. **Samtykke** — én avkrysningsboks — påkrevd — teksten skal være ordrett:

   > Jeg samtykker til å bli kontaktet om arrangementet og relatert informasjon
   > fra Hammersborgkvartalet.

## Knapp og bekreftelse

- Send-knappen skal hete: `Send påmelding`
- Etter innsending vises en bekreftelsesmelding (ikke omdirigering til egen side):
  - Overskrift: `Takk for påmeldingen!`
  - Tekst: `Vi gleder oss til å se deg under Oslo Urban Week. Du får en bekreftelse på e-post med praktisk informasjon.`

Sender skjemaet en bekreftelse på e-post, skal den inneholde dato, klokkeslett
for det eller de arrangementene personen har valgt, og adressen Kommandør
T. I. Øgrims plass 4.

## Kobling til kontaktegenskaper

- **Navn** kobles til fornavn (`firstname`). Skjemaet har bevisst ett samlet
  navnefelt, ikke fornavn og etternavn hver for seg.
- **E-post** kobles til `email`.
- **Antall personer** og **Jeg ønsker å delta på** finnes ikke som egenskaper i
  dag. Opprett dem som nye egendefinerte kontaktegenskaper med norske
  visningsnavn, i samme stil som de arrangementsegenskapene som allerede finnes
  i porteføljen (for eksempel «Påmelding julebord 2022» og «Hvilken aktivitet vil
  du gjøre?»). Gjenbruk ikke en egenskap fra et tidligere arrangement.
- **Samtykke** håndteres som samtykke til kommunikasjon, ikke som en vanlig
  avkrysningsegenskap.

## Utforming

Skjemaet styles med egen CSS utenfor HubSpot-editoren. Derfor:

- Ikke legg inn egne farger, fonter, skygger eller bakgrunner på skjemaet
- Behold HubSpots standard klassenavn og standard markup
- Skjemaet må rendres i sidens DOM, ikke inne i en iframe, ellers slår ikke
  stilen inn
- Feltene Navn, E-post og Antall personer skal ligge på samme rad når det er
  plass. Legg dem i samme feltgruppe / rad med tre kolonner.
- Sidens fonter er Newsreader (overskrifter) og Hanken Grotesk (tekst og
  skjemafelt). Ikke velg andre fonter.

## Språk

Alt skal være på norsk bokmål. Ikke oversett eller omskriv feltnavnene,
samtykketeksten, knappeteksten eller bekreftelsesmeldingen — de skal stå ordrett
som spesifisert.
