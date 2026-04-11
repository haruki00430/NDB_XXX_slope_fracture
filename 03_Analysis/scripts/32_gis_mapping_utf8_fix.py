
import geopandas as gpd
import pandas as pd
from shapely.geometry import box
import os
import sys

# UTF-8 Output
sys.stdout.reconfigure(encoding='utf-8')

# Paths
PROJECT_DIR = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture"
SHP_FILE = os.path.join(PROJECT_DIR, "data", "raw", "MLIT_N03", "N03-20240101.shp")
MESH_FILE = os.path.join(PROJECT_DIR, "03_Analysis", "data", "interim", "mesh_coordinates.csv")
OUTPUT_FILE = os.path.join(PROJECT_DIR, "03_Analysis", "data", "interim", "mesh_prefecture_mapping_verified_v2.csv")

def run_mapping():
    print("=== Start GIS Mapping (UTF-8) ===")
    
    # 1. Load Shapefile (Force UTF-8 based on investigation)
    print(f"Loading Shapefile: {os.path.basename(SHP_FILE)}")
    try:
        gdf_pref = gpd.read_file(SHP_FILE, encoding='utf-8')
        print(f"Loaded {len(gdf_pref)} polygons.")
        print(f"Sample Prefectures: {gdf_pref['N03_001'].unique()[:5]}") # Should be correct Japanese
    except Exception as e:
        print(f"Error loading shapefile: {e}")
        return

    # 2. Load Mesh
    print(f"Loading Mesh: {os.path.basename(MESH_FILE)}")
    df_mesh = pd.read_csv(MESH_FILE)
    print(f"Loaded {len(df_mesh)} meshes.")
    
    # 3. Spatial Join
    print("Creating mesh geometries...")
    geoms = [box(r['west_lon'], r['south_lat'], r['east_lon'], r['north_lat']) for _, r in df_mesh.iterrows()]
    gdf_mesh = gpd.GeoDataFrame(df_mesh, geometry=geoms, crs=gdf_pref.crs)
    
    print("Performing Spatial Join...")
    # join_result = gpd.sjoin(gdf_mesh, gdf_pref[['N03_001', 'geometry']], how='left', predicate='intersects')
    # Using 'inner' to check coverage? No 'left' to find empty ones.
    # But N03 covers all Japan?
    join_result = gpd.sjoin(gdf_mesh, gdf_pref[['N03_001', 'geometry']], how='left', predicate='intersects')
    
    # 4. Aggregation
    print("Aggregating results...")
    mesh_pref_map = {}
    for mesh_code, group in join_result.groupby('mesh_code'):
        # Get unique prefs, drop NA
        prefs = group['N03_001'].dropna().unique().tolist()
        prefs.sort()
        mesh_pref_map[mesh_code] = prefs
        
    # 5. Create Result DataFrame
    results = []
    for _, row in df_mesh.iterrows():
        mesh_code = row['mesh_code']
        prefs = mesh_pref_map.get(mesh_code, [])
        
        results.append({
            'mesh_code': mesh_code,
            'center_lat': row['center_lat'],
            'center_lon': row['center_lon'],
            'prefectures': ', '.join(prefs) if prefs else '海域/国外',
            'pref_count': len(prefs)
        })
        
    df_result = pd.DataFrame(results)
    
    # 6. Save
    print(f"Saving to {os.path.basename(OUTPUT_FILE)}...")
    df_result.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')
    
    # Verification Print
    print("\n--- Verification of Generated File ---")
    print(df_result[['mesh_code', 'prefectures']].head(10).to_string(index=False))
    
    hokkaido = df_result[df_result['prefectures'].str.contains('北海道')]
    print(f"\nHokkaido meshes: {len(hokkaido)}")

if __name__ == "__main__":
    run_mapping()
