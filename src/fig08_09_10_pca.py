"""Figuras 8–10 — PCA diagnóstico (scree, acumulada, loadings)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from config import END_DATE, START_DATE, TICKERS  # noqa: E402
from metrics_pca import loadings_subset, pca_from_correlation  # noqa: E402
from plot_style import COLOR_EQUITY, COLOR_FIXED_INCOME, apply_style, save_figure  # noqa: E402

LABELS = {
    "es": {
        "scree_title": "Figura 8. Análisis de componentes principales — gráfico de sedimentación",
        "scree_ylabel": "Proporción de varianza explicada",
        "scree_xlabel": "Componente principal",
        "cum_title": "Figura 9. Varianza explicada acumulada",
        "cum_ylabel": "Varianza explicada acumulada",
        "cum_xlabel": "Número de componentes",
        "load_title": "Figura 10. Cargas factoriales escaladas de los componentes principales",
        "cbar": r"$v_{ik}\sqrt{\lambda_k}$",
        "footer": (
            "Análisis de componentes principales sobre matriz de correlación · Retornos log diarios · "
            "Ventana {start} a {end} · Diagnóstico (no optimización)"
        ),
        "footer10": (
            "Cargas factoriales escaladas $v_{{ik}}\\sqrt{{\\lambda_k}}$ "
            "(= corr. entre variables estandarizadas y scores PC) · "
            "Ventana {start} a {end} · PC1–PC{n}"
        ),
        "stem8": "fig08_pca_scree_es",
        "stem9": "fig09_pca_cumulative_es",
        "stem10": "fig10_pca_loadings_es",
        "line80": "80%",
        "line90": "90%",
    },
    "en": {
        "scree_title": "Figure 8. PCA — Scree Plot",
        "scree_ylabel": "Explained variance ratio",
        "scree_xlabel": "Principal component",
        "cum_title": "Figure 9. Cumulative Explained Variance",
        "cum_ylabel": "Cumulative explained variance",
        "cum_xlabel": "Number of components",
        "load_title": "Figure 10. Scaled Principal Component Loadings",
        "cbar": r"$v_{ik}\sqrt{\lambda_k}$",
        "footer": (
            "PCA on correlation matrix · Daily log returns · "
            "Sample window {start} to {end} · Diagnostic (not optimization)"
        ),
        "footer10": (
            "Scaled loadings $v_{{ik}}\\sqrt{{\\lambda_k}}$ "
            "(= corr. between standardized variables and PC scores) · "
            "Sample window {start} to {end} · PC1–PC{n}"
        ),
        "stem8": "fig08_pca_scree_en",
        "stem9": "fig09_pca_cumulative_en",
        "stem10": "fig10_pca_loadings_en",
        "line80": "80%",
        "line90": "90%",
    },
}


def load_returns() -> pd.DataFrame:
    path = ROOT / "data" / "processed" / "log_returns.csv"
    rets = pd.read_csv(path, index_col=0, parse_dates=True)
    return rets.reindex(columns=TICKERS)


def export_artifacts(pca: dict) -> None:
    out = ROOT / "data" / "processed"
    out.mkdir(parents=True, exist_ok=True)

    summary = pd.DataFrame(
        {
            "eigenvalue": pca["eigenvalues"],
            "explained_variance_ratio": pca["explained_variance_ratio"],
            "cumulative_explained_variance": pca["cumulative_explained_variance"],
        }
    )
    summary.to_csv(out / "pca_explained_variance.csv")
    pca["eigenvectors"].to_csv(out / "pca_eigenvectors.csv")
    pca["scaled_loadings"].to_csv(out / "pca_scaled_loadings.csv")
    # Representación usada en Figura 10
    pca["scaled_loadings"].to_csv(out / "pca_loadings.csv")

    meta = {
        "n_assets": pca["n_assets"],
        "n_components_80": pca["n_components_80"],
        "n_components_90": pca["n_components_90"],
        "pc1_explained": float(pca["explained_variance_ratio"].iloc[0]),
        "pc2_explained": float(pca["explained_variance_ratio"].iloc[1]),
        "cum_2": float(pca["cumulative_explained_variance"].iloc[1]),
        "cum_3": float(pca["cumulative_explained_variance"].iloc[2]),
        "sample_start": START_DATE,
        "sample_end": END_DATE,
        "method": "eigendecomposition of Pearson correlation matrix",
        "figure10_shows": "scaled_loadings_v_ik_sqrt_lambda_k",
        "figure10_interpretation": (
            "correlation between standardized variables and principal component scores"
        ),
    }
    (out / "pca_summary.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    pd.DataFrame([{"metric": k, "value": v} for k, v in meta.items()]).to_csv(
        out / "pca_summary.csv", index=False
    )


def make_scree(pca: dict, lang: str) -> plt.Figure:
    labels = LABELS[lang]
    apply_style()
    ev = pca["explained_variance_ratio"]
    x = np.arange(1, len(ev) + 1)

    fig, ax = plt.subplots(figsize=(8.0, 4.8))
    ax.bar(x, ev.values, color=COLOR_EQUITY, width=0.7, zorder=3)
    ax.plot(x, ev.values, color=COLOR_FIXED_INCOME, marker="o", lw=1.5, zorder=4)
    ax.set_xlabel(labels["scree_xlabel"])
    ax.set_ylabel(labels["scree_ylabel"])
    ax.set_xticks(x)
    ax.set_xticklabels([f"PC{i}" for i in x])
    ax.set_ylim(0, max(ev.values) * 1.18)
    ax.yaxis.grid(True, zorder=0)
    ax.set_axisbelow(True)
    for i, v in enumerate(ev.values):
        ax.text(x[i], v + 0.01, f"{v*100:.1f}%", ha="center", va="bottom", fontsize=8.5)

    fig.suptitle(labels["scree_title"], fontsize=13, fontweight="semibold", y=1.02)
    fig.text(
        0.5, -0.03,
        labels["footer"].format(start=START_DATE, end=END_DATE),
        ha="center", fontsize=8.5, color="#566573",
    )
    fig.tight_layout()
    return fig


def make_cumulative(pca: dict, lang: str) -> plt.Figure:
    labels = LABELS[lang]
    apply_style()
    cum = pca["cumulative_explained_variance"]
    x = np.arange(1, len(cum) + 1)

    fig, ax = plt.subplots(figsize=(8.0, 4.8))
    ax.plot(
        x, cum.values, color=COLOR_EQUITY, marker="o", lw=2.0, markersize=7, zorder=3
    )
    ax.axhline(0.80, color="#922B21", ls="--", lw=1.2, label=labels["line80"])
    ax.axhline(0.90, color=COLOR_FIXED_INCOME, ls="--", lw=1.2, label=labels["line90"])
    ax.set_xlabel(labels["cum_xlabel"])
    ax.set_ylabel(labels["cum_ylabel"])
    ax.set_xticks(x)
    ax.set_ylim(0, 1.05)
    ax.yaxis.grid(True, zorder=0)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, loc="lower right")

    # Marcar n80 y n90
    n80 = pca["n_components_80"]
    n90 = pca["n_components_90"]
    ax.scatter([n80], [cum.iloc[n80 - 1]], color="#922B21", s=60, zorder=4)
    ax.scatter([n90], [cum.iloc[n90 - 1]], color=COLOR_FIXED_INCOME, s=60, zorder=4)
    ax.annotate(
        f"n={n80}",
        (n80, cum.iloc[n80 - 1]),
        textcoords="offset points",
        xytext=(8, -12),
        fontsize=9,
        color="#922B21",
    )
    ax.annotate(
        f"n={n90}",
        (n90, cum.iloc[n90 - 1]),
        textcoords="offset points",
        xytext=(8, 8),
        fontsize=9,
        color=COLOR_FIXED_INCOME,
    )

    fig.suptitle(labels["cum_title"], fontsize=13, fontweight="semibold", y=1.02)
    fig.text(
        0.5, -0.03,
        labels["footer"].format(start=START_DATE, end=END_DATE),
        ha="center", fontsize=8.5, color="#566573",
    )
    fig.tight_layout()
    return fig


def make_loadings(pca: dict, lang: str, n_show: int = 5) -> plt.Figure:
    labels = LABELS[lang]
    apply_style()
    # Figura 10: loadings escalados v_ik * sqrt(λ_k)
    load = loadings_subset(pca["scaled_loadings"], n_show)

    fig, ax = plt.subplots(figsize=(8.6, 6.2))
    sns.heatmap(
        load,
        ax=ax,
        cmap="RdBu_r",
        center=0.0,
        vmin=-1.0,
        vmax=1.0,
        annot=True,
        fmt=".2f",
        annot_kws={"size": 9},
        linewidths=0.5,
        linecolor="#EAECEE",
        cbar_kws={"label": labels["cbar"], "shrink": 0.82},
    )
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.tick_params(axis="both", labelsize=10)

    fig.suptitle(labels["load_title"], fontsize=13, fontweight="semibold", y=0.98)
    fig.text(
        0.5,
        0.01,
        labels["footer10"].format(start=START_DATE, end=END_DATE, n=n_show),
        ha="center",
        fontsize=8.5,
        color="#566573",
    )
    fig.tight_layout(rect=(0, 0.04, 1, 0.96))
    return fig


def main() -> None:
    returns = load_returns()
    pca = pca_from_correlation(returns)
    export_artifacts(pca)

    print("=== Capa 5 — PCA (diagnóstico) ===")
    print(pca["explained_variance_ratio"].map(lambda x: f"{x:.2%}").to_string())
    print("\nCumulative:")
    print(pca["cumulative_explained_variance"].map(lambda x: f"{x:.2%}").to_string())
    print(f"\nComponents for ≥80%: {pca['n_components_80']}")
    print(f"Components for ≥90%: {pca['n_components_90']}")
    print("\nScaled loadings v√λ (PC1–PC5) — Figura 10:")
    print(loadings_subset(pca["scaled_loadings"], 5).round(3).to_string())

    # Regenerar Figuras 8–10
    for lang in ("es", "en"):
        labels = LABELS[lang]
        for maker, stem in (
            (make_scree, labels["stem8"]),
            (make_cumulative, labels["stem9"]),
            (make_loadings, labels["stem10"]),
        ):
            fig = maker(pca, lang)
            for p in save_figure(fig, stem):
                print(p)
            plt.close(fig)


if __name__ == "__main__":
    main()
