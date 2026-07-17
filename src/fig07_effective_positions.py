"""Figura 7 — Activos nominales vs. posiciones efectivas (capital y riesgo).

Compara:
  N
  N_eff,weights = 1 / sum w_i^2
  N_eff,risk    = 1 / sum PRC_i^2
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from config import END_DATE, START_DATE, TICKERS, WEIGHTS  # noqa: E402
from metrics_effective_positions import effective_positions_summary  # noqa: E402
from plot_style import COLOR_EQUITY, COLOR_FIXED_INCOME, apply_style, save_figure  # noqa: E402

COLOR_RISK = "#922B21"  # acento sobrio para la capa de riesgo

LABELS = {
    "es": {
        "suptitle": "Figura 7. Activos nominales vs. posiciones efectivas",
        "ylabel": "Número de posiciones",
        "cat_nominal": "Activos\nnominales",
        "cat_w": "Posiciones efectivas\npor capital",
        "cat_r": "Posiciones efectivas\npor riesgo",
        "footer": (
            "N = {n} · "
            r"$N_{{\mathrm{{eff,weights}}}}=1/\sum w_i^2$ · "
            r"$N_{{\mathrm{{eff,risk}}}}=1/\sum \mathrm{{PRC}}_i^2$ · "
            "Ventana {start} a {end}"
        ),
        "stem": "fig07_effective_positions_es",
    },
    "en": {
        "suptitle": "Figure 7. Nominal Assets vs. Effective Positions",
        "ylabel": "Number of positions",
        "cat_nominal": "Nominal\nassets",
        "cat_w": "Effective positions\nby capital",
        "cat_r": "Effective positions\nby risk",
        "footer": (
            "N = {n} · "
            r"$N_{{\mathrm{{eff,weights}}}}=1/\sum w_i^2$ · "
            r"$N_{{\mathrm{{eff,risk}}}}=1/\sum \mathrm{{PRC}}_i^2$ · "
            "Sample window {start} to {end}"
        ),
        "stem": "fig07_effective_positions_en",
    },
}


def load_prc() -> pd.Series:
    path = ROOT / "data" / "processed" / "risk_contributions.csv"
    if not path.exists():
        raise FileNotFoundError(
            "Missing risk_contributions.csv; run fig05_fig06_risk_contribution.py first."
        )
    df = pd.read_csv(path, index_col=0)
    return df["prc"].reindex(TICKERS)


def make_figure(metrics: dict[str, float], lang: str) -> plt.Figure:
    labels = LABELS[lang]
    apply_style()
    fig, ax = plt.subplots(figsize=(8.4, 4.8))

    categories = [labels["cat_nominal"], labels["cat_w"], labels["cat_r"]]
    values = [
        metrics["n_nominal"],
        metrics["n_eff_weights"],
        metrics["n_eff_risk"],
    ]
    colors = [COLOR_FIXED_INCOME, COLOR_EQUITY, COLOR_RISK]

    bars = ax.bar(categories, values, color=colors, width=0.58, zorder=3)
    ax.set_ylabel(labels["ylabel"])
    ax.set_ylim(0, max(values) * 1.28)
    ax.yaxis.grid(True, zorder=0)
    ax.set_axisbelow(True)

    for bar, val in zip(bars, values):
        txt = f"{int(val)}" if abs(val - round(val)) < 1e-9 else f"{val:.2f}"
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.12,
            txt,
            ha="center",
            va="bottom",
            fontsize=12,
            fontweight="medium",
        )

    fig.suptitle(labels["suptitle"], fontsize=13, fontweight="semibold", y=1.02)
    fig.text(
        0.5,
        -0.05,
        labels["footer"].format(
            n=int(metrics["n_nominal"]),
            start=START_DATE,
            end=END_DATE,
        ),
        ha="center",
        fontsize=8.5,
        color="#566573",
    )
    fig.tight_layout()
    return fig


def main() -> None:
    prc = load_prc()
    metrics = effective_positions_summary(WEIGHTS, prc)

    out = ROOT / "data" / "processed"
    out.mkdir(parents=True, exist_ok=True)
    (out / "effective_positions.json").write_text(
        json.dumps(metrics, indent=2), encoding="utf-8"
    )
    pd.DataFrame(
        [{"metric": k, "value": v} for k, v in metrics.items()]
    ).to_csv(out / "effective_positions.csv", index=False)

    print("=== Capa 4 — posiciones efectivas ===")
    print(f"N nominal:        {metrics['n_nominal']:.0f}")
    print(f"HHI weights:      {metrics['hhi_weights']:.6f}")
    print(f"N_eff,weights:    {metrics['n_eff_weights']:.4f}")
    print(f"HHI risk:         {metrics['hhi_risk']:.6f}")
    print(f"N_eff,risk:       {metrics['n_eff_risk']:.4f}")
    print(f"sum PRC:          {metrics['sum_prc']:.12f}")

    for lang in ("es", "en"):
        fig = make_figure(metrics, lang)
        for p in save_figure(fig, LABELS[lang]["stem"]):
            print(p)
        plt.close(fig)


if __name__ == "__main__":
    main()
