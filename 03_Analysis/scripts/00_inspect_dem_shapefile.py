import geopandas as gpd
import pandas as pd
import sys

# ---------------------------------------------------------
# 設定: UTF-8出力
# ---------------------------------------------------------
sys.stdout.reconfigure(encoding='utf-8')

def inspect_shapefile():
    shp_path = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture\data\temp\inspect_dem\G04-c-11_5339-jgd_ElevationAndSlopeAngleFourthMesh.shp"
    print(f"Reading Shapefile: {shp_path}")
    
    try:
        gdf = gpd.read_file(shp_path)
        print("\n--- Columns ---")
        print(gdf.columns.tolist())
        
        print("\n--- First 5 rows ---")
        print(gdf.head())
        
        print("\n--- CRS ---")
        print(gdf.crs)
        
        # Check for Slope column
        slope_cols = [c for c in gdf.columns if 'slope' in c.lower() or 'angle' in c.lower()]
        print(f"\nPotential Slope Columns: {slope_cols}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect_shapefile()
