# Vedlegg – Python-kode

Alle analyser er gjennomført i Python 3. Koden kjøres fra prosjektets rotmappe med kommandoen `python 004_scripts/kjor_alt.py`. Avhengigheter er spesifisert i `requirements.txt`.

---

## Vedlegg A – Datainnlasting og rensing (`01_last_inn_data.py`)

```python
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
HEADER_RADER = 8

PRODUKT_KOLONNER = {
    "Terrassebord": 1,
    "Planke":       4,
    "Terrasseskrue": 7,
    "Skrue5x90":    10,
}


def uke_til_dato(yyyyww: int) -> pd.Timestamp:
    s = str(int(yyyyww))
    return pd.Timestamp.fromisocalendar(int(s[:4]), int(s[4:]), 1)


def main():
    xl   = pd.read_excel(EXCEL_FIL, header=None)
    data = xl.iloc[HEADER_RADER:].reset_index(drop=True)
    data[0] = data[0].astype(str).str.strip()
    dato = data[0].apply(
        lambda x: uke_til_dato(x) if x.replace('.', '').isdigit() else pd.NaT
    )
    df = pd.DataFrame({"Dato": dato})
    for namn, kol in PRODUKT_KOLONNER.items():
        serie = data[kol].replace("-", np.nan).astype(float)
        df[namn] = serie.clip(lower=0).fillna(0).values
    df = df.dropna(subset=["Dato"]).set_index("Dato").sort_index()
    df = df.loc["2024-01-01":"2026-04-30"]
    df.to_csv(PROC / "ukentlig_salg.csv")


if __name__ == "__main__":
    main()
```

---

## Vedlegg B – Deskriptiv analyse (`02_deskriptiv_analyse.py`)

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path

ROOT    = Path(__file__).parent.parent
PROC    = ROOT / "002_data" / "processed"
FIGURER = ROOT / "005_report" / "figures"

VISNINGSNAVN = {
    "Terrassebord":  "Terrassebord (28x120)",
    "Planke":        "Planke (48x98)",
    "Terrasseskrue": "Terrasseskrue (4,2x55)",
    "Skrue5x90":     "Skrue 5x90",
}


def deskriptiv_tabell(df):
    rader = []
    for kol in df.columns:
        s = df[kol]
        rader.append({
            "Produkt": VISNINGSNAVN.get(kol, kol),
            "N": len(s), "Snitt": round(s.mean(), 1),
            "Std": round(s.std(), 1), "Min": round(s.min(), 1),
            "Q1": round(s.quantile(0.25), 1), "Median": round(s.median(), 1),
            "Q3": round(s.quantile(0.75), 1), "Maks": round(s.max(), 1),
            "CV%": f"{round(s.std() / s.mean() * 100)}%",
        })
    return pd.DataFrame(rader)


def main():
    df = pd.read_csv(PROC / "ukentlig_salg.csv", index_col=0, parse_dates=True)
    tabell = deskriptiv_tabell(df)
    tabell.to_csv(PROC / "tabell_6_1_deskriptiv.csv", index=False)

    fig, axes = plt.subplots(2, 2, figsize=(14, 8))
    fig.suptitle("Figur 6.1 – Ukentlig salg per produkt med trendlinje", fontsize=13)
    for i, kol in enumerate(df.columns):
        ax = axes.flatten()[i]
        s  = df[kol]
        ax.plot(s.index, s.values, linewidth=0.9, label="Ukentlig salg")
        ax.plot(s.index, s.rolling(4).mean(), linestyle="--", label="4-ukers snitt")
        x = np.arange(len(s))
        ax.plot(s.index, np.poly1d(np.polyfit(x, s.values, 1))(x),
                linestyle="-.", color="red", label="Trend")
        ax.set_title(VISNINGSNAVN.get(kol, kol), fontsize=10)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b\n%Y"))
        ax.legend(fontsize=7)
    plt.tight_layout()
    plt.savefig(FIGURER / "fig6_1_ukentlig_salg.png", dpi=150, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    main()
```

---

## Vedlegg C – Stasjonaritetstest og ACF/PACF (`03_stasjonaritet_acf_pacf.py`)

```python
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
    "Terrassebord":  "Terrassebord (28x120)",  "Planke": "Planke (48x98)",
    "Terrasseskrue": "Terrasseskrue (4,2x55)", "Skrue5x90": "Skrue 5x90",
}


