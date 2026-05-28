#!/usr/bin/env python3
"""
Steg 2 – fire konkrete rettelser i LOG650 - BM - Mal.docx:
  1. Flytt tabelltitler fra over til under tabellene
  2. Nummerér ligninger i Modellering-kapittelet (5.1–5.5)
  3. Legg til Anthropic-referanse i Bibliografi
  4. Legg til Antagelser-underavsnitt i Innledning
"""
import copy
from docx import Document
from docx.oxml import OxmlElement
from docx.shared import Pt

DOC = '/Users/oskareide/Desktop/LOG650 - BM - Mal.docx'
NS  = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

doc  = Document(DOC)
body = doc.element.body

# ── helpers ────────────────────────────────────────────────────────────────────

def get_text(elem):
    return ''.join(t.text or '' for t in elem.iter(f'{{{NS}}}t'))

def body_children():
    return list(body)

def para_style(elem):
    s = elem.find(f'.//{{{NS}}}pStyle')
    return s.get(f'{{{NS}}}val') if s is not None else ''

def make_para(text, style_val='Normal', bold=False):
    p = OxmlElement('w:p')
    pPr = OxmlElement('w:pPr')
    pStyle = OxmlElement('w:pStyle')
    pStyle.set(f'{{{NS}}}val', style_val)
    pPr.append(pStyle)
    p.append(pPr)
    r = OxmlElement('w:r')
    if bold:
        rPr = OxmlElement('w:rPr')
        b = OxmlElement('w:b')
        rPr.append(b)
        r.append(rPr)
    t = OxmlElement('w:t')
    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    t.text = text
    r.append(t)
    p.append(r)
    return p

def make_h2(text):
    return make_para(text, style_val='Overskrift2')

def insert_after(ref_elem, new_elem):
    ref_elem.addnext(new_elem)

def insert_before(ref_elem, new_elem):
    ref_elem.addprevious(new_elem)


# ── 1. Flytt tabelltitler fra over til under ───────────────────────────────────

print("1. Flytter tabelltitler ...")
children = body_children()
moves = []

for i, child in enumerate(children):
    tag = child.tag.split('}')[-1]
    if tag == 'p':
        text = get_text(child).strip()
        if text.startswith('Tabell') and i + 1 < len(children):
            nxt = children[i + 1]
            if nxt.tag.split('}')[-1] == 'tbl':
                moves.append((child, nxt))   # (title_para, table)

for title_para, table in moves:
    print(f"   Flytter: '{get_text(title_para).strip()[:60]}'")
    # Remove title from current position, insert after table
    body.remove(title_para)
    table.addnext(copy.deepcopy(title_para))

print(f"   {len(moves)} tittel(r) flyttet.\n")


# ── 2. Nummerér ligninger i Modellering ────────────────────────────────────────
# Ligninger:
#   (5.1)  log-differensiering:  y't = Δ ln(d_t) = ...
#   (5.2)  SARIMA:               Φ_P(B^s) ...
#   (5.3)  SS  = z · σ_d · √L
#   (5.4)  ROP = μ · L + SS
#   (5.5)  Q*  = √(2 · K · D̄ / h)

print("2. Nummererer ligninger ...")

in_modell = False
para_map = {id(p._element): p for p in doc.paragraphs}
children = body_children()

eq_num = 1
for i, child in enumerate(children):
    tag = child.tag.split('}')[-1]
    if tag != 'p':
        continue

    para = para_map.get(id(child))
    if para is None:
        continue

    if para.style.name == 'Heading 1' and para.text.strip() == 'Modellering':
        in_modell = True
        continue
    if para.style.name == 'Heading 1' and in_modell:
        break

    if not in_modell:
        continue

    text = para.text.strip()

    # Log-differensiering
    if "ln(d_t)" in text and eq_num == 1:
        # Append equation number to last run
        runs = child.findall(f'{{{NS}}}r')
        if runs:
            last_t = runs[-1].find(f'{{{NS}}}t')
            if last_t is not None:
                last_t.text = last_t.text.rstrip() + f'    (5.{eq_num})'
        print(f"   (5.{eq_num}) Log-differensiering")
        eq_num += 1

    # SARIMA-ligning
    elif "Φ_P" in text and eq_num == 2:
        runs = child.findall(f'{{{NS}}}r')
        if runs:
            last_t = runs[-1].find(f'{{{NS}}}t')
            if last_t is not None:
                last_t.text = last_t.text.rstrip() + f'    (5.{eq_num})'
        print(f"   (5.{eq_num}) SARIMA-ligning")
        eq_num += 1

    # SS / ROP / EOQ – ett avsnitt med linjeskift, splitt til tre
    elif "Sikkerhetslager" in text and "SS" in text and eq_num == 3:
        # The paragraph has structure: run1 <br/> run2 <br/> run3
        runs = child.findall(f'{{{NS}}}r')
        brs  = child.findall(f'.//{{{NS}}}br')

        if len(runs) >= 3:
            # Get text from each run
            t1 = ''.join(t.text or '' for t in runs[0].iter(f'{{{NS}}}t')).strip()
            t2 = ''.join(t.text or '' for t in runs[1].iter(f'{{{NS}}}t')).strip()
            t3 = ''.join(t.text or '' for t in runs[2].iter(f'{{{NS}}}t')).strip()

            # Build three replacement paragraphs
            p1 = make_para(f'{t1}    (5.3)', 'Normal')
            p2 = make_para(f'{t2}    (5.4)', 'Normal')
            p3 = make_para(f'{t3}    (5.5)', 'Normal')

            # Insert three new paras before original, then remove original
            child.addprevious(p1)
            p1.addnext(p2)
            p2.addnext(p3)
            body.remove(child)

            print(f"   (5.3) SS, (5.4) ROP, (5.5) EOQ")
            eq_num += 3

