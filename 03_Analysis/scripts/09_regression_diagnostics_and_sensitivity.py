# -*- coding: utf-8 -*-
"""
09_regression_diagnostics_and_sensitivity.py
--------------------------------------------
Purpose (plain language)
    Check whether the linear regression linking terrain slope to hip fracture
    surgery rate is trustworthy, and test whether results stay similar when
    using alternative statistical methods.

What this script does
    1. Summarizes distribution of each variable (skewness, Shapiro–Wilk test).
    2. Fits Model 1 (slope only) and Model 2 (slope + aging + fast walking + density).
    3. Plots residuals vs fitted values and a normal Q–Q plot (Model 2).
    4. Repeats Model 2 with heteroskedasticity-robust standard errors (HC3).
    5. Bootstrap resamples prefectures 5,000 times to form a 95% interval for the slope.
    6. Writes a text report and saves a diagnostic figure.

Primary outcome
    ``femur_rate`` = annual hip fracture surgeries per 100,000 population.

Outputs
    - ``03_Analysis/results/regression_diagnostics_report.txt``
    - ``03_Analysis/results/figures/fig_residual_diagnostics_hip_m2.png``

Run after
    ``00_manuscript_mainline_pipeline.py`` (needs ``analysis_dataset_v1.csv``).
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))
from _utils import as_float, as_series, configure_stdout_utf8  # noqa: E402

configure_stdout_utf8()

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
DATA_PATH = PROJECT_ROOT / "03_Analysis" / "data" / "processed" / "analysis_dataset_v1.csv"
RESULTS_DIR = PROJECT_ROOT / "03_Analysis" / "results"
FIGURES_DIR = PROJECT_ROOT / "03_Analysis" / "results" / "figures"
REPORT_PATH = RESULTS_DIR / "regression_diagnostics_report.txt"

N_BOOT = 5000
RNG_SEED = 42

# Table 1 と整合する変数（論文 Table 1 の行）
TABLE1_COLS = [
    ("fracture_rate", "Total fracture surgery rate"),
    ("femur_rate", "Hip (femur) fracture surgery rate"),
    ("humerus_rate", "Humerus fracture surgery rate"),
    ("forearm_rate", "Forearm fracture surgery rate"),
    ("habitable_slope_weighted", "Habitable-area-weighted slope"),
    ("avg_slope_simple", "Simple mean slope"),
    ("aging_rate", "Aging rate (≥65 years)"),
    ("fast_walking_rate", "Fast walking rate"),
    ("pop_density", "Population density"),
]


def skewness_series(x: pd.Series) -> float:
    """Measure asymmetry of a variable's distribution (for Table 1 notes)."""
    x = x.dropna().astype(float)
    if len(x) < 3:
        return float("nan")
    return float(stats.skew(x, bias=False))


def shapiro_w(x: pd.Series) -> tuple[float, float]:
    """Shapiro–Wilk normality test statistic and p-value for one variable."""
    values = as_series(x).dropna().astype(float).to_numpy()
    if len(values) < 3:
        return float("nan"), float("nan")
    stat, p = stats.shapiro(values)
    return float(stat), float(p)


def bootstrap_slope_m2(df: pd.DataFrame, n_boot: int, seed: int) -> np.ndarray:
    """
    Resample prefectures with replacement many times and refit Model 2 each time.
    Returns the collection of slope coefficients (for a bootstrap confidence interval).
    """
    rng = np.random.default_rng(seed)
    formula = (
        "femur_rate ~ habitable_slope_weighted + aging_rate + "
        "fast_walking_rate + pop_density"
    )
    coefs = []
    n = len(df)
    for _ in range(n_boot):
        idx = rng.integers(0, n, size=n)
        sub = df.iloc[idx]
        try:
            m = smf.ols(formula, data=sub).fit()
            coefs.append(as_float(m.params["habitable_slope_weighted"]))
        except Exception:
            coefs.append(np.nan)
    return np.asarray(coefs, dtype=float)


