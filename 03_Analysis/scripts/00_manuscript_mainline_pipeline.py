# pyright: reportGeneralTypeIssues=false, reportAttributeAccessIssue=false, reportArgumentType=false, reportCallIssue=false, reportOperatorIssue=false, reportIndexIssue=false, reportReturnType=false

"""
00_manuscript_mainline_pipeline.py
--------------------------------
Purpose (plain language)
    Rebuild the entire prefecture-level analysis for the manuscript from
    official open data: fracture surgery counts and health-checkup walking
    data (NDB), population statistics (census), and precomputed terrain slope.

What this script does (step by step)
    1. Extract hip / upper-arm / forearm surgery counts per prefecture from NDB Excel.
    2. Extract the proportion reporting “fast walking” from the Specific Health Checkup file.
    3. Load 2020 census-based population, aging rate, and density (47 rows).
    4. Merge all sources with habitable-area-weighted mean slope (degrees).
    5. Compute surgery rates per 100,000 population per year.
    6. Run correlation heatmap and linear regression (Models 1–2 for hip rate).
    7. Run residual checks, robust standard errors (HC3), and bootstrap resampling.
    8. Verify that key numbers match the published Abstract (8.57°, 254, β values).

Requirements
    - Copy ``config/config.yaml.example`` to ``config/config.local.yaml`` and set paths
      to your NDB Excel files, census CSV, and terrain slope CSV (see DATA_SOURCES.md).
    - Python packages in ``requirements.txt`` (install in a virtual environment).

Output folders
    - ``03_Analysis/data/interim/`` — intermediate tables
    - ``03_Analysis/data/processed/analysis_dataset_v1.csv`` — final 47-row dataset
    - ``03_Analysis/results/`` — regression text, diagnostics, figures

Note for GitHub readers
    For a quick check without NDB downloads, use ``reproduce_from_release.py`` instead.
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

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))
from _utils import configure_stdout_utf8, load_project_paths  # noqa: E402

configure_stdout_utf8()

PROJECT_ROOT = Path(__file__).resolve().parents[2]
_CFG = load_project_paths(PROJECT_ROOT)

INTERIM_DIR = _CFG.interim_dir
PROCESSED_DIR = _CFG.processed_dir
RESULTS_DIR = _CFG.results_dir
FIG_DIR = RESULTS_DIR / "figures"

INPUT_NDB_FRACTURE = _CFG.ndb_fracture_xlsx
INPUT_NDB_WALKING = _CFG.ndb_walking_xlsx
INPUT_SLOPE = _CFG.habitable_slope_csv
CENSUS_CSV = _CFG.census_csv
BOOTSTRAP_REPLICATES = _CFG.bootstrap_replicates
RANDOM_SEED = _CFG.random_seed

EXPECTED = {"n": 47, "mean_slope": 8.57, "mean_femur_rate": 254.0, "m1_beta": 5.65, "m2_beta": 3.49}
TOL = {"mean_slope": 0.02, "mean_femur_rate": 0.1, "m1_beta": 0.02, "m2_beta": 0.02}


def ensure_dirs() -> None:
    """Create output folders if they do not exist."""
    INTERIM_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)


def extract_fracture() -> pd.DataFrame:
    """
    Read NDB inpatient surgery counts by procedure code and prefecture.
    Keeps hip (femur), humerus, and forearm fracture-related procedures only.
    """
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
    """
    Read Specific Health Checkup Q12 (self-reported fast walking: yes/no).
    Aggregates ages 65–74 by prefecture and computes percent answering “yes”.
    """
    df = pd.read_excel(INPUT_NDB_WALKING, header=None)
    records: list[dict[str, object]] = []
    current_pref: str | None = None
    # Excel columns for 65–69 and 70–74, male and female counts
    cols = [7, 8, 15, 16]
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
        raise RuntimeError(
            "Could not find yes/no answer columns for fast-walking (Q12) in NDB Excel."
        )
    out["total"] = out["はい"] + out["いいえ"]
    out["fast_walking_rate"] = (out["はい"] / out["total"]) * 100.0
    out.to_csv(INTERIM_DIR / "walking_speed_q12.csv", index=False, encoding="utf-8-sig")
    return out


def census_manual() -> pd.DataFrame:
    """Load 47-prefecture population and covariates from a pre-built census merge file."""
    census_path = CENSUS_CSV
    df = pd.read_csv(census_path) if census_path.exists() else None
    if df is not None and len(df) == 47:
        return df
    raise RuntimeError(
        f"Missing or invalid {census_path} (need exactly 47 prefecture rows)."
    )


def integrate_dataset(fracture: pd.DataFrame, walking: pd.DataFrame, census: pd.DataFrame) -> pd.DataFrame:
    """
    Merge fracture counts, walking rate, census, and terrain slope by prefecture.
    Computes surgery rates per 100,000 population per year for each body site.
    """
    # Map NDB English prefecture codes to Japanese names used in other files
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
        raise RuntimeError(f"Terrain slope file not found: {INPUT_SLOPE}")
    slope = pd.read_csv(INPUT_SLOPE)
    merged = merged.merge(slope[["prefecture", "habitable_slope_weighted", "avg_slope_simple"]], on="prefecture", how="left")
    merged["fracture_rate"] = merged["total_fracture_count"] / merged["total_pop"] * 100000.0
    merged["femur_rate"] = merged["femur_count"] / merged["total_pop"] * 100000.0
    merged["humerus_rate"] = merged["humerus_count"] / merged["total_pop"] * 100000.0
    merged["forearm_rate"] = merged["forearm_count"] / merged["total_pop"] * 100000.0
    merged.to_csv(PROCESSED_DIR / "analysis_dataset_v1.csv", index=False, encoding="utf-8-sig")
    return merged


def run_statistics(df: pd.DataFrame) -> None:
    """
    Correlation matrix, hip-fracture regression (Model 2), residual plots,
    HC3 robust SE, and bootstrap confidence interval for the slope coefficient.
    """
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

    rng = np.random.default_rng(RANDOM_SEED)
    coefs = []
    for _ in range(BOOTSTRAP_REPLICATES):
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
    """Stop with an error if recomputed values differ from the manuscript Abstract."""
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
    print("[OK] Headline values match the manuscript Abstract.")


def main() -> int:
    """Run the full manuscript analysis pipeline end to end."""
    print("Step 0: Preparing output directories...")
    ensure_dirs()

    print("Step 1: Extracting fracture surgery counts from NDB Open Data...")
    fracture = extract_fracture()

    print("Step 2: Extracting fast-walking proportion from Specific Health Checkup...")
    walking = extract_walking()

    print("Step 3: Loading census-based population and covariates (47 prefectures)...")
    census = census_manual()

    print("Step 4: Merging sources and computing surgery rates per 100,000...")
    df = integrate_dataset(fracture, walking, census)

    print("Step 5: Running regressions, diagnostics, and saving figures...")
    run_statistics(df)

    print("Step 6: Verifying headline statistics reported in the Abstract...")
    verify_headline(df)

    print("Pipeline finished successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
