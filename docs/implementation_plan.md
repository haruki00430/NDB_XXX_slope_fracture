# 実装計画書：地形傾斜度と高齢者骨折リスク研究

**プロジェクト名**: NDB_XXX_slope_fracture
**研究テーマ**: 地形傾斜度（坂道）と高齢者の骨折リスク・歩行習慣の関連
**作成日**: 2026-02-16
**バージョン**: 1.0.0

---

## 1. プロジェクト概要

### 1.1 研究背景

日本は世界有数の山岳国であり、国土の約7割が山地・丘陵地である。多くの地域では高齢者が傾斜地に居住しており、日常的に坂道を往来する生活を送っている。地形傾斜度は、以下の2つの相反する影響を高齢者の骨折リスクに与える可能性がある：

1. **転倒リスクの増加**: 急な坂道は転倒の危険性を高め、特に大腿骨近位部骨折のリスクを上昇させる
2. **歩行習慣の促進**: 適度な傾斜は日常的な歩行運動を促し、下肢筋力・骨密度を維持する効果がある

しかし、これまで地形傾斜度と骨折リスクの関連を全国規模で定量的に評価した研究は存在しない。

### 1.2 研究の独自性

本研究は、以下の3つのデータソースを統合した日本初の生態学的研究である：

| データソース | 提供情報 | 役割 |
|------------|---------|------|
| **NDB第10回オープンデータ** | 骨折手術件数、歩行速度 | 健康アウトカム |
| **国土地理院DEM** | 数値標高モデル | 傾斜度算出 |
| **e-Stat統計** | 高齢化率、人口密度 | 交絡因子調整 |

この3層統合により、**物理的環境（傾斜度）が健康アウトカム（骨折）に与える因果的影響**を論じることが可能となる。

### 1.3 研究仮説

#### 主仮説
- **H1**: 地形傾斜度が高い都道府県ほど、高齢者の骨折手術実施率が高い

#### 副仮説
- **H2**: 傾斜度は歩行習慣を媒介して骨折リスクに影響する（媒介分析）
- **H3**: 傾斜度と骨折リスクの関連は、積雪地域で増強される（交互作用）
- **H4**: 傾斜度と骨折リスクの関連はJ字カーブを描く（適度な傾斜は保護的、過度な傾斜は有害）

---

## 2. 研究デザイン

- **研究タイプ**: 生態学的研究（Ecological Study）
- **研究単位**: 都道府県レベル（47-48都道府県）
- **時点**: 2021年度（NDB第10回データ）
- **アウトカム**: 年齢調整骨折手術実施率（人口10万対）
- **曝露**: 地形傾斜度（平均、中央値、75パーセンタイル等）

---

## 3. 7フェーズ実装スケジュール

### Phase 1: NDBデータ抽出（1-2日）

#### 目的
NDB第10回オープンデータから、骨折手術データ（部位別）および歩行速度データを抽出する。

#### タスク

**1.1 骨折手術データの抽出（部位別）**
- **対象ファイル**:
  - `02_Data/raw/NDB_OpenData/No.10/01_医科診療行為（算定回数）/01_公費レセプトを含まないデータ/K_手術/款別都道府県別算定回数.xlsx`
- **抽出対象シート**: `入院` シート（主要な骨折手術は入院で算定されるため）
- **対象手術データ（診療行為コード・名称）**:
  - **大腿骨（Femur / Hip）** - 5コード:
    - `150016710`: 骨折非観血的整復術（大腿） [K044 Closed Reduction] (Row 169)
    - `150018310`: 骨折経皮的鋼線刺入固定術（大腿） [K045 Percutaneous Pinning] (Row 178)
    - `150019210`: 骨折観血的手術（大腿） [K046 Open Reduction] (Row 189)
    - `150049510`: 人工骨頭挿入術（股） [K081 Hemiarthroplasty] (Row 548)
    - `150050410`: 人工関節置換術（股） [K082 Total Hip Arthroplasty] (Row 554)
  - **上腕骨（Humerus）** - 5コード:
    - `150016610`: 骨折非観血的整復術（上腕） [K044 Closed Reduction] (Row 168)
    - `150018210`: 骨折経皮的鋼線刺入固定術（上腕） [K045 Percutaneous Pinning] (Row 177)
    - `150019110`: 骨折観血的手術（上腕） [K046 Open Reduction] (Row 188)
    - `150049410`: 人工骨頭挿入術（肩） [K081 Hemiarthroplasty] (Row 547)
    - `150050310`: 人工関節置換術（肩） [K082 Total Shoulder Arthroplasty] (Row 553)
  - **前腕骨（Forearm）** - 3コード:
    - `150016810`: 骨折非観血的整復術（前腕） [K044 Closed Reduction] (Row 170)
    - `150018410`: 骨折経皮的鋼線刺入固定術（前腕） [K045 Percutaneous Pinning] (Row 179)
    - `150019310`: 骨折観血的手術（前腕） [K046 Open Reduction] (Row 190)
