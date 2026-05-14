"""
Steg 2: Deskriptiv analyse.
Produserer tabell 6.1 og figur 6.1 fra rapporten.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path

ROOT    = Path(__file__).parent.parent
PROC    = ROOT / "002_data" / "processed"
FIGURER = ROOT / "005_report" / "figures"
FIGURER.mkdir(exist_ok=True)

PRODUKTER = ["Terrassebord", "Planke", "Terrasseskrue", "Skrue5x90"]
VISNINGSNAVN = {
    "Terrassebord":  "Terrassebord (28x120)",
    "Planke":        "Planke (48x98)",
    "Terrasseskrue": "Terrasseskrue (4,2x55)",
    "Skrue5x90":     "Skrue 5x90",
}


def deskriptiv_tabell(df: pd.DataFrame) -> pd.DataFrame:
    rader = []
    for kol in df.columns:
        s = df[kol]
        rader.append({
            "Produkt": VISNINGSNAVN.get(kol, kol),
            "N":       len(s),
            "Snitt":   round(s.mean(), 1),
            "Std":     round(s.std(), 1),
            "Min":     round(s.min(), 1),
            "Q1":      round(s.quantile(0.25), 1),
            "Median":  round(s.median(), 1),
            "Q3":      round(s.quantile(0.75), 1),
            "Maks":    round(s.max(), 1),
            "CV%":     f"{round(s.std() / s.mean() * 100)}%",
        })
    return pd.DataFrame(rader)


def plot_ukentlig_salg(df: pd.DataFrame):
    fig, axes = plt.subplots(2, 2, figsize=(14, 8))
    fig.suptitle("Figur 6.1 – Ukentlig salg per produkt med trendlinje", fontsize=13)
    axes = axes.flatten()

    for i, kol in enumerate(df.columns):
        ax = axes[i]
        s  = df[kol]
        ma = s.rolling(4).mean()

        ax.plot(s.index, s.values, color="#1f77b4", linewidth=0.9,
                label="Ukentlig salg", alpha=0.8)
        ax.plot(s.index, ma.values, color="darkorange", linewidth=1.4,
                linestyle="--", label="4-ukers snitt")

        # Lineær trendlinje
        x_num = np.arange(len(s))
        z = np.polyfit(x_num, s.values, 1)
        trend = np.poly1d(z)(x_num)
        ax.plot(s.index, trend, color="red", linewidth=1.0,
                linestyle="-.", label="Lineær trend", alpha=0.6)

        ax.set_title(VISNINGSNAVN.get(kol, kol), fontsize=10)
        ax.set_ylabel("Salg")
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b\n%Y"))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
        ax.legend(fontsize=7)
        ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    ut = FIGURER / "fig6_1_ukentlig_salg.png"
    plt.savefig(ut, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Figur lagret: {ut.name}")


def main():
    df = pd.read_csv(PROC / "ukentlig_salg.csv", index_col=0, parse_dates=True)

    tabell = deskriptiv_tabell(df)
    print("\nTabell 6.1 – Deskriptiv statistikk:")
    print(tabell.to_string(index=False))

    ut_csv = PROC / "tabell_6_1_deskriptiv.csv"
    tabell.to_csv(ut_csv, index=False)
    print(f"\nLagret: {ut_csv.name}")

    plot_ukentlig_salg(df)


if __name__ == "__main__":
    main()