def kjor_adf(serie, navn):
    s_pos = serie.replace(0, 0.01)
    resultater = []
    for label, s in [("Original", serie),
                     ("Log + diff (d=1)", np.log(s_pos).diff().dropna())]:
        res = adfuller(s, autolag="AIC")
        resultater.append({
            "Produkt": VISNINGSNAVN.get(navn, navn), "Serie": label,
            "ADF-stat": round(res[0], 3), "p-verdi": round(res[1], 4),
            "Krit. 5%": round(res[4]["5%"], 3),
            "Stasjonær": "✓" if res[1] < 0.05 else "✗",
        })
    return resultater


def main():
    df = pd.read_csv(PROC / "ukentlig_salg.csv", index_col=0, parse_dates=True)
    alle = []
    for kol in df.columns:
        alle.extend(kjor_adf(df[kol], kol))
    pd.DataFrame(alle).to_csv(PROC / "adf_resultater.csv", index=False)

    fig, axes = plt.subplots(len(df.columns), 2, figsize=(13, 12))
    for i, kol in enumerate(df.columns):
        s_diff = np.log(df[kol].replace(0, 0.01)).diff().dropna()
        plot_acf(s_diff, ax=axes[i, 0], lags=26, zero=False,
                 title=f"ACF – {VISNINGSNAVN.get(kol, kol)}")
        plot_pacf(s_diff, ax=axes[i, 1], lags=26, zero=False, method="ywm",
                  title=f"PACF – {VISNINGSNAVN.get(kol, kol)}")
        for ax in axes[i]:
            for lag in [13, 26]:
                ax.axvline(lag, color="red", linestyle="--", linewidth=0.8)
    plt.tight_layout()
    plt.savefig(FIGURER / "fig_acf_pacf.png", dpi=150, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    main()
```

---

## Vedlegg D – SARIMA-modellering (`04_sarima.py`)

```python
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

ORDER      = (1, 1, 1)
SEASONAL   = (1, 0, 1, 13)
TRAIN_FRAC = 0.80

VISNINGSNAVN = {
    "Terrassebord":  "Terrassebord (28x120)",  "Planke": "Planke (48x98)",
    "Terrasseskrue": "Terrasseskrue (4,2x55)", "Skrue5x90": "Skrue 5x90",
}


def main():
    df = pd.read_csv(PROC / "ukentlig_salg.csv", index_col=0, parse_dates=True)
    resultater, modell_tabell, prognoser = {}, [], {}

    for kol in df.columns:
        serie  = df[kol]
        n_tren = int(len(serie) * TRAIN_FRAC)
        s_log  = np.log(serie.replace(0, 0.01))
        modell = SARIMAX(s_log.iloc[:n_tren], order=ORDER, seasonal_order=SEASONAL,
                         enforce_stationarity=False, enforce_invertibility=False)
        res = modell.fit(disp=False)
        resultater[kol] = res
        modell_tabell.append({
            "Produkt": VISNINGSNAVN.get(kol, kol),
            "AIC": round(res.aic, 1), "BIC": round(res.bic, 1),
            "Log-likelihood": round(res.llf, 1),
        })
        n_test     = len(serie) - n_tren
        test_index = serie.index[n_tren:]
        prognoser[kol] = pd.Series(
            np.exp(res.forecast(steps=n_test).values), index=test_index, name=kol
        )

    pd.DataFrame(modell_tabell).to_csv(PROC / "sarima_modell_tabell.csv", index=False)

    lb_rader = []
    for navn, res in resultater.items():
        for lag in [13, 26]:
            lb = acorr_ljungbox(res.resid, lags=[lag], return_df=True)
            p  = float(lb["lb_pvalue"].iloc[0])
            lb_rader.append({
                "Produkt": VISNINGSNAVN.get(navn, navn), "Lag": lag,
                "Q-stat": round(float(lb["lb_stat"].iloc[0]), 2),
                "p-verdi": round(p, 4),
                "Konklusjon": "Ingen autokorrelasjon ✓" if p > 0.05
                              else "Signifikant autokorrelasjon",
            })
    pd.DataFrame(lb_rader).to_csv(PROC / "ljung_box.csv", index=False)
    pd.DataFrame(prognoser).to_csv(PROC / "sarima_prognoser.csv")


if __name__ == "__main__":
    main()
```

---

## Vedlegg E – Gradient Boosting (`05_gradient_boosting.py`)

```python
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error

ROOT = Path(__file__).parent.parent
PROC = ROOT / "002_data" / "processed"

GB_PARAMS  = dict(n_estimators=200, learning_rate=0.05, max_depth=3, random_state=42)
TRAIN_FRAC = 0.80

VISNINGSNAVN = {
    "Terrassebord":  "Terrassebord (28x120)",  "Planke": "Planke (48x98)",
    "Terrasseskrue": "Terrasseskrue (4,2x55)", "Skrue5x90": "Skrue 5x90",
}


def lag_features(serie):
    df = pd.DataFrame({"y": serie.values}, index=serie.index)
    for lag in range(1, 9):
        df[f"lag_{lag}"] = df["y"].shift(lag)
    df["rull_snitt_4"] = df["y"].shift(1).rolling(4).mean()
    df["rull_snitt_8"] = df["y"].shift(1).rolling(8).mean()
    df["uke_nr"]       = serie.index.isocalendar().week.astype(int).values
    df["sesong_mod13"] = df["uke_nr"] % 13
    return df.dropna()


def main():
    df = pd.read_csv(PROC / "ukentlig_salg.csv", index_col=0, parse_dates=True)
    resultater, alle_prognoser = [], {}

    for kol in df.columns:
        feat       = lag_features(df[kol])
        split_dato = df[kol].index[int(len(df[kol]) * TRAIN_FRAC)]
        tren = feat[feat.index < split_dato]
        test = feat[feat.index >= split_dato]

        modell = GradientBoostingRegressor(**GB_PARAMS)
        modell.fit(tren.drop(columns="y"), tren["y"])
        y_hat = np.clip(modell.predict(test.drop(columns="y")), 0, None)

        y_test = test["y"].values
        mask   = y_test > 0
        mape   = float(np.mean(np.abs((y_test[mask] - y_hat[mask]) / y_test[mask])) * 100)
        resultater.append({
            "Produkt": VISNINGSNAVN.get(kol, kol),
            "RMSE": round(float(np.sqrt(mean_squared_error(y_test, y_hat))), 2),
            "MAE":  round(float(mean_absolute_error(y_test, y_hat)), 2),
            "MAPE%": round(mape, 1),
        })
        alle_prognoser[kol] = pd.Series(y_hat, index=test.index, name=kol)

    pd.DataFrame(resultater).to_csv(PROC / "gb_resultater.csv", index=False)
    pd.DataFrame(alle_prognoser).to_csv(PROC / "gb_prognoser.csv")


if __name__ == "__main__":
    main()
```

---

## Vedlegg F – Modellsammenlikning (`06_modellsammenlikning.py`)

```python
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
    "Terrassebord":  "Terrassebord (28x120)",  "Planke": "Planke (48x98)",
    "Terrasseskrue": "Terrasseskrue (4,2x55)", "Skrue5x90": "Skrue 5x90",
}


