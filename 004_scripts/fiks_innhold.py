#!/usr/bin/env python3
"""
Innholdsrettelser i LOG650 - nyeste - ren.docx:
  1. Oppgavens oppbygging – kapittelnumre (1→10 ny struktur)
  2. Diskusjon – "kapittel 6.6" → "Resultat-kapittelet (kap. 8)"
  3. Kryssreferanser – "diskuteres nærmere i kapittel 7" → 9
  4. Modellering – "presenteres i kapittel 6" → 7
  5. Introduksjon – Byggmakker Gravdal-motsigelsesfiks
  6. Fosso Wamba (2017) → (2015) i løpetekst
  7. Litteratur-intro – oppdatert til å beskrive litteraturkapittelet
"""
from docx import Document

DOC = '/Users/oskareide/Desktop/LOG650 - nyeste - ren.docx'

doc = Document(DOC)
fixes = []


def replace_in_para(p, old, new):
    """Replace `old` with `new` in paragraph, collapsing all runs into the first."""
    if old not in p.text:
        return False
    new_text = p.text.replace(old, new)
    runs = p.runs
    if not runs:
        return False
    runs[0].text = new_text
    for r in runs[1:]:
        r.text = ''
    return True


for p in doc.paragraphs:
    t = p.text

    # 1. Oppgavens oppbygging
    if 'Kapittel 2 presenterer relevant teori' in t and 'kapittel 8' in t:
        ny = (
            'Oppgaven er strukturert som følger: '
            'Kapittel 2 gir en oversikt over relevant litteratur. '
            'Kapittel 3 presenterer det teoretiske grunnlaget for lagerstyring, '
            'prognosemetoder og bruk av KI i innkjøpssystemer. '
            'Kapittel 4 beskriver Byggmakker Gravdal som case, inkludert vareflyt '
            'og dagens innkjøpspraksis. '
            'Kapittel 5 redegjør for datagrunnlag og metodiske valg. '
            'Kapittel 6 presenterer prognose- og lagerstyringsmodellen. '
            'Kapittel 7 viser analysen, og kapittel 8 presenterer resultatene fra '
            'lagerstyringssimuleringen. '
            'Diskusjon følger i kapittel 9, og kapittel 10 oppsummerer konklusjonene.'
        )
        if replace_in_para(p, t, ny):
            fixes.append('Oppgavens oppbygging – kapittelnumre oppdatert')

    # 2. "kapittel 6.6" i Diskusjon
    if 'kapittel 6.6' in t:
        if replace_in_para(p, 'kapittel 6.6', 'Resultat-kapittelet (kap. 8)'):
            fixes.append('"kapittel 6.6" → "Resultat-kapittelet (kap. 8)"')

    # 3. "diskuteres nærmere i kapittel 7" (Casebeskrivelse + Metode)
    if 'diskuteres nærmere i kapittel 7' in t:
        if replace_in_para(p, 'diskuteres nærmere i kapittel 7',
                           'diskuteres nærmere i kapittel 9'):
            fixes.append('"diskuteres nærmere i kapittel 7" → 9')

    # 4. "presenteres i kapittel 6" (Modellering-kapittelet)
    if 'presenteres i kapittel 6' in t:
        if replace_in_para(p, 'presenteres i kapittel 6',
                           'presenteres i kapittel 7'):
            fixes.append('"presenteres i kapittel 6" → 7')

    # 5. Byggmakker Gravdal-motsigelse i Introduksjon
    if 'men kun til profesjonelle aktører' in t:
        if replace_in_para(p, 'men kun til profesjonelle aktører',
                           'med salg til både privatmarkedet og profesjonelle aktører '
                           'som håndverkere og entreprenører'):
            fixes.append('Introduksjon – Byggmakker-beskrivelse harmonisert med Casebeskrivelse')

    # 6. Fosso Wamba årstall
    if 'Fosso Wamba mfl., 2017' in t:
        if replace_in_para(p, 'Fosso Wamba mfl., 2017', 'Fosso Wamba mfl., 2015'):
            fixes.append('Fosso Wamba mfl., 2017 → 2015')
    if 'Fosso Wamba mfl. (2017)' in t:
        if replace_in_para(p, 'Fosso Wamba mfl. (2017)', 'Fosso Wamba mfl. (2015)'):
            fixes.append('Fosso Wamba mfl. (2017) → (2015)')

    # 7. Litteratur-intro
    if 'Kapittelet er organisert rundt fire sentrale temaer: lagerstyring' in t:
        ny = (
            'Dette kapittelet gir en oversikt over sentrale vitenskapelige arbeider '
            'som danner bakgrunnen for prosjektet. Litteraturen er knyttet til fire '
            'temaer: lagerstyring, etterspørselsprognoser, kunstig intelligens i '
            'logistikk og KI-støttede innkjøpssystemer. Det teoretiske rammeverket '
            'som bygger på denne litteraturen presenteres i sin helhet i kapittel 3.'
        )
        if replace_in_para(p, t, ny):
            fixes.append('Litteratur-intro oppdatert')


doc.save(DOC)
print(f'\n{len(fixes)} rettelse(r) lagret i {DOC}:')
for f in fixes:
    print(f'  ✓ {f}')
if not fixes:
    print('  (ingen treff – sjekk at tekstene er nøyaktig som forventet)')
