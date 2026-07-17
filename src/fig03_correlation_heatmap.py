"""Figura 3 — Matriz de correlaciones de los retornos (heatmap completo).

Muestra la dependencia lineal entre todos los pares, con valores anotados.
Orden de activos: orden metodológico del portafolio (sin clustering).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from config import (  # noqa: E402
    ASSET_CLASS,
    CORR_NETWORK_THRESHOLD,
    END_DATE,
    EQUITY_TICKERS,
    FIXED_INCOME_TICKERS,
    START_DATE,
    TICKERS,
)
from metrics_correlation import (  # noqa: E402
    correlation_edges,
    correlation_summary,
    top_bottom_pairs,
)
from plot_style import apply_style, save_figure  # noqa: E402

LABELS = {
    "es": {
        "suptitle": "Figura 3. Matriz de correlaciones de los retornos",
        "cbar": "Correlación de Pearson",
        "footer": (
            "Retornos log diarios · Ventana {start} a {end} · "
            "N = {n} instrumentos · {obs} observaciones · Orden del portafolio"
        ),
        "stem": "fig03_correlation_heatmap_es",
    },
    "en": {
        "suptitle": "Figure 3. Correlation Matrix of Returns",
        "cbar": "Pearson correlation",
        "footer": (
            "Daily log returns · Sample window {start} to {end} · "
            "N = {n} instruments · {obs} observations · Portfolio order"
        ),
        "stem": "fig03_correlation_heatmap_en",
    },
}


def load_returns() -> pd.DataFrame:
    path = ROOT / "data" / "processed" / "log_returns.csv"
    rets = pd.read_csv(path, index_col=0, parse_dates=True)
    # Orden fijo del portafolio: sin reordenamiento ni clustering
    return rets.reindex(columns=TICKERS)


def export_dependence_artifacts(corr: pd.DataFrame, returns: pd.DataFrame) -> dict:
    out = ROOT / "data" / "processed"
    out.mkdir(parents=True, exist_ok=True)

    # Garantizar orden metodológico
    corr = corr.reindex(index=TICKERS, columns=TICKERS)
    corr.to_csv(out / "correlation_matrix.csv")

    summary = correlation_summary(
        corr,
        EQUITY_TICKERS,
        FIXED_INCOME_TICKERS,
        CORR_NETWORK_THRESHOLD,
    )
    summary["n_observations"] = int(len(returns))
    summary["sample_start"] = str(returns.index.min().date())
    summary["sample_end"] = str(returns.index.max().date())

    (out / "correlation_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    pd.DataFrame(
        [{"metric": k, "value": v} for k, v in summary.items()]
    ).to_csv(out / "correlation_summary.csv", index=False)

    edges = correlation_edges(corr, CORR_NETWORK_THRESHOLD)
    edges.to_csv(out / "correlation_edges.csv", index=False)

    highest, lowest = top_bottom_pairs(corr, n=5)
    highest.to_csv(out / "correlation_top5_highest.csv", index=False)
    lowest.to_csv(out / "correlation_top5_lowest.csv", index=False)

    class_map = pd.Series({t: ASSET_CLASS[t] for t in TICKERS}, name="asset_class")
    class_map.to_csv(out / "asset_classes.csv", header=True)

    return summary, highest, lowest


def make_figure(corr: pd.DataFrame, n_obs: int, lang: str) -> plt.Figure:
    labels = LABELS[lang]
    apply_style()
    corr = corr.reindex(index=TICKERS, columns=TICKERS)

    fig, ax = plt.subplots(figsize=(8.8, 7.4))
    sns.heatmap(
        corr,
        ax=ax,
        cmap="RdBu_r",
        center=0.0,
        vmin=-1.0,
        vmax=1.0,
        square=True,
        linewidths=0.5,
        linecolor="#EAECEE",
        cbar_kws={"label": labels["cbar"], "shrink": 0.82},
        annot=True,
        fmt=".2f",
        annot_kws={"size": 8.5},
    )
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.tick_params(axis="both", labelsize=10)
    ax.set_xticklabels(TICKERS, rotation=0)
    ax.set_yticklabels(TICKERS, rotation=0)

    fig.suptitle(labels["suptitle"], fontsize=13, fontweight="semibold", y=0.98)
    fig.text(
        0.5,
        0.01,
        labels["footer"].format(
            start=START_DATE,
            end=END_DATE,
            n=len(corr),
            obs=n_obs,
        ),
        ha="center",
        fontsize=8.5,
        color="#566573",
    )
    fig.tight_layout(rect=(0, 0.03, 1, 0.96))
    return fig


def main() -> None:
    returns = load_returns()
    corr = returns.corr()
    summary, highest, lowest = export_dependence_artifacts(corr, returns)

    print("=== Capa 2 — métricas de correlación ===")
    print(f"mean_correlation:              {summary['mean_correlation']:.4f}")
    print(f"mean_correlation_equity:       {summary['mean_correlation_equity']:.4f}")
    print(f"mean_correlation_fixed_income: {summary['mean_correlation_fixed_income']:.4f}")
    print(f"mean_correlation_cross:        {summary['mean_correlation_cross']:.4f}")
    print(f"n_observations:                {summary['n_observations']}")
    print(f"n_edges_|rho|>=0.60:           {summary['n_edges_above_threshold']}")
    print("\nTop 5 highest pairwise correlations:")
    print(highest.to_string(index=False))
    print("\nTop 5 lowest pairwise correlations:")
    print(lowest.to_string(index=False))

    for lang in ("es", "en"):
        fig = make_figure(corr, len(returns), lang)
        paths = save_figure(fig, LABELS[lang]["stem"])
        plt.close(fig)
        for p in paths:
            print(p)


if __name__ == "__main__":
    main()
