# Sammendrag

Denne oppgaven undersøker hvordan etterspørselsprognoser og kunstig intelligens kan brukes til å forbedre lagerstyringen for utvalgte varer hos Byggmakker Gravdal. Bedriften benytter i dag en erfaringsbasert tilnærming til varebestilling, og har ved gjentatte anledninger opplevd utsalgssituasjoner for trelastprodukter i høysesong.

Analysen tar utgangspunkt i historiske ukentlige salgsdata for perioden januar 2024 til april 2026, og dekker fire produkter: terrassebord (28x120 mm), konstruksjonstre (48x98 mm), terrasseskrue (4,2x55 mm) og universalskrue (5x90 mm). Tre prognosemodeller sammenlignes: en naiv referansemodell, SARIMA(1,1,1)(1,0,1)₁₃ og en Gradient Boosting Regressor. Modellene evalueres på et testsett bestående av de siste 20 % av observasjonene (november 2025 – april 2026), ved hjelp av RMSE, MAE og MAPE.

Resultatene viser at SARIMA gir lavest prognosefeil i testperioden for alle fire produkter, og håndterer de avtagende sesongmønstrene i lavsesong best. Gradient Boosting forventes å yte bedre i høysesong, men begrenses av at datahistorikken kun dekker én fullstendig sesongssyklus. Basert på prognoseresultatene beregnes lagerstyringsstørrelser — sikkerhetslager, bestillingspunkt og EOQ — for en servicegrad på 95 %. En simulering viser at et KI-støttet innkjøpssystem (scenario B) gir en markant reduksjon i utsalgssituasjoner sammenlignet med erfaringsbasert styring (scenario A) for alle fire produkter.

Oppgaven konkluderer med at datadrevne prognosemetoder gir et vesentlig bedre beslutningsgrunnlag enn dagens praksis, og at et KI-støttet innkjøpssystem kan implementeres gradvis i Byggmakker Gravdals eksisterende ERP-løsning. Systemet anbefales innført som et beslutningsstøtteverktøy der systemet genererer anbefalinger og innkjøper beholder godkjenningsansvaret.

**Nøkkelord:** etterspørselsprognoser, lagerstyring, SARIMA, Gradient Boosting, KI-støttet innkjøp, byggevarehandel
