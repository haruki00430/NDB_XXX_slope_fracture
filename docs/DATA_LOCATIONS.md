# データファイル所在マップ

**プロジェクト**: NDB_XXX_slope_fracture
**作成日**: 2026-02-16
**更新日**: 2026-02-16

このドキュメントは、プロジェクトで使用するすべてのデータファイルの所在を記録します。

---

## 1. NDBオープンデータ（第10回）

### 1.1 骨折手術データ

#### 大腿骨近位部骨折
- **ファイルパス**:
  ```
  C:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\02_Data\raw\NDB_OpenData\No.10\06_手術\01_公費レセプトを含まないデータ\都道府県別_手術実施件数_2021年度_公費レセプトを含まない_大腿骨.xlsx
  ```
- **手術コード**: K0461（大腿骨近位部骨折観血的手術）
- **データ構造**: 都道府県×性別×年齢階級（5歳刻み）
- **ヘッダー**: MultiIndex（header=[2, 3]）
- **対象年齢**: 65歳以上（65-69, 70-74, 75-79, 80-84, 85+）
- **用途**: 主要アウトカム（大腿骨骨折手術率）

#### 上腕骨骨折
- **ファイルパス**:
  ```
  C:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\02_Data\raw\NDB_OpenData\No.10\06_手術\01_公費レセプトを含まないデータ\都道府県別_手術実施件数_2021年度_公費レセプトを含まない_上腕骨.xlsx
  ```
- **手術コード**: K0421（上腕骨骨折観血的手術）
- **用途**: 副次アウトカム（上腕骨骨折手術率）

---

### 1.2 特定健診質問票データ

#### 歩行速度（Q16）
- **ファイルパス**:
  ```
  C:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\02_Data\raw\NDB_OpenData\No.10\07_特定健診 質問票\01_公費レセプトを含まないデータ\都道府県別_健診_質問票_2021年度_公費レセプトを含まない.xlsx
  ```
- **質問項目**: Q16「人と比較して歩く速度が速い」（はい/いいえ）
- **データ構造**: 都道府県×性別×年代×回答（はい/いいえ）
- **ヘッダー**: MultiIndex（header=[2, 3]）
- **用途**: 媒介変数（歩行習慣の代理指標）

---

## 2. 国土地理院（GSI）地理データ

### 2.1 数値標高モデル（DEM）

#### 基盤地図情報DEM
- **データソース**: 国土地理院「基盤地図情報（数値標高モデル）」
- **URL**: https://fgd.gsi.go.jp/download/menu.php
- **解像度**: 5mメッシュ（または10mメッシュ）
- **対象範囲**: 全国47都道府県
- **フォーマット**: GeoTIFF または XML（JPGIS2.1）
- **保存先**:
  ```
  C:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture\data\raw\DEM\
  ```
- **推定容量**: 5GB（5mメッシュ全国）
- **用途**: 傾斜度算出のベースデータ

#### 傾斜度ラスター（算出済み）
- **ファイルパス**:
  ```
  projects/NDB_XXX_slope_fracture/data/interim/slope_map.tif
  ```
- **作成手法**: Horn法（3×3移動窓）
- **単位**: 度（degree）
- **除外エリア**: 森林、水域（可住地域のみ）
- **推定容量**: 500MB
- **用途**: 都道府県別傾斜度集計のベース

---

### 2.2 土地利用データ（オプション）

#### 国土数値情報「土地利用細分メッシュ」
- **データソース**: 国土交通省国土数値情報
- **URL**: https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-L03-b-u.html
- **用途**: 可住地域の抽出（森林・水域の除外）
- **保存先**:
  ```
  projects/NDB_XXX_slope_fracture/data/raw/landuse/
  ```

---

### 2.3 都道府県境界データ

#### 行政区域データ
- **データソース**: 国土数値情報「行政区域データ」
- **URL**: https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N03-v3_1.html
- **フォーマット**: Shapefile (.shp)
- **用途**: 都道府県別集計、地図可視化
- **保存先**:
  ```
  C:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\02_Data\master\japan_prefectures.shp
  ```

---

## 3. e-Stat統計データ

### 3.1 国勢調査2020年

#### 高齢化率
- **データソース**: e-Stat「国勢調査2020年」
- **URL**: https://www.e-stat.go.jp/
- **指標**:
  - 65歳以上人口比率（%）
  - 75歳以上人口比率（%）
- **粒度**: 都道府県別
- **保存先**:
  ```
  C:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\02_Data\master\aging_rate_by_prefecture_2020.csv
  ```

#### 人口密度
- **データソース**: e-Stat「国勢調査2020年」
- **指標**: 人口密度（人/km²）、人口集中地区（DID）人口比率（%）
- **保存先**:
  ```
  C:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\02_Data\master\population_density_2020.csv
  ```

---

### 3.2 気象庁データ

#### 積雪深データ
- **データソース**: 気象庁「過去の気象データ」
- **URL**: https://www.data.jma.go.jp/obd/stats/etrn/index.php
- **指標**: 年間最大積雪深（cm）
- **期間**: 2015-2020年の平均
- **保存先**:
  ```
  C:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\02_Data\master\annual_snowfall_by_prefecture.csv
  ```
- **用途**: 積雪地域フラグ作成（100cm以上/未満で二値化）

---

