"""Figura 4 — Red de correlaciones (|ρ| ≥ threshold).

Sintetiza visualmente las conexiones más intensas.
No modifica el umbral; no fuerza enlaces; nodos aislados permanecen aislados.
El layout solo compacta la composición visual.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from config import (  # noqa: E402
    ASSET_CLASS,
    CORR_NETWORK_THRESHOLD,
    END_DATE,
    START_DATE,
    TICKERS,
)
from plot_style import (  # noqa: E402
    ASSET_CLASS_COLORS,
    apply_style,
    save_figure,
)

LABELS = {
    "es": {
        "suptitle": "Figura 4. Red de correlaciones",
        "legend_eq": "Renta variable",
        "legend_fi": "Renta fija",
        "legend_edge": f"|ρ| ≥ {CORR_NETWORK_THRESHOLD:.2f}",
        "footer": (
            "Nodos = instrumentos · Grosor del enlace ∝ |correlación| · "
            "Umbral |ρ| ≥ {thr:.2f} · Ventana {start} a {end}"
        ),
        "stem": "fig04_correlation_network_es",
    },
    "en": {
        "suptitle": "Figure 4. Correlation Network",
        "legend_eq": "Equity",
        "legend_fi": "Fixed Income",
        "legend_edge": f"|ρ| ≥ {CORR_NETWORK_THRESHOLD:.2f}",
        "footer": (
            "Nodes = instruments · Edge width ∝ |correlation| · "
            "Threshold |ρ| ≥ {thr:.2f} · Sample window {start} to {end}"
        ),
        "stem": "fig04_correlation_network_en",
    },
}


def load_corr() -> pd.DataFrame:
    path = ROOT / "data" / "processed" / "correlation_matrix.csv"
    if not path.exists():
        raise FileNotFoundError(
            "Missing correlation_matrix.csv; run fig03_correlation_heatmap.py first."
        )
    corr = pd.read_csv(path, index_col=0)
    return corr.reindex(index=TICKERS, columns=TICKERS)


def build_graph(corr: pd.DataFrame) -> nx.Graph:
    g = nx.Graph()
    for t in TICKERS:
        g.add_node(t, asset_class=ASSET_CLASS[t])

    for i, a in enumerate(TICKERS):
        for b in TICKERS[i + 1 :]:
            rho = float(corr.loc[a, b])
            if abs(rho) >= CORR_NETWORK_THRESHOLD:
                g.add_edge(a, b, weight=abs(rho), correlation=rho)
    return g


def _layout_component(sub: nx.Graph, nodes: list[str]) -> dict[str, np.ndarray]:
    if len(nodes) == 1:
        return {nodes[0]: np.array([0.0, 0.0])}
    if len(nodes) == 2:
        return {
            nodes[0]: np.array([-0.28, 0.0]),
            nodes[1]: np.array([0.28, 0.0]),
        }
    if len(nodes) == 3:
        # Triángulo más chico (p. ej. renta fija)
        return {
            nodes[0]: np.array([0.0, 0.26]),
            nodes[1]: np.array([-0.26, -0.18]),
            nodes[2]: np.array([0.26, -0.18]),
        }

    local = nx.spring_layout(
        sub,
        seed=42,
        k=0.48 / np.sqrt(len(nodes)),
        iterations=400,
        weight="weight",
    )
    coords = np.array([local[n] for n in nodes])
    coords = coords - coords.mean(axis=0)
    span = np.ptp(coords, axis=0)
    span[span == 0] = 1.0
    coords = coords / span.max() * 0.95
    return {n: coords[i] for i, n in enumerate(nodes)}


def compact_layout(g: nx.Graph) -> dict[str, np.ndarray]:
    """Layout compacto por componentes conexas (sin alterar nodos/enlaces)."""
    components = [sorted(c) for c in nx.connected_components(g)]
    components = sorted(components, key=lambda c: (-len(c), c[0]))

    locals_map: dict[tuple[str, ...], dict[str, np.ndarray]] = {}
    for comp in components:
        sub = g.subgraph(comp).copy()
        locals_map[tuple(comp)] = _layout_component(sub, comp)

    large = [c for c in components if len(c) >= 3]
    isolates = [c for c in components if len(c) == 1]
    other = [c for c in components if 1 < len(c) < 3]

    pos: dict[str, np.ndarray] = {}

    # Centros de anclaje muy próximos (solo visualización)
    if len(large) >= 1:
        c0 = large[0]
        for n, xy in locals_map[tuple(c0)].items():
            pos[n] = xy + np.array([-0.35, 0.25])
    if len(large) >= 2:
        c1 = large[1]
        for n, xy in locals_map[tuple(c1)].items():
            pos[n] = xy + np.array([0.70, 0.25])

    for i, c in enumerate(other):
        for n, xy in locals_map[tuple(c)].items():
            pos[n] = xy + np.array([0.15 + 0.45 * i, -0.70])

    for i, c in enumerate(isolates):
        n = c[0]
        pos[n] = np.array([0.15 + 0.30 * i, -0.75])

    all_xy = np.vstack(list(pos.values()))
    center = all_xy.mean(axis=0)
    return {n: v - center for n, v in pos.items()}


def make_figure(corr: pd.DataFrame, lang: str) -> plt.Figure:
    labels = LABELS[lang]
    apply_style()
    g = build_graph(corr)
    pos = compact_layout(g)

    fig, ax = plt.subplots(figsize=(7.0, 5.0))

    node_colors = [ASSET_CLASS_COLORS[ASSET_CLASS[n]] for n in g.nodes()]
    nx.draw_networkx_nodes(
        g,
        pos,
        ax=ax,
        node_color=node_colors,
        node_size=1100,
        linewidths=0.8,
        edgecolors="#FBFCFC",
    )
    nx.draw_networkx_labels(
        g,
        pos,
        ax=ax,
        font_size=9,
        font_color="white",
        font_weight="bold",
    )

    widths = [2.0 + 5.5 * g[u][v]["weight"] for u, v in g.edges()]
    edge_colors = [
        "#1B4F72" if g[u][v]["correlation"] >= 0 else "#922B21"
        for u, v in g.edges()
    ]
    nx.draw_networkx_edges(
        g,
        pos,
        ax=ax,
        width=widths,
        edge_color=edge_colors,
        alpha=0.55,
    )

    legend_handles = [
        Patch(facecolor=ASSET_CLASS_COLORS["equity"], label=labels["legend_eq"]),
        Patch(
            facecolor=ASSET_CLASS_COLORS["fixed_income"],
            label=labels["legend_fi"],
        ),
        Line2D(
            [0],
            [0],
            color="#1B4F72",
            lw=3.0,
            alpha=0.7,
            label=labels["legend_edge"],
        ),
    ]
    ax.legend(
        handles=legend_handles,
        loc="upper left",
        frameon=False,
        fontsize=9,
        bbox_to_anchor=(0.0, 1.02),
    )
    ax.set_axis_off()

    xs = [p[0] for p in pos.values()]
    ys = [p[1] for p in pos.values()]
    pad_x = 0.18
    pad_y = 0.18
    ax.set_xlim(min(xs) - pad_x, max(xs) + pad_x)
    ax.set_ylim(min(ys) - pad_y, max(ys) + pad_y)
    # No forzar equal aspect: evita bandas vacías laterales
    ax.margins(0.02)

    fig.suptitle(labels["suptitle"], fontsize=13, fontweight="semibold", y=0.98)
    fig.text(
        0.5,
        0.015,
        labels["footer"].format(
            thr=CORR_NETWORK_THRESHOLD,
            start=START_DATE,
            end=END_DATE,
        ),
        ha="center",
        fontsize=8.5,
        color="#566573",
    )
    fig.tight_layout(rect=(0, 0.04, 1, 0.95))
    return fig


def main() -> None:
    corr = load_corr()
    g = build_graph(corr)
    print("=== Figura 4 — correlation network ===")
    print(f"Threshold: {CORR_NETWORK_THRESHOLD}")
    print(f"Nodes: {g.number_of_nodes()}")
    print(f"Edges: {g.number_of_edges()}")
    isolates = sorted(nx.isolates(g))
    print(f"Isolates (|ρ| < threshold with all): {isolates}")

    for lang in ("es", "en"):
        fig = make_figure(corr, lang)
        paths = save_figure(fig, LABELS[lang]["stem"])
        plt.close(fig)
        for p in paths:
            print(p)


if __name__ == "__main__":
    main()
