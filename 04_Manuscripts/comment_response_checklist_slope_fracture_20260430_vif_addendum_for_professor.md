# 提出用追補レポート（VIF検証完了・数値付き）

対象原稿: `Manuscript_slope_fracture.qmd`  
関連チェックリスト: `comment_response_checklist_slope_fracture_20260430.md`（本ファイルはその追補）

## 1. 追補の目的

佐藤先生コメントで懸念された「多重共線性」について、主解析と同一データ・同一説明変数セットで、Variance Inflation Factor（VIF）を用いた明示的検証を追加実施した。

## 2. 実施内容（再現可能性）

- 実装先（本線スクリプト）: `03_Analysis/scripts/00_manuscript_mainline_pipeline.py`
- 追加手法: `statsmodels.stats.outliers_influence.variance_inflation_factor`
- 対象説明変数（Model 2）:
  - `habitable_slope_weighted`
  - `aging_rate`
  - `fast_walking_rate`
  - `pop_density`
- 判定基準（rule-of-thumb）:
  - VIF >= 5: 注意域
  - VIF >= 10: 高度な多重共線性の懸念

## 3. 結果（数値）

出力ファイル:
- `03_Analysis/results/multicollinearity_vif.csv`
- `03_Analysis/results/multicollinearity_vif_report.txt`

VIF実測値（2026-04-30 実行）:

| 変数 | VIF | VIF>=5 | VIF>=10 |
|---|---:|:---:|:---:|
| aging_rate | 2.028 | No | No |
| pop_density | 1.707 | No | No |
| habitable_slope_weighted | 1.351 | No | No |
| fast_walking_rate | 1.243 | No | No |

## 4. 判定

- 全説明変数で VIF < 5（かつ < 10）であり、主解析モデルにおいて重篤な多重共線性は認めない。
- したがって、今回の主結果に関する回帰係数推定の解釈は、多重共線性によって著しく毀損される状況ではない。

## 5. 先生提出用の整合メモ

- 既存チェックリストNo.2（サンプルサイズとモデル安定性）に関連する「多重共線性」の実測根拠を、本追補で明示した。
- 主解析（本線）と追加感度分析（SIR補完）は分離維持したまま、主解析側の品質管理項目としてVIF検証を完了した。
- 本追補をチェックリスト本体と併せて提出することで、「多重共線性は検証済みか」に対して定量的根拠付きで回答可能。