- **抽出粒度**: 都道府県別算定回数（総数）
  - ※本ファイルには性別・年齢階級別の内訳が含まれないため、都道府県単位の総数を使用する。
- **処理**:
  ```python
  import pandas as pd
  
  # ヘッダー処理（行2がカラム名、行3からデータと仮定）
  df = pd.read_excel(file_path, header=[2])
  
  # "K046"を含む行を特定し、その近傍にある部位別行をコード(1500...)または名称で抽出
  target_codes = {
      'femur': 150019210,   # 大腿
      'humerus': 150019110, # 上腕
      'forearm': 150019310  # 前腕
  }
  
  # 都道府県列（北海道〜沖縄）を抽出
  df_extracted = extract_prefecture_counts(df, target_codes)
  ```
- **出力**: `data/interim/fracture_surgery_site.csv`

**1.2 歩行速度データの抽出**（完了）
- **対象ファイル**:
  - `07_特定健診 質問票/01_公費レセプトを含まないデータ/標準的な質問票（質問項目１２） 都道府県別性年齢階級別分布.xlsx`
- **対象質問**: Q12「ほぼ同じ年齢の同性と比較して歩く速度が速い」（はい/いいえ）
  - ※当初Q16と想定していたが、実データ検証によりQ12であることを特定済み。
- **指標**: 「はい」回答率（%）
- **処理**:
  ```python
  # Q12列を抽出 (高齢者: 65-74歳)
  walking_speed = df.loc[:, ('Q12', 'ほぼ同じ年齢の同性と比較して歩く速度が速い', 'はい')]

  # 都道府県別集計
  walking_speed_rate = (walking_speed / total_respondents) * 100
  ```
- **出力**: `data/interim/walking_speed_q12.csv`

#### スクリプト
- `03_Analysis/scripts/01_extract_ndb_fracture_v2.py`
- `03_Analysis/scripts/01_extract_walking_speed_q12.py`

#### 成果物
| ファイル名 | 内容 | 行数 |
|-----------|------|------|
| `fracture_surgery_site.csv` | 都道府県別・部位別骨折手術件数 | 48行 |
| `walking_speed_q12.csv` | 都道府県別歩行速度「速い」回答率 | 50行 |

---

### Phase 2: 地理データ処理（2-3日）

#### 目的
国土地理院DEMデータから都道府県別の傾斜度指標を算出する。

#### タスク

**2.1 DEMデータ取得**
- **データソース**: 国土数値情報（標高・傾斜度4次メッシュ）
- **URL**: https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-G04-c.html
- **対象範囲**: 全国47都道府県
- **フォーマット**: GML (XML)
- **保存先**: `02_Data/raw/MLIT/G04_c_Elevation/`

**2.2 傾斜度算出**
- **手法**: 国土数値情報に含まれる「平均傾斜角」を使用（再計算不要）
- **処理概要**:
  - GMLファイル（XML）をパースし、各メッシュの平均傾斜角を抽出
  - 都道府県ごとに平均値を集計
  ```python
  import xml.etree.ElementTree as ET
  import pandas as pd
  import glob

  # GMLパースと集計（イメージ）
  def parse_gml(xml_file):
      tree = ET.parse(xml_file)
      # ... 名前空間処理と値の抽出 ...
      return avg_slopes

  # 都道府県別平均
  df_result = pd.DataFrame(avg_slopes).groupby('pref_code').mean()
  ```

**2.3 可住地域の抽出**
- **除外エリア**: 森林、水域、農地（国土数値情報「土地利用細分メッシュ」を使用）
- **処理**:
  ```python
  # 土地利用データとのオーバーレイ
  residential_mask = (landuse == '住宅地') | (landuse == '商業地')
  slope_residential = slope[residential_mask]
  ```

**2.4 都道府県別集計**
- **集計指標**:
  1. **平均傾斜度** (mean_slope)
  2. **中央値傾斜度** (median_slope)
  3. **75パーセンタイル傾斜度** (p75_slope)
  4. **最大傾斜度** (max_slope)
  5. **急傾斜地比率** (steep_ratio): 傾斜15度以上の居住地面積比率
- **出力**: `data/interim/slope_index.csv`

#### スクリプト
- `03_Analysis/scripts/02_calculate_slope.py`

