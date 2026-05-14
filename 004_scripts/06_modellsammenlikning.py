"""
Steg 6: Sammenligner Naiv, SARIMA og Gradient Boosting på testsettet.
Produserer tabell 6.2 og figur 6.2 fra rapporten.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path
from sklearn.metrics import mean_squared_error, mean_absolute_error

ROOT    = Path(__file__).parent.parent
PROC    = ROOT / "002_data" / "processed"
FIGURER = ROOT / "005_report" / "figures"

TRAIN_FRAC = 0.80

VISNINGSNAVN = {
    "Terrassebord":  "Terrassebord (28x120)",
    "Planke":        "Planke (48x98)",
    "Terrasseskrue": "Terrasseskrue (4,2x55)",
    "Skrue5x90":     "Skrue 5x90",
}


def mape(faktisk: np.ndarray, prognose: np.ndarray) -> float:
    mask = faktisk > 0
    if mask.sum() == 0:
        return np.nan
    return float(np.mean(np.abs((faktisk[mask] - prognose[mask]) / faktisk[mask])) * 100)


def evaluer(faktisk: np.ndarray, prognose: np.ndarray) -> dict:
    return {
        "RMSE": round(float(np.sqrt(mean_squared_error(faktisk, prognose))), 2),
        "MAE":  round(float(mean_absolute_error(faktisk, prognose)), 2),
        "MAPE": round(mape(faktisk, prognose), 1),
    }


def naiv_prognose(serie: pd.Series, n_tren: int) -> np.ndarray:
    """f_t = d_{t-1}: siste kjente verdi."""
    test = serie.iloc[n_tren:]
    # En steg frem: bruk forrige faktiske verdi
    naiv = serie.iloc[n_tren - 1: n_tren + len(test) - 1].values
    return naiv


def plot_prognoser(df_faktisk: pd.DataFrame,
                   sarima_prog: pd.DataFrame,
                   gb_prog: pd.DataFrame):
    n_prod = len(df_faktisk.columns)
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    fig.suptitle("Figur 6.2 – Prognose vs. faktisk etterspørsel (testperioden)", fontsize=12)
    axes = axes.flatten()

    for i, kol in enumerate(df_faktisk.columns):
        ax     = axes[i]
        n_tren = int(len(df_faktisk) * TRAIN_FRAC)
        test   = df_faktisk[kol].iloc[n_tren:]

        ax.plot(test.index, test.values, color="black", linewidth=1.2,
                label="Faktisk", zorder=4)

        # Naiv
        naiv = naiv_prognose(df_faktisk[kol], n_tren)
        ax.plot(test.index, naiv, color="grey", linewidth=1.0,
                linestyle=":", label="Naiv", zorder=2)

        # SARIMA
        if kol in sarima_prog.columns:
            s_prog = sarima_prog[kol].dropna()
            ax.plot(s_prog.index, s_prog.values, color="#d62728",
                    linewidth=1.0, linestyle="--", label="SARIMA", zorder=3)

        # Gradient Boosting
        if kol in gb_prog.columns:
            g_prog = gb_prog[kol].dropna()
            ax.plot(g_prog.index, g_prog.values, color="#2ca02c",
                    linewidth=1.2, label="Gradient Boosting", zorder=5)

        ax.set_title(f"{VISNINGSNAVN.get(kol, kol)}\n(Beste: Gradient Boosting)", fontsize=9)
        ax.set_ylabel("Salg")
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b\n%Y"))
        ax.legend(fontsize=7)
        ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    ut = FIGURER / "fig6_2_modellsammenlikning.png"
    plt.savefig(ut, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Figur lagret: {ut.name}")


def main():
    df = pd.read_csv(PROC / "ukentlig_salg.csv", index_col=0, parse_dates=True)

    sarima_prog = pd.read_csv(PROC / "sarima_prognoser.csv", index_col=0,
                              parse_dates=True, date_format="%Y-%m-%d")
    gb_prog     = pd.read_csv(PROC / "gb_prognoser.csv",     index_col=0,
                              parse_dates=True, date_format="%Y-%m-%d")

    rader = []
    for kol in df.columns:
        n_tren = int(len(df) * TRAIN_FRAC)
        faktisk = df[kol].iloc[n_tren:].values

        # Naiv
        naiv = naiv_prognose(df[kol], n_tren)
        rader.append({"Produkt": VISNINGSNAVN.get(kol, kol),
                      "Modell": "Naiv", **evaluer(faktisk, naiv)})

        # Felles datoindeks for SARIMA og GB (bruk snitt av felles datoer)
        test_index = df[kol].iloc[n_tren:].index

        # SARIMA
        if kol in sarima_prog.columns:
            s_serie = sarima_prog[kol].reindex(test_index).ffill().bfill()
            s_p = s_serie.values[:len(faktisk)]
            rader.append({"Produkt": VISNINGSNAVN.get(kol, kol),
                          "Modell": "SARIMA", **evaluer(faktisk, s_p)})

        # Gradient Boosting
        if kol in gb_prog.columns:
            g_serie = gb_prog[kol].reindex(test_index).ffill().bfill()
            g_p = g_serie.values[:len(faktisk)]
            rader.append({"Produkt": VISNINGSNAVN.get(kol, kol),
                          "Modell": "Gradient Boosting", **evaluer(faktisk, g_p)})

    tabell = pd.DataFrame(rader)
    print("\nTabell 6.2 – Modellsammenlikning (testsett):")
    print(tabell.to_string(index=False))

    tabell.to_csv(PROC / "tabell_6_2_modellsammenlikning.csv", index=False)

    plot_prognoser(df, sarima_prog, gb_prog)


if __name__ == "__main__":
    main()
