"""
create_zenodo_bundle.py
-----------------------
論文で言及・参照されているファイルのみを収録した Zenodo 公開用 ZIP を生成する。

内部メモ・査読コメント・改訂版 DOCX・探索スクリプト等は一切含まない。
実行後に生成される NDB_XXX_slope_fracture_zenodo_v1.0.0.zip を
Zenodo の手動アップロード画面でアップロードすること。
"""

import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT_ZIP = ROOT / "NDB_XXX_slope_fracture_zenodo_v1.0.0.zip"
PREFIX = "NDB_XXX_slope_fracture-v1.0.0"  # zip 内のルートフォルダ名

# ============================================================
# 収録ファイル ホワイトリスト（論文で言及・参照されるもののみ）
# ============================================================
INCLUDE_FILES = [
    # ── リポジトリルート ──────────────────────────────────
    "CITATION.cff",
    "LICENSE",
    "LICENSE-DATA",
    "README.md",
    "REPRODUCE.md",
    "DATA_SOURCES.md",
    "requirements.txt",

    # ── 設定サンプル ──────────────────────────────────────
    "config/config.yaml.example",

    # ── 都道府県レベル集計データ（N=47、論文 Data Availability 記載） ──
    "data/release/README.md",
    "data/release/variable_dictionary.json",

    # ── 地形傾斜統計 ─────────────────────────────────────
    "results/statistics/prefecture_habitable_slope.csv",

    # ── 解析スクリプト（論文 Methods・Data Availability 記載） ──
    "03_Analysis/scripts/README.md",
    "03_Analysis/scripts/_utils.py",
    "03_Analysis/scripts/00_manuscript_mainline_pipeline.py",
    "03_Analysis/scripts/09_regression_diagnostics_and_sensitivity.py",
    "03_Analysis/scripts/10_create_prefecture_maps.py",
    "03_Analysis/scripts/11_indirect_age_standardization_analysis.py",
    "03_Analysis/scripts/12_sir_masking_sensitivity.py",
    "03_Analysis/scripts/export_release_bundle.py",
    "03_Analysis/scripts/reproduce_from_release.py",

    # ── 解析結果（論文 Table 1・2・Figure 1・2 相当） ────
    "03_Analysis/results/table1_descriptive.csv",
    "03_Analysis/results/table1_descriptive.md",
    "03_Analysis/results/regression_results.txt",
    "03_Analysis/results/correlation_matrix.csv",
    "03_Analysis/results/age_standardized_indirect_regression.txt",

    # ── 論文掲載図（Figure 1・Figure 2） ─────────────────
    "03_Analysis/results/figures/scatter_slope_fracture.png",       # Figure 1
    "03_Analysis/results/figures/fig_map_geography_composite.png",  # Figure 2
    "03_Analysis/results/figures/fig_map_fracture.png",
    "03_Analysis/results/figures/fig_map_slope.png",
    "03_Analysis/results/figures/fig_map_bivariate.png",
    "03_Analysis/results/figures/fig_map_combined.png",
    "03_Analysis/results/figures/heatmap_correlation.png",
    "03_Analysis/results/figures/fig_residual_diagnostics_hip_m2.png",

    # ── 論文本体（Quarto ソース・参考文献・CSL） ──────────
    "04_Manuscripts/Manuscript_slope_fracture.qmd",
    "04_Manuscripts/references.bib",
    "04_Manuscripts/vancouver.csl",
    "04_Manuscripts/AI_USE_DISCLOSURE.md",

    # ── Zenodo 登録マニフェスト ───────────────────────────
    "docs/ZENODO_DEPOSIT_MANIFEST.md",
]

# data/release/ 内の CSV は自動追加（export_release_bundle.py 実行後に存在する場合）
INCLUDE_DIRS_CSV = ["data/release"]


def main() -> None:
    missing = []
    included = []

    with zipfile.ZipFile(OUT_ZIP, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        # ホワイトリストファイル
        for rel in INCLUDE_FILES:
            src = ROOT / rel
            if src.exists():
                zf.write(src, f"{PREFIX}/{rel}")
                included.append(rel)
            else:
                missing.append(rel)

        # data/release/ の CSV を自動追加
        for d in INCLUDE_DIRS_CSV:
            for csv in (ROOT / d).glob("*.csv"):
                rel = csv.relative_to(ROOT).as_posix()
                if rel not in INCLUDE_FILES:
                    zf.write(csv, f"{PREFIX}/{rel}")
                    included.append(rel)

    print(f"\n[OK] Included ({len(included)} files):")
    for f in included:
        print(f"   {f}")

    if missing:
        print(f"\n[WARN] Not found ({len(missing)} files):")
        for f in missing:
            print(f"   {f}")

    size_mb = OUT_ZIP.stat().st_size / 1024 / 1024
    print(f"\nOutput: {OUT_ZIP.name}  ({size_mb:.1f} MB)")
    print("-> Upload this file to Zenodo.")


if __name__ == "__main__":
    main()
