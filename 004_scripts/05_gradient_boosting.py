"""
Steg 5: Gradient Boosting-prognosemodell.
Prediktorvektor: lagget etterspørsel (8 uker), rullerende snitt (4/8 uker),
ukenummer og sesongindeks modulo 13.
Produserer prognoser på testsettet (én steg om gangen med faktiske lagverdier).
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error

ROOT = Path(__file__).parent.parent
PROC = ROOT / "002_data" / "processed"

# Hyperparametre fra rapporten
GB_PARAMS = dict(n_estimators=200, learning_rate=0.05, max_depth=3, random_state=42)
TRAIN_FRAC = 0.80

VISNINGSNAVN = {
    "Terrassebord":  "Terrassebord (28x120)",
    "Planke":        "Planke (48x98)",
    "Terrasseskrue": "Terrasseskrue (4,2x55)",
    "Skrue5x90":     "Skrue 5x90",
}


def lag_features(serie: pd.Series) -> pd.DataFrame:
    """Bygg prediktormatrise for én produktserie."""
    df = pd.DataFrame({"y": serie.values}, index=serie.index)

    for lag in range(1, 9):
        df[f"lag_{lag}"] = df["y"].shift(lag)

    df["rull_snitt_4"] = df["y"].shift(1).rolling(4).mean()
    df["rull_snitt_8"] = df["y"].shift(1).rolling(8).mean()
    df["uke_nr"]       = serie.index.isocalendar().week.astype(int).values
    df["sesong_mod13"] = df["uke_nr"] % 13

    return df.dropna()


def tren_og_prognose(serie: pd.Series) -> tuple[np.ndarray, np.ndarray, pd.DatetimeIndex]:
    """
    Returnerer (faktisk, prognose, datoindeks) for testperioden.
    Split-dato bestemmes av original serie (80/20), ikke av feat-lengde,
    slik at test-perioden er lik SARIMA.
    """
    feat = lag_features(serie)

    # Finn split-dato basert på original serielengde
    split_dato = serie.index[int(len(serie) * TRAIN_FRAC)]

    feat_tren = feat[feat.index < split_dato]
    feat_test = feat[feat.index >= split_dato]

    X_tren = feat_tren.drop(columns="y").values
    y_tren = feat_tren["y"].values
    X_test = feat_test.drop(columns="y").values
    y_test = feat_test["y"].values

    modell = GradientBoostingRegressor(**GB_PARAMS)
    modell.fit(X_tren, y_tren)

    y_hat = np.clip(modell.predict(X_test), 0, None)

    return y_test, y_hat, feat_test.index


def mape(faktisk: np.ndarray, prognose: np.ndarray) -> float:
    mask = faktisk > 0
    if mask.sum() == 0:
        return np.nan
    return float(np.mean(np.abs((faktisk[mask] - prognose[mask]) / faktisk[mask])) * 100)


def main():
    df = pd.read_csv(PROC / "ukentlig_salg.csv", index_col=0, parse_dates=True)

    resultater = []
    alle_prognoser = {}

    for kol in df.columns:
        print(f"Trener Gradient Boosting for {kol} ...", end=" ", flush=True)
        y_test, y_hat, test_idx = tren_og_prognose(df[kol])

        rmse = float(np.sqrt(mean_squared_error(y_test, y_hat)))
        mae  = float(mean_absolute_error(y_test, y_hat))
        mp   = mape(y_test, y_hat)

        resultater.append({
            "Produkt": VISNINGSNAVN.get(kol, kol),
            "RMSE":    round(rmse, 2),
            "MAE":     round(mae, 2),
            "MAPE%":   round(mp, 1),
        })

        alle_prognoser[kol] = pd.Series(y_hat, index=test_idx, name=kol)
        print(f"MAPE = {mp:.1f}%")

    tabell = pd.DataFrame(resultater)
    print("\nGradient Boosting – Testresultater:")
    print(tabell.to_string(index=False))

    tabell.to_csv(PROC / "gb_resultater.csv", index=False)

    prog_df = pd.DataFrame(alle_prognoser)
    prog_df.to_csv(PROC / "gb_prognoser.csv")
    print(f"\nGB-prognoser lagret: gb_prognoser.csv")


if __name__ == "__main__":
    main()
