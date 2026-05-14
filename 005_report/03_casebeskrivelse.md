# Kapittel 3 – Casebeskrivelse

Dette kapittelet beskriver Byggmakker Gravdal som case for prosjektet. Formålet er å gi leseren den kontekstuelle informasjonen som er nødvendig for å forstå rammene for analysen.

---

## 3.1 Om Byggmakker Gravdal

Byggmakker Gravdal er en byggevarebedrift tilknyttet Byggmakker-kjeden, som er en av Norges ledende aktører innen salg av byggevarer. Byggmakker opererer som en franchisekjede der de enkelte butikkene drives av lokale eiere, men med felles innkjøpsavtaler, sortiment og kjedetilhørighet. Byggmakker Gravdal betjener både privatmarkedet og et betydelig segment av profesjonelle kunder, herunder håndverkere og entreprenører.

---

## 3.2 Sortiment og produktkategorier

Byggmakker Gravdal fører et bredt sortiment av byggevarer. For dette prosjektet avgrenses analysen til fire utvalgte produkter med god salgshistorikk og høy relevans for lagerstyring:

**Tabell 3.1 – Analyserte produkter**

| Produkt | Dimensjon | Kategori | Etterspørselsmønster |
|---|---|---|---|
| Terrassebord | 28x120 mm | Trelast | Sterk sesong (vår/sommer) |
| Konstruksjonstre | 48x98 mm | Trelast | Sesong (vår/sommer) |
| Terrasseskrue | 4,2x55 mm | Festemidler | Sesong (følger terrassebord) |
| Universalskrue | 5x90 mm | Festemidler | Jevn hele året |

Produktene er valgt ut fra kriterier om omløpshastighet, sesongvariasjon og relevans for lagerstyring. Trelastproduktene selges i løpende meter (RM) og festemidlene i pakker (PAK).

---

## 3.3 Innkjøp og varebestilling i dag

Varebestillingen hos Byggmakker Gravdal følger i dag en kombinasjon av manuell vurdering og systemstøtte gjennom Byggmakker-kjedens ERP-løsning. Bestilling initieres typisk på bakgrunn av erfaring og visuell kontroll av lagerbeholdning. Trelast og festemidler bestilles fra to ulike leverandører, noe som betyr at disse produktgruppene må styres separat. Ledetiden fra bestilling til levering er typisk én uke for begge leverandører.

Bedriften har ved flere anledninger opplevd utsalgssituasjoner for trelastprodukter i høysesong, noe som bekrefter behovet for et mer systematisk prognoseverktøy. I tillegg gjennomføres det sesongkampanjer på terrasseprodukter, noe som kan skape kunstige salgstopper i dataene.

Utfordringer knyttet til dagens system inkluderer at bestillingsbeslutninger baseres i stor grad på individuell erfaring fremfor systematisk dataanalyse, at sesongvariasjoner håndteres manuelt, og at det finnes begrenset systematisk evaluering av prognosetreffprosent eller lagerkostnader.

---

## 3.4 Datagrunnlag og tilgang

Prosjektet benytter historiske salgsdata fra Byggmakker Gravdals ERP-system. Dataene dekker perioden januar 2024 til april 2026, noe som gir 116 ukentlige observasjoner per produkt. Dataene er eksportert som Excel-fil og inneholder ukentlig salg per produkt.

En viktig begrensning er at datahistorikken kun dekker én fullstendig sesongssyklus grunnet systembytte hos bedriften. Dette begrenser modellens grunnlag for sesongestimering og diskuteres nærmere i kapittel 7.

*Datafil: `002_data/raw/salgsrapport Oskar v2.xlsx`*

---

## Skrivenotater
<!-- Bruk denne seksjonen til egne notater under skriving -->