### 3.3 所得データ（オプション）

#### 全国消費実態調査
- **データソース**: 総務省「全国消費実態調査」
- **指標**: 1世帯あたり平均年収（万円）
- **年次**: 2019年
- **保存先**:
  ```
  C:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\02_Data\master\average_income_by_prefecture.csv
  ```

---

## 4. 中間データ（Interim Data）

Phase 1-4で作成される中間データファイル。

| ファイル名 | パス | 作成フェーズ | サイズ | 内容 |
|-----------|------|------------|--------|------|
| `fracture_surgery.csv` | `data/interim/` | Phase 1 | ~10KB | 都道府県別骨折手術件数（年齢階級別） |
| `walking_speed_q16.csv` | `data/interim/` | Phase 1 | ~2KB | 都道府県別歩行速度「速い」回答率 |
| `slope_index.csv` | `data/interim/` | Phase 2 | ~3KB | 都道府県別傾斜度指標（5指標） |
| `demographics.csv` | `data/interim/` | Phase 3 | ~4KB | 都道府県別統計指標（高齢化率、人口密度等） |
| **`analysis_dataset.csv`** | `data/interim/` | Phase 4 | ~5KB | **最終解析用データセット（47行×15列）** |

---

## 5. 解析結果（Results）

Phase 5-6で作成される解析結果ファイル。

### 5.1 統計解析結果

| ファイル名 | パス | 内容 |
|-----------|------|------|
| `descriptive_statistics.csv` | `results/statistics/` | 記述統計表（平均、SD、最小、最大） |
| `correlation_matrix.csv` | `results/statistics/` | Pearson/Spearman相関行列 |
| `regression_summary.txt` | `results/statistics/` | 重回帰分析結果（Model 1-4） |
| `mediation_results.csv` | `results/statistics/` | 媒介分析の効果分解（直接/間接効果） |
| `subgroup_analysis.csv` | `results/statistics/` | サブグループ別回帰係数 |

---

### 5.2 図表（Figures）

| ファイル名 | タイトル | 形式 | DPI |
|-----------|---------|------|-----|
| `slope_map.png` | 都道府県別平均傾斜度マップ | PNG | 300 |
| `fracture_map.png` | 年齢調整骨折手術率マップ | PNG | 300 |
| `bivariate_map.png` | 傾斜度×骨折率の2変量マップ | PNG | 300 |
| `scatter_slope_fracture.png` | 傾斜度 vs 骨折率（散布図） | PNG | 300 |
| `correlation_heatmap.png` | 相関行列ヒートマップ | PNG | 300 |
| `forest_plot_regression.png` | 回帰係数Forest Plot | PNG | 300 |
| `mediation_dag.png` | 媒介分析の経路図（DAG） | PNG | 300 |
| `prefecture_ranking.png` | 都道府県ランキング | PNG | 300 |

---

## 6. 論文関連ファイル

| ファイル名 | パス | 内容 |
|-----------|------|------|
| `Manuscript_slope_fracture.qmd` | プロジェクトルート | 英語論文原稿（Quarto） |
| `Manuscript_slope_fracture.html` | プロジェクトルート | HTML出力 |
| `Manuscript_slope_fracture.docx` | プロジェクトルート | Word出力 |
| `Manuscript_slope_fracture.pdf` | プロジェクトルート | PDF出力 |
| `references.bib` | プロジェクトルート | 文献リスト（BibTeX、30-40件） |
| `vancouver.csl` | プロジェクトルート | Vancouver引用スタイル |

---

## 7. データ取得チェックリスト

プロジェクト開始前に、以下のデータが取得済みか確認してください。

### 必須データ
- [ ] NDB第10回 骨折手術データ（大腿骨）
- [ ] NDB第10回 骨折手術データ（上腕骨）
- [ ] NDB第10回 特定健診質問票データ
- [ ] 国土地理院DEM（5mまたは10mメッシュ）
- [ ] e-Stat 高齢化率データ（2020年）
- [ ] e-Stat 人口密度データ（2020年）
- [ ] 都道府県境界データ（Shapefile）

### 推奨データ
- [ ] 気象庁 積雪深データ
- [ ] 国土数値情報 土地利用細分メッシュ
- [ ] 全国消費実態調査 所得データ

---

## 8. データ更新履歴

| 日付 | データ名 | 更新内容 | 更新者 |
|------|---------|---------|--------|
| 2026-02-16 | - | 初版作成 | Claude Code |

---

## 9. データ使用上の注意

### NDBデータ
- **利用規約**: 第10回NDBオープンデータ利用規約に準拠
- **公開制限**: 個票データの公開は不可、都道府県レベルの集計値のみ公開可能
- **AI使用**: 生データをLLM（Cursor、ChatGPT等）に送信しない（CLAUDE.mdに準拠）

### 国土地理院データ
- **利用規約**: 基盤地図情報の利用規約に準拠
- **出典明記**: 論文中で「国土地理院基盤地図情報」と明記
- **加工**: 二次利用・加工は可能

### e-Statデータ
- **利用規約**: 政府統計の総合窓口（e-Stat）利用規約に準拠
- **出典明記**: 「総務省統計局 国勢調査2020年」と明記

---

**作成者**: NDB Research Hub / Claude Code
**バージョン**: 1.0.0
**最終更新**: 2026-02-16
