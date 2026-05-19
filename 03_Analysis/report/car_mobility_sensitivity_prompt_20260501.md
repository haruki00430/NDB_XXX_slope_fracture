# 追加感度分析プロンプト（舟久保先生③・大平先生回答対応）

## 目的
- 傾斜と大腿骨骨折手術率の関連が、地域の移動手段（自動車依存）でどの程度変わるかを感度分析として確認する。
- 主解析は変更せず、追加解析は robustness check として扱う。

## 入力ファイル
1. 既存: `03_Analysis/data/processed/analysis_dataset_v1.csv`
2. 追加: `03_Analysis/data/interim/car_mobility_prefecture.csv`
   - 必須列:
     - `prefecture`（都道府県名）
     - `car_ownership_rate`（例: 世帯当たり自家用乗用車保有率/台数）
   - 任意列:
     - `private_car_commute_rate`（自家用車通勤率）
     - `avg_steps_per_day`（平均歩数）

## 実行コマンド
```powershell
python "03_Analysis/scripts/13_car_mobility_sensitivity_analysis.py"
```

## 期待出力
- `03_Analysis/results/car_mobility_sensitivity_status.md`
- `03_Analysis/results/car_mobility_data_availability.csv`
- `03_Analysis/results/car_mobility_input_template.csv`
- （追加データがある場合）
  - `03_Analysis/results/car_mobility_sensitivity_models.csv`
  - `03_Analysis/results/car_mobility_sensitivity_prefecture.csv`

## 解釈ルール（先生共有用）
- 注目は `habitable_slope_weighted` の係数（β, 95%CI, p）。
- `baseline_model2` と `plus_car_ownership` の差分で、傾斜係数の変化を確認。
- 追加変数で係数が大きく減衰する場合は、地域移動特性による交絡の可能性を示唆。
- 追加変数の欠測が大きい場合は、推論対象の都道府県が縮小している点を明記。

## 注意
- 新規データ取得が必要な場合は、取得前に必ずユーザー確認を取る。
- 本解析は感度分析であり、主解析テーブルの置換は行わない。
