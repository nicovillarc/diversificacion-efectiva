"""Figura 1 — Portfolio Allocation (pesos objetivo constantes).

Genera versiones en español e inglés.
Solo muestra la composición de capital. No calcula concentración,
dependencia ni riesgo; no anticipa conclusiones de diversificación.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from config import (  # noqa: E402
    ASSET_CLASS,
    EQUITY_WEIGHT,
    FIXED_INCOME_WEIGHT,
    TICKERS,
    WEIGHTS,
)
from plot_style import ASSET_CLASS_COLORS, apply_style, save_figure  # noqa: E402

LABELS = {
    "es": {
        "ylabel": "Peso objetivo (%)",
        "title_a": "A. Asignación de capital por instrumento",
        "title_b": "B. Asignación por clase de activo",
        "class_equity": "Renta\nvariable",
        "class_fi": "Renta\nfija",
        "legend_equity": "Renta variable (7 instrumentos)",
        "legend_fi": "Renta fija (3 instrumentos)",
        "suptitle": "Figura 1. Asignación de capital del portafolio",
        "footer": (
            "Cartera diagnóstica estática 60/40 · N = {n} instrumentos · "
            "Pesos objetivo suman {sum_w:.0%}"
        ),
        "stem": "fig01_portfolio_allocation_es",
    },
    "en": {
        "ylabel": "Target weight (%)",
        "title_a": "A. Instrument-level capital allocation",
        "title_b": "B. Asset-class allocation",
        "class_equity": "Equity",
        "class_fi": "Fixed\nIncome",
        "legend_equity": "Equity (7 instruments)",
        "legend_fi": "Fixed Income (3 instruments)",
        "suptitle": "Figure 1. Portfolio Capital Allocation",
        "footer": (
            "Static 60/40 diagnostic portfolio · N = {n} instruments · "
            "Target weights sum to {sum_w:.0%}"
        ),
        "stem": "fig01_portfolio_allocation_en",
    },
}


def portfolio_table() -> pd.DataFrame:
    rows = [
        {"ticker": t, "asset_class": ASSET_CLASS[t], "weight": WEIGHTS[t]}
        for t in TICKERS
    ]
    df = pd.DataFrame(rows)
    df["weight_pct"] = df["weight"] * 100
    return df


def make_figure(df: pd.DataFrame, lang: str) -> plt.Figure:
    labels = LABELS[lang]
    apply_style()
    fig, axes = plt.subplots(
        1,
        2,
        figsize=(11.2, 4.6),
        gridspec_kw={"width_ratios": [3.2, 1.15]},
    )

    ax = axes[0]
    colors = [ASSET_CLASS_COLORS[c] for c in df["asset_class"]]
    bars = ax.bar(df["ticker"], df["weight_pct"], color=colors, width=0.72, zorder=3)
    ax.set_ylabel(labels["ylabel"])
    ax.set_xlabel("")
    ax.set_title(labels["title_a"], loc="left", pad=10)
    ax.set_ylim(0, max(df["weight_pct"].max() * 1.25, 18))
    ax.yaxis.grid(True, zorder=0)
    ax.set_axisbelow(True)

    for bar, w in zip(bars, df["weight_pct"]):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.35,
            f"{w:.2f}%",
            ha="center",
            va="bottom",
            fontsize=8.5,
        )

    ax2 = axes[1]
    class_weights = [EQUITY_WEIGHT * 100, FIXED_INCOME_WEIGHT * 100]
    class_labels = [labels["class_equity"], labels["class_fi"]]
    class_colors = [
        ASSET_CLASS_COLORS["equity"],
        ASSET_CLASS_COLORS["fixed_income"],
    ]
    bars2 = ax2.bar(class_labels, class_weights, color=class_colors, width=0.55, zorder=3)
    ax2.set_ylabel(labels["ylabel"])
    ax2.set_title(labels["title_b"], loc="left", pad=10)
    ax2.set_ylim(0, 75)
    ax2.yaxis.grid(True, zorder=0)
    ax2.set_axisbelow(True)
    for bar, w in zip(bars2, class_weights):
        ax2.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1.5,
            f"{w:.0f}%",
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="medium",
        )

    legend = [
        Patch(facecolor=ASSET_CLASS_COLORS["equity"], label=labels["legend_equity"]),
        Patch(facecolor=ASSET_CLASS_COLORS["fixed_income"], label=labels["legend_fi"]),
    ]
    fig.legend(
        handles=legend,
        loc="upper center",
        ncol=2,
        frameon=False,
        bbox_to_anchor=(0.5, 1.02),
    )

    fig.suptitle(labels["suptitle"], fontsize=14, fontweight="semibold", y=1.08)
    fig.text(
        0.5,
        -0.02,
        labels["footer"].format(n=len(TICKERS), sum_w=df["weight"].sum()),
        ha="center",
        fontsize=8.5,
        color="#566573",
    )
    fig.tight_layout()
    return fig


def main() -> None:
    df = portfolio_table()
    out_csv = ROOT / "data" / "processed" / "portfolio_allocation.csv"
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_csv, index=False)

    print("=== Figura 1 — Portfolio Allocation (ES / EN) ===")
    print(df.to_string(index=False))
    print(f"\nSuma de pesos: {df['weight'].sum():.6f}")
    print("\nArchivos:")
    print(f"  {out_csv}")

    for lang in ("es", "en"):
        fig = make_figure(df, lang)
        paths = save_figure(fig, LABELS[lang]["stem"])
        plt.close(fig)
        for p in paths:
            print(f"  {p}")

    # Alias sin sufijo → versión en inglés (compatibilidad)
    # No duplicamos bytes: el caller puede usar _es / _en explícitamente.


if __name__ == "__main__":
    main()
