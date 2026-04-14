# Supplementary Methods (Reproducibility for Figures)

## S1. Figure-generation scripts and outputs

- Figure 1 (`scatter_slope_fracture.png`): `03_Analysis/scripts/regen_scatter_figure1_english.py`
- Figure 2 (`heatmap_correlation.png`): `03_Analysis/scripts/07_correlation_analysis.py` (also reproducible via `10_run_complete_analysis.py`)
- Figures 3-5 (`fig_map_slope.png`, `fig_map_fracture.png`, `fig_map_bivariate.png`): `03_Analysis/scripts/10_create_prefecture_maps.py`

## S2. Inputs and execution order

Primary processed dataset:
- `03_Analysis/data/processed/analysis_dataset_v1.csv`

Additional geospatial input for maps:
- `02_Data/raw/GIS/japan.geojson`

Representative command sequence (from project root):

```bash
python "projects/NDB_XXX_slope_fracture/03_Analysis/scripts/regen_scatter_figure1_english.py"
python "projects/NDB_XXX_slope_fracture/03_Analysis/scripts/07_correlation_analysis.py"
python "projects/NDB_XXX_slope_fracture/03_Analysis/scripts/10_create_prefecture_maps.py"
```

## S3. Software environment used for figure generation

- Python 3.14.2
- pandas 2.3.3
- numpy 2.3.5
- matplotlib 3.10.8
- seaborn 0.13.2
- scipy 1.16.3
- geopandas 1.1.2
- japanize_matplotlib 1.1.3

## S4. Randomness and reproducibility

No stochastic image-generation step was used for Figure 1-5 production. The plotting workflow is deterministic given the same input files and software environment; therefore, random-seed fixation is not applicable to the figure-rendering scripts listed above.

## S5. Resolution and export settings

- Figure 1, Figure 2: exported with `dpi=300`
- Figure 3-5: exported with `dpi=180` in the current map script configuration (`10_create_prefecture_maps.py`)

