# Reproduction Guide / 再現手順書

**Project:** `NDB_XXX_slope_fracture`  
**Manuscript:** *Association between Terrain Slope and Hip Fracture Surgery Rates Among Older Adults: A Nationwide Ecological Study in Japan*  
**Repository:** https://github.com/haruki00430/NDB_XXX_slope_fracture  
**Archive DOI (reserved):** `10.5281/zenodo.XXXXXXX` — replace before submission.

This guide describes how to reproduce the **prefecture-level aggregated analysis (N = 47)** reported in the manuscript.  
本書は論文に報告した **47都道府県の集計解析** を再現する手順です。

---

## What this repository includes / 含むもの・含まないもの

| Included | Not included (download separately) |
|----------|-----------------------------------|
| Analysis scripts (`03_Analysis/scripts/`) | NDB raw Excel (MHLW portal) |
| `data/release/*.csv` (N = 47 tables, when committed) | Full national DEM rasters (GSI) |
| `REPRODUCE.md`, `DATA_SOURCES.md` | Individual-level claims |
| Key result summaries under `results/` (optional) | Files > 100 MB (GitHub limit) |

Under MHLW rules, **individual-level claims cannot be redistributed**. Prefecture-level values in `data/release/` are derived from public open data only.

---

## System requirements / システム要件

| Item | Requirement |
|------|-------------|
| Python | 3.10 or later (3.11+ tested on Windows) |
| OS | Windows 10/11, macOS 12+, Ubuntu 20.04+ |
| RAM | 8 GB minimum (16 GB if rebuilding slope from DEM) |
| Disk | ~2 GB for NDB Excel + interim files; **>50 GB** if rebuilding national DEM pipeline |

---

## Step 0: Clone and environment / 環境構築

```bash
git clone https://github.com/haruki00430/NDB_XXX_slope_fracture.git
cd NDB_XXX_slope_fracture

python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

### Path configuration / パス設定

```bash
cp config/config.yaml.example config/config.local.yaml
# Edit: ndb_fracture_xlsx, ndb_walking_xlsx, census_csv, habitable_slope_csv
```

`00_manuscript_mainline_pipeline.py` reads all input paths from `config/config.local.yaml` (or `config/config.yaml`). For a **minimal reproduce** without NDB downloads, use Route 1 (release bundle only).

---

## Route 1 — Minimal reproduce (recommended for reviewers) / 最小再現（推奨）

Uses committed **`data/release/`** files only. No NDB download required.

### 1.1 Verify release files

| File | Rows | Role |
|------|------|------|
| `data/release/analysis_dataset_prefecture_n47.csv` | 47 | Final analysis table (outcomes + covariates + slope) |
| `data/release/prefecture_habitable_slope.csv` | 47 | Habitable-area-weighted mean slope (degrees) |
| `data/release/variable_dictionary.json` | — | Column definitions and units |

### 1.2 Run regression reproduction

```bash
python 03_Analysis/scripts/reproduce_from_release.py
```

**Expected headline checks** (tolerance as in mainline):

| Quantity | Expected | Tolerance |
|----------|----------|-----------|
| N prefectures | 47 | exact |
| Mean habitable slope (°) | 8.57 | ±0.02 |
| Mean hip surgery rate (/100k) | 254.0 | ±0.1 |
| Model 1 slope coefficient | 5.65 | ±0.02 |
| Model 2 slope coefficient | 3.49 | ±0.02 |

Outputs: `03_Analysis/results/reproduce_release/` (correlation matrix, regression text, diagnostic figure).

### 1.3 Compare with Zenodo archive

The Zenodo deposit (`v1.0.0`) mirrors `data/release/` plus frozen script hashes. Cite the DOI in any derivative work.

---

## Route 2 — Full rebuild from public sources / 公式データからのフル再構築

Follow **`DATA_SOURCES.md`** to download:

1. NDB Open Data No.10 — fracture surgery counts (医科診療行為 / 手術)  
2. NDB Open Data No.10 — Specific Health Checkup Q12 fast walking (特定健診 質問票)  
3. e-Stat / census 2020 — population, aging rate, density  
4. GSI — habitable-area-weighted slope (or use `data/release/prefecture_habitable_slope.csv` if DEM rebuild is skipped)

### 2.1 Manuscript mainline (single entry point)

```bash
# Prerequisites:
# - 03_Analysis/data/interim/statistics_2020.csv  (47 rows; census merge)
# - results/statistics/prefecture_habitable_slope.csv  (or path in config)
# - NDB Excel paths configured (see DATA_SOURCES.md §1)

