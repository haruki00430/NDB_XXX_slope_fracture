# -*- coding: utf-8 -*-
"""
10_create_prefecture_maps.py
----------------------------
都道府県別日本地図を作成するスクリプト。

Main manuscript figure (Figure 2, three panels):
  (A) Terrain slope | (B) Hip fracture surgery rate  [top row, side by side]
  (C) Bivariate choropleth (slope × surgery rate)   [bottom row, full width]

Okinawa is drawn in a separate inset (upper-left of each map axes) so the mainland
fills the frame; otherwise the Kyūshū–Okinawa extent wastes canvas and shrinks
readable detail.

Display geometry (not analytic data):
  - Mainland: drop tiny / far-south parts (e.g. Ogasawara) so Honshu–Hokkaido fill the panel.
  - Okinawa inset: largest island only (沖縄本島), independent zoom.

Also writes legacy single-panel PNGs (fig_map_slope.png, etc.) for debugging.

実行方法（NDB_XXX_slope_fracture ルートまたは 03_Analysis/scripts から）:
    python 10_create_prefecture_maps.py
"""

import os
from typing import cast

import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap, Normalize, to_hex
from matplotlib import cm as mpl_cm
from mpl_toolkits.axes_grid1 import make_axes_locatable
from shapely.geometry import MultiPolygon
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

# Health & Place: 300 dpi; fonts sized for Word/PDF insertion without microscope zoom
FONT_PANEL = 20
FONT_LABEL = 15
FONT_TICK = 13
FONT_LEGEND = 13
EDGE_COLOR = "#fefefe"
INSET_EDGE_COLOR = "#555555"
LINE_WIDTH = 0.65
# Display-only filters (EPSG:6677); analytic prefecture values unchanged
MAINLAND_PART_MIN_AREA = 15e6  # 15 km² — omit tiny islets from map drawing
MAINLAND_PART_MIN_CENTROID_Y = -650_000  # excludes Ogasawara / far-south outliers
OKINAWA_INSET_PAD_FRAC = 0.06  # tight zoom on Okinawa main island only
DPI = 300

# Vivid sequential ramps (ColorBrewer-style; slope = warm, rate = cool; print-safe)
SLOPE_CMAP = LinearSegmentedColormap.from_list(
    "slope_vivid",
    ["#ffffcc", "#ffeda0", "#feb24c", "#fc4e2a", "#e31a1c", "#b10026"],
    N=256,
)
FRACTURE_CMAP = LinearSegmentedColormap.from_list(
    "fracture_vivid",
    ["#f7fbff", "#c6dbef", "#6baed6", "#2171b5", "#084594"],
    N=256,
)

# 3×3 bivariate: rows = fracture tertile (low→high), cols = slope tertile (low→high); higher chroma than prior palette
BVPAL = np.array([
    ["#e8e8e8", "#74add1", "#2166ac"],
    ["#fee090", "#fc8d59", "#d95f0e"],
    ["#f46d6c", "#d73027", "#67001f"],
])

# JIS prefecture code for Okinawa; must match merge key (CSV rows 1..47 in standard order).
OKINAWA_PREF_CODE = 47
# Inset position (axes fraction: left, bottom, width, height) — upper-left, below panel badge
OKINAWA_INSET_RECT_DEFAULT = (0.022, 0.63, 0.27, 0.30)
# Wider panel (C): narrower inset, same corner
OKINAWA_INSET_RECT_WIDE = (0.014, 0.65, 0.158, 0.26)

# Mainland: tight bounds (large map); small top/left pad only for inset overlay in axes coords
MAINLAND_PAD_TIGHT = 0.012
MAINLAND_LAYOUT_TOP = dict(
    anchor="SE",
    pad_left=0.022,
    pad_right=0.006,
    pad_bottom=0.006,
    pad_top=0.028,
)
MAINLAND_LAYOUT_CENTER = dict(
    anchor="C",
    pad_left=0.022,
    pad_right=0.022,
    pad_bottom=0.012,
    pad_top=0.028,
)


