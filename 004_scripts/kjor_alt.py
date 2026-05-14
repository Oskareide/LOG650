"""
Kjører hele analysepipelinen i riktig rekkefølge.
Bruk: python 004_scripts/kjor_alt.py  (fra prosjektrot)
"""

import subprocess
import sys
from pathlib import Path

SKRIPT_DIR = Path(__file__).parent
SKRIPT = [
    "01_last_inn_data.py",
    "02_deskriptiv_analyse.py",
    "03_stasjonaritet_acf_pacf.py",
    "04_sarima.py",
    "05_gradient_boosting.py",
    "06_modellsammenlikning.py",
    "07_lagerstyring.py",
]

for s in SKRIPT:
    sti = SKRIPT_DIR / s
    print(f"\n{'='*55}")
    print(f"  Kjører: {s}")
    print(f"{'='*55}")
    resultat = subprocess.run([sys.executable, str(sti)], check=False)
    if resultat.returncode != 0:
        print(f"\nFEIL i {s} — stopper pipelinen.")
        sys.exit(1)

print("\n" + "="*55)
print("  Pipeline fullført.")
print("="*55)
