# -*- coding: utf-8 -*-
"""
10_create_prefecture_maps.py
----------------------------
驛ｽ驕灘ｺ懃恁蛻･譌･譛ｬ蝨ｰ蝗ｳ繧・遞ｮ鬘樔ｽ懈・縺吶ｋ繧ｹ繧ｯ繝ｪ繝励ヨ縲・
Figure 3: 蛯ｾ譁懷ｺｦ縺ｮ蝨ｰ蝓溷・蟶・ｼ医さ繝ｭ繝励Ξ繧ｹ蝨ｰ蝗ｳ・・Figure 4: 螟ｧ閻ｿ鬪ｨ鬪ｨ謚俶焔陦鍋紫縺ｮ蝨ｰ蝓溷・蟶・ｼ医さ繝ｭ繝励Ξ繧ｹ蝨ｰ蝗ｳ・・Figure 5: 蛯ｾ譁懷ｺｦ ﾃ・鬪ｨ謚倡紫縺ｮ莠悟､蛾㍼繧ｳ繝ｭ繝励Ξ繧ｹ蝨ｰ蝗ｳ・・ﾃ・繧ｰ繝ｪ繝・ラ・・
蝗ｳ逡ｪ蜿ｷ繝ｻ繧ｭ繝｣繝励す繝ｧ繝ｳ縺ｯ蜴溽ｨｿ縺ｮ Figure legends 縺ｫ險倩ｼ峨☆繧九◆繧√∝慍蝗ｳ繝代ロ繝ｫ蜀・↓縺ｯ
縲熊igure N.縲榊ｽ｢蠑上・繧ｿ繧､繝医Ν繧剃ｻ倥￠縺ｪ縺・・
螳溯｡梧婿豕包ｼ・DB_Research_Hub 繝ｫ繝ｼ繝医∪縺溘・ 03_Analysis/scripts 縺九ｉ・・
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

# 譌･譛ｬ隱槭ヵ繧ｩ繝ｳ繝郁ｨｭ螳・try:
    import japanize_matplotlib
except ImportError:
    import matplotlib.font_manager as fm
    fonts = [f.name for f in fm.fontManager.ttflist if "Gothic" in f.name or "Meiryo" in f.name]
    if fonts:
        matplotlib.rcParams["font.family"] = fonts[0]

# ---------------------------------------------------------------------------
# 繝代せ險ｭ螳・# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))

DATA_CSV = os.path.join(PROJECT_DIR, "03_Analysis", "data", "processed", "analysis_dataset_v1.csv")
GEOJSON  = os.path.join(
    os.path.abspath(os.path.join(PROJECT_DIR, "..", "..")),  # 竊・NDB_Research_Hub
    "02_Data", "raw", "GIS", "japan.geojson"
)
OUT_DIR  = os.path.join(PROJECT_DIR, "03_Analysis", "results", "figures")
os.makedirs(OUT_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# 繝・・繧ｿ隱ｭ縺ｿ霎ｼ縺ｿ
# ---------------------------------------------------------------------------
df = pd.read_csv(DATA_CSV, encoding="utf-8")
# 驛ｽ驕灘ｺ懃恁繧ｳ繝ｼ繝峨ｒ霑ｽ蜉・亥圏豬ｷ驕・1 窶ｦ 豐也ｸ・47・・df["pref_code"] = range(1, len(df) + 1)

gdf = gpd.read_file(GEOJSON)  # columns: nam, nam_ja, id, geometry
# id 縺ｧ邨仙粋
gdf = gdf.rename(columns={"id": "pref_code"})
merged = gdf.merge(df, on="pref_code", how="left")
merged = merged.to_crs(epsg=6677)  # JGD2011 / Japan Plane Rectangular CS IX・亥腰菴肯・・
print(f"Merged shape: {merged.shape}")
print(f"Slope range:   {df['habitable_slope_weighted'].min():.2f} - {df['habitable_slope_weighted'].max():.2f} degrees")
print(f"Femur rate range: {df['femur_rate'].min():.1f} - {df['femur_rate'].max():.1f} per 100,000")

# ---------------------------------------------------------------------------
# 蜈ｱ騾壹Ξ繧､繧｢繧ｦ繝郁ｨｭ螳・# ---------------------------------------------------------------------------
FONT_TITLE  = 16
FONT_LABEL  = 12
FONT_TICK   = 10
EDGE_COLOR  = "white"
LINE_WIDTH  = 0.5
DPI         = 300

def style_ax(ax):
    """蝨ｰ蝗ｳ霆ｸ縺ｮ蜈ｱ騾壹せ繧ｿ繧､繝ｫ險ｭ螳・""
    ax.set_axis_off()
    ax.set_aspect("equal")


