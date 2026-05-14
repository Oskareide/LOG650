"""
Steg 4: SARIMA-modellering.
Estimerer SARIMA(1,1,1)(1,0,1)_13 for alle fire produkter.
Produserer AIC/BIC-tabell, Ljung-Box-test og residual-ACF-figur.
"""

import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.graphics.tsaplots import plot_acf

warnings.filterwarnings("ignore")

ROOT    = Path(__file__).parent.parent
PROC    = ROOT / "002_data" / "processed"
FIGURER = ROOT / "005_report" / "figures"

# SARIMA-spesifikasjon fra rapporten
ORDER         = (1, 1, 1)
SEASONAL      = (1, 0, 1, 13)
TRAIN_FRAC    = 0.80

VISNINGSNAVN = {
    "Terrassebord":  "Terrassebord (28x120)",
    "Planke":        "Planke (48x98)",
    "Terrasseskrue": "Terrasseskrue (4,2x55)",
    "Skrue5x90":     "Skrue 5x90",
}


def tren_sarima(serie: pd.Series):
    s_pos = serie.replace(0, 0.01)
    s_log = np.log(s_pos)
    modell = SARIMAX(s_log, order=ORDER, seasonal_order=SEASONAL,
                     enforce_stationarity=False, enforce_invertibility=False)
    return modell.fit(disp=False)


def ljung_box_tabell(resultater: dict) -> pd.DataFrame:
    rader = []
    for navn, res in resultater.items():
        for lag in [13, 26]:
            lb = acorr_ljungbox(res.resid, lags=[lag], return_df=True)
            p  = float(lb["lb_pvalue"].iloc[0])
            q  = float(lb["lb_stat"].iloc[0])
            rader.append({
                "Produkt":    VISNINGSNAVN.get(navn, navn),
                "Lag":        lag,
                "Q-stat":     round(q, 2),
                "p-verdi":    round(p, 4),
                "Konklusjon": "Ingen autokorrelasjon ✓" if p > 0.05 else "Signifikant autokorrelasjon",
            })
    return pd.DataFrame(rader)


def plot_residual_acf(resultater: dict):
    n = len(resultater)
    fig, axes = plt.subplots(n // 2 + n % 2, 2, figsize=(13, 3 * (n // 2 + n % 2)))
    fig.suptitle("Residual-ACF fra SARIMA\n(Prikkene skal ligge innenfor konfidensintervallet)",
                 fontsize=11)
    axes = axes.flatten()

    for i, (navn, res) in enumerate(resultater.items()):
        plot_acf(res.resid, ax=axes[i], lags=26, alpha=0.05, zero=False,
                 title=f"Residual-ACF – {VISNINGSNAVN.get(navn, navn)}")
        axes[i].set_xlabel("Lag")

    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)

    plt.tight_layout()
    ut = FIGURER / "fig_residual_acf.png"
    plt.savefig(ut, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Figur lagret: {ut.name}")


def main():
    df = pd.read_csv(PROC / "ukentlig_salg.csv", index_col=0, parse_dates=True)

    resultater   = {}
    modell_tabell = []
    prognoser    = {}

    for kol in df.columns:
        print(f"Trener SARIMA for {kol} ...", end=" ", flush=True)
        serie = df[kol]
        n_tren = int(len(serie) * TRAIN_FRAC)

        res = tren_sarima(serie.iloc[:n_tren])
        resultater[kol] = res

        modell_tabell.append({
            "Produkt":        VISNINGSNAVN.get(kol, kol),
            "AIC":            round(res.aic, 1),
            "BIC":            round(res.bic, 1),
            "Log-likelihood": round(res.llf, 1),
        })

        # Prognose på testsettet (multi-step ahead) – behold datoindeks
        n_test      = len(serie) - n_tren
        test_index  = serie.index[n_tren:]
        prognose_log = res.forecast(steps=n_test)
        prog_serie   = pd.Series(np.exp(prognose_log.values), index=test_index, name=kol)
        prognoser[kol] = prog_serie

        print("ferdig")

    # Tabell: AIC/BIC
    mt = pd.DataFrame(modell_tabell)
    print("\nSARIMA(1,1,1)(1,0,1)₁₃ – Modelltilpasning:")
    print(mt.to_string(index=False))
    mt.to_csv(PROC / "sarima_modell_tabell.csv", index=False)

    # Ljung-Box
    lb = ljung_box_tabell(resultater)
    print("\nLjung-Box test:")
    print(lb.to_string(index=False))
    lb.to_csv(PROC / "ljung_box.csv", index=False)

    # Lagre prognoser
    prognoser_df = pd.DataFrame(prognoser)
    prognoser_df.to_csv(PROC / "sarima_prognoser.csv")
    print(f"\nSARIMA-prognoser lagret: sarima_prognoser.csv")

    # Lagre antall treningsuker
    pd.Series({"n_tren": int(len(df) * TRAIN_FRAC)}).to_json(PROC / "split_info.json")

    # Residual-ACF-figur
    plot_residual_acf(resultater)


if __name__ == "__main__":
    main()
