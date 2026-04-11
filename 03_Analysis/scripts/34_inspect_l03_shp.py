
import geopandas as gpd
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

TEMP_DIR = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture\data\temp"

target_shp = os.path.join(TEMP_DIR, "L03-b-21_5339.shp")
print(f"Inspecting: {target_shp}")

try:
    gdf = gpd.read_file(target_shp, encoding='cp932') # Default for Japanese SHP
    print("\n--- Columns ---")
    cols = gdf.columns.tolist()
    print(cols)
    
    # Identify Land Use Column (usually the second one or named 'L03b_xxx')
    # Based on snippet "3923040004 0", it might be raw codes.
    
    print("\n--- First 5 rows ---")
    print(gdf.head().to_string())
    
    # Try to find code column
    # Typically 'L03b_002' or similar
    target_col = None
    for c in cols:
        if '002' in c or 'code' in c.lower():
            target_col = c
            break
            
    if target_col:
        print(f"\n--- Unique Values in {target_col} ---")
        print(gdf[target_col].unique())
    else:
        print("\nCould not identify code column automatically. Please check columns above.")
except Exception as e:
    print(f"Failed to read SHP: {e}")