def add_scalebar(ax, length_km=200, x_frac=0.05, y_frac=0.04, lw=2.5):
    """繧ｹ繧ｱ繝ｼ繝ｫ繝舌・繧定ｿｽ蜉・・m 陦ｨ遉ｺ・・""
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    x0 = xlim[0] + (xlim[1] - xlim[0]) * x_frac
    y0 = ylim[0] + (ylim[1] - ylim[0]) * y_frac
    x1 = x0 + length_km * 1000  # 繝｡繝ｼ繝医Ν螟画鋤
    ax.plot([x0, x1], [y0, y0], "k-", lw=lw, solid_capstyle="butt")
    ax.text((x0 + x1) / 2, y0 + (ylim[1] - ylim[0]) * 0.012,
            f"{length_km} km", ha="center", va="bottom", fontsize=FONT_TICK)


# ---------------------------------------------------------------------------
# Figure 3: 蛯ｾ譁懷ｺｦ縺ｮ蝨ｰ蝓溷・蟶・# ---------------------------------------------------------------------------
print("\n[Figure 3] Slope distribution map ...")

fig4, ax4 = plt.subplots(figsize=(8, 9))
divider = make_axes_locatable(ax4)
cax4 = divider.append_axes("right", size="4%", pad=0.08)

merged.plot(
    column="habitable_slope_weighted",
    ax=ax4,
    cmap="YlOrRd",
    edgecolor=EDGE_COLOR,
    linewidth=LINE_WIDTH,
    legend=True,
    cax=cax4,
    legend_kwds={"label": "Slope (degrees)", "orientation": "vertical", "shrink": 0.8},
    missing_kwds={"color": "#cccccc"},
)

# 5蛻・ｽ阪・遲牙､邱壼｢・阜繧堤せ邱壹〒遉ｺ縺・style_ax(ax4)
add_scalebar(ax4)
cax4.tick_params(labelsize=FONT_TICK)

fig4.tight_layout()
out_path = os.path.join(OUT_DIR, "fig_map_slope.png")
fig4.savefig(out_path, dpi=DPI, bbox_inches="tight", facecolor="white")
plt.close(fig4)
print(f"  Saved: {out_path}")

# ---------------------------------------------------------------------------
# Figure 4: 螟ｧ閻ｿ鬪ｨ鬪ｨ謚俶焔陦鍋紫縺ｮ蝨ｰ蝓溷・蟶・# ---------------------------------------------------------------------------
print("[Figure 4] Fracture rate distribution map ...")

fig5, ax5 = plt.subplots(figsize=(8, 9))
divider = make_axes_locatable(ax5)
cax5 = divider.append_axes("right", size="4%", pad=0.08)

merged.plot(
    column="femur_rate",
    ax=ax5,
    cmap="Blues",
    edgecolor=EDGE_COLOR,
    linewidth=LINE_WIDTH,
    legend=True,
    cax=cax5,
    legend_kwds={"label": "Hip fracture surgery rate\n(per 100,000 population)",
                 "orientation": "vertical", "shrink": 0.8},
    missing_kwds={"color": "#cccccc"},
)

style_ax(ax5)
add_scalebar(ax5)
cax5.tick_params(labelsize=FONT_TICK)

fig5.tight_layout()
out_path = os.path.join(OUT_DIR, "fig_map_fracture.png")
fig5.savefig(out_path, dpi=DPI, bbox_inches="tight", facecolor="white")
plt.close(fig5)
print(f"  Saved: {out_path}")

# ---------------------------------------------------------------------------
# Figure 5: 莠悟､蛾㍼繧ｳ繝ｭ繝励Ξ繧ｹ蝨ｰ蝗ｳ・亥だ譁懷ｺｦ ﾃ・鬪ｨ謚倡紫 3ﾃ・・・# ---------------------------------------------------------------------------
print("[Figure 5] Bivariate choropleth map ...")

#  3ﾃ・ 莠悟､蛾㍼繧ｫ繝ｩ繝ｼ繝代Ξ繝・ヨ・・tevens & Brewer palette・・#  陦・= 鬪ｨ謚倡紫・井ｽ寂・鬮假ｼ・ 蛻・= 蛯ｾ譁懷ｺｦ・井ｽ寂・鬮假ｼ・BVPAL = np.array([
    ["#e8e8e8", "#b0d5df", "#64acbe"],   # low fracture
    ["#e4d9ac", "#ad9ea5", "#627f8c"],   # mid fracture
    ["#c85a5a", "#985356", "#574249"],   # high fracture
])

def quantile3(series):
    """0/1/2 縺ｮ3蛻・ｽ阪け繝ｩ繧ｹ・育ｭ蛾ｻ蠎ｦ・峨ｒ霑斐☆"""
    q33 = series.quantile(1 / 3)
    q67 = series.quantile(2 / 3)
    return pd.cut(series, bins=[-np.inf, q33, q67, np.inf],
                  labels=[0, 1, 2]).astype(int)


merged["slope_class"]   = quantile3(merged["habitable_slope_weighted"])
merged["fracture_class"] = quantile3(merged["femur_rate"])
merged["bv_color"] = merged.apply(
    lambda r: BVPAL[int(r["fracture_class"]), int(r["slope_class"])],
    axis=1
)

fig6, ax6 = plt.subplots(figsize=(8, 9))

for _, row in merged.iterrows():
    gpd.GeoSeries([row.geometry]).plot(
        ax=ax6,
        color=row["bv_color"],
        edgecolor=EDGE_COLOR,
        linewidth=LINE_WIDTH,
    )

style_ax(ax6)
add_scalebar(ax6)

# --- 蜃｡萓具ｼ・ﾃ・ 繧ｰ繝ｪ繝・ラ繧・inset axes 縺ｫ謠冗判 ---
inset = fig6.add_axes([0.72, 0.08, 0.18, 0.18])  # [left, bottom, width, height]
inset.set_aspect("equal")
for fi in range(3):          # fracture_class (菴・0 縺御ｸ・
    for si in range(3):      # slope_class (菴・0 縺悟ｷｦ)
        inset.add_patch(mpatches.Rectangle(
            (si, fi), 1, 1,
            color=BVPAL[fi, si],
            ec="white", lw=0.5
        ))

inset.set_xlim(0, 3)
inset.set_ylim(0, 3)
inset.set_xticks([0, 1.5, 3])
inset.set_yticks([0, 1.5, 3])
inset.set_xticklabels(["Low", "", "High"], fontsize=6)
inset.set_yticklabels(["Low", "", "High"], fontsize=6)
inset.set_xlabel("Slope 竊・, fontsize=6, labelpad=1)
inset.set_ylabel("Fracture 竊・, fontsize=6, labelpad=1)
inset.set_title("Legend", fontsize=7, pad=3)
inset.tick_params(length=0)

fig6.tight_layout()
out_path = os.path.join(OUT_DIR, "fig_map_bivariate.png")
fig6.savefig(out_path, dpi=DPI, bbox_inches="tight", facecolor="white")
plt.close(fig6)
print(f"  Saved: {out_path}")

# ---------------------------------------------------------------------------
# 陬懆ｶｳ: 2蛻玲ｨｪ荳ｦ縺ｳ・亥だ譁懷ｺｦ | 鬪ｨ謚倡紫・会ｼ狗嶌髢｢謨｣蟶・峙・域悽譁・悴謗ｲ霈峨・蜷域・蝗ｳ・・# ---------------------------------------------------------------------------
print("[Supplementary combined map] Side-by-side maps + scatter ...")

fig_sb, axes = plt.subplots(1, 3, figsize=(18, 8))

# ---- panel A: slope ----
ax_a = axes[0]
divider_a = make_axes_locatable(ax_a)
cax_a = divider_a.append_axes("right", size="5%", pad=0.08)
merged.plot(column="habitable_slope_weighted", ax=ax_a, cmap="YlOrRd",
            edgecolor=EDGE_COLOR, linewidth=LINE_WIDTH,
            legend=True, cax=cax_a,
            legend_kwds={"label": "Slope (degrees)", "orientation": "vertical"},
            missing_kwds={"color": "#cccccc"})
style_ax(ax_a)
ax_a.set_title("(A) Terrain Slope", fontsize=FONT_TITLE, fontweight="bold", pad=8)
add_scalebar(ax_a, length_km=200)
cax_a.tick_params(labelsize=FONT_TICK)

# ---- panel B: fracture rate ----
ax_b = axes[1]
divider_b = make_axes_locatable(ax_b)
cax_b = divider_b.append_axes("right", size="5%", pad=0.08)
merged.plot(column="femur_rate", ax=ax_b, cmap="Blues",
            edgecolor=EDGE_COLOR, linewidth=LINE_WIDTH,
            legend=True, cax=cax_b,
            legend_kwds={"label": "Rate per 100,000", "orientation": "vertical"},
            missing_kwds={"color": "#cccccc"})
style_ax(ax_b)
ax_b.set_title("(B) Hip Fracture Surgery Rate", fontsize=FONT_TITLE, fontweight="bold", pad=8)
add_scalebar(ax_b, length_km=200)
cax_b.tick_params(labelsize=FONT_TICK)

# ---- panel C: scatter (slope vs femur) ----
ax_c = axes[2]
sc = ax_c.scatter(
    df["habitable_slope_weighted"], df["femur_rate"],
    c=df["habitable_slope_weighted"], cmap="YlOrRd",
    s=70, edgecolors="grey", linewidths=0.5, zorder=3
)
# 蝗槫ｸｰ逶ｴ邱・m, b = np.polyfit(df["habitable_slope_weighted"], df["femur_rate"], 1)
xs = np.linspace(df["habitable_slope_weighted"].min(), df["habitable_slope_weighted"].max(), 100)
ax_c.plot(xs, m * xs + b, "k--", lw=1.5, label=f"ﾎｲ = {m:.2f}")
ax_c.set_xlabel("Terrain slope (degrees)", fontsize=FONT_LABEL)
ax_c.set_ylabel("Hip fracture surgery rate (per 100,000)", fontsize=FONT_LABEL)
ax_c.set_title("(C) Slope vs. Hip Fracture Rate\n(r = 0.475, p < 0.01)", fontsize=FONT_TITLE, fontweight="bold", pad=8)
ax_c.tick_params(labelsize=FONT_TICK)
ax_c.legend(fontsize=FONT_TICK)
ax_c.spines["top"].set_visible(False)
ax_c.spines["right"].set_visible(False)
ax_c.grid(alpha=0.3, lw=0.5)

fig_sb.suptitle(
    "Supplementary figure. Geographic Distribution of Terrain Slope and Hip Fracture Surgery Rate\nAcross 47 Japanese Prefectures",
    fontsize=FONT_TITLE + 1, fontweight="bold", y=1.02
)
fig_sb.tight_layout()
out_path_sb = os.path.join(OUT_DIR, "fig_map_combined.png")
fig_sb.savefig(out_path_sb, dpi=DPI, bbox_inches="tight", facecolor="white")
plt.close(fig_sb)
print(f"  Saved: {out_path_sb}")

print("\n=== All maps created successfully ===")
print(f"Output directory: {OUT_DIR}")
