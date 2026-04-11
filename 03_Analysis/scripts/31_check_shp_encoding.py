
import geopandas as gpd
import os
import sys

# UTF-8 Encoding for Windows Console
sys.stdout.reconfigure(encoding='utf-8')

SHP_FILE = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture\data\raw\MLIT_N03\N03-20240101.shp"

def check_encoding():
    print(f"Checking encoding for: {os.path.basename(SHP_FILE)}")
    
    # Try CP932 (Shift-JIS) - Traditional
    try:
        print("\n--- Trying CP932 (Shift-JIS) ---")
        gdf = gpd.read_file(SHP_FILE, encoding='cp932', rows=5)
        print(gdf[['N03_001', 'N03_002', 'N03_003', 'N03_004']].head())
    except Exception as e:
        print(f"Error reading as CP932: {e}")

    # Try UTF-8 - Modern
    try:
        print("\n--- Trying UTF-8 ---")
        gdf = gpd.read_file(SHP_FILE, encoding='utf-8', rows=5)
        print(gdf[['N03_001', 'N03_002', 'N03_003', 'N03_004']].head())
    except Exception as e:
        print(f"Error reading as UTF-8: {e}")

if __name__ == "__main__":
    check_encoding()