def mape(y, yhat):
    mask = y > 0
    return float(np.mean(np.abs((y[mask] - yhat[mask]) / y[mask])) * 100) if mask.sum() else np.nan


def evaluer(y, yhat):
    return {
        "RMSE": round(float(np.sqrt(mean_squared_error(y, yhat))), 2),
        "MAE":  round(float(mean_absolute_error(y, yhat)), 2),
        "MAPE": round(mape(y, yhat), 1),
    }


def main():
    df = pd.read_csv(PROC / "ukentlig_salg.csv", index_col=0, parse_dates=True)
    sarima = pd.read_csv(PROC / "sarima_prognoser.csv", index_col=0,
                         parse_dates=True, date_format="%Y-%m-%d")
    gb     = pd.read_csv(PROC / "gb_prognoser.csv", index_col=0,
                         parse_dates=True, date_format="%Y-%m-%d")
    rader  = []

    for kol in df.columns:
        n_tren     = int(len(df) * TRAIN_FRAC)
        faktisk    = df[kol].iloc[n_tren:].values
        test_index = df[kol].iloc[n_tren:].index

        # Naiv
        naiv = df[kol].iloc[n_tren - 1:n_tren + len(faktisk) - 1].values
        rader.append({"Produkt": VISNINGSNAVN.get(kol, kol),
                      "Modell": "Naiv", **evaluer(faktisk, naiv)})
        # SARIMA
        s_p = sarima[kol].reindex(test_index).ffill().bfill().values[:len(faktisk)]
        rader.append({"Produkt": VISNINGSNAVN.get(kol, kol),
                      "Modell": "SARIMA", **evaluer(faktisk, s_p)})
        # GB
        g_p = gb[kol].reindex(test_index).ffill().bfill().values[:len(faktisk)]
        rader.append({"Produkt": VISNINGSNAVN.get(kol, kol),
                      "Modell": "Gradient Boosting", **evaluer(faktisk, g_p)})

    pd.DataFrame(rader).to_csv(PROC / "tabell_6_2_modellsammenlikning.csv", index=False)


