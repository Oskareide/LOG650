# Sjekkliste – Ferdigstilling av rapport

## Innhold
- [ ] Les gjennom alle kapittelfiler i `005_report/` og sammenlign med PDF-utkastet
- [ ] Fyll ut `## Skrivenotater`-seksjonene med egne tillegg/justeringer
- [ ] Oppdater diskusjonen (kap. 7) med endelige resultater fra skriptene
- [ ] Sjekk at alle tabellnumre og figurhenvisninger stemmer med Word-dokumentet

## Analyse
- [ ] Kjør `python 004_scripts/kjor_alt.py` på nytt hvis salgsdata oppdateres
- [ ] Vurder om GB-modellen bør justeres (mer treningsdata gir bedre resultater)
- [ ] Vurder å endre servicegrad fra 95 % til produktspesifikk verdi (diskuter med Byggmakker)

## Figurer
- [ ] Importer figurene fra `005_report/figures/` inn i Word/LaTeX
- [ ] Legg til figurtekster som matcher rapporten (se kap. 6 i PDF-utkastet)
- [ ] Sjekk at fig6_1, fig6_2 og fig6_3 er leselige i svart-hvitt (for trykk)

## Referanser
- [x] Sjekk at alle referanser i `003_references/referanser.md` faktisk er sitert i teksten (alle 9 OK)
- [ ] Legg til DOI-lenker der de mangler i referanselisten
- [ ] Formatsjekk: APA 7 konsekvent gjennom hele rapporten

## Formalia
- [ ] Forside, innholdsfortegnelse og sidenummerering
- [x] Sammendrag / abstract → `005_report/00_sammendrag.md`
- [x] Vedlegg: Python-kode → `005_report/09_vedlegg.md` (klar til å lime inn i Word)
- [ ] Plagiatsjekk
- [ ] Rettskrivings- og korrekturlesing

## Innlevering
- [ ] Eksporter ferdig rapport til PDF
- [ ] Kopier PDF til `001_info/` med versjonsnummer (f.eks. `LOG650 - Oskar Eide - Final.pdf`)