def style_ax(ax):
    ax.set_axis_off()


def add_panel_label(ax, label):
    ax.text(
        0.02, 0.98, label,
        transform=ax.transAxes,
        ha="left", va="top",
        fontsize=FONT_PANEL, fontweight="bold",
        zorder=25,
        bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="none", alpha=0.85),
    )


def _infer_nice_scale_length_km(ax, *, map_fraction: float = 0.20) -> int:
    """Pick a round bar length (km) ~ map_fraction of axes width (projected metres, EPSG:6677)."""
    xlim = ax.get_xlim()
    width_km = (float(xlim[1]) - float(xlim[0])) / 1000.0
    target = width_km * map_fraction
    for step in (50, 75, 100, 125, 150, 200, 250, 300, 400, 500, 600, 750, 800, 1000):
        if step >= target:
            return step
    return max(50, int(round(target / 25.0)) * 25)


def add_scalebar(
    ax,
    length_km: int | None = 200,
    *,
    x_frac=0.05,
    y_frac=0.04,
    lw=2.5,
    fontsize: int | None = None,
    dy_frac=0.012,
):
    """Horizontal scale bar in projected metres (1 unit = 1 m). Pass length_km=None for auto length."""
    if length_km is None:
        length_km = _infer_nice_scale_length_km(ax)
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    x0 = xlim[0] + (xlim[1] - xlim[0]) * x_frac
    y0 = ylim[0] + (ylim[1] - ylim[0]) * y_frac
    x1 = x0 + length_km * 1000
    ax.plot([x0, x1], [y0, y0], "k-", lw=lw, solid_capstyle="butt")
    fs = FONT_TICK if fontsize is None else fontsize
    ax.text(
        (x0 + x1) / 2,
        y0 + (ylim[1] - ylim[0]) * dy_frac,
        f"{length_km} km",
        ha="center",
        va="bottom",
        fontsize=fs,
        fontweight="medium",
    )


def quantile3(series: pd.Series) -> pd.Series:
    q33 = float(series.quantile(1 / 3))
    q67 = float(series.quantile(2 / 3))
    cats = cast(
        pd.Series,
        pd.cut(series, bins=[-np.inf, q33, q67, np.inf], labels=[0, 1, 2]),
    )
    return cats.astype(int)


def assign_bivariate_classes(gdf):
    out = gdf.copy()
    out["slope_class"] = quantile3(out["habitable_slope_weighted"])
    out["fracture_class"] = quantile3(out["femur_rate"])
    out["bv_color"] = out.apply(
        lambda r: BVPAL[int(r["fracture_class"]), int(r["slope_class"])],
        axis=1,
    )
    return out


def _explode_parts(geom) -> list:
    if geom is None or geom.is_empty:
        return []
    if geom.geom_type == "MultiPolygon":
        return list(geom.geoms)
    return [geom]


def _filter_mainland_display_geom(geom):
    """Keep major island parts for drawing; prefecture attribute values stay unchanged."""
    parts = _explode_parts(geom)
    if not parts:
        return geom
    kept = [
        p for p in parts
        if float(p.area) >= MAINLAND_PART_MIN_AREA
        and float(p.centroid.y) >= MAINLAND_PART_MIN_CENTROID_Y
    ]
    if not kept:
        kept = [max(parts, key=lambda p: float(p.area))]
    if len(kept) == 1:
        return kept[0]
    return MultiPolygon(kept)


