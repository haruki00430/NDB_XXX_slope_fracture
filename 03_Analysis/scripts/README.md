# Mainline Script Guide

本研究で「論文数値に直結する本線」は、以下の単一エントリポイントに統一:

- `00_manuscript_mainline_pipeline.py`

このスクリプトは次を順に実行します。

1. `10_run_complete_analysis.py`（抽出→統合→回帰→図）
2. `09_regression_diagnostics_and_sensitivity.py`（診断・HC3・bootstrap）
3. `analysis_dataset_v1.csv` から主要数値の再現チェック

## 実行

```bash
python 03_Analysis/scripts/00_manuscript_mainline_pipeline.py
```

## 主要出力

- `03_Analysis/data/processed/analysis_dataset_v1.csv`
- `03_Analysis/results/table1_descriptive.csv`
- `03_Analysis/results/regression_results.txt`
- `03_Analysis/results/regression_diagnostics_report.txt`
- `03_Analysis/results/figures/*.png`

## 注意

- 追加検討用スクリプト（例: `11_indirect_age_standardization_analysis.py`）は本線ではありません。
- 本線と差分がある解析は、必ず別名出力・監査ログを残してください。