#### 成果物
| ファイル名 | 内容 | 行数 |
|-----------|------|------|
| `slope_index.csv` | 都道府県別傾斜度指標（5指標） | 47行 |
| `slope_map.tif` | 全国傾斜度ラスターマップ | - |

---

### Phase 3: 統計データ収集（1日）

#### 目的
e-Statから高齢化率、人口密度、積雪データを取得し、交絡因子として整備する。

#### タスク

**3.1 高齢化率データ**
- **データソース**: e-Stat 国勢調査2020年
- **指標**:
  - 65歳以上人口比率（%）
  - 75歳以上人口比率（%）
- **API使用**: 可能であればe-Stat API、または手動ダウンロード

**3.2 人口密度データ**
- **データソース**: e-Stat 国勢調査2020年
- **指標**: 人口密度（人/km²）
- **都市化指標**: 人口集中地区（DID）人口比率（%）

**3.3 積雪データ**
- **データソース**: 気象庁過去データ
- **指標**: 年間最大積雪深（cm）
- **二値化**: 100cm以上/未満で積雪地域フラグ作成

**3.4 所得データ（オプション）**
- **データソース**: 総務省「全国消費実態調査」
- **指標**: 1世帯あたり平均年収（万円）

#### スクリプト
- `03_Analysis/scripts/03_collect_statistics.py`

#### 成果物
| ファイル名 | 内容 | 列数 |
|-----------|------|------|
| `demographics.csv` | 都道府県別統計指標 | 6-8列 |

---

### Phase 4: データ統合（1日）

#### 目的
Phase 1-3で作成した3つのデータセットを都道府県コードで結合し、最終解析用データセットを作成する。

#### タスク

**4.1 データ結合**
- **キー**: 都道府県コード（JIS X 0401）
- **結合方法**: 内部結合（inner join）
- **処理**:
  ```python
  import pandas as pd

  # 3つのデータセット読み込み
  fracture = pd.read_csv('data/interim/fracture_surgery.csv')
  slope = pd.read_csv('data/interim/slope_index.csv')
  demographics = pd.read_csv('data/interim/demographics.csv')
  walking = pd.read_csv('data/interim/walking_speed_q16.csv')

  # 結合
  df = fracture.merge(slope, on='prefecture_code') \
               .merge(demographics, on='prefecture_code') \
               .merge(walking, on='prefecture_code')
  ```

**4.2 骨折手術実施率の算出**
- **方法**: 粗罹患率（Crude Rate）の算出
  - ※部位別データには年齢内訳がないため、直接法の年齢調整は行わない。
  - ※解析フェーズ（重回帰分析）にて「高齢化率」を調整変数として投入することで、年齢構成の差異を統計的に制御する。
- **計算式**:
  ```
  手術実施率（人口10万対） = (手術件数 / 65歳以上人口) × 100,000
  ```
- **処理**:
  ```python
  # 人口データを使用
  df['fracture_rate_femoral'] = (df['count_femur'] / df['population_65plus']) * 100000
  df['fracture_rate_humerus'] = (df['count_humerus'] / df['population_65plus']) * 100000
  ```

**4.3 欠損値処理**
- **確認**: 欠損値の有無をチェック
- **対応**:
  - 完全欠損の都道府県は除外
  - 部分欠損は多重代入法（MICE）または中央値補完

**4.4 変数リスト確定**

最終データセットの変数（列）：

| 変数名 | 説明 | 型 |
|--------|------|-----|
| `prefecture_code` | 都道府県コード | int |
| `prefecture_name` | 都道府県名 | str |
| `fracture_rate_femoral` | 大腿骨骨折手術率（粗罹患率、人口10万対） | float |
| `fracture_rate_humerus` | 上腕骨骨折手術率（粗罹患率） | float |
| `walking_speed_fast_rate` | 歩行速度「速い」回答率（%） | float |
| `mean_slope` | 平均傾斜度（度） | float |
| `median_slope` | 中央値傾斜度（度） | float |
| `p75_slope` | 75パーセンタイル傾斜度（度） | float |
| `steep_ratio` | 急傾斜地比率（%） | float |
| `aging_rate_65plus` | 65歳以上人口比率（%） | float |
| `aging_rate_75plus` | 75歳以上人口比率（%） | float |
| `population_density` | 人口密度（人/km²） | float |
| `did_ratio` | DID人口比率（%） | float |
| `snowfall_flag` | 積雪地域フラグ（1: 100cm以上, 0: 未満） | int |
| `average_income` | 平均年収（万円）※オプション | float |

#### スクリプト
- `03_Analysis/scripts/04_integrate_data.py`

