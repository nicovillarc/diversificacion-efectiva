"""Figura 5 — Pesos vs contribución porcentual al riesgo (PRC).

Figura 6 — Asignación de capital vs asignación de riesgo por clase.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from config import (  # noqa: E402
    ANNUALIZATION_FACTOR,
    ASSET_CLASS,
    END_DATE,
    START_DATE,
    TICKERS,
    WEIGHTS,
)
from metrics_risk import class_aggregates, portfolio_risk_contributions  # noqa: E402
from plot_style import COLOR_EQUITY, COLOR_FIXED_INCOME, apply_style, save_figure  # noqa: E402

LABELS_FIG5 = {
    "es": {
        "suptitle": "Figura 5. Peso en cartera vs. contribución porcentual al riesgo",
        "ylabel": "Porcentaje (%)",
        "weight": "Peso objetivo",
        "prc": "Contribución al riesgo (PRC)",
        "footer": (
            "Pesos objetivo constantes · Retornos log diarios · "
            "Ventana {start} a {end} · Σ PRC = {sum_prc:.0%}"
        ),
        "stem": "fig05_weight_vs_prc_es",
    },
    "en": {
        "suptitle": "Figure 5. Portfolio Weight vs. Percentage Risk Contribution",
        "ylabel": "Percentage (%)",
        "weight": "Target weight",
        "prc": "Risk contribution (PRC)",
        "footer": (
            "Constant target weights · Daily log returns · "
            "Sample window {start} to {end} · Σ PRC = {sum_prc:.0%}"
        ),
        "stem": "fig05_weight_vs_prc_en",
    },
}

LABELS_FIG6 = {
    "es": {
        "suptitle": "Figura 6. Asignación de capital vs. asignación de riesgo",
        "ylabel": "Porcentaje (%)",
        "capital": "Capital",
        "risk": "Riesgo (PRC)",
        "equity": "Renta variable",
        "fi": "Renta fija",
        "footer": (
            "Agregación por clase de activo · Pesos objetivo 60/40 · "
            "Ventana {start} a {end}"
        ),
        "stem": "fig06_capital_vs_risk_allocation_es",
    },
    "en": {
        "suptitle": "Figure 6. Capital Allocation vs. Risk Allocation",
        "ylabel": "Percentage (%)",
        "capital": "Capital",
        "risk": "Risk (PRC)",
        "equity": "Equity",
        "fi": "Fixed Income",
        "footer": (
            "Aggregation by asset class · Target weights 60/40 · "
            "Sample window {start} to {end}"
        ),
        "stem": "fig06_capital_vs_risk_allocation_en",
    },
}


def load_returns() -> pd.DataFrame:
    path = ROOT / "data" / "processed" / "log_returns.csv"
    rets = pd.read_csv(path, index_col=0, parse_dates=True)
    return rets.reindex(columns=TICKERS)


def export_artifacts(
    result: dict, class_agg: pd.DataFrame, n_observations: int
) -> None:
    out = ROOT / "data" / "processed"
    out.mkdir(parents=True, exist_ok=True)

    detail = result["detail"].copy()
    detail["asset_class"] = [ASSET_CLASS[t] for t in detail.index]
    detail["weight_pct"] = detail["weight"] * 100
    detail["prc_pct"] = detail["prc"] * 100
    detail.to_csv(out / "risk_contributions.csv")

    class_out = class_agg.copy()
    class_out["capital_pct"] = class_out["capital_weight"] * 100
    class_out["risk_pct"] = class_out["risk_share"] * 100
    class_out.to_csv(out / "risk_contributions_by_class.csv")

    summary = {
        "sigma_p_daily": result["sigma_p_daily"],
        "sigma_p_annual": result["sigma_p_annual"],
        "sum_rc": result["sum_rc"],
        "sum_prc": result["sum_prc"],
        "identity_ok": result["identity_ok"],
        "n_observations": n_observations,
        "sample_start": START_DATE,
        "sample_end": END_DATE,
        "equity_capital": float(class_agg.loc["equity", "capital_weight"]),
        "fixed_income_capital": float(class_agg.loc["fixed_income", "capital_weight"]),
        "equity_risk_share": float(class_agg.loc["equity", "risk_share"]),
        "fixed_income_risk_share": float(class_agg.loc["fixed_income", "risk_share"]),
    }
    (out / "risk_contribution_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    pd.DataFrame(
        [{"metric": k, "value": v} for k, v in summary.items()]
    ).to_csv(out / "risk_contribution_summary.csv", index=False)

    result["covariance"].to_csv(out / "covariance_matrix.csv")


def make_figure_5(detail: pd.DataFrame, sum_prc: float, lang: str) -> plt.Figure:
    labels = LABELS_FIG5[lang]
    apply_style()

    tickers = list(detail.index)
    x = np.arange(len(tickers))
    width = 0.38

    fig, ax = plt.subplots(figsize=(11.0, 5.0))
    bars_w = ax.bar(
        x - width / 2,
        detail["weight"] * 100,
        width,
        label=labels["weight"],
        color=COLOR_FIXED_INCOME,
        zorder=3,
    )
    bars_p = ax.bar(
        x + width / 2,
        detail["prc"] * 100,
        width,
        label=labels["prc"],
        color=COLOR_EQUITY,
        zorder=3,
    )

    ax.set_ylabel(labels["ylabel"])
    ax.set_xticks(x)
    ax.set_xticklabels(tickers)
    ax.yaxis.grid(True, zorder=0)
    ax.set_axisbelow(True)
    ymax = max((detail["weight"] * 100).max(), (detail["prc"] * 100).max())
    ax.set_ylim(0, ymax * 1.22)
    ax.legend(frameon=False, loc="upper right")

    for bar in list(bars_w) + list(bars_p):
        h = bar.get_height()
        if h >= 0.4:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                h + 0.25,
                f"{h:.1f}",
                ha="center",
                va="bottom",
                fontsize=7.5,
            )

    fig.suptitle(labels["suptitle"], fontsize=13, fontweight="semibold", y=1.02)
    fig.text(
        0.5,
        -0.02,
        labels["footer"].format(start=START_DATE, end=END_DATE, sum_prc=sum_prc),
        ha="center",
        fontsize=8.5,
        color="#566573",
    )
    fig.tight_layout()
    return fig


def make_figure_6(class_agg: pd.DataFrame, lang: str) -> plt.Figure:
    labels = LABELS_FIG6[lang]
    apply_style()

    # Orden fijo: equity, fixed_income
    order = [c for c in ("equity", "fixed_income") if c in class_agg.index]
    data = class_agg.loc[order]
    class_names = [
        labels["equity"] if c == "equity" else labels["fi"] for c in order
    ]

    x = np.arange(len(order))
    width = 0.32

    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    bars_c = ax.bar(
        x - width / 2,
        data["capital_weight"] * 100,
        width,
        label=labels["capital"],
        color=COLOR_FIXED_INCOME,
        zorder=3,
    )
    bars_r = ax.bar(
        x + width / 2,
        data["risk_share"] * 100,
        width,
        label=labels["risk"],
        color=COLOR_EQUITY,
        zorder=3,
    )

    ax.set_ylabel(labels["ylabel"])
    ax.set_xticks(x)
    ax.set_xticklabels(class_names)
    ax.yaxis.grid(True, zorder=0)
    ax.set_axisbelow(True)
    ax.set_ylim(0, 110)
    ax.legend(frameon=False, loc="upper right")

    for bar in list(bars_c) + list(bars_r):
        h = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            h + 1.5,
            f"{h:.1f}%",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="medium",
        )

    fig.suptitle(labels["suptitle"], fontsize=13, fontweight="semibold", y=1.02)
    fig.text(
        0.5,
        -0.03,
        labels["footer"].format(start=START_DATE, end=END_DATE),
        ha="center",
        fontsize=8.5,
        color="#566573",
    )
    fig.tight_layout()
    return fig


def main() -> None:
    returns = load_returns()
    result = portfolio_risk_contributions(
        returns, WEIGHTS, annualization_factor=ANNUALIZATION_FACTOR
    )
    detail = result["detail"]
    class_agg = class_aggregates(detail, ASSET_CLASS)
    # Orden explícito de clases
    class_agg = class_agg.reindex(
        [c for c in ("equity", "fixed_income") if c in class_agg.index]
    )

    export_artifacts(result, class_agg, n_observations=len(returns))

    print("=== Capa 3 — contribución al riesgo ===")
    print(f"σ_p (daily):   {result['sigma_p_daily']:.6f}")
    print(f"σ_p (annual):  {result['sigma_p_annual']:.4%}")
    print(f"Σ RC:          {result['sum_rc']:.6f}")
    print(f"Σ PRC:         {result['sum_prc']:.8f}")
    print(f"Identity OK:   {result['identity_ok']}")
    print("\nInstrument-level:")
    show = detail.copy()
    show["weight_%"] = show["weight"] * 100
    show["prc_%"] = show["prc"] * 100
    print(show[["weight_%", "prc_%"]].round(2).to_string())
    print("\nBy asset class:")
    print(
        (class_agg[["capital_weight", "risk_share"]] * 100)
        .rename(columns={"capital_weight": "capital_%", "risk_share": "risk_%"})
        .round(2)
        .to_string()
    )

    for lang in ("es", "en"):
        fig5 = make_figure_5(detail, result["sum_prc"], lang)
        for p in save_figure(fig5, LABELS_FIG5[lang]["stem"]):
            print(p)
        plt.close(fig5)

        fig6 = make_figure_6(class_agg, lang)
        for p in save_figure(fig6, LABELS_FIG6[lang]["stem"]):
            print(p)
        plt.close(fig6)


if __name__ == "__main__":
    main()
