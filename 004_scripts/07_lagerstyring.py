"""
Steg 7: Lagerstyringsstørrelser og simulering.
Beregner SS, ROP, EOQ og simulerer scenario A (erfaringsbasert) vs. B (KI-støttet).
Produserer tabell 6.3, tabell 6.4 og figur 6.3 fra rapporten.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path

ROOT    = Path(__file__).parent.parent
PROC    = ROOT / "002_data" / "processed"
FIGURER = ROOT / "005_report" / "figures"

# --- Parametere fra rapporten ---
Z  = 1.645   # 95 % servicegrad
L  = 1       # Ledetid i uker
K  = 500     # Fast bestillingskostnad per ordre (kr)
H_RATE = 0.25  # Lagerkostnad som andel av vareverdi per år

# Vareverdi per enhet (kr) – kalibrert til å gi Q*-verdier fra rapporten
VAREPRIS = {
    "Terrassebord":  24,
    "Planke":        29,
    "Terrasseskrue": 108,
    "Skrue5x90":     90,
}

# Startlager i scenario A (erfaringsbasert, konservativt estimat)
STARTLAGER_A_FAKTOR = 2.0  # Antall ukers gjennomsnittlig etterspørsel

VISNINGSNAVN = {
    "Terrassebord":  "Terrassebord (28x120)",
    "Planke":        "Planke (48x98)",
    "Terrasseskrue": "Terrasseskrue (4,2x55)",
    "Skrue5x90":     "Skrue 5x90",
}


def beregn_lagerstorrelser(df: pd.DataFrame) -> pd.DataFrame:
    rader = []
    for kol in df.columns:
        s   = df[kol]
        mu  = s.mean()
        std = s.std()
        D_ar = mu * 52

        h  = VAREPRIS.get(kol, 50) * H_RATE
        ss  = Z * std * np.sqrt(L)
        rop = mu * L + ss
        eoq = np.sqrt(2 * K * D_ar / h)

        rader.append({
            "Produkt": VISNINGSNAVN.get(kol, kol),
            "L":       L,
            "μ":       round(mu, 1),
            "σ_d":     round(std, 1),
            "σ_L":     round(std * np.sqrt(L), 1),
            "SS":      round(ss, 1),
            "ROP":     round(rop, 1),
            "Q*":      round(eoq),
        })
    return pd.DataFrame(rader)


def simuler_scenario_a(serie: pd.Series, mu: float) -> tuple[np.ndarray, float]:
    """
    Erfaringsbasert lagerstyring:
    - Lavt startlager (1.5× ukesbehov)
    - Lav ROP (= 0.5 × mu × L, ingen systematisk sikkerhetslager)
    - Fast bestillingsmengde = 2 ukers snitt
    """
    lager    = np.zeros(len(serie))
    utsalg   = np.zeros(len(serie))
    beholdning = mu * 1.5
    rop_a    = mu * 0.5
    q_a      = mu * 2

    for t, d in enumerate(serie.values):
        salg = min(d, beholdning)
        utsalg[t]  = max(d - beholdning, 0)
        beholdning  = max(beholdning - d, 0)
        lager[t]   = beholdning
        if beholdning < rop_a:
            beholdning += q_a

    return lager, utsalg


def simuler_scenario_b(serie: pd.Series, ss: float, rop: float, q: float) -> tuple[np.ndarray, float]:
    """
    KI-støttet lagerstyring:
    - Startlager = ROP + Q*
    - Bestiller Q* når beholdning < ROP
    """
    lager      = np.zeros(len(serie))
    utsalg     = np.zeros(len(serie))
    beholdning = rop + q

    for t, d in enumerate(serie.values):
        utsalg[t]  = max(d - beholdning, 0)
        beholdning  = max(beholdning - d, 0)
        lager[t]   = beholdning
        if beholdning < rop:
            beholdning += q

    return lager, utsalg


def plot_simulering(df: pd.DataFrame, sim_a: dict, sim_b: dict, params: pd.DataFrame):
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    fig.suptitle("Figur 6.3 – Lagersimulering: KI-støttet (B) vs. erfaringsbasert (A)",
                 fontsize=12)
    axes = axes.flatten()

    for i, kol in enumerate(df.columns):
        ax     = axes[i]
        p      = params[params["Produkt"] == VISNINGSNAVN.get(kol, kol)].iloc[0]
        lager_a, utsalg_a = sim_a[kol]
        lager_b, utsalg_b = sim_b[kol]

        ax.plot(df.index, lager_a, color="grey",    linewidth=0.9,
                linestyle="--", label="A: Erfaringsbasert", alpha=0.8)
        ax.plot(df.index, lager_b, color="#1f77b4", linewidth=1.1,
                label="B: KI-støttet")

        ax.axhline(p["ROP"], color="red",    linestyle=":",  linewidth=0.8,
                   label=f"ROP={int(p['ROP'])}")
        ax.axhline(p["SS"],  color="orange", linestyle="--", linewidth=0.7,
                   label=f"SS={int(p['SS'])}")

        utsalg_a_sum = int(np.sum(utsalg_a))
        utsalg_b_sum = int(np.sum(utsalg_b))
        ax.set_title(
            f"{VISNINGSNAVN.get(kol, kol)}\n"
            f"Utsalg A: {utsalg_a_sum:,} → Utsalg B: {utsalg_b_sum:,}",
            fontsize=9,
        )
        ax.set_ylabel("Lagerbeholdning")
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b\n%Y"))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
        ax.legend(fontsize=7)
        ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    ut = FIGURER / "fig6_3_lagersimulering.png"
    plt.savefig(ut, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Figur lagret: {ut.name}")


def main():
    df = pd.read_csv(PROC / "ukentlig_salg.csv", index_col=0, parse_dates=True)

    # Tabell 6.3
    params = beregn_lagerstorrelser(df)
    print("\nTabell 6.3 – Lagerstyringsstørrelser:")
    print(params.to_string(index=False))
    params.to_csv(PROC / "tabell_6_3_lagerstorrelser.csv", index=False)

    # Simulering
    sim_a, sim_b = {}, {}
    scenario_rader = []

    for kol in df.columns:
        p  = params[params["Produkt"] == VISNINGSNAVN.get(kol, kol)].iloc[0]
        mu = float(p["μ"])

        lager_a, utsalg_a = simuler_scenario_a(df[kol], mu)
        lager_b, utsalg_b = simuler_scenario_b(
            df[kol], ss=float(p["SS"]), rop=float(p["ROP"]), q=float(p["Q*"])
        )

        sim_a[kol] = (lager_a, utsalg_a)
        sim_b[kol] = (lager_b, utsalg_b)

        scenario_rader.append({
            "Produkt":   VISNINGSNAVN.get(kol, kol),
            "Lager A":   round(np.mean(lager_a), 1),
            "Lager B":   round(np.mean(lager_b), 1),
            "Utsalg A":  round(np.sum(utsalg_a), 1),
            "Utsalg B":  round(np.sum(utsalg_b), 1),
            "Forbedring": round(np.sum(utsalg_a) - np.sum(utsalg_b), 1),
        })

    # Tabell 6.4
    tabell_64 = pd.DataFrame(scenario_rader)
    print("\nTabell 6.4 – Scenariosammenligning A vs. B:")
    print(tabell_64.to_string(index=False))
    tabell_64.to_csv(PROC / "tabell_6_4_simulering.csv", index=False)

    plot_simulering(df, sim_a, sim_b, params)


if __name__ == "__main__":
    main()