#### 成果物
| ファイル名 | 内容 | サイズ |
|-----------|------|--------|
| `analysis_dataset.csv` | 最終解析用データセット（47行×15列） | ~10KB |

---

### Phase 5: 統計解析（2日）

#### 目的
傾斜度と骨折リスクの関連を、相関分析、重回帰分析、媒介分析により評価する。

#### タスク

**5.1 記述統計**
- **内容**:
  - 各変数の平均、標準偏差、最小値、最大値
  - ヒストグラム（傾斜度、骨折率の分布）
  - 都道府県ランキング（傾斜度上位10、骨折率上位10）

**5.2 相関分析**
- **手法**: Pearson相関係数、Spearman順位相関係数
- **対象**: 全変数間の相関行列
- **主要ペア**:
  - 傾斜度 vs 骨折手術率
  - 傾斜度 vs 歩行速度
  - 歩行速度 vs 骨折手術率
- **処理**:
  ```python
  import pandas as pd
  import scipy.stats as stats

  # Pearson相関
  corr_matrix = df.corr(method='pearson')

  # p値計算
  p_values = df.corr(method=lambda x, y: stats.pearsonr(x, y)[1])
  ```

**5.3 重回帰分析**
- **従属変数**: 骨折手術率（粗罹患率）
  - ※モデル内で「高齢化率」を調整変数として投入する。
- **独立変数**:
  - Model 1: 傾斜度のみ
  - Model 2: 傾斜度 + 高齢化率
  - Model 3: 傾斜度 + 高齢化率 + 人口密度 + 積雪フラグ

  - Model 4: Model 3 + 傾斜度の2乗項（非線形関係の検証）
- **処理**:
  ```python
  import statsmodels.api as sm

  # Model 3の例
  X = df[['mean_slope', 'aging_rate_65plus', 'population_density', 'snowfall_flag']]
  X = sm.add_constant(X)
  y = df['fracture_rate_femoral']

  model = sm.OLS(y, X).fit()
  print(model.summary())
  ```
- **出力**:
  - 回帰係数、標準誤差、t値、p値、95%信頼区間
  - R², 調整済みR²、F統計量

**5.4 媒介分析（Mediation Analysis）**
- **仮説**: 傾斜度 → 歩行速度 → 骨折リスク
- **手法**: Bootstrap法（1,000回リサンプリング）
- **推定値**:
  - 直接効果（Direct Effect）
  - 間接効果（Indirect Effect / ACME: Average Causal Mediation Effect）
  - 総効果（Total Effect）
  - 媒介比率（Proportion Mediated）
- **処理**:
  ```python
  from statsmodels.stats.mediation import Mediation

  # Step 1: X → M (傾斜度 → 歩行速度)
  model_m = sm.OLS.from_formula('walking_speed_fast_rate ~ mean_slope', data=df).fit()

  # Step 2: X + M → Y (傾斜度 + 歩行速度 → 骨折率)
  model_y = sm.OLS.from_formula('fracture_rate_femoral ~ mean_slope + walking_speed_fast_rate', data=df).fit()

  # Mediation分析
  med = Mediation(model_y, model_m, 'mean_slope', 'walking_speed_fast_rate').fit(n_rep=1000)
  print(med.summary())
  ```

**5.5 サブグループ解析**
- **層別化変数**:
  1. 積雪地域（あり/なし）
  2. 都市化レベル（DID比率の中央値で2分割）
- **手法**: 各サブグループでの重回帰分析
- **交互作用検定**: 傾斜度 × 積雪フラグ、傾斜度 × 都市化フラグ

**5.6 感度分析**
- **目的**: 外れ値の影響を確認
- **手法**:
  - Cook's distance による影響力診断
  - ロバスト回帰（Huber回帰）との比較

#### スクリプト
- `03_Analysis/scripts/05_statistical_analysis.py`

#### 成果物
| ファイル名 | 内容 |
|-----------|------|
| `correlation_matrix.csv` | 相関行列（Pearson & Spearman） |
| `regression_summary.txt` | 重回帰分析結果（Model 1-4） |
| `mediation_results.csv` | 媒介分析の効果分解 |
| `subgroup_analysis.csv` | サブグループ別の回帰係数 |
| `descriptive_statistics.csv` | 記述統計表 |

---

### Phase 6: 可視化（2日）

#### 目的
解析結果を論文掲載レベルの図表として可視化する。

#### タスク

**6.1 地図可視化**