print(f"   Ferdig – totalt {eq_num - 1} ligninger nummerert.\n")


# ── 3. Legg til Anthropic i Bibliografi ───────────────────────────────────────

print("3. Legger til Anthropic-referanse ...")

anthropic_ref = (
    "Anthropic. (2025). Claude Code [Kodingsassistent]. https://claude.ai/code"
)

children = body_children()
in_biblio = False
insert_pos = None

for i, child in enumerate(children):
    tag = child.tag.split('}')[-1]
    if tag != 'p':
        continue
    para = para_map.get(id(child))
    if para and para.style.name == 'Heading 1' and para.text.strip() == 'Bibliografi':
        in_biblio = True
        continue
    if para and para.style.name == 'Heading 1' and in_biblio:
        break
    if in_biblio and para:
        text = para.text.strip()
        # Insert Anthropic before Carbonneau (alphabetical: A before C)
        if text.startswith('Carbonneau') and insert_pos is None:
            insert_pos = child
            break

new_ref = make_para(anthropic_ref, 'Normal (Web)' if 'Normal (Web)' in
                    [s.name for s in doc.styles] else 'Normal')

if insert_pos is not None:
    insert_pos.addprevious(new_ref)
    print(f"   Lagt til Anthropic (2025) før Carbonneau.\n")
else:
    # Fallback: find Bibliografi H1 and insert after it
    for child in body_children():
        para = para_map.get(id(child))
        if para and para.style.name == 'Heading 1' and para.text.strip() == 'Bibliografi':
            child.addnext(new_ref)
            print("   Lagt til Anthropic (2025) i Bibliografi (slutt).\n")
            break


# ── 4. Legg til Antagelser i Innledning ───────────────────────────────────────

print("4. Legger til Antagelser-underavsnitt ...")

antagelser_tekst = [
    ("Antagelser", "heading"),
    ("Analysen bygger på følgende forutsetninger:", "normal"),
    ("1. Normalfordelt etterspørsel: Sikkerhetslageret beregnes med SS = z·σ_d·√L der z = 1,645 (95 % servicegrad). Dette forutsetter at etterspørselen er tilnærmet normalfordelt.", "normal"),
    ("2. Deterministisk og konstant ledetid: Ledetiden settes til L = 1 uke og antas å være kjent og konstant. Variasjon i ledetid er ikke modellert.", "normal"),
    ("3. Stabile kostnadsparametere: Ordrekostnaden K = kr 500 og lagerkostnadsandelen h = 25 % av vareprisen per enhet per år antas å være konstante.", "normal"),
    ("4. Stasjonære residualer etter transformasjon: Etter log-transformasjon og differensiering (d=1) antas tidsseriene å ha uavhengige residualer, som er en forutsetning for SARIMA-modellen.", "normal"),
    ("5. Sesongperiode på 13 uker: Det antas at etterspørselsmønsteret gjentar seg med en periode på s = 13 uker, tilsvarende ett kvartal.", "normal"),
]

# Find "Avgrensninger" H2 in Innledning, insert Antagelser after it and its content
children = body_children()
in_innledning = False
avgrensninger_end = None   # last element belonging to Avgrensninger section

for i, child in enumerate(children):
    tag = child.tag.split('}')[-1]
    if tag != 'p':
        if in_innledning and avgrensninger_end is not None:
            avgrensninger_end = child  # tables inside Avgrensninger section
        continue
    para = para_map.get(id(child))
    if not para:
        continue

    if para.style.name == 'Heading 1' and para.text.strip() == 'Innledning':
        in_innledning = True
        continue
    if para.style.name == 'Heading 1' and in_innledning:
        break

    if in_innledning:
        if para.style.name == 'Heading 2' and 'Avgrensninger' in para.text:
            avgrensninger_end = child
        elif avgrensninger_end is not None and para.style.name == 'Heading 2':
            # Next H2 found — insert before it
            break
        elif avgrensninger_end is not None:
            avgrensninger_end = child  # keep updating to last para of section

# Build Antagelser elements
new_elems = []
for text, kind in antagelser_tekst:
    if kind == "heading":
        new_elems.append(make_h2(text))
    else:
        new_elems.append(make_para(text, 'Normal'))

# Insert after avgrensninger_end
if avgrensninger_end is not None:
    ref = avgrensninger_end
    for elem in new_elems:
        ref.addnext(elem)
        ref = elem
    print("   Antagelser lagt til etter Avgrensninger.\n")
else:
    print("   ADVARSEL: Fant ikke Avgrensninger-seksjonen.\n")


# ── lagre ──────────────────────────────────────────────────────────────────────
doc.save(DOC)
print(f"Lagret → {DOC}")
