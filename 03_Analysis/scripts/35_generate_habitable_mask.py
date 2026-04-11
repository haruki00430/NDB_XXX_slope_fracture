
import pandas as pd
import geopandas as gpd
import os
import sys
import zipfile
import shutil
import glob

# UTF-8 Output
sys.stdout.reconfigure(encoding='utf-8')

# Paths
PROJECT_DIR = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture"
L03_DIR = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\02_Data\raw\MLIT\L03_b_Land_Use"
TEMP_DIR = os.path.join(PROJECT_DIR, "data", "temp_l03")
OUTPUT_FILE = os.path.join(PROJECT_DIR, "03_Analysis", "data", "interim", "habitable_mask.csv")

# Habitable Codes (2021 definition)
# 0100: Rice Field
# 0200: Farm
# 0500: Building
# 0600: Road
# 0700: Railway
# 0901: Other Site
# 0902: Park
HABITABLE_CODES = ['0100', '0200', '0500', '0600', '0700', '0901', '0902']

def get_4th_mesh_code(mesh_100m):
    """
    Convert 100m mesh code (10 digits) to 4th mesh code (9 digits).
    100m Mesh: AABBCCDDYX (Y: Lat index 0-9, X: Lon index 0-9 within 3rd mesh)
    4th Mesh: AABBCCDDM
    
    Mapping 100m (Y, X) to 4th Mesh M:
    Y in 0-4, X in 0-4 -> M=1 (SW)
    Y in 0-4, X in 5-9 -> M=2 (SE)
    Y in 5-9, X in 0-4 -> M=3 (NW)
    Y in 5-9, X in 5-9 -> M=4 (NE)
    """
    s = str(mesh_100m)
    if len(s) != 10:
        return None
    
    base_code = s[:8] # 3rd mesh
    y = int(s[8])
    x = int(s[9])
    
    if 0 <= y <= 4:
        if 0 <= x <= 4:
            m = '1'
        else:
            m = '2'
    else: # 5 <= y <= 9
        if 0 <= x <= 4:
            m = '3'
        else:
            m = '4'
            
    return base_code + m

def process_all():
    print("=== Start Generating Habitable Mask ===")
    
    # Init accumulator
    # Key: 4th Mesh Code, Value: {total: 0, habitable: 0}
    mesh_stats = {}
    
    # 1. Find Zips
    zip_pattern = os.path.join(L03_DIR, "L03-b-21_*.zip")
    zip_files = glob.glob(zip_pattern)
    print(f"Found {len(zip_files)} zip files.")
    
    if not zip_files:
        print("No L03-b-21 files found. Please check directory.")
        return

    os.makedirs(TEMP_DIR, exist_ok=True)
    
    count_processed = 0
    
    for zip_path in zip_files:
        count_processed += 1
        if count_processed % 10 == 0:
            print(f"Processing {count_processed}/{len(zip_files)}: {os.path.basename(zip_path)}")
            
        # Clean Temp
        for f in os.listdir(TEMP_DIR):
            try:
                os.remove(os.path.join(TEMP_DIR, f))
            except:
                pass
                
        # Extract
        try:
            with zipfile.ZipFile(zip_path, 'r') as z:
                z.extractall(TEMP_DIR)
        except Exception as e:
            print(f"Error unpacking {zip_path}: {e}")
            continue
            
        # Find SHP
        shp_files = [f for f in os.listdir(TEMP_DIR) if f.endswith('.shp')]
        if not shp_files:
            continue
            
        target_shp = os.path.join(TEMP_DIR, shp_files[0])
        
        # Read Attributes Only (ignore_geometry=True is faster)
        try:
            df = gpd.read_file(target_shp, ignore_geometry=True, encoding='cp932')
            
            # Columns check
            # Usually 'L03b_002' is code, 'L03b_001' is mesh code?
            # Or standard mesh code might be implicit? 
            # In N03/L03, mesh code often IS a column.
            # Step 803 output implies code column exists.
            
            # Heuristic for columns
            code_col = 'L03b_002'
            mesh_col = 'L03b_001' # Assuming this. If not, we check.
            
            if code_col not in df.columns:
                # Fallback search
                for c in df.columns:
                    if '002' in c: code_col = c
                    if '001' in c: mesh_col = c
            
            if code_col not in df.columns:
                print(f"Skipping {zip_path}: Code column not found. Cols: {df.columns.tolist()}")
                continue
                
            # Filter valid rows
            # Calculate 4th mesh code
            # Vectorized approach for speed
            
            # We iterate rows or use apply. For 25xN rows, apply is fine.
            # But wait, 100m mesh code logic needs verify.
            # Values in 'mesh_col' might be strings.
            
            for _, row in df.iterrows():
                m100 = str(row[mesh_col])
                land_code = str(row[code_col])
                
                m4 = get_4th_mesh_code(m100)
                if not m4: continue
                
                is_habitable = 1 if land_code in HABITABLE_CODES else 0
                
                if m4 not in mesh_stats:
                    mesh_stats[m4] = {'total': 0, 'habitable': 0}
                
                mesh_stats[m4]['total'] += 1
                mesh_stats[m4]['habitable'] += is_habitable
                
        except Exception as e:
            print(f"Error reading shp in {zip_path}: {e}")
            continue

    # Clean up temp
    shutil.rmtree(TEMP_DIR, ignore_errors=True)
    
    # 2. Convert to DataFrame
    print("Aggregating results...")
    results = []
    for m4, stats in mesh_stats.items():
        ratio = stats['habitable'] / stats['total'] if stats['total'] > 0 else 0
        results.append({
            'mesh_code': m4,
            'habitable_ratio': ratio,
            'total_100m_cells': stats['total'],
            'habitable_100m_cells': stats['habitable']
        })
        
    df_result = pd.DataFrame(results)
    
    # 3. Save
    print(f"Saving {len(df_result)} entries to {OUTPUT_FILE}")
    df_result.to_csv(OUTPUT_FILE, index=False)
    
    print("\n--- Preview ---")
    print(df_result.head().to_string(index=False))
    
    print("\n--- Statistics ---")
    print(f"Average Habitable Ratio: {df_result['habitable_ratio'].mean():.4f}")
    print(f"Fully Habitable Meshes: {len(df_result[df_result['habitable_ratio'] == 1.0])}")
    print(f"Fully Non-Habitable Meshes: {len(df_result[df_result['habitable_ratio'] == 0.0])}")

if __name__ == "__main__":
    process_all()