**図1: 都道府県別傾斜度マップ（Choropleth Map）**
- **変数**: 平均傾斜度（度）
- **カラースケール**: Viridis（青→黄）
- **処理**:
  ```python
  import geopandas as gpd
  import matplotlib.pyplot as plt
  from ndb_library.viz import set_japanese_font

  set_japanese_font()

  # 都道府県境界データ読み込み
  gdf = gpd.read_file('japan_prefectures.shp')
  gdf = gdf.merge(df, on='prefecture_code')

  # プロット
  fig, ax = plt.subplots(figsize=(10, 12))
  gdf.plot(column='mean_slope', cmap='viridis', legend=True, ax=ax)
  ax.set_title('都道府県別平均傾斜度', fontsize=16)
  plt.savefig('results/figures/slope_map.png', dpi=300, bbox_inches='tight')
  ```

**図2: 骨折手術率マップ**
- **変数**: 年齢調整骨折手術率
- **カラースケール**: Reds（白→赤）

**図3: 2変量マップ（Bivariate Map）**
- **変数**: 傾斜度（x軸） × 骨折率（y軸）
- **カラー**: 3×3グリッド（9色）で2変数を同時表示

**6.2 散布図**

**図4: 傾斜度 vs 骨折手術率**
- **プロット**: 散布図 + 回帰直線 + 95%信頼区間
- **バブルサイズ**: 高齢化率（大きいほど高齢化が進んでいる）
- **ラベル**: 傾斜度・骨折率が共に高い都道府県名を表示
- **処理**:
  ```python
  import seaborn as sns

  fig, ax = plt.subplots(figsize=(10, 8))

  # 散布図
  sns.scatterplot(data=df, x='mean_slope', y='fracture_rate_femoral',
                  size='aging_rate_65plus', sizes=(50, 500), alpha=0.6, ax=ax)

  # 回帰直線
  sns.regplot(data=df, x='mean_slope', y='fracture_rate_femoral',
              scatter=False, color='red', ax=ax)

  ax.set_xlabel('平均傾斜度（度）', fontsize=14)
  ax.set_ylabel('年齢調整骨折手術率（人口10万対）', fontsize=14)
  ax.set_title('地形傾斜度と骨折手術率の関連', fontsize=16)

  # 外れ値にラベル
  for idx, row in df.iterrows():
      if row['mean_slope'] > 10 or row['fracture_rate_femoral'] > 200:
          ax.text(row['mean_slope'], row['fracture_rate_femoral'],
                  row['prefecture_name'], fontsize=9)

  plt.savefig('results/figures/scatter_slope_fracture.png', dpi=300, bbox_inches='tight')
  ```

**6.3 相関ヒートマップ**

**図5: 全変数間の相関行列**
- **手法**: Seaborn heatmap
- **表示**: Pearson相関係数 + 有意水準の星印（*, **, ***）

**6.4 Forest Plot**

**図6: 重回帰分析の係数プロット**
- **内容**: Model 3（完全調整モデル）の各変数の標準化回帰係数 + 95%CI
- **処理**:
  ```python
  import matplotlib.pyplot as plt

  # 回帰係数と信頼区間
  coefs = model.params[1:]  # 定数項を除く
  ci = model.conf_int().iloc[1:, :]

  fig, ax = plt.subplots(figsize=(8, 6))
  ax.errorbar(coefs, range(len(coefs)), xerr=[coefs - ci.iloc[:, 0], ci.iloc[:, 1] - coefs],
              fmt='o', capsize=5, capthick=2)
  ax.axvline(0, color='gray', linestyle='--')
  ax.set_yticks(range(len(coefs)))
  ax.set_yticklabels(coefs.index)
  ax.set_xlabel('標準化回帰係数', fontsize=14)
  ax.set_title('骨折手術率に対する各要因の影響（Forest Plot）', fontsize=16)
  plt.savefig('results/figures/forest_plot_regression.png', dpi=300, bbox_inches='tight')
  ```

**6.5 媒介分析の経路図（DAG）**

**図7: 傾斜度 → 歩行速度 → 骨折リスクの媒介モデル**
- **ツール**: Graphviz または手描き風（matplotlib + annotate）
- **表示内容**:
  - 各パスの係数（β）とp値
  - 直接効果、間接効果の大きさ

**6.6 都道府県ランキング**

**図8: 傾斜度・骨折率の上位/下位10都道府県**
- **形式**: 横棒グラフ（Horizontal Bar Chart）
- **並び順**: 降順（上位から表示）

#### スクリプト
- `03_Analysis/scripts/06_visualization.py`

