"""
追加感度分析: 自動車関連指標を用いた都道府県レベル回帰の頑健性確認。

前提:
- 既存の主解析データ: analysis_dataset_v1.csv
- 追加データ(任意): car_mobility_prefecture.csv

追加データが未配置でも本スクリプトは失敗せず、必要項目を結果ディレクトリへ出力する。
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd
import statsmodels.formula.api as smf


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASET_PATH = PROJECT_ROOT / "03_Analysis" / "data" / "processed" / "analysis_dataset_v1.csv"
CAR_DATA_PATH = PROJECT_ROOT / "03_Analysis" / "data" / "interim" / "car_mobility_prefecture.csv"
RESULTS_DIR = PROJECT_ROOT / "03_Analysis" / "results"

STATUS_MD = RESULTS_DIR / "car_mobility_sensitivity_status.md"
AVAILABILITY_CSV = RESULTS_DIR / "car_mobility_data_availability.csv"
TEMPLATE_CSV = RESULTS_DIR / "car_mobility_input_template.csv"
MODEL_SUMMARY_CSV = RESULTS_DIR / "car_mobility_sensitivity_models.csv"
JOINED_DATA_CSV = RESULTS_DIR / "car_mobility_sensitivity_prefecture.csv"


REQUIRED_COLS = ["prefecture", "car_ownership_rate"]
OPTIONAL_COLS = ["private_car_commute_rate", "avg_steps_per_day"]


@dataclass
class ModelResult:
    model_name: str
    n: int
    beta_slope: float
    ci_low_slope: float
    ci_high_slope: float
    p_slope: float
    r2: float
    adj_r2: float


def _build_template() -> pd.DataFrame:
    """47都道府県テンプレートを作成する。"""
    base = pd.read_csv(DATASET_PATH, usecols=["prefecture"]).copy()
    base["car_ownership_rate"] = pd.NA
    base["private_car_commute_rate"] = pd.NA
    base["avg_steps_per_day"] = pd.NA
    return base


def _normalize_prefecture(s: pd.Series) -> pd.Series:
    """都道府県名の軽微な表記差を吸収する。"""
    return (
        s.astype(str)
        .str.strip()
        .str.replace("都|道|府|県", "", regex=True)
    )


def _availability_rows(car_df: pd.DataFrame | None) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    candidates: Iterable[str] = REQUIRED_COLS + OPTIONAL_COLS
    for col in candidates:
        exists = car_df is not None and col in car_df.columns
        non_null = int(car_df[col].notna().sum()) if exists else 0
        rows.append(
            {
                "variable": col,
                "required": col in REQUIRED_COLS,
                "exists_in_input": bool(exists),
                "non_null_rows": non_null,
            }
        )
    return rows


def _fit_model(df: pd.DataFrame, formula: str, model_name: str) -> ModelResult:
    model = smf.ols(formula, data=df).fit()
    ci = model.conf_int().loc["habitable_slope_weighted"].tolist()
    return ModelResult(
        model_name=model_name,
        n=int(model.nobs),
        beta_slope=float(model.params["habitable_slope_weighted"]),
        ci_low_slope=float(ci[0]),
        ci_high_slope=float(ci[1]),
        p_slope=float(model.pvalues["habitable_slope_weighted"]),
        r2=float(model.rsquared),
        adj_r2=float(model.rsquared_adj),
    )


def main() -> int:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # 追加データテンプレートを常に出力し、取得・整形作業の受け皿を固定する。
    template = _build_template()
    template.to_csv(TEMPLATE_CSV, index=False, encoding="utf-8-sig")

    base = pd.read_csv(DATASET_PATH).copy()
    base["pref_key"] = _normalize_prefecture(base["prefecture"])

    if not CAR_DATA_PATH.exists():
        availability = pd.DataFrame(_availability_rows(None))
        availability.to_csv(AVAILABILITY_CSV, index=False, encoding="utf-8-sig")
        STATUS_MD.write_text(
            "\n".join(
                [
                    "# Car Mobility Sensitivity: Status",
                    "",
                    "- status: waiting_for_additional_data",
                    f"- missing_file: `{CAR_DATA_PATH}`",
                    "- required_columns: prefecture, car_ownership_rate",
                    "- optional_columns: private_car_commute_rate, avg_steps_per_day",
                    f"- generated_template: `{TEMPLATE_CSV}`",
                    "",
                    "次アクション: テンプレートに都道府県別の自動車関連指標を入力し、"
                    "同パスへ `car_mobility_prefecture.csv` として保存して再実行する。",
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        print(f"[WAIT] missing input: {CAR_DATA_PATH}")
        print(f"[OK] generated: {STATUS_MD}")
        print(f"[OK] generated: {AVAILABILITY_CSV}")
        print(f"[OK] generated: {TEMPLATE_CSV}")
        return 0

    car = pd.read_csv(CAR_DATA_PATH).copy()
    availability = pd.DataFrame(_availability_rows(car))
    availability.to_csv(AVAILABILITY_CSV, index=False, encoding="utf-8-sig")

    missing_required = [c for c in REQUIRED_COLS if c not in car.columns]
    if missing_required:
        STATUS_MD.write_text(
            "\n".join(
                [
                    "# Car Mobility Sensitivity: Status",
                    "",
                    "- status: invalid_input_columns",
                    f"- missing_required_columns: {', '.join(missing_required)}",
                    f"- checked_file: `{CAR_DATA_PATH}`",
                    f"- template: `{TEMPLATE_CSV}`",
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        print(f"[ERROR] required columns missing: {missing_required}")
        print(f"[OK] generated: {STATUS_MD}")
        return 1

    car["pref_key"] = _normalize_prefecture(car["prefecture"])
    merged = base.merge(
        car.drop(columns=["prefecture"], errors="ignore"),
        on="pref_key",
        how="left",
    )

    # 主解析の共変量 + 自動車関連指標。
    core = [
        "femur_rate",
        "habitable_slope_weighted",
        "aging_rate",
        "fast_walking_rate",
        "pop_density",
        "car_ownership_rate",
    ]
    run_df = merged.dropna(subset=core).copy()
    run_df.to_csv(JOINED_DATA_CSV, index=False, encoding="utf-8-sig")

    results: list[ModelResult] = []
    results.append(
        _fit_model(
            run_df,
            "femur_rate ~ habitable_slope_weighted + aging_rate + fast_walking_rate + pop_density",
            "baseline_model2",
        )
    )
    results.append(
        _fit_model(
            run_df,
            "femur_rate ~ habitable_slope_weighted + aging_rate + fast_walking_rate + pop_density + car_ownership_rate",
            "plus_car_ownership",
        )
    )

    if "private_car_commute_rate" in run_df.columns and run_df["private_car_commute_rate"].notna().sum() >= 30:
        run_df_commute = run_df.dropna(subset=["private_car_commute_rate"]).copy()
        results.append(
            _fit_model(
                run_df_commute,
                "femur_rate ~ habitable_slope_weighted + aging_rate + fast_walking_rate + pop_density + private_car_commute_rate",
                "plus_private_car_commute",
            )
        )

    if "avg_steps_per_day" in run_df.columns and run_df["avg_steps_per_day"].notna().sum() >= 30:
        run_df_steps = run_df.dropna(subset=["avg_steps_per_day"]).copy()
        results.append(
            _fit_model(
                run_df_steps,
                "femur_rate ~ habitable_slope_weighted + aging_rate + fast_walking_rate + pop_density + avg_steps_per_day",
                "plus_avg_steps",
            )
        )

    out = pd.DataFrame([r.__dict__ for r in results])
    out.to_csv(MODEL_SUMMARY_CSV, index=False, encoding="utf-8-sig")

    STATUS_MD.write_text(
        "\n".join(
            [
                "# Car Mobility Sensitivity: Status",
                "",
                "- status: completed",
                f"- input_file: `{CAR_DATA_PATH}`",
                f"- output_models: `{MODEL_SUMMARY_CSV}`",
                f"- output_joined_data: `{JOINED_DATA_CSV}`",
                f"- output_availability: `{AVAILABILITY_CSV}`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"[OK] generated: {MODEL_SUMMARY_CSV}")
    print(f"[OK] generated: {JOINED_DATA_CSV}")
    print(f"[OK] generated: {STATUS_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
