# -*- coding: utf-8 -*-
"""Regenerate Figure 1 scatter with English prefecture labels (supervisor comment ⑨)."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

# Resolve project root explicitly (avoid symlinked workspace paths).
BASE = Path(r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture\03_Analysis")
CSV_PATH = BASE / "data" / "processed" / "analysis_dataset_v1.csv"
OUT_PATH = BASE / "results" / "figures" / "scatter_slope_fracture.png"

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


def main() -> None:
    df = pd.read_csv(CSV_PATH, encoding="utf-8")
    df["pref_en"] = df["prefecture"].map(JP_TO_EN)
    missing = df.loc[df["pref_en"].isna(), "prefecture"].tolist()
    if missing:
        raise SystemExit(f"Unmapped prefectures: {missing}")

    x = df["habitable_slope_weighted"].to_numpy()
    y = df["femur_rate"].to_numpy()

    slope, intercept, _, _, _ = stats.linregress(x, y)
    xs = np.linspace(x.min(), x.max(), 200)
    ys = slope * xs + intercept
    pred = slope * x + intercept
    resid = y - pred
    dof = max(len(x) - 2, 1)
    mse = np.sum(resid**2) / dof
    sxx = np.sum((x - x.mean()) ** 2)
    se = np.sqrt(mse * (1 / len(x) + (xs - x.mean()) ** 2 / sxx))
    tval = stats.t.ppf(0.975, dof)
    ci = tval * se

    plt.figure(figsize=(11, 8))
    ax = plt.gca()
    ax.fill_between(xs, ys - ci, ys + ci, color="#f8b4b4", alpha=0.7, linewidth=0)
    ax.plot(xs, ys, color="red", linewidth=2)
    ax.scatter(x, y, color="steelblue", s=40, zorder=3, edgecolors="white", linewidths=0.5)

    for _, row in df.iterrows():
        ax.annotate(
            row["pref_en"],
            (row["habitable_slope_weighted"], row["femur_rate"]),
            fontsize=9,
            ha="center",
            va="bottom",
            alpha=0.85,
        )

    ax.set_xlabel("Habitable-area-weighted slope (degrees)", fontsize=11)
    ax.set_ylabel("Hip fracture surgery rate (per 100,000)", fontsize=11)
    ax.set_title("Terrain slope and hip fracture surgery rate by prefecture", fontsize=12)
    ax.tick_params(labelsize=10)
    ax.grid(True, linestyle="--", alpha=0.35)
    plt.tight_layout()
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUT_PATH, dpi=300, bbox_inches="tight")
    plt.close()
    print("Wrote", OUT_PATH)


if __name__ == "__main__":
    main()
