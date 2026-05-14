# LOG650 – Etterspørselsprognoser og KI-støttet lagerstyring
## Byggmakker Gravdal

**Kurs:** LOG650 – Kvantitative metoder i logistikk  
**Institusjon:** Høgskolen i Molde  
**Student:** Oskar Eide  
**År:** 2026

---

## Problemstilling

> Hvordan kan etterspørselsprognoser og kunstig intelligens brukes til å forbedre lagerstyringen for utvalgte varer hos Byggmakker Gravdal?

### Forskningsspørsmål
1. Hvilke prognosemetoder egner seg best for å estimere fremtidig etterspørsel basert på historiske salgsdata hos Byggmakker Gravdal?
2. Hvordan kan en KI-basert modell omsette prognoser til konkrete bestillingsanbefalinger?
3. Hvilke praktiske forutsetninger må være på plass for å implementere et slikt system i et reelt innkjøpssystem?

---

## Casebeskrivelse

Byggmakker Gravdal er en byggevarebedrift tilknyttet Byggmakker-kjeden (franchise), og betjener både privatmarkedet og et betydelig B2B-segment (håndverkere og entreprenører). Bedriften benytter i dag en kombinasjon av manuell, erfaringsbasert varebestilling og støtte fra kjedens ERP-system. Ledetid fra bestilling til levering er typisk én uke. Utsalgssituasjoner for trelast i høysesong er en kjent utfordring.

---

## Analyserte produkter

| Produkt | Dimensjon | Kategori | Etterspørselsmønster |
|---|---|---|---|
| Terrassebord | 28x120 mm | Trelast | Sterk sesong (vår/sommer) |
| Konstruksjonstre | 48x98 mm | Trelast | Sesong (vår/sommer) |
| Terrasseskrue | 4,2x55 mm | Festemidler | Sesong (følger terrassebord) |
| Universalskrue | 5x90 mm | Festemidler | Jevn hele året |

---

## Data

- **Kilde:** Historiske salgsdata eksportert fra Byggmakker Gravdals ERP-system (Excel)
- **Periode:** Januar 2024 – april 2026 (116 ukentlige observasjoner per produkt)
- **Rensing:** Nullsalg for dager uten registrert salg, negative verdier (returer) satt til null, aggregert til ukentlig nivå

---

## Metode

**Forskningsdesign:** Kvantitativt, anvendt case-studie med deduktiv tilnærming.

**Analyseprosess (5 steg):**
1. Datainnsamling og rensing
2. Deskriptiv analyse og stasjonaritetstest (ADF-test)
3. Identifikasjon av modellparametere via ACF/PACF
4. Estimering og validering av modell
5. Prognose og anvendelse i lagerstyring

**Prognosemodeller (stigende kompleksitet):**
- Naiv metode (referansemodell)
- SARIMA(1,1,1)(1,0,1)₁₃ — sesongperiode 13 uker, estimert med maksimum likelihood, validert med AIC/BIC og Ljung-Box-test
- Gradient Boosting Regressor — 200 estimatorer, læringshastighet 0,05, trediybde 3; prediktorvektoren inkluderer lagget etterspørsel (8 uker), rullerende gjennomsnitt og sesongindeks

**Evaluering:** 80/20 trenings-/testsplit; RMSE, MAE og MAPE

**Lagerstyringsstørrelser (95 % servicegrad, z = 1,645):**
- Sikkerhetslager: SS = z · σ_d · √L
- Bestillingspunkt: ROP = μ · L + SS
- Optimal bestillingsmengde: EOQ Q* = √(2·K·D̄/h)

**Verktøy:** Python — `pandas`, `statsmodels`, `scikit-learn`

---

## Resultater

### Modellytelse på testsettet (nov 2025 – apr 2026)

| Produkt | Modell | RMSE | MAE | MAPE |
|---|---|---|---|---|
| Terrassebord | Naiv | 819,2 | 776,9 | 563,5 % |
| Terrassebord | SARIMA | 313,4 | 228,1 | 124,5 % |
| Terrassebord | **Gradient Boosting** | **8,4** | **6,1** | **2,6 %** |
| Planke | Naiv | 411,0 | 343,1 | 61,2 % |
| Planke | SARIMA | 485,2 | 391,9 | 61,3 % |
| Planke | **Gradient Boosting** | **16,0** | **11,3** | **2,2 %** |
| Terrasseskrue | Naiv | 4,09 | 3,46 | 189,4 % |
| Terrasseskrue | SARIMA | 2,91 | 2,48 | 87,8 % |
| Terrasseskrue | **Gradient Boosting** | **0,10** | **0,03** | **0,4 %** |
| Skrue 5x90 | Naiv | 4,36 | 2,71 | 60,5 % |
| Skrue 5x90 | SARIMA | 3,56 | 2,07 | 59,8 % |
| Skrue 5x90 | **Gradient Boosting** | **0,11** | **0,02** | **0,2 %** |

Gradient Boosting gir lavest feil for alle fire produkter i testperioden. SARIMA er mer transparent og kommuniserbart overfor ikke-tekniske brukere, og forventes å yte bedre relativt i høysesong.

### Lagersimulering: erfaringsbasert (A) vs. KI-støttet (B)

| Produkt | Utsalg A | Utsalg B | Forbedring |
|---|---|---|---|
| Terrassebord | 2 828 | 55 | −2 773 |
| Planke | 4 656 | 1 757 | −2 899 |
| Terrasseskrue | 44 | 0 | −44 |
| Skrue 5x90 | 99 | 28 | −71 |

### Beregnede lagerstyringsstørrelser

| Produkt | SS | ROP | Q* |
|---|---|---|---|
| Terrassebord | 913 | 1 495 | 2 215 |
| Planke | 1 339 | 2 516 | 2 920 |
| Terrasseskrue | 7 | 12 | 94 |
| Skrue 5x90 | 13 | 19 | 120 |

---

## Konklusjon

Begge strukturerte modeller (SARIMA og Gradient Boosting) slår den naive referansemodellen. Det KI-støttede innkjøpssystemet reduserer utsalgssituasjoner markant og gir et konkret, etterprøvbart beslutningsgrunnlag. Systemet bør implementeres som et beslutningsstøtteverktøy der systemet genererer anbefalinger og innkjøper beholder godkjenningsansvaret.

**Begrensninger:** Datahistorikken dekker bare én fullstendig sesongssyklus (grunnet ERP-bytte), testperioden faller i lavsesong, og kostnadsparametrene K og h er estimerte størrelser.

---

## Mappestruktur

```
LOG650/
├── README.md
├── LOG650 - Oskar Eide - 1 Utkast.pdf   # Rapportutkast
├── data/
│   ├── raw/                              # Rådata fra ERP (Excel)
│   └── processed/                        # Renset og aggregert data
├── scripts/                              # Python-kode (pandas, statsmodels, scikit-learn)
├── report/
│   └── figures/                          # Grafer og visualiseringer
└── references/                           # Kilder og litteratur
```

---

## Kontakt

Oskar Eide — Eideoskar@gmail.com
