# Reanalysis Audit (2026-04-30)

## 1) 論文本体の数値に直結する既存プログラム（監査で確定）

- 主データセット生成: `03_Analysis/data/processed/analysis_dataset_v1.csv`
- 既存パイプライン（実質本線）:
  - `03_Analysis/scripts/10_run_complete_analysis.py`
  - `03_Analysis/scripts/04_integrate_datasets.py`
  - `03_Analysis/scripts/08_regression_analysis.py`
  - `03_Analysis/scripts/09_regression_diagnostics_and_sensitivity.py`
- 既存結果ファイル:
  - `03_Analysis/results/table1_descriptive.csv`
  - `03_Analysis/results/regression_results.txt`
  - `03_Analysis/results/regression_diagnostics_report.txt`

## 2) 既存論文数値との一致確認（再計算）

`analysis_dataset_v1.csv` から再計算した結果:

- N = 47
- mean slope = 8.57, SD = 3.16
- mean femur rate = 254.0, SD = 37.6
- Model 1 slope β = 5.65, p = 0.001
- Model 2 slope β = 3.49, 95% CI [0.11, 6.86], p = 0.043

上記は `Manuscript_slope_fracture.qmd` の主要結果と一致。

## 3) 新規再解析（間接法SIR/ISR）の監査結果

監査対象: `03_Analysis/scripts/11_indirect_age_standardization_analysis.py`

### 3.1 重大所見

- NDB公開ファイル `款別性年齢別算定回数.xlsx` において、主要femur手術コードである `150019210`（K046 ORIF相当）の性年齢階級別セルがほぼ秘匿値 `-`。
- 実際に年齢階級別値が得られたのは `150016710` 等の一部コードのみで、主要件数を構成するコードの年齢分布が欠落。
- このため、観察件数（都道府県合計）と期待件数（間接法）の整合性が成立しない。

### 3.2 結論

- 公開NDBのみでは、寳澤先生提案の「防御可能な間接法標準化」を厳密には完遂不可。
- したがって、新規再解析の推定値を論文本体の確定値として採用してはならない。
- 本文では「実施不能の理由（公開データの秘匿制約）」を明示するのが妥当。

## 4) 監査後の原稿修正方針

- 「間接法で有意だった」等の断定記載は削除済み。
- 代わりに「公開データ制約により完全な間接標準化は実施不能」をMethods/Results/Discussion/Limitationsに反映済み。

## 5) e-Stat追加ダウンロードで実現可能か（再検討）

### 結論

- **e-Stat追加取得のみでは解決しない。**

### 理由

1. 間接法に必要な要素は以下:
   - 分子（観察）: 都道府県別の総手術件数（これは既にある）
   - 期待値算出用: **全国の年齢階級別手術率（主要コードを含む完全な年齢分布）**
   - 分母: 都道府県別年齢階級人口（e-Statで取得可能）
2. 今回のボトルネックは分母ではなく、**NDB公開表側の年齢階級セル秘匿**（主要femurコードで `-` が多発）である。
3. e-Statは人口統計（分母）を補完できるが、NDB手術件数の秘匿セル（分子の年齢分布）を埋めることはできない。

### 実装上の意味

- e-Stat人口データの追加取得は有益だが、現行公開NDBのみでは完全な間接法SIR推定の成立条件を満たさない。
- 実現には、秘匿のない年齢階級別手術件数（より詳細なNDB提供データ等）が別途必要。
