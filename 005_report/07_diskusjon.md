# Kapittel 7 – Diskusjon

Dette kapittelet tolker og vurderer resultatene fra analysen i lys av problemstillingen, det teoretiske rammeverket og den praktiske konteksten hos Byggmakker Gravdal.

---

## 7.1 Prognosemodellenes ytelse

Resultatene fra kapittel 6 viser at både SARIMA og Gradient Boosting gir bedre prognoseakkuratesse enn den naive referansemodellen for alle analyserte produkter. Dette er i tråd med forventningene fra teorien og støttes av funn i litteraturen, der strukturerte prognosemodeller konsekvent slår naive metoder for produkter med identifiserbare mønstre (Hyndman & Athanasopoulos, 2021).

SARIMA gir gjennomgående lavere feil enn Gradient Boosting i testperioden (november 2025 – april 2026). En mulig forklaring er at testperioden faller i lavsesong for terrasseprodukter, der sesongstrukturen som SARIMA er designet for å fange er tydelig avtakende. Gradient Boosting er avhengig av at treningsdataene inneholder representativ variasjon for den perioden modellen skal predikere — med kun én fullstendig sesongssyklus i treningsdataene kan modellen ha begrenset generaliseringsevne for vinterperioden.

Det er også verdt å merke seg at maskinlæringsmodellen krever jevnlig retrening etter hvert som nye data akkumuleres, og at den er vanskeligere å tolke for ikke-tekniske brukere. For en bedrift som Byggmakker Gravdal, der innkjøperne skal ha tillit til systemets anbefalinger, kan SARIMA være et mer transparent og kommuniserbart valg til tross for noe høyere kompleksitet i estimeringssteget.

---

## 7.2 Lagerstyringsstørrelser og praktiske implikasjoner

De beregnede lagerstyringsstørrelsene i kapittel 6.6 gir et konkret og etterprøvbart grunnlag for innkjøpsbeslutninger. Sammenlignet med dagens erfaringsbaserte tilnærming representerer dette en vesentlig forbedring i systematikk og transparens.

Valget av servicegrad på 95 % er en faglig begrunnelse, ikke en absolutt sannhet. For lavmarginsprodukt der utsalg har begrenset konsekvens, kan en lavere servicegrad og dermed et mindre sikkerhetslager være mer kostnadseffektivt. Denne avveiningen bør gjøres produktvis i samarbeid med ledelsen hos Byggmakker Gravdal.

---

## 7.3 KI-støttet innkjøpssystem — muligheter og utfordringer

Simuleringen antyder at et KI-støttet innkjøpssystem kan gi målbare forbedringer i lagerstyringen sammenlignet med dagens praksis. Det er likevel viktig å ikke overdrive konklusjonene fra simuleringen. Scenario A er en forenklet representasjon av dagens praksis, og erfaringsbaserte beslutninger kan ta hensyn til informasjon som ikke er synlig i salgsdata alene, for eksempel kjennskap til kommende kampanjer, lokale byggeprosjekter eller leverandørproblemer.

Et KI-støttet system bør derfor ses som et beslutningsstøtteverktøy som supplerer menneskelig vurdering, ikke som en erstatning for den. Dette er i tråd med Fosso Wamba mfl. (2017), som peker på at vellykkede implementeringer kjennetegnes av en hybrid tilnærming der systemet genererer anbefalinger og mennesket beholder godkjenningsansvaret.

---

## 7.4 Forutsetninger for implementering hos Byggmakker Gravdal

For at det beskrevne systemet skal kunne implementeres i praksis hos Byggmakker Gravdal, må tre typer forutsetninger være på plass:

- **Tekniske forutsetninger:** Prognosemodellen og bestillingslogikken må integreres med ERP-systemet, enten via direkte API-kobling eller en halvautomatisk løsning der systemet eksporterer bestillingsanbefalinger til et regneark.
- **Organisatoriske forutsetninger:** Innkjøpere må introduseres til systemet og forstå logikken bak anbefalingene. Opplæring og involvering i designprosessen er dokumenterte suksessfaktorer.
- **Datamessige forutsetninger:** Systemet er avhengig av løpende tilgang til oppdaterte salgsdata og lagerbeholdning. Datakvaliteten må opprettholdes over tid.

---

## 7.5 Skalerbarhet til hele sortimentet

Dette prosjektet demonstrerer metoden på fire utvalgte produkter som et proof of concept. Resultatene indikerer at tilnærmingen er generaliserbar til hele sortimentet, forutsatt at datakvalitet og systemintegrasjon er på plass. En full implementering ville innebære at ERP-systemet nattlig eksporterer salgsdata for alle produkter, kjører prognosemodellen og genererer en prioritert bestillingsliste til innkjøper ved arbeidsdagens start.

---

## 7.6 Begrensninger ved studien

Studien har tre sentrale begrensninger:

1. **Begrenset datahistorikk:** Datahistorikken dekker kun én fullstendig sesongssyklus grunnet systembytte, noe som svekker modellens grunnlag for sesongestimering.
2. **Simuleringsbasert evaluering:** Simuleringen er basert på historiske data og fanger ikke fullt ut dynamikken i en reell implementering.
3. **Estimerte kostnadsparametere:** Kostnadsparametrene K og h er estimerte størrelser, og usikkerhet i disse vil propagere til usikkerhet i Q*.

---

## Skrivenotater
<!-- Bruk denne seksjonen til egne notater under skriving -->