def _build_mainland_display(main: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    out = main.copy()
    out["geometry"] = [_filter_mainland_display_geom(g) for g in main.geometry]
    return out


def _split_okinawa(gdf: gpd.GeoDataFrame) -> tuple[gpd.GeoDataFrame, gpd.GeoDataFrame]:
    if "prefecture" in gdf.columns:
        oki_mask = gdf["prefecture"].astype(str) == "沖縄県"
    else:
        oki_mask = gdf["pref_code"] == OKINAWA_PREF_CODE
    main = cast(gpd.GeoDataFrame, gdf[~oki_mask].copy())
    oki = cast(gpd.GeoDataFrame, gdf[oki_mask].copy())
    return main, oki


def _bounds_float4(bounds) -> tuple[float, float, float, float]:
    a = np.asarray(bounds, dtype=float).ravel()
    return float(a[0]), float(a[1]), float(a[2]), float(a[3])


def _set_axes_bounds(
    ax,
    bounds,
    *,
    anchor: str = "C",
    pad_left: float = 0.012,
    pad_right: float = 0.012,
    pad_bottom: float = 0.012,
    pad_top: float = 0.012,
):
    """Set projected bounds; asymmetric padding + anchor shift mainland toward bottom-right."""
    x0, y0, x1, y1 = _bounds_float4(bounds)
    dx = x1 - x0
    dy = y1 - y0
    ax.set_xlim(x0 - dx * pad_left, x1 + dx * pad_right)
    ax.set_ylim(y0 - dy * pad_bottom, y1 + dy * pad_top)
    ax.set_aspect("equal", anchor=anchor)


def _color_from_cmap(cmap, value: float, vmin: float, vmax: float):
    norm = Normalize(vmin=vmin, vmax=vmax)
    if isinstance(cmap, str):
        return mpl_cm.get_cmap(cmap)(norm(value))
    return cmap(norm(value))


def _oki_main_island_geoms(oki: gpd.GeoDataFrame) -> list:
    """Okinawa inset: largest island (本島) only, separate scale from mainland."""
    if len(oki.index) == 0:
        return []
    parts = _explode_parts(oki.geometry.iloc[0])
    if not parts:
        return []
    return [max(parts, key=lambda p: float(p.area))]


def _oki_bounds(islands: list) -> tuple[float, float, float, float]:
    xs0, ys0, xs1, ys1 = [], [], [], []
    for g in islands:
        b = g.bounds
        xs0.append(b[0])
        ys0.append(b[1])
        xs1.append(b[2])
        ys1.append(b[3])
    return min(xs0), min(ys0), max(xs1), max(ys1)


def _plot_islands_inset(ax_i, islands: list, *, facecolor, crs):
    for geom in islands:
        gpd.GeoSeries([geom], crs=crs).plot(
            ax=ax_i,
            color=facecolor,
            edgecolor=INSET_EDGE_COLOR,
            linewidth=0.55,
        )


def _style_okinawa_inset_ax(ax_i, title: str = "Okinawa"):
    ax_i.set_aspect("equal")
    ax_i.set_xticks([])
    ax_i.set_yticks([])
    ax_i.set_facecolor("white")
    ax_i.patch.set_alpha(0.98)
    ax_i.set_title(title, fontsize=FONT_TICK, pad=3, fontweight="semibold")
    for s in ax_i.spines.values():
        s.set_visible(True)
        s.set_linewidth(1.2)
        s.set_edgecolor("#333333")


def _draw_okinawa_inset_sequential(
    ax,
    oki: gpd.GeoDataFrame,
    *,
    column: str,
    cmap,
    vmin: float,
    vmax: float,
    rect: tuple[float, float, float, float],
    title: str = "Okinawa",
):
    if len(oki.index) == 0:
        return
    islands = _oki_main_island_geoms(oki)
    if not islands:
        return
    val = float(oki.iloc[0][column])
    facecolor = to_hex(_color_from_cmap(cmap, val, vmin, vmax))
    ax_i = ax.inset_axes(rect, transform=ax.transAxes, zorder=20)
    _plot_islands_inset(ax_i, islands, facecolor=facecolor, crs=oki.crs)
    x0, y0, x1, y1 = _oki_bounds(islands)
    pad_x = max((x1 - x0) * OKINAWA_INSET_PAD_FRAC, 3_000)
    pad_y = max((y1 - y0) * OKINAWA_INSET_PAD_FRAC, 3_000)
    ax_i.set_xlim(x0 - pad_x, x1 + pad_x)
    ax_i.set_ylim(y0 - pad_y, y1 + pad_y)
    _style_okinawa_inset_ax(ax_i, title)


def _draw_okinawa_inset_bivariate(
    ax,
    oki: gpd.GeoDataFrame,
    rect: tuple[float, float, float, float],
    *,
    title: str = "Okinawa",
):
    if len(oki.index) == 0:
        return
    islands = _oki_main_island_geoms(oki)
    if not islands:
        return
    facecolor = str(oki.iloc[0]["bv_color"])
    ax_i = ax.inset_axes(rect, transform=ax.transAxes, zorder=20)
    _plot_islands_inset(ax_i, islands, facecolor=facecolor, crs=oki.crs)
    x0, y0, x1, y1 = _oki_bounds(islands)
    pad_x = max((x1 - x0) * OKINAWA_INSET_PAD_FRAC, 3_000)
    pad_y = max((y1 - y0) * OKINAWA_INSET_PAD_FRAC, 3_000)
    ax_i.set_xlim(x0 - pad_x, x1 + pad_x)
    ax_i.set_ylim(y0 - pad_y, y1 + pad_y)
    _style_okinawa_inset_ax(ax_i, title)


def _apply_mainland_layout(ax, main_bounds, layout: dict | None):
    if layout is None:
        _set_axes_bounds(ax, main_bounds, pad_left=MAINLAND_PAD_TIGHT, pad_right=MAINLAND_PAD_TIGHT,
                         pad_bottom=MAINLAND_PAD_TIGHT, pad_top=MAINLAND_PAD_TIGHT)
    else:
        _set_axes_bounds(ax, main_bounds, **layout)


def plot_slope_choropleth(
    ax,
    gdf,
    *,
    legend=True,
    scalebar=False,
    panel_label=None,
    cbar_size="4%",
    cbar_pad=0.06,
    okinawa_inset=False,
    okinawa_inset_rect: tuple[float, float, float, float] | None = None,
    mainland_layout: dict | None = None,
):
    rect = okinawa_inset_rect if okinawa_inset_rect is not None else OKINAWA_INSET_RECT_DEFAULT
    main, oki = _split_okinawa(gdf)
    main_disp = _build_mainland_display(main)
    vmin = float(gdf["habitable_slope_weighted"].min())
    vmax = float(gdf["habitable_slope_weighted"].max())

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size=cbar_size, pad=cbar_pad)
    main_disp.plot(
        column="habitable_slope_weighted",
        ax=ax,
        cmap=SLOPE_CMAP,
        edgecolor=EDGE_COLOR,
        linewidth=LINE_WIDTH,
        vmin=vmin,
        vmax=vmax,
        legend=legend,
        cax=cax,
        legend_kwds={"label": "Slope (degrees)", "orientation": "vertical", "shrink": 0.88},
        missing_kwds={"color": "#cccccc"},
    )
    style_ax(ax)
    layout = mainland_layout if okinawa_inset else None
    _apply_mainland_layout(ax, tuple(main_disp.total_bounds), layout)
    if scalebar:
        add_scalebar(ax)
    if okinawa_inset:
        _draw_okinawa_inset_sequential(
            ax, oki, column="habitable_slope_weighted", cmap=SLOPE_CMAP, vmin=vmin, vmax=vmax, rect=rect
        )
    if panel_label:
        add_panel_label(ax, panel_label)
    cax.tick_params(labelsize=FONT_TICK)
    cax.yaxis.label.set_size(FONT_LABEL)