def main() -> int:
    """Run all diagnostic and sensitivity analyses and write the report file."""
    print("Regression diagnostics and sensitivity analysis (N = 47 prefectures)")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    if not DATA_PATH.exists():
        print(f"Missing data: {DATA_PATH}", file=sys.stderr)
        return 1

    df = pd.read_csv(DATA_PATH, encoding="utf-8")
    lines: list[str] = []

    def write_line(text: str) -> None:
        lines.append(text)
        print(text)

    write_line("=" * 72)
    write_line("Regression diagnostics & sensitivity (prefecture N=47)")
    write_line(f"Data: {DATA_PATH}")
    write_line("=" * 72)

    # --- Marginal distributions (Table 1 variables) ---
    write_line("\n## Marginal distributions (for Table 1 reporting)\n")
    write_line(f"{'Variable':<40} {'n':>4} {'skew':>8} {'SW p':>10}")
    write_line("-" * 72)
    skew_map: dict[str, float] = {}
    for col, label in TABLE1_COLS:
        if col not in df.columns:
            continue
        series = as_series(df[col])
        sk = skewness_series(series)
        _, swp = shapiro_w(series)
        skew_map[col] = sk
        write_line(f"{label[:39]:<40} {len(series.dropna()):>4} {sk:>8.3f} {swp:>10.4f}")

    # --- Model 1 & 2: femur (hip) ---
    f1 = "femur_rate ~ habitable_slope_weighted"
    f2 = (
        "femur_rate ~ habitable_slope_weighted + aging_rate + "
        "fast_walking_rate + pop_density"
    )
    m1 = smf.ols(f1, data=df).fit()
    m2 = smf.ols(f2, data=df).fit()
    m2_hc3 = smf.ols(f2, data=df).fit(cov_type="HC3")

    write_line("\n## Model 1 OLS (slope only)\n")
    write_line(m1.summary().as_text())

    write_line("\n## Model 2 OLS (default SE)\n")
    write_line(m2.summary().as_text())

    write_line("\n## Model 2 OLS with heteroskedasticity-robust SE (HC3)\n")
    write_line(m2_hc3.summary().as_text())

    resid2 = m2.resid
    fitted2 = m2.fittedvalues
    sw_stat, sw_p = stats.shapiro(resid2.values)

    write_line("\n## Residual normality (Model 2), Shapiro–Wilk on OLS residuals\n")
    write_line(f"Shapiro–Wilk W = {sw_stat:.4f}, p = {sw_p:.4f}")
    write_line("(Small-sample tests on residuals are indicative only.)\n")

    # Plots
    plt.rcParams["font.family"] = "DejaVu Sans"
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    ax0, ax1 = axes
    ax0.scatter(fitted2, resid2, alpha=0.75, edgecolors="k", linewidths=0.3)
    ax0.axhline(0, color="gray", linestyle="--", linewidth=1)
    ax0.set_xlabel("Fitted values (Model 2)")
    ax0.set_ylabel("Residuals")
    ax0.set_title("Residuals vs fitted (hip fracture rate)")

    stats.probplot(resid2, dist="norm", plot=ax1)
    ax1.set_title("Normal Q–Q plot of residuals (Model 2)")
    fig.tight_layout()
    fig_path = FIGURES_DIR / "fig_residual_diagnostics_hip_m2.png"
    fig.savefig(fig_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    write_line(f"Saved: {fig_path}")

    # Bootstrap CI for slope in Model 2
    write_line(f"\n## Nonparametric bootstrap for β(slope), Model 2 (B={N_BOOT}, prefecture resampling)\n")
    boot = bootstrap_slope_m2(df, N_BOOT, RNG_SEED)
    boot_clean = boot[np.isfinite(boot)]
    lo, hi = np.percentile(boot_clean, [2.5, 97.5])
    write_line(f"Bootstrap 95% CI for habitable_slope_weighted: [{lo:.4f}, {hi:.4f}]")
    write_line(f"OLS 95% CI (default):   [{m2.conf_int().loc['habitable_slope_weighted', 0]:.4f}, {m2.conf_int().loc['habitable_slope_weighted', 1]:.4f}]")
    write_line(f"OLS 95% CI (HC3):      [{m2_hc3.conf_int().loc['habitable_slope_weighted', 0]:.4f}, {m2_hc3.conf_int().loc['habitable_slope_weighted', 1]:.4f}]")
    write_line(f"Point estimate β:      {m2.params['habitable_slope_weighted']:.4f}")

    # HC3 p for slope
    p_hc3 = float(m2_hc3.pvalues["habitable_slope_weighted"])
    write_line(f"p-value (slope, default SE): {float(m2.pvalues['habitable_slope_weighted']):.4f}")
    write_line(f"p-value (slope, HC3):        {p_hc3:.4f}")

    write_line("\n## Synthesis for manuscript\n")
    write_line(
        "- OLS assumes linearity and (for classical SE) homoskedastic, independent errors; "
        "marginal normality of Table 1 variables is not required."
    )
    write_line(
        "- Compare bootstrap / HC3 to default OLS: if substantive conclusions agree, "
        "state robustness in Methods/Results."
    )

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nWrote report: {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
