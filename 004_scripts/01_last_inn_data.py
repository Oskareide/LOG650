"""
Steg 1: Last inn og rens salgsdata fra ERP-eksport (Byggmakker Gravdal).

Filformat (Customreport):
  - Rad 0–7:  metadata/header
  - Kolonne 0: YYYYWW-ukenummer (f.eks. 202401 = 2024 uke 1)
  - Kolonnerekkefølge per produkt: Quantity | Cost price | kostpris pr enhet
    Produkt 1 (Terrassebord): kol 1–3
    Produkt 2 (Planke):       kol 4–6
    Produkt 3 (Terrasseskrue): kol 7–9
    Produkt 4 (Skrue5x90):    kol 10–12
"""

import pandas as pd
import numpy as np
from pathlib import Path

ROOT = Path(__file__).parent.parent
RAW  = ROOT / "002_data" / "raw"
PROC = ROOT / "002_data" / "processed"
PROC.mkdir(exist_ok=True)

EXCEL_FIL    = RAW / "salgsrapport Oskar v2.xlsx"
HEADER_RADER = 8   # Antall rader å hoppe over

PRODUKT_KOLONNER = {
    "Terrassebord": 1,
    "Planke":       4,
    "Terrasseskrue": 7,
    "Skrue5x90":    10,
}


def uke_til_dato(yyyyww: int) -> pd.Timestamp:
    """Konverterer YYYYWW (f.eks. 202401) til mandag i den uken."""
    s = str(int(yyyyww))
    return pd.Timestamp.fromisocalendar(int(s[:4]), int(s[4:]), 1)


def main():
    print(f"Leser: {EXCEL_FIL.name}")
    xl = pd.read_excel(EXCEL_FIL, header=None)

    # Behold bare datarader (fra rad HEADER_RADER og ned)
    data = xl.iloc[HEADER_RADER:].reset_index(drop=True)

    # Parse dato-kolonne
    data[0] = data[0].astype(str).str.strip()
    dato = data[0].apply(lambda x: uke_til_dato(x) if x.replace('.', '').isdigit() else pd.NaT)

    # Bygg renset DataFrame med én kolonne per produkt (Quantity)
    df = pd.DataFrame({"Dato": dato})
    for namn, kol in PRODUKT_KOLONNER.items():
        serie = data[kol].replace("-", np.nan).astype(float)
        serie = serie.clip(lower=0).fillna(0)
        df[namn] = serie.values

    df = df.dropna(subset=["Dato"]).set_index("Dato").sort_index()

    # Filtrer til analyseperioden
    df = df.loc["2024-01-01":"2026-04-30"]

    print(f"\nPeriode: {df.index[0].date()} → {df.index[-1].date()}")
    print(f"Antall uker: {len(df)}")
    print(f"Produkter:   {list(df.columns)}")
    print("\nDeskriptiv (spot-sjekk):")
    print(df.describe().round(1))

    ut = PROC / "ukentlig_salg.csv"
    df.to_csv(ut)
    print(f"\nLagret: {ut}")


if __name__ == "__main__":
    main()