def plot_fracture_choropleth(
    ax,
    gdf,
    *,
    legend=True,
    scalebar=False,
    panel_label=None,
    cbar_size="4%",
    cbar_pad=0.06,
    okinawa_inset=False,
    okinawa_inset_rect: tuple[float, float, float, float] | None = None,
    mainland_layout: dict | None = None,
):
    rect = okinawa_inset_rect if okinawa_inset_rect is not None else OKINAWA_INSET_RECT_DEFAULT
    main, oki = _split_okinawa(gdf)
    main_disp = _build_mainland_display(main)
    vmin = float(gdf["femur_rate"].min())
    vmax = float(gdf["femur_rate"].max())

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size=cbar_size, pad=cbar_pad)
    main_disp.plot(
        column="femur_rate",
        ax=ax,
        cmap=FRACTURE_CMAP,
        edgecolor=EDGE_COLOR,
        linewidth=LINE_WIDTH,
        vmin=vmin,
        vmax=vmax,
        legend=legend,
        cax=cax,
        legend_kwds={
            "label": "Hip fracture surgery rate\n(per 100,000 population)",
            "orientation": "vertical",
            "shrink": 0.88,
        },
        missing_kwds={"color": "#cccccc"},
    )
    style_ax(ax)
    layout = mainland_layout if okinawa_inset else None
    _apply_mainland_layout(ax, tuple(main_disp.total_bounds), layout)
    if scalebar:
        add_scalebar(ax)
    if okinawa_inset:
        _draw_okinawa_inset_sequential(
            ax, oki, column="femur_rate", cmap=FRACTURE_CMAP, vmin=vmin, vmax=vmax, rect=rect
        )
    if panel_label:
        add_panel_label(ax, panel_label)
    cax.tick_params(labelsize=FONT_TICK)
    cax.yaxis.label.set_size(FONT_LABEL)


