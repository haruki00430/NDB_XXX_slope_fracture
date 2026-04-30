# pyright: reportGeneralTypeIssues=false, reportAttributeAccessIssue=false, reportArgumentType=false, reportCallIssue=false, reportOperatorIssue=false, reportIndexIssue=false, reportReturnType=false

"""
Masking-imputation sensitivity analysis for indirect standardization (SIR/ISR).

Policy:
- Keep primary manuscript analysis unchanged.
- Run separated sensitivity scenarios for masked "-" cells in age-stratified NDB table.
  - Scenario A: "-" -> 0
  - Scenario B: "-" -> 5
  - Scenario C: "-" -> 9

Outputs:
- 03_Analysis/results/sir_masking_sensitivity_prefecture.csv
- 03_Analysis/results/sir_masking_sensitivity_summary.csv
- 03_Analysis/results/sir_masking_sensitivity_report.txt
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd
import requests
import statsmodels.formula.api as smf


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RESULTS_DIR = PROJECT_ROOT / "03_Analysis" / "results"
ANALYSIS_DATA = PROJECT_ROOT / "03_Analysis" / "data" / "processed" / "analysis_dataset_v1.csv"

SEX_AGE_SURGERY_XLSX = Path(
    "C:/Users/user/SharedWorkspace/projects/NDB_Research_Hub/02_Data/raw/NDB_OpenData/No.10/"
    "01_医科診療行為（算定回数）/01_公費レセプトを含まないデータ/K_手術/款別性年齢別算定回数.xlsx"
)

ESTAT_APP_ID = "8ee5a987b9ec70631de1977bde3afd7ebc11140d"
ESTAT_STATS_DATA_ID = "0003448237"  # prefecture x 5-year age population

FEMUR_CODES = [150016710, 150018310, 150019210, 150049510, 150050410]
SCENARIOS = {"A_mask0": 0.0, "B_mask5": 5.0, "C_mask9": 9.0}


def age_key(label: str) -> str | None:
    nums = re.findall(r"\d+", str(label))
    if not nums:
        return None
    if len(nums) >= 2:
        return f"{int(nums[0])}-{int(nums[1])}"
    if "以" in str(label) or "�ȏ�" in str(label):
        return f"{int(nums[0])}+"
    return str(int(nums[0]))


def load_prefecture_covariates() -> pd.DataFrame:
    df = pd.read_csv(ANALYSIS_DATA)
    cols = [
        "prefecture",
        "femur_count",
        "habitable_slope_weighted",
        "aging_rate",
        "fast_walking_rate",
        "pop_density",
    ]
    return df[cols].copy()


def load_age_stratified_femur_table() -> tuple[pd.DataFrame, list]:
    df = pd.read_excel(SEX_AGE_SURGERY_XLSX, header=[2, 3])
    code_col = df.columns[3]
    total_col = df.columns[6]
    age_cols = list(df.columns[7:45])  # male 19 + female 19

    df[code_col] = pd.to_numeric(df[code_col], errors="coerce")
    fem = df[df[code_col].isin(FEMUR_CODES)].copy()
    if fem.empty:
        raise RuntimeError("No femur rows found in sex-age surgery table.")

    # Keep only required columns
    use_cols = [code_col, total_col] + age_cols
    fem = fem[use_cols].copy()
    return fem, age_cols


def fetch_estat_population() -> pd.DataFrame:
    params = {
        "appId": ESTAT_APP_ID,
        "statsDataId": ESTAT_STATS_DATA_ID,
        "cdCat01": "000",  # total sex
        "cdCat03": "001",  # total population
        "cdTime": "1601",  # 2020-10-01
    }
    url = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"
    res = requests.get(url, params=params, timeout=60)
    res.raise_for_status()
    body = res.json()["GET_STATS_DATA"]["STATISTICAL_DATA"]

    class_obj = body["CLASS_INF"]["CLASS_OBJ"]
    cat02 = {x["@code"]: x["@name"] for c in class_obj if c["@id"] == "cat02" for x in c["CLASS"]}
    area = {x["@code"]: x["@name"] for c in class_obj if c["@id"] == "area" for x in c["CLASS"]}

    vals = body["DATA_INF"]["VALUE"]
    if isinstance(vals, dict):
        vals = [vals]

    rows: list[dict[str, object]] = []
    for v in vals:
        a = v.get("@area")
        c2 = v.get("@cat02")
        if a is None or c2 is None:
            continue
        akey = age_key(cat02.get(c2, ""))
        if akey is None:
            continue
        try:
            pop = float(str(v.get("$", "0")).replace(",", ""))
        except Exception:
            continue
        rows.append({"area_code": a, "prefecture": area.get(a, ""), "age_key": akey, "population": pop})

    df = pd.DataFrame(rows)
    # API table values are in thousand persons. Convert to persons.
    if not df.empty and df[(df["area_code"] == "00000") & (df["age_key"] == "0-4")]["population"].sum() < 10000:
        df["population"] = df["population"] * 1000.0
    return df


def national_age_counts_by_scenario(fem: pd.DataFrame, age_cols: list, mask_fill: float) -> pd.Series:
    counts: dict[str, float] = {}
    for col in age_cols:
        k = age_key(col[1])
        if k is None:
            continue
        s = fem[col].copy()
        # Masked "-" cells are replaced by scenario-specific dummy values
        s = pd.to_numeric(s.replace("-", mask_fill), errors="coerce").fillna(mask_fill)
        counts[k] = counts.get(k, 0.0) + float(s.sum())
    out = pd.Series(counts, dtype=float)
    out = out[out > 0]
    return out


def run_scenario(
    name: str,
    mask_fill: float,
    fem: pd.DataFrame,
    age_cols: list,
    pop_df: pd.DataFrame,
    covar_df: pd.DataFrame,
) -> tuple[pd.DataFrame, dict[str, object]]:
    nat_counts = national_age_counts_by_scenario(fem, age_cols, mask_fill)
    nat_pop = pop_df[pop_df["area_code"] == "00000"].groupby("age_key")["population"].sum()

    common = sorted(set(nat_counts.index) & set(nat_pop.index))
    nat_counts = nat_counts[common]
    nat_pop = nat_pop[common]
    rates = nat_counts / nat_pop
    nat_crude = float(nat_counts.sum() / nat_pop.sum() * 100000.0)

    pref_pop = pop_df[pop_df["area_code"].str.match(r"^\d{2}000$")].copy()
    pref_pop = pref_pop[pref_pop["age_key"].isin(common)]
    pref_pop = pref_pop.merge(rates.rename("rate"), left_on="age_key", right_index=True, how="left")
    pref_pop["exp_comp"] = pref_pop["population"] * pref_pop["rate"]
    expected = pref_pop.groupby("prefecture", as_index=False)["exp_comp"].sum().rename(columns={"exp_comp": "expected"})

    data = covar_df.merge(expected, on="prefecture", how="left")
    if data["expected"].isna().any():
        miss = data.loc[data["expected"].isna(), "prefecture"].tolist()
        raise RuntimeError(f"Scenario {name}: missing expected counts for {miss}")

    data["sir"] = data["femur_count"] / data["expected"]
    data["isr_per100k"] = data["sir"] * nat_crude
    data["scenario"] = name

    m1 = smf.ols("isr_per100k ~ habitable_slope_weighted", data=data).fit()
    m2 = smf.ols(
        "isr_per100k ~ habitable_slope_weighted + aging_rate + fast_walking_rate + pop_density",
        data=data,
    ).fit()
    ci1 = m1.conf_int().loc["habitable_slope_weighted"].tolist()
    ci2 = m2.conf_int().loc["habitable_slope_weighted"].tolist()

    summary = {
        "scenario": name,
        "mask_fill": mask_fill,
        "age_groups_used": ",".join(common),
        "nat_crude_per100k": nat_crude,
        "beta_m1": float(m1.params["habitable_slope_weighted"]),
        "ci_low_m1": float(ci1[0]),
        "ci_high_m1": float(ci1[1]),
        "p_m1": float(m1.pvalues["habitable_slope_weighted"]),
        "beta_m2": float(m2.params["habitable_slope_weighted"]),
        "ci_low_m2": float(ci2[0]),
        "ci_high_m2": float(ci2[1]),
        "p_m2": float(m2.pvalues["habitable_slope_weighted"]),
    }
    return data, summary


def main() -> int:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    covar = load_prefecture_covariates()
    fem, age_cols = load_age_stratified_femur_table()
    pop = fetch_estat_population()

    all_pref = []
    summaries = []
    for s_name, fill in SCENARIOS.items():
        pref_df, sm = run_scenario(s_name, fill, fem, age_cols, pop, covar)
        all_pref.append(pref_df)
        summaries.append(sm)

    out_pref = pd.concat(all_pref, ignore_index=True)
    out_sum = pd.DataFrame(summaries)
    out_pref.to_csv(RESULTS_DIR / "sir_masking_sensitivity_prefecture.csv", index=False, encoding="utf-8-sig")
    out_sum.to_csv(RESULTS_DIR / "sir_masking_sensitivity_summary.csv", index=False, encoding="utf-8-sig")

    # Stability check (sign + magnitude range)
    b = out_sum["beta_m2"]
    same_sign = bool((b > 0).all() or (b < 0).all())
    b_ratio = float(b.max() / b.min()) if (b.min() != 0) else float("nan")

    lines = [
        "SIR masking-imputation sensitivity analysis",
        "=========================================",
        "Main analysis remains unchanged; this is sensitivity-only.",
        "",
        "Scenarios:",
        "  A: '-' = 0",
        "  B: '-' = 5",
        "  C: '-' = 9",
        "",
        "Model for comparison (primary): isr_per100k ~ slope + aging + fast_walking + pop_density",
        "",
        out_sum[
            ["scenario", "mask_fill", "beta_m2", "ci_low_m2", "ci_high_m2", "p_m2"]
        ].to_string(index=False),
        "",
        f"Sign stability (beta_m2): {same_sign}",
        f"Magnitude ratio max/min (beta_m2): {b_ratio:.4f}",
        "",
        "Note on chained masking:",
        "  Public NDB masking rule can include secondary masking;",
        "  therefore A/B/C should be interpreted as pragmatic sensitivity bounds,",
        "  not exact reconstruction of hidden cells.",
    ]
    (RESULTS_DIR / "sir_masking_sensitivity_report.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("[OK] generated: sir_masking_sensitivity_prefecture.csv")
    print("[OK] generated: sir_masking_sensitivity_summary.csv")
    print("[OK] generated: sir_masking_sensitivity_report.txt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