python 03_Analysis/scripts/00_manuscript_mainline_pipeline.py
```

**Pipeline steps (internal):**

1. Extract fracture surgery by site (hip / humerus / forearm) from NDB Excel  
2. Extract fast-walking proportion (Q12) from NDB Excel  
3. Load `statistics_2020.csv` (census denominators and covariates)  
4. Merge → `03_Analysis/data/processed/analysis_dataset_v1.csv`  
5. OLS models, HC3, bootstrap (5000), figures → `03_Analysis/results/`  
6. `verify_headline()` against manuscript constants  

### 2.2 DEM / slope rebuild (optional, advanced)

Large geospatial workflow under `03_Analysis/scripts/35–37_*`, `36_recalculate_slope_habitable.py`.  
Not required if using released `prefecture_habitable_slope.csv`. See `docs/DATA_LOCATIONS.md` (legacy paths).

### 2.3 Manuscript figures and tables

```bash
python 03_Analysis/scripts/09_regression_diagnostics_and_sensitivity.py
python 03_Analysis/scripts/10_create_prefecture_maps.py
# Quarto (optional):
quarto render 04_Manuscripts/Manuscript_slope_fracture.qmd
```

---

## Zenodo ↔ GitHub release workflow / リリース手順（運用メモ）

1. Tag `v1.0.0` on GitHub after public repository check (no secrets, no raw NDB).  
2. Enable **Zenodo–GitHub integration** for `haruki00430/NDB_XXX_slope_fracture`.  
3. Upload or auto-archive per `docs/ZENODO_DEPOSIT_MANIFEST.md`.  
4. Reserve DOI early; replace `XXXXXXX` in `04_Manuscripts/Manuscript_slope_fracture.qmd` § Data availability.  
5. Publish Zenodo record when journal policy allows (may follow acceptance).

---

## Troubleshooting / トラブルシュート

| Issue | Action |
|-------|--------|
| `statistics_2020.csv` missing | Build via `03_Analysis/scripts/01_fetch_census_data.py` or copy from Zenodo `data/release/` |
| Headline β mismatch | Confirm Reiwa 5 NDB round and same surgery code set as Methods |
| `*.csv` not tracked by git | Only `data/release/*.csv` is whitelisted; see `.gitignore` |
| Encoding errors on Windows | Scripts use UTF-8; run `chcp 65001` or Python 3.10+ |

---

## Citation / 引用

If you use this repository or the Zenodo archive, cite:

- Software/code: GitHub repository URL + Zenodo DOI (see `CITATION.cff`).  
- Data: MHLW NDB Open Data portal + e-Stat + GSI (see `DATA_SOURCES.md`).

---

## Document map / 関連ドキュメント

| File | Purpose |
|------|---------|
| `DATA_SOURCES.md` | Official download URLs and file names |
| `docs/ZENODO_DEPOSIT_MANIFEST.md` | Files bundled in Zenodo `v1.0.0` |
| `data/release/README.md` | Column-level dictionary for N = 47 CSV |
| `03_Analysis/scripts/README.md` | Plain-English guide to each public Python script |
| `CITATION.cff` | Machine-readable citation metadata |
| `config/config.yaml.example` | Local path template (no secrets) |

**Last updated:** 2026-05-21
