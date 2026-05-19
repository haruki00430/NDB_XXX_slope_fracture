# -*- coding: utf-8 -*-
"""Regenerate Figure 1 scatter with English prefecture labels (supervisor comment 竭ｨ)."""
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
    "蛹玲ｵｷ驕・: "Hokkaido",
    "髱呈｣ｮ逵・: "Aomori",
    "蟯ｩ謇狗恁": "Iwate",
    "螳ｮ蝓守恁": "Miyagi",
    "遘狗伐逵・: "Akita",
    "螻ｱ蠖｢逵・: "Yamagata",
    "遖丞ｳｶ逵・: "Fukushima",
    "闌ｨ蝓守恁": "Ibaraki",
    "譬・惠逵・: "Tochigi",
    "鄒､鬥ｬ逵・: "Gunma",
    "蝓ｼ邇臥恁": "Saitama",
    "蜊・痩逵・: "Chiba",
    "譚ｱ莠ｬ驛ｽ": "Tokyo",
    "逾槫･亥ｷ晉恁": "Kanagawa",
    "譁ｰ貎溽恁": "Niigata",
    "蟇悟ｱｱ逵・: "Toyama",
    "遏ｳ蟾晉恁": "Ishikawa",
    "遖丈ｺ慕恁": "Fukui",
    "螻ｱ譴ｨ逵・: "Yamanashi",
    "髟ｷ驥守恁": "Nagano",
    "蟯宣・逵・: "Gifu",
    "髱吝ｲ｡逵・: "Shizuoka",
    "諢帷衍逵・: "Aichi",
    "荳蛾㍾逵・: "Mie",
    "貊玖ｳ逵・: "Shiga",
    "莠ｬ驛ｽ蠎・: "Kyoto",
    "螟ｧ髦ｪ蠎・: "Osaka",
    "蜈ｵ蠎ｫ逵・: "Hyogo",
    "螂郁憶逵・: "Nara",
    "蜥梧ｭ悟ｱｱ逵・: "Wakayama",
    "魑･蜿也恁": "Tottori",
    "蟲ｶ譬ｹ逵・: "Shimane",
    "蟯｡螻ｱ逵・: "Okayama",
    "蠎・ｳｶ逵・: "Hiroshima",
    "螻ｱ蜿｣逵・: "Yamaguchi",
    "蠕ｳ蟲ｶ逵・: "Tokushima",
    "鬥吝ｷ晉恁": "Kagawa",
    "諢帛ｪ帷恁": "Ehime",
    "鬮倡衍逵・: "Kochi",
    "遖丞ｲ｡逵・: "Fukuoka",
    "菴占ｳ逵・: "Saga",
    "髟ｷ蟠守恁": "Nagasaki",
    "辭頑悽逵・: "Kumamoto",
    "螟ｧ蛻・恁": "Oita",
    "螳ｮ蟠守恁": "Miyazaki",
    "鮖ｿ蜈仙ｳｶ逵・: "Kagoshima",
    "豐也ｸ・恁": "Okinawa",
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
