"""
reproduce_from_release.py
-------------------------
Purpose (plain language)
    Re-check the main findings of the manuscript using only the small,
    public prefecture-level CSV files in ``data/release/`` (47 rows = 47
    prefectures). You do **not** need to download raw NDB Excel files.

What this script does
    1. Loads the released analysis table (or a local fallback copy).
    2. Fits the same regression models as the paper (hip surgery rate vs terrain
       slope, with aging, fast walking, and population density).
    3. Confirms headline numbers: N=47, mean slope 8.57°, mean hip rate 254,
       unadjusted slope coefficient 5.65, adjusted 3.49 (within tolerance).
    4. Saves a short regression report and correlation table under
       ``03_Analysis/results/reproduce_release/``.

Who should run this
    Reviewers, readers, and authors verifying the Zenodo/GitHub deposit.

See also: REPRODUCE.md (Route 1 — Minimal reproduce).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))
from _utils import as_float, configure_stdout_utf8  # noqa: E402

configure_stdout_utf8()

ROOT = Path(__file__).resolve().parents[2]
RELEASE = ROOT / "data" / "release"
OUT = ROOT / "03_Analysis" / "results" / "reproduce_release"

DATASET = RELEASE / "analysis_dataset_prefecture_n47.csv"
FALLBACK = ROOT / "03_Analysis" / "data" / "processed" / "analysis_dataset_v1.csv"

# Manuscript headline values and acceptable numerical tolerance
EXPECTED = {"n": 47, "mean_slope": 8.57, "mean_femur_rate": 254.0, "m1_beta": 5.65, "m2_beta": 3.49}
TOL = {"mean_slope": 0.02, "mean_femur_rate": 0.1, "m1_beta": 0.02, "m2_beta": 0.02}


def load_dataset() -> pd.DataFrame:
    """Load the 47-prefecture table from the public release folder."""
    if DATASET.exists():
        return pd.read_csv(DATASET)
    if FALLBACK.exists():
        print(f"[warn] Using fallback processed file: {FALLBACK}")
        return pd.read_csv(FALLBACK)
    raise FileNotFoundError(
        f"Missing {DATASET}. Run export_release_bundle.py or the mainline pipeline first."
    )


def verify_headline(df: pd.DataFrame) -> None:
    """
    Compare recomputed statistics to the values reported in the manuscript Abstract.
    Raises an error if any check fails (helps catch data or code drift).
    """
    m1 = smf.ols("femur_rate ~ habitable_slope_weighted", data=df).fit()
    m2 = smf.ols(
        "femur_rate ~ habitable_slope_weighted + aging_rate + fast_walking_rate + pop_density",
        data=df,
    ).fit()
    observed = {
        "n": int(len(df)),
        "mean_slope": as_float(df["habitable_slope_weighted"].mean()),
        "mean_femur_rate": as_float(df["femur_rate"].mean()),
        "m1_beta": as_float(m1.params["habitable_slope_weighted"]),
        "m2_beta": as_float(m2.params["habitable_slope_weighted"]),
    }
    for key, expected in EXPECTED.items():
        if key == "n":
            if observed[key] != expected:
                raise RuntimeError(f"Prefecture count mismatch: {observed[key]} != {expected}")
            continue
        if abs(observed[key] - expected) > TOL[key]:
            raise RuntimeError(
                f"{key}: got {observed[key]:.4f}, expected {expected} (tolerance {TOL[key]})"
            )
    print("[OK] Headline values match the manuscript:", observed)


def main() -> int:
    """Run minimal reproduction and write summary outputs."""
    OUT.mkdir(parents=True, exist_ok=True)

    print("Loading public prefecture-level dataset...")
    df = load_dataset()

    print("Verifying headline statistics from the manuscript...")
    verify_headline(df)

    print("Fitting adjusted Model 2 (hip rate ~ slope + covariates)...")
    m2 = smf.ols(
        "femur_rate ~ habitable_slope_weighted + aging_rate + fast_walking_rate + pop_density",
        data=df,
    ).fit()
    (OUT / "regression_m2_summary.txt").write_text(m2.summary().as_text(), encoding="utf-8")

    corr_cols = [
        c
        for c in [
            "fracture_rate",
            "femur_rate",
            "humerus_rate",
            "forearm_rate",
            "habitable_slope_weighted",
            "aging_rate",
            "fast_walking_rate",
            "pop_density",
        ]
        if c in df.columns
    ]
    pd.DataFrame(df[corr_cols]).corr().to_csv(OUT / "correlation_matrix.csv", encoding="utf-8-sig")
    print(f"Done. Outputs saved under: {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
