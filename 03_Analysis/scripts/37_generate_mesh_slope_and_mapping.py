import os
import sys
import glob
import zipfile
import re
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, box

# UTF-8 Output configuration
sys.stdout.reconfigure(encoding='utf-8')

# --- Configuration ---
PROJECT_DIR = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture"
DEM_DIR = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\02_Data\raw\MLIT\G04_c_Elevation"
LAB_MASK_FILE = os.path.join(PROJECT_DIR, "data", "interim", "habitable_mask.csv")
PREF_SHP_DIR = os.path.join(PROJECT_DIR, "data", "raw", "MLIT_N03")
OUTPUT_FILE = os.path.join(PROJECT_DIR, "data", "interim", "slope_by_mesh_final.csv")

# Constants for Mesh Calculation
LAT_1ST_LEN = 2/3
LON_1ST_LEN = 1.0
LAT_2ND_LEN = LAT_1ST_LEN / 8
LON_2ND_LEN = LON_1ST_LEN / 8
LAT_3RD_LEN = LAT_2ND_LEN / 10
LON_3RD_LEN = LON_2ND_LEN / 10
LAT_4TH_LEN = LAT_3RD_LEN / 2
LON_4TH_LEN = LON_3RD_LEN / 2

def get_mesh_bounds(mesh_code):
    """
    Calculate bounds (south, north, west, east) for a 4th mesh code (9 digits).
    """
    s = str(mesh_code)
    if len(s) != 9:
        return None
    
    # 1st Mesh (4 digits)
    aa = int(s[0:2])
    bb = int(s[2:4])
    lat_1st_s = aa * LAT_1ST_LEN
    lon_1st_w = 100 + bb * LON_1ST_LEN
    
    # 2nd Mesh (2 digits)
    c1 = int(s[4])
    c2 = int(s[5])
    lat_2nd_s = lat_1st_s + c1 * LAT_2ND_LEN
    lon_2nd_w = lon_1st_w + c2 * LON_2ND_LEN
    
    # 3rd Mesh (2 digits)
    d1 = int(s[6])
    d2 = int(s[7])
    lat_3rd_s = lat_2nd_s + d1 * LAT_3RD_LEN
    lon_3rd_w = lon_2nd_w + d2 * LON_3RD_LEN
    
    # 4th Mesh (1 digit)
    e = int(s[8])
    # 1: SW, 2: SE, 3: NW, 4: NE
    # Lat offset: 1,2 -> 0; 3,4 -> 1
    # Lon offset: 1,3 -> 0; 2,4 -> 1
    
    lat_off = 1 if e in [3, 4] else 0
    lon_off = 1 if e in [2, 4] else 0
    
    lat_s = lat_3rd_s + lat_off * LAT_4TH_LEN
    lon_w = lon_3rd_w + lon_off * LON_4TH_LEN
    
    lat_n = lat_s + LAT_4TH_LEN
    lon_e = lon_w + LON_4TH_LEN
    
    return lat_s, lat_n, lon_w, lon_e

def load_prefecture_polygons():
    """Load N03 Prefecture Polygons."""
    # Find the prefecture shapefile
    # Prefer 'prefecture.shp' variants if available for faster processing
    candidates = glob.glob(os.path.join(PREF_SHP_DIR, "*_prefecture.shp"))
    if not candidates:
        candidates = glob.glob(os.path.join(PREF_SHP_DIR, "*.shp"))
        
    if not candidates:
        raise FileNotFoundError(f"No shapefiles found in {PREF_SHP_DIR}")
        
    target_shp = candidates[0]
    print(f"Loading Prefecture Polygons: {os.path.basename(target_shp)}")
    
    try:
        gdf = gpd.read_file(target_shp, encoding='utf-8')
    except:
        gdf = gpd.read_file(target_shp, encoding='cp932')
        
    # Ensure columns. N03_001 is prefecture name.
    # N03-2024 format: N03_001
    return gdf[['N03_001', 'geometry']]

