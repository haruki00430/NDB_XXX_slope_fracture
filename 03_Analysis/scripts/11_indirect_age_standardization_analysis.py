# pyright: reportGeneralTypeIssues=false, reportAttributeAccessIssue=false, reportArgumentType=false, reportCallIssue=false, reportOperatorIssue=false, reportIndexIssue=false, reportReturnType=false

import re
from pathlib import Path

import pandas as pd
import requests
import statsmodels.formula.api as smf


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ANALYSIS_DATA_PATH = PROJECT_ROOT / "03_Analysis" / "data" / "processed" / "analysis_dataset_v1.csv"
SURGERY_AGE_PATH = (
    Path("C:/Users/user/SharedWorkspace/projects/NDB_Research_Hub/02_Data/raw/NDB_OpenData/No.10")
    / "01_医科診療行為（算定回数）"
    / "01_公費レセプトを含まないデータ"
    / "K_手術"
    / "款別性年齢別算定回数.xlsx"
)
OUT_DIR = PROJECT_ROOT / "03_Analysis" / "results"
OUT_CSV = OUT_DIR / "age_standardized_indirect_results.csv"
OUT_TXT = OUT_DIR / "age_standardized_indirect_regression.txt"

ESTAT_APP_ID = "8ee5a987b9ec70631de1977bde3afd7ebc11140d"
ESTAT_STATS_DATA_ID = "0003448237"

# 現行原稿でfemur outcomeに含めている手術コード群
FEMUR_CODES = {"150016710", "150018310", "150019210", "150049510", "150050410"}
META_COL_LEVEL0 = {"��", "����\n�R�[�h", "���ޖ���", "�f�Ís��\n�R�[�h", "�f�Ís��", "�_��", "���v\n(�Z���)"}


def age_key_from_label(label: str) -> str | None:
    text = str(label)
    nums = re.findall(r"\d+", text)
    if not nums:
        return None
    if len(nums) >= 2:
        return f"{int(nums[0])}-{int(nums[1])}"
    if len(nums) == 1:
        if "以" in text or "�ȏ�" in text:
            return f"{int(nums[0])}+"
        return f"{int(nums[0])}"
    return None


def load_national_femur_counts_by_age() -> pd.Series:
    df = pd.read_excel(SURGERY_AGE_PATH, header=[2, 3])

    # 4列目が手術コード列（既存スクリプト群の前提と整合）
    code_col = df.columns[3]
    df[code_col] = pd.to_numeric(df[code_col], errors="coerce").astype("Int64").astype(str).str.strip()
    df_target = df[df[code_col].isin(FEMUR_CODES)].copy()
    if df_target.empty:
        raise RuntimeError("femur対象コードが性年齢別算定回数ファイルから抽出できませんでした。")

    # 列構造が固定（7-25: 男0-4..90+, 26-44: 女0-4..90+）なので位置で厳密抽出
    age_cols = df.columns[7:45]
    if len(age_cols) != 38:
        raise RuntimeError("性年齢別列の列数が想定と一致しませんでした。")

    age_totals: dict[str, float] = {}
    for col in age_cols:
        age_key = age_key_from_label(col[1])
        if age_key is None:
            continue
        vals = pd.to_numeric(df_target[col], errors="coerce").fillna(0.0)
        age_totals[age_key] = age_totals.get(age_key, 0.0) + float(vals.sum())

    out = pd.Series(age_totals, dtype=float).sort_index()
    out = out[out > 0]
    if out.empty:
        raise RuntimeError("年齢階級別femur算定回数が作成できませんでした。")
    return out