#### 成果物（図表）
| ファイル名 | 図のタイトル | 形式 |
|-----------|------------|------|
| `slope_map.png` | 都道府県別平均傾斜度 | PNG, 300dpi |
| `fracture_map.png` | 年齢調整骨折手術率 | PNG, 300dpi |
| `bivariate_map.png` | 傾斜度×骨折率の2変量マップ | PNG, 300dpi |
| `scatter_slope_fracture.png` | 傾斜度 vs 骨折率（散布図） | PNG, 300dpi |
| `correlation_heatmap.png` | 相関行列ヒートマップ | PNG, 300dpi |
| `forest_plot_regression.png` | 回帰係数Forest Plot | PNG, 300dpi |
| `mediation_dag.png` | 媒介分析の経路図 | PNG, 300dpi |
| `prefecture_ranking.png` | 都道府県ランキング | PNG, 300dpi |

---

### Phase 7: 論文執筆（3日）

#### 目的
Quarto形式で英語論文原稿を作成し、HTML/DOCX/PDF出力を行う。

#### 論文構成（IMRAD形式）

**Title（タイトル）**
"Association between Terrain Slope and Hip Fracture Surgery Rates among Older Adults: A Nationwide Ecological Study in Japan"

**Abstract（要旨、250 words）**
- Background
- Methods
- Results
- Conclusions

**Introduction（序論、800 words）**
- 高齢者の骨折負担（疫学、医療費）
- 地形環境と健康の関連（先行研究）
- 日本の地形的特性（山岳国）
- Research Gap（これまで全国規模の定量研究がない）
- 研究目的と仮説

**Methods（方法、1,200 words）**
- Study Design: Ecological study
- Data Sources:
  - NDB Open Data (骨折手術、歩行速度)
  - GSI Digital Elevation Model (傾斜度)
  - e-Stat Census (高齢化率、人口密度)
- Slope Calculation: Horn法、可住地域の抽出
- Outcome: 年齢調整骨折手術率
- Statistical Analysis: 相関、回帰、媒介分析
- Ethics: 公開データのため倫理審査不要

**Results（結果、1,500 words）**
- Descriptive Statistics（表1: 変数の記述統計）
- Correlation Analysis（図1: 相関ヒートマップ）
- Regression Analysis（表2: Model 1-4の結果、図2: Forest Plot）
- Mediation Analysis（図3: DAG、表3: 効果分解）
- Subgroup Analysis（積雪地域、都市化レベル）
- Geographic Distribution（図4: 傾斜度マップ、図5: 骨折率マップ）

**Discussion（考察、1,800 words）**
- Main Findings（主要な発見）
- Biological Plausibility（生物学的妥当性）
  - 傾斜地での転倒リスク増加メカニズム
  - 歩行習慣の媒介効果
- Comparison with Previous Studies（先行研究との比較）
- Policy Implications（政策的示唆）
  - バリアフリー化の優先順位（急傾斜地）
  - 適度な傾斜を活用した歩行促進プログラム
- Strengths and Limitations
  - **Strengths**: 全国規模、3層データ統合、DEMの活用
  - **Limitations**: 生態学的研究（個人レベルの因果推論不可）、横断研究、転倒データの欠如
- Future Directions（今後の課題）
  - 市区町村レベルの分析
  - 縦断研究（時系列分析）
  - 個人レベルの調査（コホート研究）

**Conclusion（結論、200 words）**
- 研究の要約
- 実務的意義

**References（文献、30-40件）**
- Vancouver Style
- 主要分野: 骨折疫学、環境疫学、GIS in public health

#### タスク

**7.1 文献収集（Zotero）**
- **検索キーワード**:
  - "hip fracture" AND "terrain"
  - "falls" AND "slope" AND "elderly"
  - "Digital Elevation Model" AND "public health"
  - "walkability" AND "fracture risk"
- **データベース**: PubMed, Web of Science, Google Scholar
- **目標**: 30-40件の文献をZoteroに登録
- **Export**: `references.bib`（BibTeX形式）

**7.2 Quarto原稿作成**
- **ファイル名**: `Manuscript_slope_fracture.qmd`
- **YAMLヘッダー**:
  ```yaml
  ---
  title: "Association between Terrain Slope and Hip Fracture Surgery Rates among Older Adults: A Nationwide Ecological Study in Japan"
  author:
    - name: "Author Name"
      affiliation: "Institution"
      email: "email@example.com"
  date: "2026-02-16"
  format:
    html:
      toc: true
      toc-depth: 3
      number-sections: true
      embed-resources: true
    docx:
      reference-doc: custom-reference.docx
    pdf:
      documentclass: article
      geometry: margin=1in
  bibliography: references.bib
  csl: vancouver.csl
  ---
  ```

**7.3 図表の埋め込み**
- **方法**: `![Figure 1: ...](results/figures/slope_map.png){width=80%}`
- **表**: Markdown tableまたはCSVからの読み込み

