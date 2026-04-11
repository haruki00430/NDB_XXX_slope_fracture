# NDB_XXX_slope_fracture

## 地形傾斜度と高齢者骨折リスク・歩行習慣の関連研究

**プロジェクト開始日**: 2026-02-16
**研究タイプ**: 生態学的研究（Ecological Study）
**データソース**: NDB第10回 × 国土地理院DEM × e-Stat統計

## ステータス（2026-04-05 リポジトリ照合）

- **原稿**: `04_Manuscripts/Manuscript_slope_fracture.qmd`
- **備考**: README の Phase チェックリストと実体がずれる場合は `analysis/`・`results/` を正とする。

---

## 🎯 研究目的

地形傾斜度（坂道）が高齢者の骨折手術実施率に与える影響を、全国47都道府県を対象に定量的に評価する。さらに、歩行習慣が傾斜度と骨折リスクの関連を媒介するかを検証する。

---

## 🔬 研究仮説

### 主仮説
**H1**: 地形傾斜度が高い都道府県ほど、高齢者の骨折手術実施率が高い

### 副仮説
- **H2**: 傾斜度は歩行習慣を媒介して骨折リスクに影響する
- **H3**: 傾斜度と骨折リスクの関連は、積雪地域で増強される
- **H4**: 傾斜度と骨折リスクの関連はJ字カーブを描く（適度な傾斜は保護的、過度な傾斜は有害）

---

## 📊 データソース

| データ | 出所 | 用途 |
|--------|------|------|
| 骨折手術データ | NDB第10回/06_手術/ | アウトカム指標 |
| 歩行速度データ | NDB第10回/07_特定健診 質問票/ | 媒介変数 |
| 数値標高モデル（DEM） | 国土地理院基盤地図情報 | 傾斜度算出 |
| 高齢化率・人口密度 | e-Stat国勢調査2020 | 交絡因子 |
| 積雪データ | 気象庁 | サブグループ解析 |

---

## 📁 プロジェクト構造

```
projects/NDB_XXX_slope_fracture/
├── config/
│   └── config.yaml              # 設定ファイル
├── data/
│   ├── raw/                     # 生データ（DEMなど）
│   └── interim/                 # 中間データ（CSV）
│       ├── fracture_surgery.csv
│       ├── walking_speed_q16.csv
│       ├── slope_index.csv
│       ├── demographics.csv
│       └── analysis_dataset.csv  # ★最終解析用データ
├── 03_Analysis/
│   └── scripts/
│       ├── 01_extract_ndb_fracture.py
│       ├── 02_calculate_slope.py
│       ├── 03_collect_statistics.py
│       ├── 04_integrate_data.py
│       ├── 05_statistical_analysis.py
│       └── 06_visualization.py
├── results/
│   ├── statistics/              # 統計解析結果
│   └── figures/                 # 図表（PNG, 300dpi）
├── docs/
│   ├── implementation_plan.md   # 詳細実装計画（7フェーズ）
│   ├── DATA_LOCATIONS.md        # データファイル所在
│   ├── hypothesis_and_discussion.md  # 研究仮説と議論
│   └── session_log.log          # 実行ログ
├── references.bib               # 文献リスト（BibTeX）
├── vancouver.csl                # 引用スタイル
├── Manuscript_slope_fracture.qmd     # 英語論文原稿
└── README.md                    # 本ファイル
```

---

## 🚀 実装フェーズ（7段階）

| Phase | タスク | 成果物 | 日数 |
|-------|--------|--------|------|
| **Phase 1** | NDBデータ抽出 | fracture_surgery.csv, walking_speed_q16.csv | 2日 |
| **Phase 2** | 地理データ処理（DEM→傾斜度） | slope_index.csv, slope_map.tif | 3日 |
| **Phase 3** | 統計データ収集 | demographics.csv | 1日 |
| **Phase 4** | データ統合 | analysis_dataset.csv | 1日 |
| **Phase 5** | 統計解析（相関・回帰・媒介分析） | 統計結果CSV/TXT | 2日 |
| **Phase 6** | 可視化（地図・散布図・Forest plot） | 図表PNG（8枚） | 2日 |
| **Phase 7** | 論文執筆（Quarto） | .qmd → HTML/DOCX/PDF | 3日 |

**合計**: 14日（約3週間）

詳細は [implementation_plan.md](docs/implementation_plan.md) を参照。

---

## 🛠️ 環境セットアップ

### 必要な環境
- Python >= 3.11
- GDAL >= 3.6（DEM処理用）
- Quarto（論文執筆用）