def plot_bivariate_choropleth(
    ax,
    gdf,
    fig,
    *,
    scalebar=True,
    scalebar_length_km: int | None = 200,
    scalebar_kw=None,
    panel_label=None,
    legend_rect=(0.78, 0.10, 0.16, 0.16),
    okinawa_inset=False,
    okinawa_inset_rect: tuple[float, float, float, float] | None = None,
    mainland_layout: dict | None = None,
):
    rect = okinawa_inset_rect if okinawa_inset_rect is not None else OKINAWA_INSET_RECT_DEFAULT
    main, oki = _split_okinawa(gdf)
    main_disp = _build_mainland_display(main)
    for _, row in main_disp.iterrows():
        gpd.GeoSeries([row.geometry]).plot(
            ax=ax,
            color=row["bv_color"],
            edgecolor=EDGE_COLOR,
            linewidth=LINE_WIDTH,
        )
    style_ax(ax)
    layout = mainland_layout if okinawa_inset else None
    _apply_mainland_layout(ax, tuple(main_disp.total_bounds), layout)
    if scalebar:
        sb = {"lw": 2.5, "fontsize": FONT_TICK, "dy_frac": 0.012}
        if scalebar_kw:
            sb.update(scalebar_kw)
        add_scalebar(ax, scalebar_length_km, **sb)
    if okinawa_inset:
        _draw_okinawa_inset_bivariate(ax, oki, rect)
    if panel_label:
        add_panel_label(ax, panel_label)

    inset = fig.add_axes(legend_rect)
    inset.set_aspect("equal")
    for fi in range(3):
        for si in range(3):
            inset.add_patch(mpatches.Rectangle(
                (si, fi), 1, 1,
                color=BVPAL[fi, si],
                ec="white", lw=1.0,
            ))
    inset.set_xlim(0, 3)
    inset.set_ylim(0, 3)
    inset.set_xticks([0, 1.5, 3])
    inset.set_yticks([0, 1.5, 3])
    inset.set_xticklabels(["Low", "", "High"], fontsize=FONT_LEGEND + 1, fontweight="medium")
    inset.set_yticklabels(["Low", "", "High"], fontsize=FONT_LEGEND + 1, fontweight="medium")
    inset.set_xlabel("Slope →", fontsize=FONT_LEGEND + 1, labelpad=4, fontweight="medium")
    inset.set_ylabel("Fracture →", fontsize=FONT_LEGEND + 1, labelpad=4, fontweight="medium")
    inset.set_title("Legend", fontsize=FONT_LEGEND + 2, pad=6, fontweight="semibold")
    for spine in inset.spines.values():
        spine.set_linewidth(0.8)
    inset.tick_params(length=0)


