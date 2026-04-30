# pyright: reportGeneralTypeIssues=false, reportAttributeAccessIssue=false, reportArgumentType=false, reportCallIssue=false, reportOperatorIssue=false, reportIndexIssue=false, reportReturnType=false

"""
Manuscript mainline pipeline (true single-file implementation).

This file alone performs:
1) NDB fracture extraction
2) NDB walking-speed extraction
3) census merge (manual baseline used in current manuscript)
4) dataset integration
5) regression / tables / core figures
6) residual diagnostics + HC3 + bootstrap
7) manuscript headline-value verification
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.formula.api as smf
from scipy import stats
from statsmodels.stats.outliers_influence import variance_inflation_factor

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
INTERIM_DIR = PROJECT_ROOT / "03_Analysis" / "data" / "interim"
PROCESSED_DIR = PROJECT_ROOT / "03_Analysis" / "data" / "processed"
RESULTS_DIR = PROJECT_ROOT / "03_Analysis" / "results"
FIG_DIR = RESULTS_DIR / "figures"
STATS_DIR = PROJECT_ROOT / "results" / "statistics"

INPUT_NDB_FRACTURE = Path(
    "C:/Users/user/SharedWorkspace/projects/NDB_Research_Hub/02_Data/raw/NDB_OpenData/No.10/"
    "01_医科診療行為（算定回数）/01_公費レセプトを含まないデータ/K_手術/款別都道府県別算定回数.xlsx"
)
INPUT_NDB_WALKING = Path(
    "C:/Users/user/SharedWorkspace/projects/NDB_Research_Hub/02_Data/raw/NDB_OpenData/No.10/"
    "07_特定健診 質問票/01_公費レセプトを含まないデータ/"
    "標準的な質問票（質問項目１２） 都道府県別性年齢階級別分布.xlsx"
)
INPUT_SLOPE = STATS_DIR / "prefecture_habitable_slope.csv"

EXPECTED = {"n": 47, "mean_slope": 8.57, "mean_femur_rate": 254.0, "m1_beta": 5.65, "m2_beta": 3.49}
TOL = {"mean_slope": 0.02, "mean_femur_rate": 0.1, "m1_beta": 0.02, "m2_beta": 0.02}


def ensure_dirs() -> None:
    INTERIM_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)


def extract_fracture() -> pd.DataFrame:
    df = pd.read_excel(INPUT_NDB_FRACTURE, sheet_name="入院", header=None)
    target_codes = {
        150016710: ("femur", "K044_ClosedReduction"),
        150018310: ("femur", "K045_Percutaneous"),
        150019210: ("femur", "K046_ORIF"),
        150049510: ("femur", "K081_Hemiarthroplasty"),
        150050410: ("femur", "K082_THA"),
        150016610: ("humerus", "K044_ClosedReduction"),
        150018210: ("humerus", "K045_Percutaneous"),
        150019110: ("humerus", "K046_ORIF"),
        150049410: ("humerus", "K081_Hemiarthroplasty"),
        150050310: ("humerus", "K082_TSA"),
        150016810: ("forearm", "K044_ClosedReduction"),
        150018410: ("forearm", "K045_Percutaneous"),
        150019310: ("forearm", "K046_ORIF"),
    }
    pref_names = [
        "01_Hokkaido", "02_Aomori", "03_Iwate", "04_Miyagi", "05_Akita", "06_Yamagata", "07_Fukushima",
        "08_Ibaraki", "09_Tochigi", "10_Gunma", "11_Saitama", "12_Chiba", "13_Tokyo", "14_Kanagawa",
        "15_Niigata", "16_Toyama", "17_Ishikawa", "18_Fukui", "19_Yamanashi", "20_Nagano", "21_Gifu",
        "22_Shizuoka", "23_Aichi", "24_Mie", "25_Shiga", "26_Kyoto", "27_Osaka", "28_Hyogo", "29_Nara",
        "30_Wakayama", "31_Tottori", "32_Shimane", "33_Okayama", "34_Hiroshima", "35_Yamaguchi",
        "36_Tokushima", "37_Kagawa", "38_Ehime", "39_Kochi", "40_Fukuoka", "41_Saga", "42_Nagasaki",
        "43_Kumamoto", "44_Oita", "45_Miyazaki", "46_Kagoshima", "47_Okinawa",
    ]
    rows = []
    for _, row in df.iterrows():
        try:
            code = int(row[3])
        except Exception:
            continue
        if code not in target_codes:
            continue
        site, cat = target_codes[code]
        counts = row[7:54].values
        d = {"code": code, "site": site, "category": cat}
        for i, pref in enumerate(pref_names):
            v = counts[i]
            d[pref] = 0 if (pd.isna(v) or v == "-") else int(v)
        rows.append(d)
    out = pd.DataFrame(rows)
    out.to_csv(INTERIM_DIR / "fracture_surgery_site.csv", index=False, encoding="utf-8-sig")
    return out


def extract_walking() -> pd.DataFrame:
    df = pd.read_excel(INPUT_NDB_WALKING, header=None)
    records: list[dict[str, object]] = []
    current_pref: str | None = None
    cols = [7, 8, 15, 16]  # 65-69M,70-74M,65-69F,70-74F
    for i in range(5, len(df)):
        row = df.iloc[i]
        if pd.notna(row[0]):
            current_pref = str(row[0]).strip()
        if not current_pref or pd.isna(row[1]):
            continue
        cnt = 0
        for c in cols:
            v = row[c]
            if pd.isna(v) or str(v) == "-":
                v = 0
            try:
                cnt += int(v)
            except Exception:
                pass
        records.append({"prefecture": current_pref, "answer": str(row[1]).strip(), "count_65_74": cnt})
    tmp = pd.DataFrame(records)
    out = tmp.pivot_table(index="prefecture", columns="answer", values="count_65_74", aggfunc="sum").reset_index()
    if "はい" not in out.columns or "いいえ" not in out.columns:
        raise RuntimeError("walking_speed_q12 の「はい/いいえ」列を抽出できませんでした。")
    out["total"] = out["はい"] + out["いいえ"]
    out["fast_walking_rate"] = (out["はい"] / out["total"]) * 100.0
    out.to_csv(INTERIM_DIR / "walking_speed_q12.csv", index=False, encoding="utf-8-sig")
    return out


def census_manual() -> pd.DataFrame:
    df = pd.read_csv(INTERIM_DIR / "statistics_2020.csv") if (INTERIM_DIR / "statistics_2020.csv").exists() else None
    if df is not None and len(df) == 47:
        return df
    raise RuntimeError("statistics_2020.csv が見つからないため本線を継続できません。")


def integrate_dataset(fracture: pd.DataFrame, walking: pd.DataFrame, census: pd.DataFrame) -> pd.DataFrame:
    pref_map = {
        "01_Hokkaido": "北海道", "02_Aomori": "青森県", "03_Iwate": "岩手県", "04_Miyagi": "宮城県",
        "05_Akita": "秋田県", "06_Yamagata": "山形県", "07_Fukushima": "福島県", "08_Ibaraki": "茨城県",
        "09_Tochigi": "栃木県", "10_Gunma": "群馬県", "11_Saitama": "埼玉県", "12_Chiba": "千葉県",
        "13_Tokyo": "東京都", "14_Kanagawa": "神奈川県", "15_Niigata": "新潟県", "16_Toyama": "富山県",
        "17_Ishikawa": "石川県", "18_Fukui": "福井県", "19_Yamanashi": "山梨県", "20_Nagano": "長野県",
        "21_Gifu": "岐阜県", "22_Shizuoka": "静岡県", "23_Aichi": "愛知県", "24_Mie": "三重県",
        "25_Shiga": "滋賀県", "26_Kyoto": "京都府", "27_Osaka": "大阪府", "28_Hyogo": "兵庫県",
        "29_Nara": "奈良県", "30_Wakayama": "和歌山県", "31_Tottori": "鳥取県", "32_Shimane": "島根県",
        "33_Okayama": "岡山県", "34_Hiroshima": "広島県", "35_Yamaguchi": "山口県", "36_Tokushima": "徳島県",
        "37_Kagawa": "香川県", "38_Ehime": "愛媛県", "39_Kochi": "高知県", "40_Fukuoka": "福岡県",
        "41_Saga": "佐賀県", "42_Nagasaki": "長崎県", "43_Kumamoto": "熊本県", "44_Oita": "大分県",
        "45_Miyazaki": "宮崎県", "46_Kagoshima": "鹿児島県", "47_Okinawa": "沖縄県",
    }
    m = fracture.melt(id_vars=["code", "site", "category"], var_name="prefecture_code_name", value_name="count")
    m["prefecture"] = m["prefecture_code_name"].map(pref_map)
    agg = m.groupby("prefecture")["count"].sum().reset_index().rename(columns={"count": "total_fracture_count"})
    site = m.pivot_table(index="prefecture", columns="site", values="count", aggfunc="sum").reset_index()
    site.columns = ["prefecture", "femur_count", "forearm_count", "humerus_count"]
    merged = census.merge(agg, on="prefecture", how="left").merge(site, on="prefecture", how="left")
    merged = merged.merge(walking[["prefecture", "fast_walking_rate"]], on="prefecture", how="left")
    if not INPUT_SLOPE.exists():
        raise RuntimeError(f"傾斜ファイルが見つかりません: {INPUT_SLOPE}")
    slope = pd.read_csv(INPUT_SLOPE)
    merged = merged.merge(slope[["prefecture", "habitable_slope_weighted", "avg_slope_simple"]], on="prefecture", how="left")
    merged["fracture_rate"] = merged["total_fracture_count"] / merged["total_pop"] * 100000.0
    merged["femur_rate"] = merged["femur_count"] / merged["total_pop"] * 100000.0
    merged["humerus_rate"] = merged["humerus_count"] / merged["total_pop"] * 100000.0
    merged["forearm_rate"] = merged["forearm_count"] / merged["total_pop"] * 100000.0
    merged.to_csv(PROCESSED_DIR / "analysis_dataset_v1.csv", index=False, encoding="utf-8-sig")
    return merged


def run_statistics(df: pd.DataFrame) -> None:
    corr_cols = [
        "fracture_rate", "femur_rate", "humerus_rate", "forearm_rate",
        "habitable_slope_weighted", "aging_rate", "fast_walking_rate", "pop_density",
    ]
    df[corr_cols].corr().to_csv(RESULTS_DIR / "correlation_matrix.csv", encoding="utf-8-sig")

    plt.figure(figsize=(10, 8))
    sns.heatmap(df[corr_cols].corr(), annot=True, cmap="coolwarm", fmt=".2f", vmin=-1, vmax=1)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "heatmap_correlation.png", dpi=300)
    plt.close()

    m2 = smf.ols(
        "femur_rate ~ habitable_slope_weighted + aging_rate + fast_walking_rate + pop_density",
        data=df,
    ).fit()
    m2_hc3 = smf.ols(
        "femur_rate ~ habitable_slope_weighted + aging_rate + fast_walking_rate + pop_density",
        data=df,
    ).fit(cov_type="HC3")

    vif_cols = ["habitable_slope_weighted", "aging_rate", "fast_walking_rate", "pop_density"]
    x = df[vif_cols].copy()
    x["const"] = 1.0
    vif_rows = []
    for i, c in enumerate(x.columns):
        if c == "const":
            continue
        v = float(variance_inflation_factor(x.values, i))
        vif_rows.append(
            {
                "variable": c,
                "vif": v,
                "flag_ge_5": bool(v >= 5.0),
                "flag_ge_10": bool(v >= 10.0),
            }
        )
    vif_df = pd.DataFrame(vif_rows).sort_values("vif", ascending=False)
    vif_df.to_csv(RESULTS_DIR / "multicollinearity_vif.csv", index=False, encoding="utf-8-sig")
    vif_lines = [
        "Multicollinearity check (VIF)",
        "=============================",
        "Rule-of-thumb thresholds: VIF >= 5 (moderate), VIF >= 10 (high)",
        "",
        vif_df.to_string(index=False),
    ]
    (RESULTS_DIR / "multicollinearity_vif_report.txt").write_text("\n".join(vif_lines) + "\n", encoding="utf-8")

    lines = [m2.summary().as_text(), "", "HC3", m2_hc3.summary().as_text()]
    (RESULTS_DIR / "regression_results.txt").write_text("\n".join(lines), encoding="utf-8")

    resid = m2.resid
    fitted = m2.fittedvalues
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].scatter(fitted, resid, alpha=0.75, edgecolors="k", linewidths=0.3)
    axes[0].axhline(0, color="gray", linestyle="--", linewidth=1)
    stats.probplot(resid, dist="norm", plot=axes[1])
    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig_residual_diagnostics_hip_m2.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    rng = np.random.default_rng(42)
    coefs = []
    for _ in range(5000):
        idx = rng.integers(0, len(df), size=len(df))
        sub = df.iloc[idx]
        coefs.append(
            smf.ols(
                "femur_rate ~ habitable_slope_weighted + aging_rate + fast_walking_rate + pop_density",
                data=sub,
            ).fit().params["habitable_slope_weighted"]
        )
    lo, hi = np.percentile(np.asarray(coefs, dtype=float), [2.5, 97.5])
    report = (
        f"Shapiro-Wilk p={stats.shapiro(resid.values).pvalue:.4f}\n"
        f"Bootstrap 95% CI slope=[{lo:.4f}, {hi:.4f}]\n"
        f"HC3 CI slope={tuple(m2_hc3.conf_int().loc['habitable_slope_weighted'].tolist())}\n"
    )
    (RESULTS_DIR / "regression_diagnostics_report.txt").write_text(report, encoding="utf-8")


def verify_headline(df: pd.DataFrame) -> None:
    m1 = smf.ols("femur_rate ~ habitable_slope_weighted", data=df).fit()
    m2 = smf.ols("femur_rate ~ habitable_slope_weighted + aging_rate + fast_walking_rate + pop_density", data=df).fit()
    observed = {
        "n": int(len(df)),
        "mean_slope": float(df["habitable_slope_weighted"].mean()),
        "mean_femur_rate": float(df["femur_rate"].mean()),
        "m1_beta": float(m1.params["habitable_slope_weighted"]),
        "m2_beta": float(m2.params["habitable_slope_weighted"]),
    }
    if observed["n"] != EXPECTED["n"]:
        raise RuntimeError(f"N mismatch: {observed['n']} != {EXPECTED['n']}")
    for k in ("mean_slope", "mean_femur_rate", "m1_beta", "m2_beta"):
        if abs(observed[k] - EXPECTED[k]) > TOL[k]:
            raise RuntimeError(f"{k} mismatch: observed={observed[k]:.4f}, expected={EXPECTED[k]:.4f}, tol={TOL[k]}")
    print("[OK] headline values validated")


def main() -> int:
    ensure_dirs()
    fracture = extract_fracture()
    walking = extract_walking()
    census = census_manual()
    df = integrate_dataset(fracture, walking, census)
    run_statistics(df)
    verify_headline(df)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
