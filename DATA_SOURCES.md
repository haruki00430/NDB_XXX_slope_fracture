# Data Sources / データソース

This repository does **not** include NDB raw Excel files or national DEM rasters.  
All primary inputs are **publicly available** administrative or geospatial open data.

本リポジトリは NDB 生 Excel および全国 DEM ラスターを同梱しません。  
一次データはすべて公開情報です。

---

## 1. NDB Open Data / NDB オープンデータ（第10回）

| Item | Details |
|------|---------|
| Provider | Ministry of Health, Labour and Welfare (MHLW) / 厚生労働省 |
| Portal | https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000177182.html |
| Round used | **第10回**（令和5年度＝2023年4月–2024年3月の集計に相当する公開ファイル） |
| Format | Excel (`.xlsx`) |
| Redistribution | **Authors cannot redistribute raw files**; users must download from the portal |

### 1.1 Fracture surgery counts (outcomes) / 骨折手術（アウトカム）

| Item | Value |
|------|--------|
| Category | `01_医科診療行為（算定回数）` → `K_手術` |
| Subfolder | `01_公費レセプトを含まないデータ` |
| File (mainline) | `款別都道府県別算定回数.xlsx`（シート `入院`） |
| Unit | Prefecture × procedure code (aggregated counts) |
| Manuscript use | Hip, humerus, forearm surgery rates per 100,000 population per year |

**Procedure codes (examples, manuscript Methods):**  
大腿骨・上腕骨・前腕骨の骨折関連手術コード（K044–K082 系；詳細は `00_manuscript_mainline_pipeline.py` 内 `target_codes`）。

**Rate calculation:**  
`(sum of relevant surgery counts) / (prefecture population from census) × 100,000`.

### 1.2 Specific Health Checkup (covariate) / 特定健診（共変量）

| Item | Value |
|------|--------|
| Category | `07_特定健診 質問票` |
| Subfolder | `01_公費レセプトを含まないデータ` |
| File (mainline) | `標準的な質問票（質問項目１２） 都道府県別性年齢階級別分布.xlsx` |
| Variable | Q12 fast walking: “はい” proportion among ages 65–74 (prefecture-level) |
| Manuscript label | Fast-walking proportion (Reiwa 4 tabulation) |

**Note:** Public open data for this covariate are often limited to ages **40–74** at prefecture resolution; see manuscript Limitations.

---

## 2. Population and area statistics / 人口・面積（2020年国勢調査）

| Item | Details |
|------|---------|
| Provider | Statistics Bureau of Japan (e-Stat) / 総務省統計局 |
| Portal | https://www.e-stat.go.jp/ |
| Dataset | 2020 Population Census — prefecture totals |
| Variables | `total_pop`, `aging_rate` (≥65 / total), `pop_density` (persons/km²) |
| Project file | `03_Analysis/data/interim/statistics_2020.csv` (built locally or from `data/release/`) |

**Land area:** Prefecture area from e-Stat / national tables (for density). Document the table ID in `statistics_2020` provenance when rebuilding.

---

## 3. Terrain slope (exposure) / 地形傾斜（曝露）

| Item | Details |
|------|---------|
| Provider | Geospatial Information Authority of Japan (GSI) / 国土地理院 |
| DEM | National 10-m (or 5-m) elevation grids — 基盤地図情報・数値標高モデル |
| Download | https://fgd.gsi.go.jp/download/menu.php |
| Manuscript metric | **Habitable-area-weighted mean slope** (degrees) |
| Released derivative | `data/release/prefecture_habitable_slope.csv` |
| Full pipeline | `03_Analysis/scripts/36_recalculate_slope_habitable.py` (requires land-use mask; large downloads) |

**Habitable weighting:** Residential, agricultural, and commercial land classes (see Methods); excludes uninhabited steep mountain area where configured in mask pipeline.

**Do not commit:** Multi-GB GeoTIFF/XML tiles (see `.gitignore`).

---

## 4. What we deposit vs what you download / デポジットと取得の分担

| Data product | In GitHub `data/release/` | In Zenodo `v1.0.0` | User must download |
|--------------|----------------------------|--------------------|--------------------|
| `analysis_dataset_prefecture_n47.csv` | Yes (planned) | Yes | — |
| `prefecture_habitable_slope.csv` | Yes (planned) | Yes | — (or rebuild from GSI) |
| NDB raw `.xlsx` | No | No | Yes (portal) |
| DEM rasters | No | No | Yes (GSI) |
| Census microdata | No | No | Use e-Stat tables |

---

## 5. Licenses and attribution / ライセンス・引用

| Source | Typical use condition |
|--------|------------------------|
| NDB Open Data | Free for research; **cite MHLW portal and survey round**; no re-sharing of raw files |
| e-Stat | Follow portal terms; cite table name and retrieval date |
| GSI geodata | Follow GSI terms of use; cite product name and version |

**Recommended citation sentence (manuscript Data availability):**  
Prefecture-level values can be reproduced from the above public sources using scripts in this repository and the Zenodo DOI.

---

## 6. Local path configuration / ローカルパス

Copy `config/config.yaml.example` → `config/config.local.yaml` and set:

```yaml
paths:
  ndb_fracture_xlsx: "/path/to/款別都道府県別算定回数.xlsx"
  ndb_walking_xlsx: "/path/to/標準的な質問票（質問項目１２）...xlsx"
  census_csv: "03_Analysis/data/interim/statistics_2020.csv"
  habitable_slope_csv: "data/release/prefecture_habitable_slope.csv"
```

Paths may point to a sibling `NDB_Research_Hub/02_Data/raw/` tree if you use the Hub monorepo layout.

---

## 7. Related internal docs / 内部参照（レガシー）

| File | Note |
|------|------|
| `docs/DATA_LOCATIONS.md` | Machine-specific paths (2026-02); verify against this file before reuse |
| `config/config.yaml` | Project defaults; may reference Hub-relative paths |

**Last updated:** 2026-05-21
