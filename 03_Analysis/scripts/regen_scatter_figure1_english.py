# -*- coding: utf-8 -*-
"""Regenerate Figure 1 scatter with English prefecture labels (supervisor comment ⑨)."""
from __future__ import annotations

from pathlib import Path
from typing import Tuple, cast

import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from adjustText import adjust_text  # type: ignore[import-untyped]
from matplotlib import rcParams
from scipy import stats

# Resolve project root explicitly (avoid symlinked workspace paths).
BASE = Path(r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture\03_Analysis")
CSV_PATH = BASE / "data" / "processed" / "analysis_dataset_v1.csv"
OUT_PATH = BASE / "results" / "figures" / "scatter_slope_fracture.png"

DPI = 300
rcParams.update(
    {
        "figure.dpi": DPI,
        "savefig.dpi": DPI,
        "font.size": 13,
        "axes.labelsize": 15,
        "axes.titlesize": 15,
        "xtick.labelsize": 13,
        "ytick.labelsize": 13,
        "axes.linewidth": 1.1,
        "grid.linewidth": 0.9,
    }
)

JP_TO_EN = {
    "北海道": "Hokkaido",
    "青森県": "Aomori",
    "岩手県": "Iwate",
    "宮城県": "Miyagi",
    "秋田県": "Akita",
    "山形県": "Yamagata",
    "福島県": "Fukushima",
    "茨城県": "Ibaraki",
    "栃木県": "Tochigi",
    "群馬県": "Gunma",
    "埼玉県": "Saitama",
    "千葉県": "Chiba",
    "東京都": "Tokyo",
    "神奈川県": "Kanagawa",
    "新潟県": "Niigata",
    "富山県": "Toyama",
    "石川県": "Ishikawa",
    "福井県": "Fukui",
    "山梨県": "Yamanashi",
    "長野県": "Nagano",
    "岐阜県": "Gifu",
    "静岡県": "Shizuoka",
    "愛知県": "Aichi",
    "三重県": "Mie",
    "滋賀県": "Shiga",
    "京都府": "Kyoto",
    "大阪府": "Osaka",
    "兵庫県": "Hyogo",
    "奈良県": "Nara",
    "和歌山県": "Wakayama",
    "鳥取県": "Tottori",
    "島根県": "Shimane",
    "岡山県": "Okayama",
    "広島県": "Hiroshima",
    "山口県": "Yamaguchi",
    "徳島県": "Tokushima",
    "香川県": "Kagawa",
    "愛媛県": "Ehime",
    "高知県": "Kochi",
    "福岡県": "Fukuoka",
    "佐賀県": "Saga",
    "長崎県": "Nagasaki",
    "熊本県": "Kumamoto",
    "大分県": "Oita",
    "宮崎県": "Miyazaki",
    "鹿児島県": "Kagoshima",
    "沖縄県": "Okinawa",
}


def _place_prefecture_labels(
    ax,
    labels: list[str],
    xs_lab: list[float],
    ys_lab: list[float],
) -> None:
    """Repel overlapping labels; thin leader lines link each label to its point."""
    halo = [pe.withStroke(linewidth=3.5, foreground="white", alpha=0.95)]
    texts = []
    for lbl, xf, yf in zip(labels, xs_lab, ys_lab, strict=True):
        texts.append(
            ax.text(
                xf,
                yf,
                lbl,
                fontsize=10.5,
                fontweight="medium",
                ha="center",
                va="center",
                path_effects=halo,
                zorder=6,
            )
        )
    adjust_text(
        texts,
        x=xs_lab,
        y=ys_lab,
        ax=ax,
        arrowprops={
            "arrowstyle": "-",
            "color": "#555555",
            "lw": 0.7,
            "alpha": 0.8,
            "shrinkA": 6,
            "shrinkB": 3,
        },
        expand=(1.14, 1.22),
        force_text=(0.6, 1.0),
        force_points=(0.4, 0.65),
        only_move={"text": "xy", "points": "y", "objects": "xy"},
        lim=500,
    )


def main() -> None:
    df = pd.read_csv(CSV_PATH, encoding="utf-8")
    df["pref_en"] = df["prefecture"].replace(JP_TO_EN)
    missing = df.loc[df["pref_en"].isna(), "prefecture"].tolist()
    if missing:
        raise SystemExit(f"Unmapped prefectures: {missing}")

    x = df["habitable_slope_weighted"].to_numpy(dtype=float)
    y = df["femur_rate"].to_numpy(dtype=float)

    slope, intercept, _, _, _ = cast(
        Tuple[float, float, float, float, float],
        stats.linregress(x, y),
    )
    xs = np.linspace(float(x.min()), float(x.max()), 200)
    ys = slope * xs + intercept
    pred = slope * x + intercept
    resid = y - pred
    dof = max(len(x) - 2, 1)
    mse = float(np.sum(resid**2) / dof)
    sxx = float(np.sum((x - x.mean()) ** 2))
    se = np.sqrt(mse * (1 / len(x) + (xs - x.mean()) ** 2 / sxx))
    tval = stats.t.ppf(0.975, dof)
    ci = tval * se

    fig, ax = plt.subplots(figsize=(14.5, 10.0))
    ax.fill_between(xs, ys - ci, ys + ci, color="#fca5a5", alpha=0.5, linewidth=0, zorder=1)
    ax.plot(xs, ys, color="#dc2626", linewidth=3.0, zorder=2)
    ax.scatter(
        x,
        y,
        color="#1d4ed8",
        s=100,
        zorder=4,
        edgecolors="white",
        linewidths=1.1,
        alpha=0.95,
    )

    labels = df["pref_en"].astype(str).tolist()
    xs_lab = df["habitable_slope_weighted"].astype(float).tolist()
    ys_lab = df["femur_rate"].astype(float).tolist()
    _place_prefecture_labels(ax, labels, xs_lab, ys_lab)

    ax.set_xlabel("Habitable-area-weighted terrain slope (degrees)")
    ax.set_ylabel("Hip fracture surgery rate (per 100,000 population)")
    ax.grid(True, linestyle="--", alpha=0.35, zorder=0)
    ax.set_xlim(float(x.min()) - 0.6, float(x.max()) + 0.6)
    ax.set_ylim(float(y.min()) - 12, float(y.max()) + 12)

    fig.tight_layout()
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PATH, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("Wrote", OUT_PATH)


if __name__ == "__main__":
    main()