**7.4 レンダリング**
- **コマンド**:
  ```bash
  quarto render Manuscript_slope_fracture.qmd --to html
  quarto render Manuscript_slope_fracture.qmd --to docx
  quarto render Manuscript_slope_fracture.qmd --to pdf
  ```
- **出力確認**: HTML（ブラウザ）、DOCX（Word）、PDF（Acrobat）

**7.5 日本語版原稿**
- **ファイル名**: `Manuscript_slope_fracture_JP.qmd`
- **用途**: 国内学会発表、日本語ジャーナル投稿

#### スクリプト
- なし（手動執筆）

#### 成果物
| ファイル名 | 内容 |
|-----------|------|
| `Manuscript_slope_fracture.qmd` | 英語論文原稿（Quarto） |
| `Manuscript_slope_fracture.html` | HTML出力 |
| `Manuscript_slope_fracture.docx` | Word出力 |
| `Manuscript_slope_fracture.pdf` | PDF出力 |
| `references.bib` | 文献リスト（BibTeX） |
| `vancouver.csl` | Vancouver引用スタイル |

---

## 4. データ管理計画

### 4.1 データファイル一覧

| ファイル名 | パス | サイズ | 説明 |
|-----------|------|--------|------|
| NDB骨折手術データ | `02_Data/raw/NDB_OpenData/No.10/06_手術/` | ~50MB | 元データ |
| NDB質問票データ | `02_Data/raw/NDB_OpenData/No.10/07_特定健診 質問票/` | ~30MB | 元データ |
| DEMデータ | `projects/NDB_XXX_slope_fracture/data/raw/DEM/` | ~5GB | 5mメッシュ全国 |
| 傾斜度ラスター | `data/interim/slope_map.tif` | ~500MB | 算出済み |
| 骨折手術CSV | `data/interim/fracture_surgery.csv` | ~10KB | 抽出済み |
| 歩行速度CSV | `data/interim/walking_speed_q16.csv` | ~2KB | 抽出済み |
| 傾斜度指標CSV | `data/interim/slope_index.csv` | ~3KB | 集計済み |
| 統計データCSV | `data/interim/demographics.csv` | ~4KB | 収集済み |
| **最終データセット** | `data/interim/analysis_dataset.csv` | ~5KB | **解析用** |

### 4.2 データバックアップ
- **バックアップ先**: OneDrive または外付けHDD
- **頻度**: Phase完了ごと
- **対象**: `data/interim/`, `results/`, `docs/`

### 4.3 データ公開方針
- **NDB生データ**: 公開不可（利用規約）
- **集計データ**: 都道府県レベルの集計値は論文のSupplementary Dataとして公開可能
- **コード**: GitHubで公開（MITライセンス）

---

## 5. 技術スタック詳細

### 5.1 Python環境
- **Python**: 3.11以上
- **仮想環境**: venv または conda

### 5.2 必須ライブラリ

| ライブラリ | 用途 | バージョン |
|-----------|------|-----------|
| pandas | データ操作 | >=2.0 |
| numpy | 数値計算 | >=1.24 |
| matplotlib | 可視化 | >=3.7 |
| seaborn | 統計可視化 | >=0.12 |
| geopandas | 地理データ | >=0.13 |
| rasterio | ラスターデータ | >=1.3 |
| GDAL | DEM処理 | >=3.6 |
| statsmodels | 統計モデル | >=0.14 |
| scipy | 科学計算 | >=1.11 |
| pingouin | 媒介分析 | >=0.5 |
| openpyxl | Excel読み込み | >=3.1 |
| ndb_library | NDB専用ライブラリ | >=1.0 |

### 5.3 インストールコマンド
```bash
# 仮想環境作成
python -m venv .venv
.venv\Scripts\activate  # Windows

# 依存関係インストール
pip install -r requirements.txt

# または editable install
pip install -e .
```

---

## 6. 想定課題と対策

| 課題 | 影響度 | 対策 |
|------|--------|------|
| **DEMデータ容量が大きい（数GB）** | 中 | 都道府県単位で分割処理、10mメッシュにダウンサンプリング |
| **傾斜度の定義が複雑** | 中 | 複数指標（平均、中央値、パーセンタイル）を試行し、感度分析 |
| **積雪地域での骨折リスク増強** | 低 | サブグループ解析で層別化 |
| **生態学的研究の限界** | 高 | Discussionで明記、個人レベルの因果推論は不可と記載 |
| **NDBデータの粒度（都道府県のみ）** | 中 | 将来的に市区町村レベルのデータ利用を検討（個票データ申請） |
| **転倒データの欠如** | 中 | 歩行速度を代理指標として使用 |
| **時間的因果関係の欠如（横断研究）** | 高 | 縦断研究の必要性をLimitationに記載 |

