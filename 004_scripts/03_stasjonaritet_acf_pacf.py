"""
Steg 3: Stasjonaritetstest (ADF) og ACF/PACF-analyse.
Produserer ADF-tabellen og figur med ACF/PACF for log-differensierte serier.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

ROOT    = Path(__file__).parent.parent
PROC    = ROOT / "002_data" / "processed"
FIGURER = ROOT / "005_report" / "figures"

VISNINGSNAVN = {
    "Terrassebord":  "Terrassebord (28x120)",
    "Planke":        "Planke (48x98)",
    "Terrasseskrue": "Terrasseskrue (4,2x55)",
    "Skrue5x90":     "Skrue 5x90",
}

SESONGLAG = [13, 26]  # Markeres med røde stiplede linjer i ACF/PACF


def kjor_adf(serie: pd.Series, navn: str) -> list[dict]:
    """Kjører ADF-test på original og log-differensiert serie."""
    resultater = []

    # Erstatt nuller med liten verdi for log-transformasjon
    s_pos = serie.replace(0, 0.01)

    for label, s in [("Original", serie), ("Log + diff (d=1)", np.log(s_pos).diff().dropna())]:
        res = adfuller(s, autolag="AIC")
        resultater.append({
            "Produkt": VISNINGSNAVN.get(navn, navn),
            "Serie":   label,
            "ADF-stat": round(res[0], 3),
            "p-verdi":  round(res[1], 4),
            "Krit. 5%": round(res[4]["5%"], 3),
            "Stasjonær": "✓" if res[1] < 0.05 else "✗",
        })
    return resultater


def plot_acf_pacf(df: pd.DataFrame):
    n_prod = len(df.columns)
    fig, axes = plt.subplots(n_prod, 2, figsize=(13, 3 * n_prod))
    fig.suptitle("ACF og PACF – Log-differensierte serier\n"
                 "(Brukes til å identifisere SARIMA-parametere)", fontsize=11)

    for i, kol in enumerate(df.columns):
        s_pos = df[kol].replace(0, 0.01)
        s_diff = np.log(s_pos).diff().dropna()

        ax_acf  = axes[i, 0]
        ax_pacf = axes[i, 1]

        plot_acf(s_diff, ax=ax_acf, lags=26, alpha=0.05, zero=False,
                 title=f"ACF – {VISNINGSNAVN.get(kol, kol)}")
        plot_pacf(s_diff, ax=ax_pacf, lags=26, alpha=0.05, zero=False,
                  method="ywm",
                  title=f"PACF – {VISNINGSNAVN.get(kol, kol)}")

        # Marker sesonglag med røde stiplede linjer
        for ax in [ax_acf, ax_pacf]:
            for lag in SESONGLAG:
                ax.axvline(lag, color="red", linestyle="--", linewidth=0.8, alpha=0.7)
            ax.set_xlabel("Lag")

    plt.tight_layout()
    ut = FIGURER / "fig_acf_pacf.png"
    plt.savefig(ut, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Figur lagret: {ut.name}")


def main():
    df = pd.read_csv(PROC / "ukentlig_salg.csv", index_col=0, parse_dates=True)

    # ADF-test
    alle = []
    for kol in df.columns:
        alle.extend(kjor_adf(df[kol], kol))

    adf_tabell = pd.DataFrame(alle)
    print("\nADF-stasjonaritetstest:")
    print(adf_tabell.to_string(index=False))

    adf_tabell.to_csv(PROC / "adf_resultater.csv", index=False)
    print(f"\nLagret: adf_resultater.csv")

    # ACF/PACF-plott
    plot_acf_pacf(df)


if __name__ == "__main__":
    main()
