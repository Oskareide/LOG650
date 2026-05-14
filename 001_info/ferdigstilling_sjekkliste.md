# Sjekkliste – Ferdigstilling av rapport

## Gjort av Claude (trenger ikke gjøres manuelt)
- [x] Alle 10 kapittelfiler skrevet med full prosatekst (`005_report/00–09`)
- [x] Sammendrag / abstract → `005_report/00_sammendrag.md`
- [x] Vedlegg: Python-kode → `005_report/09_vedlegg.md`
- [x] Alle 9 referanser sitert i teksten, ingen hull
- [x] `rapport.docx` generert med forside, kap. 1–8, referanser og vedlegg
- [x] Alle 5 figurer embedded automatisk i `rapport.docx`
- [x] Pushet til GitHub: https://github.com/Oskareide/LOG650

---

## Gjenstår — gjøres i Word

### Innhold
- [ ] Les gjennom rapporten og sammenlign med PDF-utkastet
- [ ] Fyll ut `## Skrivenotater` i kapitelfilene med egne tillegg, kjør deretter `python 004_scripts/bygg_rapport_docx.py` på nytt

### Formalia i Word
- [ ] Legg til automatisk innholdsfortegnelse (References → Table of Contents)
- [ ] Sjekk sidenummerering og marger
- [ ] Sjekk at figurtekstene stemmer med nummereringen i teksten

### Referanser
- [ ] Legg til DOI-lenker der de mangler (`003_references/referanser.md`, deretter regenerer docx)
- [ ] Formatsjekk: APA 7 konsekvent gjennom hele rapporten

### Kvalitet
- [ ] Sjekk at fig6_1, fig6_2 og fig6_3 er leselige i svart-hvitt (for trykk)
- [ ] Rettskrivings- og korrekturlesing
- [ ] Plagiatsjekk

### Innlevering
- [ ] Eksporter ferdig rapport til PDF
- [ ] Kopier PDF til `001_info/` med navn `LOG650 - Oskar Eide - Final.pdf`
- [ ] Lever inn
