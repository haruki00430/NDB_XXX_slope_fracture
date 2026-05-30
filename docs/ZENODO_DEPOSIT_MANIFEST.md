# Zenodo Deposit Manifest (v1.0.0)

**Record type:** Software + dataset (prefecture-level aggregate, N = 47)  
**GitHub tag:** `v1.0.0`  
**DOI:** `10.5281/zenodo.20452953`  
**License:** Code MIT; data CC BY 4.0 (derived aggregates only)

---

## 1. Purpose / 目的

Bundle everything needed to:

1. Cite a **version-fixed** snapshot (Zenodo DOI).  
2. Reproduce manuscript headline statistics **without** NDB raw files (via `data/release/`).  
3. Document how to rebuild from MHLW / e-Stat / GSI primary sources (`DATA_SOURCES.md`).

**Do not upload:** NDB raw Excel, individual-level records, multi-GB DEM tiles, `.env`, machine-specific paths with usernames.

---

## 2. Required files (Zenodo archive) / 必須同梱

### 2.1 Metadata and policy

| Path | Description |
|------|-------------|
| `CITATION.cff` | Citation metadata (update DOI/ORCID at release) |
| `LICENSE` | MIT (code) — add if not present at release |
| `LICENSE-DATA` | CC BY 4.0 for `data/release/*.csv` (recommended separate file) |
| `README.md` | Project overview + badges (DOI, license) |
| `REPRODUCE.md` | Step-by-step reproduction |
| `DATA_SOURCES.md` | Official download URLs |
| `docs/ZENODO_DEPOSIT_MANIFEST.md` | This file |

### 2.2 Analysis code (manuscript mainline + minimal reproduce)

| Path | Description |
|------|-------------|
| `requirements.txt` | Python dependencies |
| `config/config.yaml.example` | Path template (no secrets) |
| `03_Analysis/scripts/00_manuscript_mainline_pipeline.py` | Full rebuild entry (NDB + slope + census) |
| `03_Analysis/scripts/README.md` | Plain-English descriptions of each public script |
| `03_Analysis/scripts/_utils.py` | Shared helpers (UTF-8 stdout, typed scalars) |
| `03_Analysis/scripts/reproduce_from_release.py` | **Minimal reproduce** from `data/release/` only |
| `03_Analysis/scripts/09_regression_diagnostics_and_sensitivity.py` | HC3 / bootstrap / diagnostics (optional) |
| `03_Analysis/scripts/10_create_prefecture_maps.py` | Figure 2 maps (optional; needs geodata) |

All public Python files use **English** module docstrings and user-facing messages (nejm-climate-medication-jp policy).

### 2.3 Released data (N = 47 only)

| Path | Rows | Size (est.) | Description |
|------|------|-------------|-------------|
| `data/release/README.md` | — | <5 KB | Data dictionary |
| `data/release/variable_dictionary.json` | — | <10 KB | Machine-readable column specs |
| `data/release/analysis_dataset_prefecture_n47.csv` | 47 | <20 KB | Final analysis table |
| `data/release/prefecture_habitable_slope.csv` | 47 | <5 KB | Exposure: habitable-weighted slope (°) |
| `data/release/provenance.json` | — | <5 KB | Source rounds, script git SHA, build date |

**Export command (maintainers, before tag):**

```bash
# From project root after successful mainline run:
python 03_Analysis/scripts/export_release_bundle.py
# Creates/updates data/release/* and provenance.json
```

*(Implement `export_release_bundle.py` before Zenodo upload; or copy manually from `03_Analysis/data/processed/analysis_dataset_v1.csv`.)*

### 2.4 Key numerical outputs (optional but recommended)

| Path | Description |
|------|-------------|
| `results/statistics/prefecture_habitable_slope.csv` | Source slope table (if identical to release, one copy suffices) |
| `03_Analysis/results/regression_results.txt` | Model summaries |
| `03_Analysis/results/regression_diagnostics_report.txt` | HC3 / bootstrap headline |
| `03_Analysis/results/correlation_matrix.csv` | Table S1 support |

### 2.5 Manuscript source (optional)

| Path | Description |
|------|-------------|
| `04_Manuscripts/Manuscript_slope_fracture.qmd` | Source manuscript (anonymized variant if under review) |
| `04_Manuscripts/references.bib` | Bibliography |

---

## 3. Explicitly excluded / 同梱禁止

| Pattern | Reason |
|---------|--------|
| `02_Data/raw/**` | NDB raw; MHLW redistribution prohibited |
| `**/NDB_OpenData/**/*.xlsx` | Same |
| `data/raw/DEM/**`, `*.tif`, large `*.xml` | Size; GSI re-download |
| `*.env`, `config/config.local.yaml` | Secrets / local paths |
| `.claude/`, `.cursor/`, `.venv/` | Tooling |
| Untracked DOCX with author comments | Review-only |
| `03_Analysis/scripts/2[0-9]_*.py` (exploratory DEM) | Optional “supplementary”; omit from v1.0.0 unless documented |

---

## 4. Zenodo metadata fields (suggested) / メタデータ案

| Field | Value |
|-------|--------|
| Title | Terrain slope and hip fracture surgery rates in Japan (NDB Open Data, N=47 prefectures) — code and data |
| Upload type | Software / Dataset |
| Description | Reproducible pipeline and prefecture-level aggregated dataset for ecological analysis. Raw NDB not included. |
| Keywords | hip fracture; ecological study; NDB; terrain; Japan; open science |
| License | MIT (code) + CC BY 4.0 (data release) |
| Related identifier | `https://github.com/haruki00430/NDB_XXX_slope_fracture` (isSupplementTo or isVersionOf) |
| Grant / funding | [fill at release] |

---

## 5. GitHub ↔ Zenodo integration checklist

- [ ] Repository public (or Zenodo manual upload from tag tarball)  
- [ ] Turn on Zenodo-GitHub integration for `haruki00430/NDB_XXX_slope_fracture`  
- [ ] Reserve DOI → update `CITATION.cff`, `Manuscript_slope_fracture.qmd` Data availability  
- [ ] Commit `data/release/*.csv` (`.gitignore` exception active)  
- [ ] Tag `v1.0.0` → confirm Zenodo build  
- [ ] Verify `reproduce_from_release.py` passes on clean clone  
- [ ] Add README badges: DOI + license  

---

## 6. Version history

| Version | Date | Notes |
|---------|------|-------|
| v1.0.0 | TBD | Initial public release aligned with manuscript submission |

**Last updated:** 2026-05-21
