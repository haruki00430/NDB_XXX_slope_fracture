# Analysis scripts (public release)

English descriptions for readers who are **not Python experts**.  
For full reproduction steps, see [`../../REPRODUCE.md`](../../REPRODUCE.md).

---

## Scripts included in the GitHub / Zenodo release

| Script | What it does (in plain language) |
|--------|----------------------------------|
| [`reproduce_from_release.py`](reproduce_from_release.py) | **Start here for a quick check.** Loads the small public CSV (47 prefectures), re-runs the main regression, and checks that key numbers match the paper (mean slope 8.57°, hip rate 254, etc.). No download of raw NDB files needed. |
| [`export_release_bundle.py`](export_release_bundle.py) | **For maintainers.** Copies the final 47-row analysis table into `data/release/` for Zenodo and GitHub, plus a small “provenance” JSON (date, git version). |
| [`00_manuscript_mainline_pipeline.py`](00_manuscript_mainline_pipeline.py) | **Full rebuild.** Reads raw NDB Excel (fracture surgery counts, walking survey), merges census and terrain slope, runs regressions and diagnostic plots, and verifies headline results. Copy `config/config.yaml.example` → `config/config.local.yaml` and set paths (see `DATA_SOURCES.md`). |
| [`09_regression_diagnostics_and_sensitivity.py`](09_regression_diagnostics_and_sensitivity.py) | **Extra statistics for the paper.** Checks regression assumptions (residual plots), robust standard errors (HC3), and bootstrap confidence intervals for the slope–hip association. |
| [`10_create_prefecture_maps.py`](10_create_prefecture_maps.py) | **Maps for Figure 2.** Draws Japan prefecture maps: terrain slope, hip surgery rate, and a combined two-variable map. Needs a GeoJSON boundary file and the analysis CSV. |

---

## Suggested order

```text
1. reproduce_from_release.py     ← reviewers / quick validation
2. export_release_bundle.py      ← before Zenodo v1.0.0 (after full pipeline)
3. 00_manuscript_mainline_pipeline.py   ← only if rebuilding from MHLW + GSI sources
4. 09_regression_diagnostics_and_sensitivity.py   ← optional supplementary stats
5. 10_create_prefecture_maps.py  ← optional figures
```

---

## Other scripts in this folder

Numbered scripts (`01_`–`37_`, etc.) are **development and geospatial pipeline** steps (DEM tiles, mesh mapping, exploratory runs). They are **not** required for the minimal Zenodo bundle unless you rebuild terrain slope from national elevation grids. See [`../../docs/DATA_LOCATIONS.md`](../../docs/DATA_LOCATIONS.md) (legacy paths).

---

## Language policy

All **public-release** Python files use **English** module headers, function docstrings, and user-facing messages so international readers and journals can follow the workflow without reading code syntax.
