"""Estilo visual compartido para figuras del paper."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
FIGURES_DIR = ROOT / "figures"

# Paleta sobria (evitar púrpuras / look genérico IA)
COLOR_EQUITY = "#1B4F72"
COLOR_FIXED_INCOME = "#5D6D7E"
COLOR_EQUITY_LIGHT = "#5DADE2"
COLOR_FIXED_INCOME_LIGHT = "#AEB6BF"
COLOR_TEXT = "#1C2833"
COLOR_GRID = "#D5D8DC"
COLOR_BG = "#FFFFFF"

ASSET_CLASS_COLORS = {
    "equity": COLOR_EQUITY,
    "fixed_income": COLOR_FIXED_INCOME,
}


def apply_style() -> None:
    plt.rcParams.update(
        {
            "figure.facecolor": COLOR_BG,
            "axes.facecolor": COLOR_BG,
            "axes.edgecolor": COLOR_TEXT,
            "axes.labelcolor": COLOR_TEXT,
            "axes.titlecolor": COLOR_TEXT,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "xtick.color": COLOR_TEXT,
            "ytick.color": COLOR_TEXT,
            "text.color": COLOR_TEXT,
            "grid.color": COLOR_GRID,
            "grid.linewidth": 0.6,
            "font.family": "sans-serif",
            "font.size": 11,
            "axes.titlesize": 13,
            "axes.labelsize": 11,
            "figure.dpi": 150,
            "savefig.dpi": 300,
            "savefig.bbox": "tight",
            "savefig.facecolor": COLOR_BG,
        }
    )


def save_figure(fig: plt.Figure, stem: str) -> list[Path]:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    paths = []
    for ext in ("png", "pdf"):
        path = FIGURES_DIR / f"{stem}.{ext}"
        fig.savefig(path)
        paths.append(path)
    return paths
