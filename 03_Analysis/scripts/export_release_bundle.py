"""
export_release_bundle.py
------------------------
Purpose (plain language)
    Prepare the files that will be shared on GitHub and Zenodo: the final
    47-prefecture analysis table, a slope-only table, and a small JSON file
    recording when and how the bundle was built.

What this script does
    1. Reads the full analysis CSV produced by the main pipeline.
    2. Checks that there are exactly 47 rows (one per prefecture).
    3. Copies data into ``data/release/`` with stable filenames for citation.
    4. Writes ``provenance.json`` (build time, git commit id, source path).

When to run
    After ``00_manuscript_mainline_pipeline.py`` succeeds, and before tagging
    ``v1.0.0`` for Zenodo.

Who should run this
    Study authors / repository maintainers (not required for ordinary readers).
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))
from _utils import configure_stdout_utf8  # noqa: E402

configure_stdout_utf8()

ROOT = Path(__file__).resolve().parents[2]
RELEASE = ROOT / "data" / "release"
PROCESSED = ROOT / "03_Analysis" / "data" / "processed" / "analysis_dataset_v1.csv"
SLOPE_SRC = ROOT / "results" / "statistics" / "prefecture_habitable_slope.csv"
SLOPE_ALT = ROOT / "03_Analysis" / "results" / "statistics" / "prefecture_habitable_slope.csv"


def git_sha() -> str:
    """Return the current git commit hash for reproducibility metadata."""
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        return out.strip()
    except Exception:
        return "unknown"


def main() -> int:
    """Export Zenodo/GitHub release files under data/release/."""
    RELEASE.mkdir(parents=True, exist_ok=True)

    if not PROCESSED.exists():
        print(
            f"ERROR: Processed dataset not found: {PROCESSED}\n"
            "Run 00_manuscript_mainline_pipeline.py first.",
            file=sys.stderr,
        )
        return 1

    print("Reading processed analysis dataset...")
    df = pd.read_csv(PROCESSED)
    if len(df) != 47:
        print(f"ERROR: Expected 47 prefectures, found {len(df)} rows.", file=sys.stderr)
        return 1

    out_main = RELEASE / "analysis_dataset_prefecture_n47.csv"
    df.to_csv(out_main, index=False, encoding="utf-8-sig")
    print(f"Wrote public analysis table: {out_main}")

    slope_path = SLOPE_SRC if SLOPE_SRC.exists() else SLOPE_ALT
    if slope_path.exists():
        slope = pd.read_csv(slope_path)
        cols = [c for c in ["prefecture", "habitable_slope_weighted", "avg_slope_simple"] if c in slope.columns]
        slope[cols].to_csv(RELEASE / "prefecture_habitable_slope.csv", index=False, encoding="utf-8-sig")
        print(f"Wrote terrain slope table from: {slope_path}")
    elif "habitable_slope_weighted" in df.columns:
        df[["prefecture", "habitable_slope_weighted"]].to_csv(
            RELEASE / "prefecture_habitable_slope.csv", index=False, encoding="utf-8-sig"
        )
        print("Wrote terrain slope table from analysis dataset columns.")

    provenance = {
        "built_at_utc": datetime.now(timezone.utc).isoformat(),
        "git_sha": git_sha(),
        "source_processed": str(PROCESSED.relative_to(ROOT)).replace("\\", "/"),
        "n_prefectures": int(len(df)),
        "script": "03_Analysis/scripts/export_release_bundle.py",
        "description": "Prefecture-level aggregate bundle for open access (no individual-level NDB records).",
    }
    (RELEASE / "provenance.json").write_text(
        json.dumps(provenance, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print("Wrote provenance.json (build metadata for Zenodo).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
