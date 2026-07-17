"""Figura central — embudo / autopsia diagnóstica progresiva."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from config import END_DATE, START_DATE  # noqa: E402
from plot_style import COLOR_EQUITY, COLOR_FIXED_INCOME, apply_style, save_figure  # noqa: E402

COLOR_RISK = "#922B21"
COLOR_PCA = "#1A5276"

LABELS = {
    "es": {
        "suptitle": "Figura central. Autopsia diagnóstica del portafolio",
        "footer": (
            "Diagnóstico progresivo · Cartera 60/40 estática · "
            "Ventana {start} a {end}"
        ),
        "stem": "fig_central_autopsia_es",
        "rows": [
            ("Activos nominales", "n_nominal", COLOR_FIXED_INCOME),
            ("Posiciones efectivas por capital", "n_eff_weights", COLOR_EQUITY),
            ("Posiciones efectivas por riesgo", "n_eff_risk", COLOR_RISK),
            ("Componentes para ≥80% (PCA)", "n_components_80", COLOR_PCA),
        ],
    },
    "en": {
        "suptitle": "Central figure. Progressive portfolio diagnosis",
        "footer": (
            "Progressive diagnosis · Static 60/40 portfolio · "
            "Sample window {start} to {end}"
        ),
        "stem": "fig_central_autopsy_en",
        "rows": [
            ("Nominal assets", "n_nominal", COLOR_FIXED_INCOME),
            ("Effective positions by capital", "n_eff_weights", COLOR_EQUITY),
            ("Effective positions by risk", "n_eff_risk", COLOR_RISK),
            ("Components for ≥80% (PCA)", "n_components_80", COLOR_PCA),
        ],
    },
}


def load_metrics() -> dict:
    ep = json.loads((ROOT / "data" / "processed" / "effective_positions.json").read_text())
    pca = json.loads((ROOT / "data" / "processed" / "pca_summary.json").read_text())
    return {
        "n_nominal": ep["n_nominal"],
        "n_eff_weights": ep["n_eff_weights"],
        "n_eff_risk": ep["n_eff_risk"],
        "n_components_80": pca["n_components_80"],
        "n_components_90": pca["n_components_90"],
    }


def make_figure(metrics: dict, lang: str) -> plt.Figure:
    labels = LABELS[lang]
    apply_style()
    fig, ax = plt.subplots(figsize=(8.2, 5.4))

    names = [r[0] for r in labels["rows"]]
    values = [float(metrics[r[1]]) for r in labels["rows"]]
    colors = [r[2] for r in labels["rows"]]
    y = list(range(len(names) - 1, -1, -1))  # top = first layer

    # Embudo visual: anchos proporcionales al valor, centrados
    max_v = max(values)
    for yi, val, name, color in zip(y, values, names, colors):
        width = 0.55 + 0.45 * (val / max_v)
        left = 0.5 - width / 2
        ax.barh(
            yi,
            width,
            left=left,
            height=0.62,
            color=color,
            zorder=3,
            edgecolor="white",
            linewidth=0.8,
        )
        ax.text(
            0.5,
            yi,
            f"{name}\n{val:.2f}" if val != int(val) else f"{name}\n{int(val)}",
            ha="center",
            va="center",
            color="white",
            fontsize=10,
            fontweight="medium",
            zorder=4,
        )

    ax.set_xlim(0, 1)
    ax.set_ylim(-0.7, len(names) - 0.3)
    ax.axis("off")

    fig.suptitle(labels["suptitle"], fontsize=13, fontweight="semibold", y=0.98)
    fig.text(
        0.5,
        0.02,
        labels["footer"].format(start=START_DATE, end=END_DATE),
        ha="center",
        fontsize=8.5,
        color="#566573",
    )
    fig.tight_layout(rect=(0, 0.05, 1, 0.95))
    return fig


def export_table(metrics: dict) -> None:
    out = ROOT / "data" / "processed"
    table = pd.DataFrame(
        [
            {"dimension": "Número nominal de activos", "result": metrics["n_nominal"]},
            {
                "dimension": "Effective Positions by Capital",
                "result": metrics["n_eff_weights"],
            },
            {
                "dimension": "Effective Positions by Risk",
                "result": metrics["n_eff_risk"],
            },
            {
                "dimension": "Componentes para explicar 80%",
                "result": metrics["n_components_80"],
            },
            {
                "dimension": "Componentes para explicar 90%",
                "result": metrics["n_components_90"],
            },
        ]
    )
    table.to_csv(out / "autopsy_summary.csv", index=False)
    (out / "autopsy_summary.json").write_text(
        json.dumps(metrics, indent=2), encoding="utf-8"
    )


def main() -> None:
    metrics = load_metrics()
    export_table(metrics)
    print("=== Autopsia del portafolio ===")
    for k, v in metrics.items():
        print(f"{k}: {v}")

    for lang in ("es", "en"):
        fig = make_figure(metrics, lang)
        for p in save_figure(fig, LABELS[lang]["stem"]):
            print(p)
        plt.close(fig)


if __name__ == "__main__":
    main()