def fetch_estat_population_by_age() -> pd.DataFrame:
    url = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"
    params = {
        "appId": ESTAT_APP_ID,
        "statsDataId": ESTAT_STATS_DATA_ID,
        "cdCat01": "000",  # 男女計
        "cdCat03": "001",  # 総人口
        "cdTime": "1601",  # 2020-10-01
    }
    r = requests.get(url, params=params, timeout=60)
    r.raise_for_status()
    obj = r.json()["GET_STATS_DATA"]["STATISTICAL_DATA"]

    class_obj = obj["CLASS_INF"]["CLASS_OBJ"]
    cat02_map = {c["@code"]: c["@name"] for c in class_obj if c["@id"] == "cat02" for c in c["CLASS"]}
    area_map = {c["@code"]: c["@name"] for c in class_obj if c["@id"] == "area" for c in c["CLASS"]}
    values = obj["DATA_INF"]["VALUE"]
    if isinstance(values, dict):
        values = [values]

    rows = []
    for v in values:
        age_name = cat02_map.get(v.get("@cat02"), "")
        age_key = age_key_from_label(age_name)
        if age_key is None:
            continue
        area_code = v.get("@area")
        area_name = area_map.get(area_code, "")
        if area_code is None:
            continue
        try:
            pop = float(str(v.get("$", "0")).replace(",", ""))
        except ValueError:
            continue
        rows.append({"area_code": area_code, "area_name": area_name, "age_key": age_key, "population": pop})

    df = pd.DataFrame(rows)
    if df.empty:
        raise RuntimeError("e-Stat人口データの取得・整形に失敗しました。")
    # e-Stat人口は「千人」単位で返る表があるため、桁を実人口に補正
    # 2020年全国人口は約1.26億人であり、12万台なら千人単位と判断する。
    nat_total_like = (
        df[(df["area_code"] == "00000") & (df["age_key"] == "0-4")]["population"].sum()
    )
    if nat_total_like < 10000:
        df["population"] = df["population"] * 1000.0
    return df


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    df_main = pd.read_csv(ANALYSIS_DATA_PATH)
    national_counts = load_national_femur_counts_by_age()
    df_pop = fetch_estat_population_by_age()

    # 全国（area 00000）人口
    nat_pop = (
        df_pop[df_pop["area_code"] == "00000"]
        .groupby("age_key", as_index=True)["population"]
        .sum()
    )
    common_ages = sorted(set(national_counts.index) & set(nat_pop.index))
    if not common_ages:
        raise RuntimeError("femur年齢階級と国勢調査年齢階級の共通集合がありません。")

    rates = (national_counts[common_ages] / nat_pop[common_ages]).rename("national_rate")

    # 都道府県コード 01000..47000
    df_pref_pop = df_pop[df_pop["area_code"].str.match(r"^\d{2}000$")].copy()
    df_pref_pop = df_pref_pop[df_pref_pop["age_key"].isin(common_ages)]

    # 期待値（間接法）
    df_pref_pop = df_pref_pop.merge(rates.rename("rate"), left_on="age_key", right_index=True, how="left")
    df_pref_pop["expected_component"] = df_pref_pop["population"] * df_pref_pop["rate"]
    expected = df_pref_pop.groupby("area_name", as_index=True)["expected_component"].sum().rename("expected_femur_count")

    # 全国粗率（per 100,000）
    nat_total_count = national_counts[common_ages].sum()
    nat_total_pop = nat_pop[common_ages].sum()
    nat_crude_rate = (nat_total_count / nat_total_pop) * 100000.0

    # 都道府県名の表記ゆれを吸収（都/道/府/県付き）
    area_names = expected.index.to_series()
    area_base = area_names.str.replace("都|道|府|県", "", regex=True)
    expected_df = pd.DataFrame(
        {"pref_base": area_base.values, "expected_femur_count": expected.values},
        index=expected.index,
    ).reset_index().rename(columns={"index": "area_name"})

    main_df = df_main.copy()
    main_df["pref_base"] = main_df["prefecture"].astype(str).str.replace("都|道|府|県", "", regex=True)
    merged = main_df.merge(expected_df[["pref_base", "expected_femur_count"]], on="pref_base", how="left")

    if merged["expected_femur_count"].isna().any():
        missing = merged.loc[merged["expected_femur_count"].isna(), "prefecture"].tolist()
        raise RuntimeError(f"期待値が結合できない都道府県があります: {missing}")

    merged["sir_femur"] = merged["femur_count"] / merged["expected_femur_count"]
    merged["isr_femur_per100k"] = merged["sir_femur"] * nat_crude_rate

    # 再解析: 年齢標準化アウトカムを目的変数に回帰
    m1 = smf.ols("isr_femur_per100k ~ habitable_slope_weighted", data=merged).fit()
    m2 = smf.ols(
        "isr_femur_per100k ~ habitable_slope_weighted + fast_walking_rate + pop_density + aging_rate",
        data=merged,
    ).fit()

    merged.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")

    with open(OUT_TXT, "w", encoding="utf-8") as f:
        f.write("Indirect age-standardization analysis (femur surgery outcome)\n")
        f.write("================================================================\n")
        f.write(f"Common age groups: {', '.join(common_ages)}\n")
        f.write(f"National crude femur surgery rate (/100,000): {nat_crude_rate:.4f}\n\n")
        f.write("Model A: isr_femur_per100k ~ habitable_slope_weighted\n")
        f.write(m1.summary().as_text())
        f.write("\n\n")
        f.write("Model B: isr_femur_per100k ~ habitable_slope_weighted + fast_walking_rate + pop_density + aging_rate\n")
        f.write(m2.summary().as_text())
        f.write("\n")

    print(f"[OK] saved: {OUT_CSV}")
    print(f"[OK] saved: {OUT_TXT}")
    print(f"[Model A slope beta] {m1.params['habitable_slope_weighted']:.4f}, p={m1.pvalues['habitable_slope_weighted']:.4f}")
    print(f"[Model B slope beta] {m2.params['habitable_slope_weighted']:.4f}, p={m2.pvalues['habitable_slope_weighted']:.4f}")


if __name__ == "__main__":
    main()
