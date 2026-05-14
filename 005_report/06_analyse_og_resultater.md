# Kapittel 6 – Analyse og resultater

## 6.1 Deskriptiv analyse

| Produkt | N | Snitt | Std | Min | Q1 | Median | Q3 | Maks | CV% |
|---|---|---|---|---|---|---|---|---|---|
| Terrassebord (28x120) | 116 | 581,4 | 557,6 | 0,0 | 156,6 | 418,6 | 845,1 | 3140,1 | 96 % |
| Planke (48x98) | 116 | 1177,1 | 817,6 | 0,0 | 698,3 | 1003,5 | 1526,8 | 4914,5 | 69 % |
| Terrasseskrue (4,2x55) | 116 | 4,6 | 4,5 | 0,0 | 1,0 | 3,5 | 6,0 | 23,0 | 99 % |
| Skrue 5x90 | 116 | 6,2 | 8,0 | 0,0 | 2,0 | 4,0 | 6,2 | 53,0 | 129 % |

*Kilde: `02_deskriptiv_analyse.py` / `tabell_6_1_deskriptiv.csv`*

Høy CV% for terrasseprodukter reflekterer sterk sesongavhengighet.
→ Figur: `005_report/figures/fig6_1_ukentlig_salg.png`

---

## 6.2 Stasjonaritetstest (ADF)

| Serie | ADF-stat | p-verdi | Krit. 5 % | Konklusjon |
|---|---|---|---|---|
| Terrassebord – original | −10,925 | 0,0000 | −2,887 | Stasjonær |
| Terrassebord – log+diff | −5,513 | 0,0000 | −2,889 | Stasjonær ✓ |
| Planke – original | −3,309 | 0,0145 | −2,888 | Stasjonær |
| Planke – log+diff | −5,898 | 0,0000 | −2,890 | Stasjonær ✓ |
| Terrasseskrue – original | −3,745 | 0,0035 | −2,887 | Stasjonær |
| Terrasseskrue – log+diff | −8,677 | 0,0000 | −2,888 | Stasjonær ✓ |
| Skrue 5x90 – original | −12,117 | 0,0000 | −2,887 | Stasjonær |
| Skrue 5x90 – log+diff | −7,108 | 0,0000 | −2,889 | Stasjonær ✓ |

*Kilde: `03_stasjonaritet_acf_pacf.py` / `adf_resultater.csv`*

d=1 bekreftet som korrekt differensieringsorden for SARIMA.

---

## 6.3 ACF/PACF-analyse

Signifikant negativ verdi ved lag 1 for alle produkter (typisk for differensierte serier). Aktivitet ved sesonglag 13 for terrasseprodukter støtter valget av s=13 i SARIMA-modellen.

→ Figur: `005_report/figures/fig_acf_pacf.png`

---

## 6.4 SARIMA-parameterestimater

| Produkt | AIC | BIC | Log-likelihood |
|---|---|---|---|
| Terrassebord (28x120) | 339,2 | 350,9 | −164,6 |
| Planke (48x98) | 288,9 | 300,5 | −139,4 |
| Terrasseskrue (4,2x55) | 332,4 | 344,0 | −161,2 |
| Skrue 5x90 | 298,6 | 310,2 | −144,3 |

*Kilde: `04_sarima.py` / `sarima_modell_tabell.csv`*

**Ljung-Box-test:** ingen signifikant autokorrelasjon i residualer for planke, terrasseskrue og skrue 5x90. Terrassebord viser signifikant autokorrelasjon ved lag 13 (p=0,008) — modellen kan forbedres for dette produktet.

→ Figur: `005_report/figures/fig_residual_acf.png`

---

## 6.5 Modellsammenlikning (testsettet)

*Testperiode: ca. november 2025 – april 2026 (lavsesong). Kilde: `06_modellsammenlikning.py` / `tabell_6_2_modellsammenlikning.csv`*

| Produkt | Modell | RMSE | MAE | MAPE |
|---|---|---|---|---|
| Terrassebord | Naiv | 365,7 | 275,3 | 162,1 % |
| Terrassebord | **SARIMA** | **313,4** | **228,1** | **124,5 %** |
| Terrassebord | Gradient Boosting | 408,1 | 364,0 | 284,1 % |
| Planke | Naiv | 596,5 | 520,2 | 85,3 % |
| Planke | **SARIMA** | **485,2** | **391,9** | **61,3 %** |
| Planke | Gradient Boosting | 602,1 | 519,4 | 97,4 % |
| Terrasseskrue | Naiv | 3,3 | 2,4 | 86,0 % |
| Terrasseskrue | **SARIMA** | **2,9** | **2,5** | **87,8 %** |
| Terrasseskrue | Gradient Boosting | 3,4 | 2,6 | 128,1 % |
| Skrue 5x90 | Naiv | 5,1 | 3,2 | 86,9 % |
| Skrue 5x90 | **SARIMA** | **3,6** | **2,1** | **59,8 %** |
| Skrue 5x90 | Gradient Boosting | 9,6 | 7,7 | 280,6 % |

SARIMA gir lavest feil for alle fire produkter i testperioden. Testperioden faller i lavsesong (vinter), der SARIMA fanger de avtagende sesongmønstrene bedre enn GB, som krever mer treningsdata for å generalisere godt utenfor høysesong.

→ Figur: `005_report/figures/fig6_2_modellsammenlikning.png`

---

## 6.6 Lagerstyringsstørrelser

*Beregnet med z = 1,645 (95 % servicegrad), K = kr 500, h = 25 % av vareverdi/år, L = 1 uke. Kilde: `07_lagerstyring.py` / `tabell_6_3_lagerstorrelser.csv`*

| Produkt | L | μ | σ_d | SS | ROP | Q* |
|---|---|---|---|---|---|---|
| Terrassebord (28x120) | 1 | 581,4 | 557,6 | 917 | 1 499 | 2 245 |
| Planke (48x98) | 1 | 1177,1 | 817,6 | 1 345 | 2 522 | 2 906 |
| Terrasseskrue (4,2x55) | 1 | 4,6 | 4,5 | 8 | 12 | 94 |
| Skrue 5x90 | 1 | 6,2 | 8,0 | 13 | 19 | 120 |

---

## 6.7 Lagersimulering

*Scenario A: erfaringsbasert (lav ROP, liten fast ordremengde). Scenario B: KI-støttet (beregnet ROP og Q*). Kilde: `07_lagerstyring.py` / `tabell_6_4_simulering.csv`*

| Produkt | Utsalg A | Utsalg B | Forbedring |
|---|---|---|---|
| Terrassebord (28x120) | 15 307 | 1 410 | **−13 897** |
| Planke (48x98) | 16 616 | 1 384 | **−15 232** |
| Terrasseskrue (4,2x55) | 124 | 0 | **−124** |
| Skrue 5x90 | 195 | 2 | **−193** |

Det KI-støttede systemet (B) gir markant reduksjon i utsalgssituasjoner for alle fire produkter. Retningen er tydelig: systematisk prognosebasert innkjøp reduserer utsalg kraftig, særlig for sesongprodukter der erfaringsbasert styring underpresterer i oppkjøringsfasen mot høysesong.

→ Figur: `005_report/figures/fig6_3_lagersimulering.png`

---

## Skrivenotater
<!-- Bruk denne seksjonen til egne notater under skriving -->

