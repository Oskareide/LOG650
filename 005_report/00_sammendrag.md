# Sammendrag

Denne oppgaven undersøker hvordan etterspørselsprognoser og kunstig intelligens kan brukes til å forbedre lagerstyringen for utvalgte varer hos Byggmakker Gravdal. Bedriften benytter i dag en erfaringsbasert tilnærming til varebestilling, og har ved gjentatte anledninger opplevd utsalgssituasjoner for trelastprodukter i høysesong.

Analysen tar utgangspunkt i historiske ukentlige salgsdata for perioden januar 2024 til april 2026, og dekker fire produkter: terrassebord (28x120 mm), konstruksjonstre (48x98 mm), terrasseskrue (4,2x55 mm) og universalskrue (5x90 mm). Tre prognosemodeller sammenlignes: en naiv referansemodell, SARIMA(1,1,1)(1,0,1)₁₃ og en Gradient Boosting Regressor. Modellene evalueres på et testsett bestående av de siste 20 % av observasjonene (november 2025 – april 2026), ved hjelp av RMSE, MAE og MAPE.

Resultatene viser at SARIMA gir lavest prognosefeil i testperioden for alle fire produkter, og håndterer de avtagende sesongmønstrene i lavsesong best. Gradient Boosting forventes å yte bedre i høysesong, men begrenses av at datahistorikken kun dekker én fullstendig sesongssyklus. Basert på prognoseresultatene beregnes lagerstyringsstørrelser — sikkerhetslager, bestillingspunkt og EOQ — for en servicegrad på 95 %. En simulering viser at et KI-støttet innkjøpssystem (scenario B) gir en markant reduksjon i utsalgssituasjoner sammenlignet med erfaringsbasert styring (scenario A) for alle fire produkter.

Oppgaven konkluderer med at datadrevne prognosemetoder gir et vesentlig bedre beslutningsgrunnlag enn dagens praksis, og at et KI-støttet innkjøpssystem kan implementeres gradvis i Byggmakker Gravdals eksisterende ERP-løsning. Systemet anbefales innført som et beslutningsstøtteverktøy der systemet genererer anbefalinger og innkjøper beholder godkjenningsansvaret.

**Nøkkelord:** etterspørselsprognoser, lagerstyring, SARIMA, Gradient Boosting, KI-støttet innkjøp, byggevarehandel

---

# Abstract

This paper investigates how demand forecasting and artificial intelligence can improve inventory management for selected products at Byggmakker Gravdal, a Norwegian building materials retailer. The company currently relies on experience-based ordering and has repeatedly faced stockout situations for timber products during peak season.

The analysis is based on weekly historical sales data from January 2024 to April 2026, covering four products: decking boards (28x120 mm), structural timber (48x98 mm), decking screws (4.2x55 mm), and wood screws (5x90 mm). Three forecasting models are compared: a naïve benchmark, SARIMA(1,1,1)(1,0,1)₁₃, and a Gradient Boosting Regressor, evaluated on a hold-out test set (November 2025 – April 2026) using RMSE, MAE, and MAPE.

SARIMA achieves the lowest forecast error across all four products in the test period. Inventory parameters — safety stock, reorder point, and EOQ — are derived from the forecast results at a 95% service level. A simulation shows that an AI-supported ordering system (scenario B) substantially reduces stockouts compared to the experience-based approach (scenario A).

The paper concludes that data-driven forecasting provides a significantly better basis for ordering decisions than current practice, and that an AI-supported procurement system can be implemented incrementally within Byggmakker Gravdal's existing ERP infrastructure.

**Keywords:** demand forecasting, inventory management, SARIMA, Gradient Boosting, AI-supported procurement, building materials retail