### インストール手順
```bash
# 仮想環境作成
python -m venv .venv
.venv\Scripts\activate  # Windows

# 依存関係インストール
cd C:\Users\user\SharedWorkspace\projects\NDB_Research_Hub
pip install -r requirements.txt

# または editable install
pip install -e .
```

### 主要ライブラリ
- **データ処理**: pandas, numpy, polars
- **GIS**: geopandas, rasterio, GDAL
- **統計**: statsmodels, scipy, pingouin
- **可視化**: matplotlib, seaborn, plotly
- **論文**: Quarto, pandoc

---

## 📈 解析手法

### 統計手法
1. **記述統計**: 平均、標準偏差、分布確認
2. **相関分析**: Pearson/Spearman相関係数
3. **重回帰分析**:
   - Model 1: 傾斜度のみ
   - Model 2: 傾斜度 + 高齢化率
   - Model 3: 完全調整モデル（傾斜度 + 高齢化率 + 人口密度 + 積雪フラグ）
   - Model 4: 非線形関係（傾斜度の2乗項追加）
4. **媒介分析**: Bootstrap法（1,000回リサンプリング）
   - 傾斜度 → 歩行速度 → 骨折リスク
5. **サブグループ解析**: 積雪地域、都市化レベルでの層別化

### 傾斜度算出
- **手法**: Horn法（3×3移動窓）
- **単位**: 度（degree）
- **除外エリア**: 森林、水域（可住地域のみ）
- **集計指標**: 平均、中央値、75パーセンタイル、最大、急傾斜地比率（15度以上）

---

## 📊 期待される成果

### 学術的貢献
- **新規性**: 地形傾斜度と骨折リスクの全国規模定量評価（世界初）
- **方法論**: DEM×NDB×統計の3層統合手法テンプレート化
- **因果推論**: 媒介分析による歩行習慣の役割解明

### 政策的示唆
- **バリアフリー政策**: 急傾斜地での高齢者住宅の優先的改修
- **歩行促進プログラム**: 適度な傾斜を活用した運動プログラム開発
- **医療資源配分**: 傾斜地での訪問リハビリ強化

### 投稿候補ジャーナル
- **Journal of Epidemiology** (IF ~3.0)
- **Environmental Health Perspectives** (IF ~10.4)
- **Injury Prevention** (IF ~3.8)
- **Preventive Medicine** (IF ~4.4)

---

## 📚 関連ドキュメント

| ファイル名 | 説明 |
|-----------|------|
| [implementation_plan.md](docs/implementation_plan.md) | 7フェーズの詳細実装計画 |
| [DATA_LOCATIONS.md](docs/DATA_LOCATIONS.md) | 全データファイルの所在 |
| [hypothesis_and_discussion.md](docs/hypothesis_and_discussion.md) | 研究仮説と議論の枠組み |
| [config.yaml](config/config.yaml) | プロジェクト設定ファイル |

---

## ⚠️ 注意事項

### データ取り扱い
- **NDB生データ**: 外部LLMに送信しない（CLAUDE.mdに準拠）
- **公開可能データ**: 都道府県レベルの集計値のみ（個票不可）
- **バックアップ**: Phase完了ごとにOneDrive/外付けHDDにバックアップ

### 研究の限界
- **生態学的研究**: 個人レベルの因果推論は不可（Ecological Fallacy）
- **横断研究**: 時間的因果関係は検証不可
- **転倒データ欠如**: 直接的な転倒データは含まれない（歩行速度で代用）
- **粒度の制約**: NDBデータは都道府県レベル（市区町村レベル不可）

---

## 🏁 次のステップ

### 即時実行タスク
1. ✅ プロジェクトフォルダ作成
2. ✅ config.yaml作成
3. ✅ 研究計画書作成
4. 🔲 NDBデータの所在確認（`02_Data/raw/NDB_OpenData/No.10/`）
5. 🔲 DEMデータの取得方法確認（国土地理院サイト）
6. 🔲 Phase 1スクリプト作成開始

### Phase 1準備
```bash
# NDBデータ確認
ls "../../02_Data/raw/NDB_OpenData/No.10/06_手術/01_公費レセプトを含まないデータ/"
ls "../../02_Data/raw/NDB_OpenData/No.10/07_特定健診 質問票/01_公費レセプトを含まないデータ/"

# スクリプト作成
cd 03_Analysis/scripts
touch 01_extract_ndb_fracture.py
```

---

**プロジェクトステータス**: 🟢 Phase 0（準備完了）
**最終更新**: 2026-02-16
**問い合わせ**: NDB Research Hub