---

## 7. 期待される成果

### 7.1 学術的貢献
1. **新規性**: 地形傾斜度と骨折リスクを全国規模で定量化した世界初の研究
2. **方法論的革新**: DEM×NDB×統計の3層統合手法のテンプレート化
3. **因果推論**: 媒介分析による歩行習慣の役割解明

### 7.2 政策的示唆
1. **バリアフリー政策**: 急傾斜地での高齢者住宅のバリアフリー化優先順位付け
2. **歩行促進プログラム**: 適度な傾斜を活用した運動プログラムの開発
3. **医療資源配分**: 傾斜地での訪問リハビリテーションの強化

### 7.3 社会的インパクト
- **メディア**: 地形と健康の関連は一般にもわかりやすく、報道価値が高い
- **自治体**: 都道府県ごとのリスク可視化により、地域特性に応じた対策立案が可能

---

## 8. 投稿候補ジャーナル

| ジャーナル名 | IF | 分野 | 理由 |
|------------|----|----|------|
| **Journal of Epidemiology** | 3.0 | 疫学 | 日本からの投稿が多く、NDB研究の実績あり |
| **Environmental Health Perspectives** | 10.4 | 環境保健 | 物理的環境と健康の関連に強い |
| **Injury Prevention** | 3.8 | 傷害予防 | 転倒・骨折専門誌（BMJ系） |
| **Preventive Medicine** | 4.4 | 予防医学 | 環境要因と疾病予防 |
| **Osteoporosis International** | 4.2 | 骨粗鬆症 | 骨折疫学の専門誌 |

**推奨**: Journal of Epidemiology（日本の読者層、オープンアクセス）

---

## 9. スケジュール概算

| フェーズ | 作業日数 | 累積日数 | 完了予定日 |
|---------|---------|---------|-----------|
| Phase 1: NDBデータ抽出 | 2日 | 2日 | 2026-02-18 |
| Phase 2: 地理データ処理 | 3日 | 5日 | 2026-02-21 |
| Phase 3: 統計データ収集 | 1日 | 6日 | 2026-02-22 |
| Phase 4: データ統合 | 1日 | 7日 | 2026-02-23 |
| Phase 5: 統計解析 | 2日 | 9日 | 2026-02-25 |
| Phase 6: 可視化 | 2日 | 11日 | 2026-02-27 |
| Phase 7: 論文執筆 | 3日 | 14日 | 2026-03-02 |
| **合計** | **14日** | - | **2026-03-02** |

※土日を含む場合、実質3週間程度

---

## 10. リファレンス

### 10.1 先行研究（例）
1. Kelsey JL, et al. Risk factors for fractures of the distal forearm and proximal humerus. *Am J Epidemiol*. 1992.
2. Cummings SR, Nevitt MC. Falls. *N Engl J Med*. 2015.
3. Stevens JA, Sogolow ED. Gender differences for non-fatal unintentional fall related injuries among older adults. *Inj Prev*. 2005.

### 10.2 GIS in Public Health
1. Cromley EK, McLafferty SL. *GIS and Public Health*. Guilford Press; 2011.
2. Huang G, et al. Using spatial analysis to understand the associations between terrain slope and risk of falls. *BMC Public Health*. 2020.

### 10.3 日本の関連研究
1. Suzuki T, et al. Risk factors for hip fracture in Japan: a nationwide cohort study. *J Bone Miner Res*. 2018.
2. Yamamoto N, et al. Geographic variation in hip fracture incidence in Japan. *Osteoporos Int*. 2019.

---

## 11. 次のステップ

プロジェクト開始にあたり、以下のタスクから着手してください：

### 即時実行タスク
1. ✅ プロジェクトフォルダ作成（完了）
2. ✅ config.yaml作成（完了）
3. ✅ implementation_plan.md作成（本ファイル）
4. 🔲 README.md作成
5. 🔲 DATA_LOCATIONS.md作成
6. 🔲 hypothesis_and_discussion.md作成

### Phase 1準備タスク
1. 🔲 NDBデータの所在確認（06_手術、07_質問票フォルダ）
2. 🔲 Excelファイルのヘッダー構造確認（MultiIndex確認）
3. 🔲 `01_extract_ndb_fracture.py` スクリプト作成
4. 🔲 ndb_library.utils.clean_numeric() の動作確認

---

**文書バージョン**: 1.0.0
**最終更新**: 2026-02-16
**作成者**: NDB Research Hub / Claude Code
**レビュー**: 未実施