def parse_g04_xmls():
    """
    Parse all G04-c XML files to extract Mesh Code and Avg Slope.
    Returns: DataFrame
    """
    print("Parsing G04-c XML files...")
    
    zip_files = glob.glob(os.path.join(DEM_DIR, "*.zip"))
    print(f"Found {len(zip_files)} zip files.")
    
    data_list = []
    
    for i, zpath in enumerate(zip_files):
        if (i+1) % 10 == 0:
            print(f"Processing {i+1}/{len(zip_files)}...")
            
        try:
            with zipfile.ZipFile(zpath, 'r') as z:
                xmls = [f for f in z.namelist() if f.endswith('.xml') and 'META' not in f]
                if not xmls: continue
                
                with z.open(xmls[0]) as f:
                    content = f.read().decode('utf-8')
                    
                    # Extract ALL tupleList content blocks using regex
                    # The content inside tupleList contains the csv data
                    tuple_blocks = re.findall(r'<gml:tupleList>(.*?)</gml:tupleList>', content, re.DOTALL)
                    
                    for body in tuple_blocks:
                        lines = body.strip().split('\n')
                        
                        for line in lines:
                            parts = line.strip().split(',')
                            if len(parts) < 10: continue
                            
                            mesh_code = parts[0]
                            # Avg Slope is index 9 (10th item)
                            try:
                                avg_slope = float(parts[9])
                                data_list.append({
                                    'mesh_code': mesh_code,
                                    'avg_slope': avg_slope
                                })
                            except ValueError:
                                continue
                            
        except Exception as e:
            print(f"Error reading {os.path.basename(zpath)}: {e}")
            
    df = pd.DataFrame(data_list)
    return df

def main():
    print("=== Start Master Slope Data Generation ===")
    
    # 1. Parse G04-c Slope Data
    df_slope = parse_g04_xmls()
    print(f"Extracted {len(df_slope)} meshes with slope data.")
    
    # 2. Add Center Coordinates
    print("Calculating mesh coordinates...")
    # Calculate Lat/Lon center
    
    def get_center(code):
        bounds = get_mesh_bounds(code)
        if not bounds: return None, None
        s, n, w, e = bounds
        return (s + n) / 2, (w + e) / 2
        
    coords = df_slope['mesh_code'].apply(lambda x: get_center(x))
    df_slope['center_lat'] = coords.apply(lambda x: x[0])
    df_slope['center_lon'] = coords.apply(lambda x: x[1])
    
    # Drop invalid coordinates
    df_slope = df_slope.dropna(subset=['center_lat', 'center_lon'])
    
    # 3. Spatial Join with Prefectures
    print("Mapping meshes to prefectures (Spatial Join)...")
    gdf_pref = load_prefecture_polygons()
    
    # Convert slope df to GeoDataFrame
    geometry = [Point(xy) for xy in zip(df_slope['center_lon'], df_slope['center_lat'])]
    gdf_mesh = gpd.GeoDataFrame(df_slope, geometry=geometry, crs=gdf_pref.crs)
    
    # Spatial Join
    # 'intersects' or 'within'. Since we use center point, 'within' is appropriate.
    gdf_joined = gpd.sjoin(gdf_mesh, gdf_pref, how='left', predicate='within')
    
    # Rename and clean
    gdf_joined = gdf_joined.rename(columns={'N03_001': 'prefecture'})
    df_result = pd.DataFrame(gdf_joined.drop(columns=['geometry', 'index_right']))
    
    # Handle meshes not matched (e.g. over water bodies not in polygon)
    # We keep them but prefecture will be NaN.
    # Or should we use 'nearest'? No, 'within' is safer for attribution.
    
    matched_count = df_result['prefecture'].notnull().sum()
    print(f"Mapped {matched_count}/{len(df_result)} meshes to prefectures.")
    
    # 4. Merge with Habitable Mask
    print("Merging with Habitable Mask...")
    if os.path.exists(LAB_MASK_FILE):
        df_mask = pd.read_csv(LAB_MASK_FILE, dtype={'mesh_code': str})
        # Ensure mesh_code match
        # G04-c mesh_code might be int or str. df_slope['mesh_code'] came from XML parsing (str)
        # df_mask['mesh_code'] is str
        
        df_result['mesh_code'] = df_result['mesh_code'].astype(str)
        df_final = pd.merge(df_result, df_mask[['mesh_code', 'habitable_ratio']], on='mesh_code', how='left')
        
        # Fill NaN habitable_ratio with 0 (if not in mask, likely not habitable or no L03 data)
        # However, L03 covers whole Japan.
        df_final['habitable_ratio'] = df_final['habitable_ratio'].fillna(0)
    else:
        print("Warning: Habitable Mask file not found. Skipping merge.")
        df_final = df_result
        df_final['habitable_ratio'] = None
        
    # 5. Save
    print(f"Saving to {OUTPUT_FILE}...")
    df_final.to_csv(OUTPUT_FILE, index=False)
    print("Done.")

if __name__ == "__main__":
    main()