def main():
    df = pd.read_csv(DATA_CSV, encoding="utf-8")
    df["pref_code"] = range(1, len(df) + 1)

    gdf = gpd.read_file(GEOJSON)
    gdf = gdf.rename(columns={"id": "pref_code"})
    merged = gdf.merge(df, on="pref_code", how="left").to_crs(epsg=6677)
    merged_bv = assign_bivariate_classes(merged)
    main_all, _ = _split_okinawa(merged)
    main_disp = _build_mainland_display(main_all)
    b0 = main_all.total_bounds
    b1 = main_disp.total_bounds
    print(f"Mainland display span (km): "
          f"{(b1[2]-b1[0])/1000:.0f} x {(b1[3]-b1[1])/1000:.0f} "
          f"(was {(b0[2]-b0[0])/1000:.0f} x {(b0[3]-b0[1])/1000:.0f} with all islets)")
    print(f"Slope range: {df['habitable_slope_weighted'].min():.2f} - {df['habitable_slope_weighted'].max():.2f} degrees")
    print(f"Femur rate range: {df['femur_rate'].min():.1f} - {df['femur_rate'].max():.1f} per 100,000")

    # --- Legacy single-panel outputs (optional reference) ---
    print("\n[Legacy] Single-panel slope map ...")
    fig, ax = plt.subplots(figsize=(9, 10.5))
    plot_slope_choropleth(ax, merged, scalebar=True, okinawa_inset=True, mainland_layout=MAINLAND_LAYOUT_TOP)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_map_slope.png"), dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    print("[Legacy] Single-panel fracture map ...")
    fig, ax = plt.subplots(figsize=(9, 10.5))
    plot_fracture_choropleth(ax, merged, scalebar=True, okinawa_inset=True, mainland_layout=MAINLAND_LAYOUT_TOP)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_map_fracture.png"), dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    print("[Legacy] Single-panel bivariate map ...")
    fig, ax = plt.subplots(figsize=(9, 10.5))
    plot_bivariate_choropleth(
        ax, merged_bv, fig, legend_rect=(0.72, 0.08, 0.18, 0.18),
        okinawa_inset=True, mainland_layout=MAINLAND_LAYOUT_CENTER,
    )
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_map_bivariate.png"), dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    # --- Main manuscript Figure 2: composite layout ---
    # Larger canvas + slimmer colorbars so Japan fills more of the figure; panel (C) scale bar auto-length + thicker line.
    print("[Figure 2 composite] Top: slope | fracture; bottom: bivariate ...")
    fig = plt.figure(figsize=(21, 22))
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.15], hspace=0.035, wspace=0.028)
    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[0, 1])
    ax_c = fig.add_subplot(gs[1, :])

    plot_slope_choropleth(
        ax_a,
        merged,
        scalebar=False,
        panel_label="(A)",
        cbar_size="3.8%",
        cbar_pad=0.045,
        okinawa_inset=True,
        mainland_layout=MAINLAND_LAYOUT_TOP,
    )
    plot_fracture_choropleth(
        ax_b,
        merged,
        scalebar=False,
        panel_label="(B)",
        cbar_size="3.8%",
        cbar_pad=0.045,
        okinawa_inset=True,
        mainland_layout=MAINLAND_LAYOUT_TOP,
    )
    plot_bivariate_choropleth(
        ax_c,
        merged_bv,
        fig,
        scalebar=True,
        scalebar_length_km=None,
        scalebar_kw={"lw": 3.4, "fontsize": FONT_TICK + 2, "x_frac": 0.045, "y_frac": 0.035, "dy_frac": 0.014},
        panel_label="(C)",
        legend_rect=(0.805, 0.12, 0.155, 0.195),
        okinawa_inset=True,
        okinawa_inset_rect=OKINAWA_INSET_RECT_WIDE,
        mainland_layout=MAINLAND_LAYOUT_CENTER,
    )

    composite_path = os.path.join(OUT_DIR, "fig_map_geography_composite.png")
    fig.savefig(composite_path, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  Saved: {composite_path}")

    print("\n=== All maps created successfully ===")
    print(f"Output directory: {OUT_DIR}")


if __name__ == "__main__":
    main()