if __name__ == "__main__":
    main()
```

---

## Vedlegg G – Lagerstyring og simulering (`07_lagerstyring.py`)

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path

ROOT    = Path(__file__).parent.parent
PROC    = ROOT / "002_data" / "processed"
FIGURER = ROOT / "005_report" / "figures"

Z, L, K, H_RATE = 1.645, 1, 500, 0.25
VAREPRIS = {"Terrassebord": 24, "Planke": 29, "Terrasseskrue": 108, "Skrue5x90": 90}
VISNINGSNAVN = {
    "Terrassebord":  "Terrassebord (28x120)",  "Planke": "Planke (48x98)",
    "Terrasseskrue": "Terrasseskrue (4,2x55)", "Skrue5x90": "Skrue 5x90",
}


def beregn(df):
    rader = []
    for kol in df.columns:
        mu, std = df[kol].mean(), df[kol].std()
        h = VAREPRIS.get(kol, 50) * H_RATE
        ss, rop, eoq = (Z * std * np.sqrt(L),
                        mu * L + Z * std * np.sqrt(L),
                        np.sqrt(2 * K * mu * 52 / h))
        rader.append({"Produkt": VISNINGSNAVN.get(kol, kol), "L": L,
                      "μ": round(mu, 1), "σ_d": round(std, 1),
                      "SS": round(ss, 1), "ROP": round(rop, 1), "Q*": round(eoq)})
    return pd.DataFrame(rader)


def sim_a(serie, mu):
    lager, utsalg, beh = np.zeros(len(serie)), np.zeros(len(serie)), mu * 1.5
    for t, d in enumerate(serie.values):
        utsalg[t] = max(d - beh, 0)
        beh = max(beh - d, 0)
        lager[t] = beh
        if beh < mu * 0.5:
            beh += mu * 2
    return lager, utsalg


def sim_b(serie, ss, rop, q):
    lager, utsalg, beh = np.zeros(len(serie)), np.zeros(len(serie)), rop + q
    for t, d in enumerate(serie.values):
        utsalg[t] = max(d - beh, 0)
        beh = max(beh - d, 0)
        lager[t] = beh
        if beh < rop:
            beh += q
    return lager, utsalg


def main():
    df     = pd.read_csv(PROC / "ukentlig_salg.csv", index_col=0, parse_dates=True)
    params = beregn(df)
    params.to_csv(PROC / "tabell_6_3_lagerstorrelser.csv", index=False)

    rader = []
    for kol in df.columns:
        p = params[params["Produkt"] == VISNINGSNAVN.get(kol, kol)].iloc[0]
        la, ua = sim_a(df[kol], float(p["μ"]))
        lb, ub = sim_b(df[kol], float(p["SS"]), float(p["ROP"]), float(p["Q*"]))
        rader.append({
            "Produkt": VISNINGSNAVN.get(kol, kol),
            "Lager A": round(np.mean(la), 1), "Lager B": round(np.mean(lb), 1),
            "Utsalg A": round(np.sum(ua), 1), "Utsalg B": round(np.sum(ub), 1),
            "Forbedring": round(np.sum(ua) - np.sum(ub), 1),
        })
    pd.DataFrame(rader).to_csv(PROC / "tabell_6_4_simulering.csv", index=False)


if __name__ == "__main__":
    main()
```
