# Kapittel 4 – Data og metode

Dette kapittelet beskriver hvordan prosjektet er gjennomført — hvilke data som er brukt, hvordan de er samlet inn og bearbeidet, og hvilke analysemetoder som er valgt.

---

## 4.1 Forskningsdesign

Prosjektet følger et kvantitativt forskningsdesign basert på analyse av historiske salgsdata fra Byggmakker Gravdal. Designet er en anvendt case-studie der målet er å utvikle og evaluere prognosemodeller som kan forbedre lagerstyringen for utvalgte produkter. Tilnærmingen er deduktiv i den forstand at etablerte teorier om etterspørselsprognoser og lagerstyring danner grunnlaget for valg av metoder, og at disse metodene deretter testes mot empiriske data fra bedriften.

Analyseprosessen følger en femstegsstruktur i tråd med kompendiet:

1. Datainnsamling og rensing
2. Deskriptiv analyse og stasjonaritetstest
3. Identifikasjon av modellparametere via ACF/PACF
4. Estimering og validering av modell
5. Prognose og anvendelse i lagerstyring

---

## 4.2 Datagrunnlag

Datagrunnlaget for prosjektet er historiske salgsdata hentet fra Byggmakker Gravdals ERP-system. Dataene inneholder ukentlig salg per produkt for perioden januar 2024 til april 2026. Analysen avgrenses til fire utvalgte produkter valgt ut fra kriterier om omløpshastighet, sesongvariasjon og relevans for lagerstyring.

*Datafil: `002_data/raw/salgsrapport Oskar v2.xlsx` → renset: `002_data/processed/ukentlig_salg.csv`*

---

## 4.3 Datainnsamling og datakvalitet

Dataene er eksportert direkte fra bedriftens ERP-system i Excel-format. Før analyse er dataene gjennomgått og renset for følgende forhold:

- **Manglende verdier:** Dager uten registrert salg er behandlet som nullsalg.
- **Negative verdier:** Returer og kreditnotaer er fjernet ved å sette negative verdier til null.
- **Kampanjeperioder:** Det gjennomføres sesongkampanjer på terrasseprodukter, noe som kan introdusere støy i dataene.
- **Aggregeringsnivå:** Salgsdata er aggregert til ukentlige observasjoner.

En viktig begrensning er at datahistorikken kun dekker én fullstendig sesongssyklus grunnet systembytte hos bedriften. Dette diskuteres nærmere i kapittel 7.

*Script: `004_scripts/01_last_inn_data.py`*

---

## 4.4 Analysemetoder

Prosjektet benytter tre metodiske tilnærminger som bygger på hverandre: deskriptiv analyse, prognosemodellering og evaluering av modellytelse.

### Deskriptiv analyse

Gjennomføres for å kartlegge grunnleggende egenskaper ved etterspørselsdataene, inkludert gjennomsnitt, standardavvik, kvartiler og sesongindekser. ADF-testen (Augmented Dickey-Fuller) benyttes for å teste for stasjonaritet.

*Script: `004_scripts/02_deskriptiv_analyse.py`, `004_scripts/03_stasjonaritet_acf_pacf.py`*

### Prognosemodellering

Tre modeller av stigende kompleksitet sammenlignes:

- **Naiv metode (referansemodell):** Neste periodes etterspørsel settes lik foregående periodes faktiske etterspørsel.
- **SARIMA:** Seasonal Autoregressive Integrated Moving Average — statistisk modell som håndterer sesongmønstre.
- **Gradient Boosting:** Maskinlæringsmodell som fanger opp ikke-lineære mønstre i dataene.

*Script: `004_scripts/04_sarima.py`, `004_scripts/05_gradient_boosting.py`*

### Evaluering av modellytelse

Datasettet deles i treningsperiode (80 %) og testperiode (20 %). Prognoseakkuratessen måles med RMSE, MAE og MAPE.

*Script: `004_scripts/06_modellsammenlikning.py`*

---

## 4.5 Verktøy

Alle analyser gjennomføres i Python, med bibliotekene `pandas` (databehandling), `statsmodels` (SARIMA) og `scikit-learn` (Gradient Boosting). Fullstendig kode ligger i `004_scripts/`. Installasjonskrav er dokumentert i `requirements.txt`.

---

## Skrivenotater
<!-- Bruk denne seksjonen til egne notater under skriving -->
