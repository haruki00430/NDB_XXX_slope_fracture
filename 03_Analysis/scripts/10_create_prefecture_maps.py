# -*- coding: utf-8 -*-
"""
10_create_prefecture_maps.py
----------------------------
都道府県別日本地図を作成するスクリプト。

Main manuscript figure (Figure 2, three panels):
  (A) Terrain slope | (B) Hip fracture surgery rate  [top row, side by side]
  (C) Bivariate choropleth (slope × surgery rate)   [bottom row, full width]

Also writes legacy single-panel PNGs (fig_map_slope.png, etc.) for debugging.

実行方法（NDB_XXX_slope_fracture ルートまたは 03_Analysis/scripts から）:
    python 10_create_prefecture_maps.py
"""

import os
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from mpl_toolkits.axes_grid1 import make_axes_locatable
import warnings

warnings.filterwarnings("ignore")

try:
    import japanize_matplotlib
except ImportError:
    import matplotlib.font_manager as fm

    fonts = [f.name for f in fm.fontManager.ttflist if "Gothic" in f.name or "Meiryo" in f.name]
    if fonts:
        matplotlib.rcParams["font.family"] = fonts[0]

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))

DATA_CSV = os.path.join(PROJECT_DIR, "03_Analysis", "data", "processed", "analysis_dataset_v1.csv")
GEOJSON = os.path.join(
    os.path.abspath(os.path.join(PROJECT_DIR, "..", "..")),
    "02_Data", "raw", "GIS", "japan.geojson",
)
OUT_DIR = os.path.join(PROJECT_DIR, "03_Analysis", "results", "figures")
os.makedirs(OUT_DIR, exist_ok=True)

# Health & Place: 300 dpi; legible panel labels and color-bar text
FONT_PANEL = 13
FONT_TITLE = 12
FONT_LABEL = 11
FONT_TICK = 10
FONT_LEGEND = 9
EDGE_COLOR = "white"
LINE_WIDTH = 0.5
DPI = 300

BVPAL = np.array([
    ["#e8e8e8", "#b0d5df", "#64acbe"],
    ["#e4d9ac", "#ad9ea5", "#627f8c"],
    ["#c85a5a", "#985356", "#574249"],
])


def style_ax(ax):
    ax.set_axis_off()
    ax.set_aspect("equal")


def add_panel_label(ax, label):
    ax.text(
        0.02, 0.98, label,
        transform=ax.transAxes,
        ha="left", va="top",
        fontsize=FONT_PANEL, fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="none", alpha=0.85),
    )


def add_scalebar(ax, length_km=200, x_frac=0.05, y_frac=0.04, lw=2.5):
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    x0 = xlim[0] + (xlim[1] - xlim[0]) * x_frac
    y0 = ylim[0] + (ylim[1] - ylim[0]) * y_frac
    x1 = x0 + length_km * 1000
    ax.plot([x0, x1], [y0, y0], "k-", lw=lw, solid_capstyle="butt")
    ax.text(
        (x0 + x1) / 2, y0 + (ylim[1] - ylim[0]) * 0.012,
        f"{length_km} km", ha="center", va="bottom", fontsize=FONT_TICK,
    )


def quantile3(series):
    q33 = series.quantile(1 / 3)
    q67 = series.quantile(2 / 3)
    return pd.cut(series, bins=[-np.inf, q33, q67, np.inf], labels=[0, 1, 2]).astype(int)


def assign_bivariate_classes(gdf):
    out = gdf.copy()
    out["slope_class"] = quantile3(out["habitable_slope_weighted"])
    out["fracture_class"] = quantile3(out["femur_rate"])
    out["bv_color"] = out.apply(
        lambda r: BVPAL[int(r["fracture_class"]), int(r["slope_class"])],
        axis=1,
    )
    return out


def plot_slope_choropleth(ax, gdf, *, legend=True, scalebar=False, panel_label=None):
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="4%", pad=0.06)
    gdf.plot(
        column="habitable_slope_weighted",
        ax=ax,
        cmap="YlOrRd",
        edgecolor=EDGE_COLOR,
        linewidth=LINE_WIDTH,
        legend=legend,
        cax=cax,
        legend_kwds={"label": "Slope (degrees)", "orientation": "vertical", "shrink": 0.85},
        missing_kwds={"color": "#cccccc"},
    )
    style_ax(ax)
    if scalebar:
        add_scalebar(ax)
    if panel_label:
        add_panel_label(ax, panel_label)
    cax.tick_params(labelsize=FONT_TICK)
    cax.yaxis.label.set_size(FONT_LABEL)


