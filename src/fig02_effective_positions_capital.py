"""Figura 2 — Activos nominales vs posiciones efectivas por capital.

Primera capa del diagnóstico: concentración de pesos (HHI, N_eff,weights).
No incorpora correlación ni riesgo.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from config import TICKERS, WEIGHTS  # noqa: E402
from metrics_weights import weight_concentration  # noqa: E402
from plot_style import COLOR_EQUITY, COLOR_FIXED_INCOME, apply_style, save_figure  # noqa: E402

LABELS = {
    "es": {
        "suptitle": "Figura 2. Activos nominales vs. posiciones efectivas por capital",
        "ylabel": "Número de posiciones",
        "cat_nominal": "Activos\nnominales",
        "cat_eff": "Posiciones efectivas\npor capital",
        "annot_hhi": "HHI = {hhi:.4f}",
        "footer": (
            "Cartera diagnóstica estática 60/40 · N = {n} instrumentos · "
            "Métricas basadas en pesos objetivo · "
            r"$N_{{\mathrm{{eff,weights}}}} = 1/\sum w_i^2$"
        ),
        "stem": "fig02_effective_positions_capital_es",
    },
    "en": {
        "suptitle": "Figure 2. Nominal Assets vs. Effective Positions by Capital",
        "ylabel": "Number of positions",
        "cat_nominal": "Nominal\nassets",
        "cat_eff": "Effective positions\nby capital",
        "annot_hhi": "HHI = {hhi:.4f}",
        "footer": (
            "Static 60/40 diagnostic portfolio · N = {n} instruments · "
            "Metrics based on target weights · "
            r"$N_{{\mathrm{{eff,weights}}}} = 1/\sum w_i^2$"
        ),
        "stem": "fig02_effective_positions_capital_en",
    },
}


def make_figure(metrics: dict[str, float], lang: str) -> plt.Figure:
    labels = LABELS[lang]
    apply_style()
    fig, ax = plt.subplots(figsize=(7.2, 4.8))

    categories = [labels["cat_nominal"], labels["cat_eff"]]
    values = [metrics["n_nominal"], metrics["n_eff_weights"]]
    colors = [COLOR_FIXED_INCOME, COLOR_EQUITY]

    bars = ax.bar(categories, values, color=colors, width=0.55, zorder=3)
    ax.set_ylabel(labels["ylabel"])
    ax.set_ylim(0, max(values) * 1.25)
    ax.yaxis.grid(True, zorder=0)
    ax.set_axisbelow(True)

    for bar, val in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.15,
            f"{val:.2f}" if val != int(val) else f"{int(val)}",
            ha="center",
            va="bottom",
            fontsize=12,
            fontweight="medium",
        )

    ax.text(
        0.98,
        0.95,
        labels["annot_hhi"].format(hhi=metrics["hhi"]),
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=10,
        color="#566573",
        bbox={"boxstyle": "round,pad=0.35", "facecolor": "#F8F9F9", "edgecolor": "#D5D8DC", "linewidth": 0.8},
    )

    fig.suptitle(labels["suptitle"], fontsize=13, fontweight="semibold", y=1.02)
    fig.text(
        0.5,
        -0.04,
        labels["footer"].format(n=int(metrics["n_nominal"])),
        ha="center",
        fontsize=8.5,
        color="#566573",
    )
    fig.tight_layout()
    return fig


def main() -> None:
    metrics = weight_concentration(WEIGHTS)
    out_dir = ROOT / "data" / "processed"
    out_dir.mkdir(parents=True, exist_ok=True)

    metrics_path = out_dir / "weight_concentration.json"
    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    table = pd.DataFrame(
        [
            {"metric": "n_nominal", "value": metrics["n_nominal"]},
            {"metric": "hhi", "value": metrics["hhi"]},
            {"metric": "n_eff_weights", "value": metrics["n_eff_weights"]},
        ]
    )
    csv_path = out_dir / "weight_concentration.csv"
    table.to_csv(csv_path, index=False)

    print("=== Capa 1 — concentración de pesos ===")
    print(f"N nominal:        {metrics['n_nominal']:.0f}")
    print(f"HHI:              {metrics['hhi']:.6f}")
    print(f"N_eff,weights:    {metrics['n_eff_weights']:.4f}")
    print(f"Tickers:          {TICKERS}")
    print("\nArchivos:")
    print(f"  {metrics_path}")
    print(f"  {csv_path}")

    for lang in ("es", "en"):
        fig = make_figure(metrics, lang)
        paths = save_figure(fig, LABELS[lang]["stem"])
        plt.close(fig)
        for p in paths:
            print(f"  {p}")


if __name__ == "__main__":
    main()
