# CLAUDE.md – LOG650 Prosjektveiledning

## Om prosjektet

**Kurs:** LOG650 – Kvantitative metoder i logistikk  
**Institusjon:** Høgskolen i Molde  
**Student:** Oskar Eide  
**Problemstilling:** Hvordan kan etterspørselsprognoser og kunstig intelligens brukes til å forbedre lagerstyringen for utvalgte varer hos Byggmakker Gravdal?

Rapporten er strukturert i 8 kapitler og analyserer fire konkrete produkter fra Byggmakker Gravdals sortiment ved hjelp av SARIMA, Gradient Boosting og klassisk lagerstyringsteoori (EOQ, ROP, SS).

---

## Mappestruktur

```
LOG650/
├── CLAUDE.md                  # Denne filen
├── README.md                  # Prosjektsammendrag med resultater
├── 001_info/
│   └── LOG650 - Oskar Eide - 1 Utkast.pdf   # Gjeldende rapportutkast
├── 002_data/
│   ├── raw/                   # Rådata fra ERP (Excel-eksport)
│   └── processed/             # Renset og aggregert data (Python-output)
├── 003_references/            # PDF-er av vitenskapelige artikler og bøker
├── 004_scripts/               # Python-kode (analyse, modellering, figurer)
└── 005_report/
    ├── figures/               # Grafer og visualiseringer generert fra scripts
    ├── 01_introduksjon.md
    ├── 02_teori_og_litteratur.md
    ├── 03_casebeskrivelse.md
    ├── 04_data_og_metode.md
    ├── 05_modellering.md
    ├── 06_analyse_og_resultater.md
    ├── 07_diskusjon.md
    └── 08_konklusjon.md
```

---

## Nøkkelinformasjon Claude skal ha i bakhodet

### Produkter og data
- Fire produkter: terrassebord 28x120 mm, konstruksjonstre 48x98 mm, terrasseskrue 4,2x55 mm, universalskrue 5x90 mm
- 116 ukentlige observasjoner, jan 2024 – apr 2026
- Datakilde: Byggmakker Gravdals ERP-system (Excel-eksport)
- Viktig begrensning: kun én fullstendig sesongssyklus pga. ERP-bytte

### Metoder brukt
- ADF-test for stasjonaritet, log-transformasjon + d=1 differensiering
- ACF/PACF-analyse → SARIMA(1,1,1)(1,0,1)₁₃ for alle fire produkter
- Gradient Boosting Regressor (200 est., lr=0.05, max_depth=3)
- Naiv referansemodell (benchmark)
- EOQ, SS = z·σ_d·√L, ROP = μ·L + SS med z=1.645 (95 % servicegrad)
- Lagersimulering: scenario A (erfaringsbasert) vs. scenario B (KI-støttet)

### Nøkkelresultater
- Gradient Boosting beste modell på alle fire produkter i testperioden (lavsesong)
- KI-støttet system reduserer utsalg kraftig: terrassebord 2828→55, planke 4656→1757
- Anbefalt tilnærming: hybrid — systemet genererer anbefalinger, mennesket godkjenner

---

## Hvordan Claude skal hjelpe

### Skriving og innhold
- Hjelp til å skrive og forbedre tekst i kapitelfilene i `005_report/`
- Bruk alltid norsk (bokmål) i rapporten
- Hold faglig presisjon: bruk korrekte fagtermer fra logistikk og statistikk
- Henvis til kilder som allerede er brukt (se referanselisten i rapporten)
- Ikke legg til nye påstander uten at Oskar bekrefter dem

### Kode og analyse
- Python-skript lagres i `004_scripts/`
- Figurer lagres i `005_report/figures/`
- Bruk `pandas`, `statsmodels`, `scikit-learn` — ikke introduser nye biblioteker uten å spørre
- Koden skal matche det som allerede er gjort i rapporten (SARIMA-parametere, GB-parametere osv.)

### Generelle preferanser
- Svar konsist og direkte — ikke overforklare
- Når Claude foreslår endringer i rapporten, vis konkret hva som endres
- Spør hvis noe er uklart heller enn å gjette
- Ikke lag nye filer uten at Oskar ber om det

### Hva Claude ikke skal gjøre
- Ikke endre metodiske valg (modellspesifikasjon, parametere) uten godkjenning
- Ikke legg til referanser som ikke finnes i `003_references/` eller er sitert i utkastet
- Ikke anta at ting er "ferdig" — rapporten er fortsatt under arbeid
