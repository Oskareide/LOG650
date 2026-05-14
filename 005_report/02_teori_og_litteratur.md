# Kapittel 2 – Teori og litteratur

Dette kapittelet presenterer det teoretiske grunnlaget for prosjektet. Kapittelet er organisert rundt fire sentrale temaer: lagerstyring, etterspørselsprognoser, kunstig intelligens i logistikk og KI-støttede innkjøpssystemer. Til sammen danner disse teoriene rammeverket for modellering, analyse og diskusjon i de påfølgende kapitlene.

---

## 2.1 Lagerstyring

Lagerstyring handler om å bestemme hvor mye av en vare som skal holdes på lager, når det skal bestilles og hvor mye som skal bestilles om gangen. Målet er å balansere to motstridende kostnader: kostnaden ved å ha for lite på lager (utsalg, tapte inntekter, misfornøyde kunder) og kostnaden ved å ha for mye (kapitalbinding, lagerkostnader, ukurans). Dette avveiningsproblemet er sentralt i all lagerstyringsteorien (Silver, Pyke & Thomas, 2017).

Et grunnleggende skille i lagerstyring er mellom kontinuerlig gjennomgang og periodisk gjennomgang. Ved kontinuerlig gjennomgang overvåkes lagerbeholdningen løpende, og en bestilling utløses når beholdningen faller under et bestemt nivå, kalt bestillingspunktet (ROP). Ved periodisk gjennomgang kontrolleres lageret med faste intervaller, og det bestilles opp til et bestemt maksnivå. Valget mellom disse systemene avhenger av blant annet ERP-systemets kapabiliteter, leverandørenes fleksibilitet og verdien av varene (Chopra & Meindl, 2016).

To sentrale størrelser i lagerstyring er sikkerhetslager (SS) og bestillingspunkt (ROP). Sikkerhetslageret er den ekstra beholdningen som holdes for å beskytte mot usikkerhet i etterspørsel og ledetid. Bestillingspunktet er det beholdningsnivået som utløser en ny bestilling, og beregnes som forventet etterspørsel i ledetiden pluss sikkerhetslageret. Den klassiske EOQ-modellen (Economic Order Quantity) gir den optimale bestillingsmengden som minimerer summen av bestillingskostnader og lagerkostnader (Harris, 1913).

---

## 2.2 Etterspørselsprognoser

En etterspørselsprognose er et estimat av fremtidig etterspørsel basert på tilgjengelig informasjon. Gode prognoser reduserer usikkerheten i lagerstyringsbeslutninger og gjør det mulig å tilpasse bestillinger mer presist til faktisk behov (Hyndman & Athanasopoulos, 2021).

Prognosemetoder kan deles inn i to hovedkategorier: kvalitative og kvantitative metoder. Kvalitative metoder bygger på vurderinger og ekspertskjønn, og brukes typisk når historiske data er begrenset eller utilstrekkelige. Kvantitative metoder bruker historiske data og matematiske modeller, og er mer relevante når det finnes tilstrekkelig datagrunnlag, slik tilfellet er i varehandel med ERP-systemer.

SARIMA (Seasonal Autoregressive Integrated Moving Average) er en utvidelse av ARIMA-modellen som eksplisitt håndterer sesongmønstre i tidsseriedata. Modellen er velegnet for ukentlige salgsdata med sesongvariasjoner, og er en sentral metode i dette prosjektet. Modellen identifiseres gjennom analyse av ACF- og PACF-plott etter log-transformasjon og differensiering for å oppnå stasjonaritet (Hyndman & Athanasopoulos, 2021).

En viktig egenskap ved alle prognosemetoder er at de alltid vil inneholde en viss prognoseusikkerhet. Denne usikkerheten måles gjerne med RMSE (Root Mean Squared Error), MAE (Mean Absolute Error) og MAPE (Mean Absolute Percentage Error), som alle kvantifiserer gjennomsnittlig avvik mellom prognose og faktisk etterspørsel.

---

## 2.3 Kunstig intelligens i logistikk

Kunstig intelligens (KI) er en samlebetegnelse for metoder som gjør det mulig for datamaskiner å lære fra data og utføre oppgaver som tradisjonelt har krevd menneskelig intelligens. Innen logistikk og supply chain management har KI de siste årene fått betydelig oppmerksomhet som verktøy for å forbedre beslutningsprosesser, automatisere rutineoppgaver og avdekke mønstre i store datamengder (Toorajipour mfl., 2021).

Maskinlæring er en sentral gren av KI der modeller trenes på historiske data for å gjenkjenne mønstre og gjøre prediksjoner. I kontekst av etterspørselsprognoser er maskinlæringsmodeller som Gradient Boosting vist å gi høy prognoseakkuratesse, særlig ved komplekse og ikke-lineære etterspørselsmønstre (Carbonneau, Laframboise & Vahidov, 2008).

Likevel er det viktig å nyansere bildet: maskinlæringsmodeller krever større datamengder for å trenes effektivt, er vanskeligere å tolke og kan overprøve (overfit) dersom datagrunnlaget er begrenset. For mindre bedrifter med kortere datahistorikk kan enklere statistiske metoder tidvis gi konkurransedyktige resultater med langt lavere kompleksitet (Makridakis, Spiliotis & Assimakopoulos, 2018).

---

## 2.4 KI-støttede innkjøpssystemer

Et KI-støttet innkjøpssystem er et system som kombinerer etterspørselsprognoser med regelbasert eller læringsbasert logikk for å generere automatiske eller halvautomatiske bestillingsanbefalinger. Slike systemer kan redusere den manuelle arbeidsmengden knyttet til varebestilling, minimere menneskelige feil og sørge for at bestillinger baseres på data fremfor intuisjon (van der Vorst, Beulens & van Beek, 2000).

Et typisk KI-støttet innkjøpssystem består av tre hovedkomponenter: en prognosemodell som estimerer fremtidig etterspørsel, en lagerstyringsmodul som beregner optimalt bestillingspunkt og bestillingsmengde, og et beslutningslag som omsetter beregningene til konkrete bestillingsanbefalinger. Implementering av slike systemer i eksisterende ERP-løsninger er imidlertid ikke uten utfordringer, der datakvalitet og organisatorisk tilpasning er gjennomgående flaskehalser (Fosso Wamba mfl., 2017).

---

## Skrivenotater
<!-- Bruk denne seksjonen til egne notater under skriving -->
