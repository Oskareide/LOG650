# Kapittel 5 – Modellering

Dette kapittelet presenterer den matematiske og analytiske modellen som ligger til grunn for prosjektets prognose- og lagerstyringssystem.

---

## 5.1 Notasjon og parametere

**Tabell 5.1 – Oversikt over symboler og parametere**

| Symbol | Beskrivelse | Enhet |
|---|---|---|
| t | Tidsindeks (uke) | — |
| d_t | Faktisk etterspørsel i uke t | enheter |
| f_t | Prognose for etterspørsel i uke t | enheter |
| L | Ledetid fra bestilling til levering | uker |
| σ_d | Standardavvik i ukentlig etterspørsel | enheter |
| σ_L | Standardavvik i etterspørsel over ledetiden | enheter |
| z | Servicegradfaktor (z-verdi fra normalfordeling) | — |
| SS | Sikkerhetslager | enheter |
| ROP | Bestillingspunkt (Reorder Point) | enheter |
| Q* | Anbefalt bestillingsmengde (EOQ) | enheter |
| μ | Gjennomsnittlig ukentlig etterspørsel | enheter |
| K | Fast bestillingskostnad per ordre | kr |
| h | Lagerkostnad per enhet per år | kr |

---

## 5.2 Stasjonaritetsanalyse

Før SARIMA-modellen estimeres, testes tidsseriene for stasjonaritet ved hjelp av ADF-testen. For ikke-stasjonære serier benyttes log-transformasjon etterfulgt av første differensiering, i tråd med fremgangsmåten beskrevet i kompendiet. Resultater fra ADF-testen presenteres i kapittel 6.

Log-transformasjonen stabiliserer variansen i serien, mens differensieringen fjerner trend og gjør serien stasjonær:

```
y't = Δ ln(d_t) = ln(d_t) - ln(d_{t-1})
```

---

## 5.3 SARIMA-modellen

SARIMA(p,d,q)(P,D,Q)_s er definert ved følgende ligning:

```
Φ_P(B^s) φ_p(B) Δ^d Δ^D_s y_t = Θ_Q(B^s) θ_q(B) ε_t
```

Basert på ACF/PACF-analyse av de log-differensierte seriene estimeres modellen **SARIMA(1,1,1)(1,0,1)₁₃** for alle fire produkter, der sesongperioden er satt til 13 uker (kvartalssesong). Parametrene estimeres ved maksimum likelihood, og modellvalget valideres med AIC, BIC og Ljung-Box-test på residualene.

*Script: `004_scripts/04_sarima.py`*

---

## 5.4 Gradient Boosting

Som alternativ til den statistiske modellen benyttes en Gradient Boosting Regressor, som er en ensemblemetode som kombinerer mange enkle beslutningstrær til én sterk prognosemodell. Prediktorvektoren x_t inneholder:

- Etterspørselen de siste 8 ukene (lag 1–8)
- Rullerende gjennomsnitt over 4 og 8 uker
- Ukenummer og sesongindeks modulo 13

Modellen trenes med 200 estimatorer, læringshastighet 0,05 og maksimal trediybde 3.

*Script: `004_scripts/05_gradient_boosting.py`*

---

## 5.5 Lagerstyringsstørrelser

Prognoseresultatene omsettes til lagerstyringsstørrelser via følgende formler:

```
Sikkerhetslager:   SS  = z · σ_d · √L
Bestillingspunkt:  ROP = μ · L + SS
EOQ:               Q*  = √(2 · K · D̄ / h)
```

der z = 1,645 tilsvarer en servicegrad på 95 %, L er ledetiden i uker, σ_d er standardavviket i ukentlig etterspørsel, μ er gjennomsnittlig ukentlig etterspørsel, K er fast bestillingskostnad per ordre og h er lagerkostnad per enhet per år.

I simuleringen benyttes K = kr 500 og h = 25 % av vareprisen per enhet per år.

*Script: `004_scripts/07_lagerstyring.py`*

---

## Skrivenotater
<!-- Bruk denne seksjonen til egne notater under skriving -->