def plot_fracture_choropleth(ax, gdf, *, legend=True, scalebar=False, panel_label=None):
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="4%", pad=0.06)
    gdf.plot(
        column="femur_rate",
        ax=ax,
        cmap="Blues",
        edgecolor=EDGE_COLOR,
        linewidth=LINE_WIDTH,
        legend=legend,
        cax=cax,
        legend_kwds={
            "label": "Hip fracture surgery rate\n(per 100,000 population)",
            "orientation": "vertical",
            "shrink": 0.85,
        },
        missing_kwds={"color": "#cccccc"},
    )
    style_ax(ax)
    if scalebar:
        add_scalebar(ax)
    if panel_label:
        add_panel_label(ax, panel_label)
    cax.tick_params(labelsize=FONT_TICK)
    cax.yaxis.label.set_size(FONT_LABEL)


def plot_bivariate_choropleth(ax, gdf, fig, *, scalebar=True, panel_label=None, legend_rect=(0.78, 0.10, 0.16, 0.16)):
    for _, row in gdf.iterrows():
        gpd.GeoSeries([row.geometry]).plot(
            ax=ax,
            color=row["bv_color"],
            edgecolor=EDGE_COLOR,
            linewidth=LINE_WIDTH,
        )
    style_ax(ax)
    if scalebar:
        add_scalebar(ax)
    if panel_label:
        add_panel_label(ax, panel_label)

    inset = fig.add_axes(legend_rect)
    inset.set_aspect("equal")
    for fi in range(3):
        for si in range(3):
            inset.add_patch(mpatches.Rectangle(
                (si, fi), 1, 1,
                color=BVPAL[fi, si],
                ec="white", lw=0.5,
            ))
    inset.set_xlim(0, 3)
    inset.set_ylim(0, 3)
    inset.set_xticks([0, 1.5, 3])
    inset.set_yticks([0, 1.5, 3])
    inset.set_xticklabels(["Low", "", "High"], fontsize=FONT_LEGEND)
    inset.set_yticklabels(["Low", "", "High"], fontsize=FONT_LEGEND)
    inset.set_xlabel("Slope →", fontsize=FONT_LEGEND, labelpad=1)
    inset.set_ylabel("Fracture →", fontsize=FONT_LEGEND, labelpad=1)
    inset.set_title("Legend", fontsize=FONT_LEGEND + 1, pad=3)
    inset.tick_params(length=0)


def main():
    df = pd.read_csv(DATA_CSV, encoding="utf-8")
    df["pref_code"] = range(1, len(df) + 1)

    gdf = gpd.read_file(GEOJSON)
    gdf = gdf.rename(columns={"id": "pref_code"})
    merged = gdf.merge(df, on="pref_code", how="left").to_crs(epsg=6677)
    merged_bv = assign_bivariate_classes(merged)

    print(f"Merged shape: {merged.shape}")
    print(f"Slope range: {df['habitable_slope_weighted'].min():.2f} - {df['habitable_slope_weighted'].max():.2f} degrees")
    print(f"Femur rate range: {df['femur_rate'].min():.1f} - {df['femur_rate'].max():.1f} per 100,000")

    # --- Legacy single-panel outputs (optional reference) ---
    print("\n[Legacy] Single-panel slope map ...")
    fig, ax = plt.subplots(figsize=(8, 9))
    plot_slope_choropleth(ax, merged, scalebar=True)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_map_slope.png"), dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    print("[Legacy] Single-panel fracture map ...")
    fig, ax = plt.subplots(figsize=(8, 9))
    plot_fracture_choropleth(ax, merged, scalebar=True)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_map_fracture.png"), dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    print("[Legacy] Single-panel bivariate map ...")
    fig, ax = plt.subplots(figsize=(8, 9))
    plot_bivariate_choropleth(ax, merged_bv, fig, legend_rect=(0.72, 0.08, 0.18, 0.18))
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_map_bivariate.png"), dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    # --- Main manuscript Figure 2: composite layout ---
    print("[Figure 2 composite] Top: slope | fracture; bottom: bivariate ...")
    fig = plt.figure(figsize=(14, 15))
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.2], hspace=0.06, wspace=0.08)
    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[0, 1])
    ax_c = fig.add_subplot(gs[1, :])

    plot_slope_choropleth(ax_a, merged, scalebar=False, panel_label="(A)")
    plot_fracture_choropleth(ax_b, merged, scalebar=False, panel_label="(B)")
    plot_bivariate_choropleth(ax_c, merged_bv, fig, scalebar=True, panel_label="(C)", legend_rect=(0.84, 0.12, 0.12, 0.14))

    composite_path = os.path.join(OUT_DIR, "fig_map_geography_composite.png")
    fig.savefig(composite_path, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  Saved: {composite_path}")

    print("\n=== All maps created successfully ===")
    print(f"Output directory: {OUT_DIR}")


if __name__ == "__main__":
    main()
