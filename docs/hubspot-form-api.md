# Opprette påmeldingsskjemaet via HubSpots API

Alternativ til å bygge skjemaet manuelt eller med HubSpots AI. Kallene under
oppretter først de to egenskapene skjemaet trenger, deretter selve skjemaet.

## Før du begynner

Du trenger et **private app token** fra HubSpot med disse scopene:

- `forms`
- `crm.schemas.contacts.write`

Lag det selv i HubSpot under Innstillinger → Integrasjoner → Private apper.
**Ikke del tokenet i chatten** — det skal bli hos deg. Kallene under kjører du
selv; sett tokenet i miljøvariabelen `HS_TOKEN` først:

```bash
export HS_TOKEN="ditt-token-her"
```

## Forbehold om formatet

Jeg fikk ikke verifisert dette mot HubSpots dokumentasjon — den krever innlogging,
og de offentlige spesifikasjons-endepunktene svarer 404. Payloadene under er
skrevet ut fra kjennskap til Forms API v3, ikke lest av gjeldende spesifikasjon.

Praktisk betyr det: et feil felt gir en `400` med melding om hva som er galt, og
ingenting blir ødelagt. Men regn med at du kan måtte justere. Delen jeg er minst
sikker på er `legalConsentOptions` — samtykke er også det som må stemme best, så
kontroller den mot dokumentasjonen du har tilgang til.

**GDPR-samtykke må være slått på i porteføljen** (Innstillinger → Personvern og
samtykke) før `legalConsentOptions` kan brukes. Er det av, feiler kallet.

## Steg 1: to nye kontaktegenskaper

Navnekonvensjonen følger de eksisterende arrangementsegenskapene i porteføljen.
`firstname` og `email` finnes fra før og skal ikke opprettes.

```bash
curl -X POST https://api.hubapi.com/crm/v3/properties/contacts \
  -H "Authorization: Bearer $HS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "antall_personer_ouw_2026",
    "label": "Antall personer (OUW 2026)",
    "description": "Antall personer påmeldt til Hammersborgkvartalet under Oslo Urban Week 2026.",
    "groupName": "contactinformation",
    "type": "number",
    "fieldType": "number"
  }'
```

```bash
curl -X POST https://api.hubapi.com/crm/v3/properties/contacts \
  -H "Authorization: Bearer $HS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "onsker_a_delta_pa_ouw_2026",
    "label": "Ønsker å delta på (OUW 2026)",
    "description": "Hvilke av de to arrangementene under Oslo Urban Week 2026 personen melder seg på.",
    "groupName": "contactinformation",
    "type": "enumeration",
    "fieldType": "checkbox",
    "options": [
      { "label": "Nabolagstreffet", "value": "Nabolagstreffet", "displayOrder": 0 },
      { "label": "Ungdom først",    "value": "Ungdom først",    "displayOrder": 1 }
    ]
  }'
```

`fieldType: "checkbox"` betyr flere avkrysningsbokser i HubSpot. En enkelt
av/på-boks heter `booleancheckbox` — det er ikke det vi vil her.

## Steg 2: skjemaet

Feltene ligger i to grupper med vilje. Én `fieldGroup` er én rad, så de tre
første feltene havner på samme linje — slik prototypen og `hubspot-form.css`
forutsetter.

```bash
curl -X POST https://api.hubapi.com/marketing/v3/forms/ \
  -H "Authorization: Bearer $HS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Påmelding – Hammersborgkvartalet, Oslo Urban Week 2026",
    "formType": "hubspot",
    "archived": false,
    "fieldGroups": [
      {
        "groupType": "default_group",
        "richTextType": "text",
        "fields": [
          {
            "objectTypeId": "0-1",
            "name": "firstname",
            "label": "Navn",
            "fieldType": "single_line_text",
            "required": true,
            "hidden": false,
            "placeholder": "Ditt navn"
          },
          {
            "objectTypeId": "0-1",
            "name": "email",
            "label": "E-post",
            "fieldType": "email",
            "required": true,
            "hidden": false,
            "placeholder": "navn@epost.no"
          },
          {
            "objectTypeId": "0-1",
            "name": "antall_personer_ouw_2026",
            "label": "Antall personer",
            "fieldType": "number",
            "required": false,
            "hidden": false,
            "defaultValue": "1"
          }
        ]
      },
      {
        "groupType": "default_group",
        "richTextType": "text",
        "fields": [
          {
            "objectTypeId": "0-1",
            "name": "onsker_a_delta_pa_ouw_2026",
            "label": "Jeg ønsker å delta på",
            "fieldType": "multiple_checkboxes",
            "required": true,
            "hidden": false,
            "options": [
              { "label": "Nabolagstreffet", "value": "Nabolagstreffet", "displayOrder": 0 },
              { "label": "Ungdom først",    "value": "Ungdom først",    "displayOrder": 1 }
            ]
          }
        ]
      }
    ],
    "configuration": {
      "language": "nb",
      "cloneable": true,
      "editable": true,
      "archivable": true,
      "recaptchaEnabled": false,
      "notifyContactOwner": false,
      "notifyRecipients": [],
      "createNewContactForNewEmail": false,
      "prePopulateKnownValues": false,
      "allowLinkToResetKnownValues": false,
      "postSubmitAction": {
        "type": "thank_you",
        "value": "<h2>Takk for påmeldingen!</h2><p>Vi gleder oss til å se deg under Oslo Urban Week. Du får en bekreftelse på e-post med praktisk informasjon.</p>"
      }
    },
    "displayOptions": {
      "renderRawHtml": true,
      "theme": "default",
      "submitButtonText": "Send påmelding",
      "cssClass": ""
    },
    "legalConsentOptions": {
      "type": "explicit_consent_to_process",
      "consentToProcessCheckboxLabel": "Jeg samtykker til å bli kontaktet om arrangementet og relatert informasjon fra Hammersborgkvartalet.",
      "communicationsCheckboxes": [],
      "privacyText": "",
      "consentToProcessFooterText": ""
    }
  }'
```

To valg verdt å merke seg:

- `renderRawHtml: true` gjør at HubSpot ikke legger på sin egen styling. Det er
  forutsetningen for at `hubspot-form.css` skal virke.
- `prePopulateKnownValues: false` gjør at feltene ikke fylles ut på forhånd for
  kjente kontakter. Er den `true`, kan avkrysningene komme forhåndsvalgt for
  noen — stikk i strid med at påmelderen skal velge selv.

## Steg 3: kontroller

Svaret inneholder skjemaets `id` (guid). Bruk den når du bygger skjemaet inn på
siden. Kontroller så i HubSpot at:

- Ingen av de to arrangementsvalgene er forhåndsavkrysset
- Både Navn, E-post, «Jeg ønsker å delta på» og samtykke er påkrevd
- «Antall personer» har standardverdi 1 og ikke er påkrevd
- Send-knappen heter «Send påmelding»

Deretter legger du inn `hubspot-form.css` for utformingen.
