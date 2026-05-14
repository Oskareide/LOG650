# Kapittel 8 – Konklusjon

---

## 8.1 Besvarelse av problemstillingen

> **Problemstilling:** Hvordan kan etterspørselsprognoser og kunstig intelligens brukes til å forbedre lagerstyringen for utvalgte varer hos Byggmakker Gravdal?

Analysen viser at etterspørselsprognoser basert på historiske salgsdata gir et vesentlig bedre grunnlag for lagerstyringsbeslutninger enn den erfaringsbaserte tilnærmingen som benyttes i dag. Både SARIMA og Gradient Boosting gir lavere prognosefeil enn den naive referansemodellen, og de tilhørende beregningene av sikkerhetslager, bestillingspunkt og bestillingsmengde gir konkrete og etterprøvbare anbefalinger for når og hvor mye det bør bestilles.

Det KI-støttede innkjøpssystemet som er utviklet kombinerer prognosemodellen med en regelbasert beslutningslogikk som overvåker lagerbeholdningen løpende og genererer bestillingsanbefalinger automatisk når beholdningen faller under beregnet bestillingspunkt. Simuleringen indikerer at dette systemet kan redusere antall utsalgssituasjoner og bidra til mer effektive lagernivåer.

---

## 8.2 Svar på forskningsspørsmålene

**Forskningsspørsmål 1 – Beste prognosemetode:**
SARIMA gir lavest feil i testperioden (lavsesong) for alle fire produkter, mens Gradient Boosting kan forventes å yte bedre relativt i høysesong der treningsdataene er mer representative. Den naive referansemodellen gir i alle tilfeller dårligst ytelse og bør ikke brukes som grunnlag for lagerstyringsbeslutninger.

**Forskningsspørsmål 2 – Fra prognose til bestillingsanbefaling:**
Prognoseresultatene omsettes til bestillingsanbefalinger gjennom en tredelt beregningslogikk: prognoseusikkerheten dimensjonerer sikkerhetslageret (SS = z · σ_d · √L), forventet etterspørsel i ledetiden kombinert med sikkerhetslageret gir bestillingspunktet (ROP = μ · L + SS), og EOQ-formelen gir den optimale bestillingsmengden (Q* = √(2 · K · D̄ / h)).

**Forskningsspørsmål 3 – Implementeringsforutsetninger:**
En vellykket implementering krever tilstrekkelig datakvalitet, en teknisk løsning for integrasjon med eksisterende ERP-system, og organisatorisk forankring der ansatte forstår og har tillit til systemets anbefalinger.

---

## 8.3 Faglig bidrag og videre forskning

Prosjektet demonstrerer at etablerte metoder fra lagerstyringsteorien kan kombineres med moderne maskinlæringsbaserte prognosemodeller i en sammenhengende og etterprøvbar analyseramme. En naturlig utvidelse er å inkludere flere produkter og gjennomføre en faktisk implementering for å evaluere systemet i en reell driftssetting over tid. Det vil også være verdifullt å evaluere SARIMA mot Gradient Boosting over en fullstendig sesongssyklus som inkluderer både høy- og lavsesong, for å gi et mer robust bilde av de relative fordelene.

---

## 8.4 Avsluttende refleksjon

For Byggmakker Gravdal representerer det beskrevne systemet et realistisk og konkret neste steg mot en mer datadrevet innkjøpspraksis — ett som kan implementeres gradvis, evalueres løpende og bygges videre på etter hvert som erfaring og datagrunnlag vokser. Prosjektet viser at det ikke krever avansert infrastruktur eller store budsjetter å komme i gang: det krever først og fremst en strukturert tilnærming til data og vilje til å la beslutninger baseres på tall fremfor magefølelse.

Selve arbeidsprosessen med dette prosjektet har gitt en uventet, men konkret illustrasjon av nettopp dette. Deler av analysen — fra datarensing og modellering til organisering av kode og skriving av rapport — ble gjennomført i samarbeid med en KI-agent (Claude Code). Å se en slik agent analysere salgsdata, identifisere mønstre, generere Python-kode og strukturere faglig tekst i sanntid er ikke bare en effektiv arbeidsmåte: det er et direkte eksempel på den samme underliggende teknologien som dette prosjektet argumenterer for å ta i bruk i innkjøpssystemer. Der agenten i skriveprosessen tolket instruksjoner og produserte strukturerte output, vil en tilsvarende agent i et ERP-system tolke lagernivåer og prognoser og produsere bestillingsanbefalinger. Erfaringen understreker at terskelen for å ta KI i praktisk bruk er lavere enn mange antar — og at den kanskje mest verdifulle innsikten ikke alltid fremkommer fra modellenes resultater alene, men fra selve prosessen med å bygge og bruke dem.

---

## Skrivenotater
<!-- Bruk denne seksjonen til egne notater under skriving -->
