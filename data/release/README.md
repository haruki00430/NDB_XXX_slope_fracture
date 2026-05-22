# Public release data (`data/release/`)

**Scope:** Prefecture-level aggregated tables only (**N = 47**).  
**Not included:** NDB raw Excel, individual-level records, national DEM rasters.

These files are intended for **GitHub** (small CSV exception) and **Zenodo v1.0.0** deposition.  
See `DATA_SOURCES.md` for primary data download URLs.

---

## Files

| File | Description |
|------|-------------|
| `analysis_dataset_prefecture_n47.csv` | Analysis-ready table (outcomes, covariates, slope) |
| `prefecture_habitable_slope.csv` | Exposure: habitable-area-weighted mean slope (degrees) |
| `variable_dictionary.json` | Column names, types, units, source round |
| `provenance.json` | Build metadata (date, git commit, script version) |

---

## Key columns (`analysis_dataset_prefecture_n47.csv`)

| Column | Unit / type | Source |
|--------|-------------|--------|
| `prefecture` | text | 47 prefectures (Japanese name) |
| `total_pop` | persons | 2020 census |
| `aging_rate` | % | 2020 census (≥65 / total) |
| `pop_density` | per km² | 2020 census |
| `femur_rate` | per 100,000 / year | NDB Reiwa 5 surgery counts |
| `humerus_rate` | per 100,000 / year | NDB Reiwa 5 |
| `forearm_rate` | per 100,000 / year | NDB Reiwa 5 |
| `fast_walking_rate` | % | NDB Reiwa 4 Specific Health Checkup Q12 |
| `habitable_slope_weighted` | degrees | GSI DEM + habitable mask |

---

## Regenerate before Zenodo upload

```bash
python 03_Analysis/scripts/export_release_bundle.py
```

**Last updated:** 2026-05-21
