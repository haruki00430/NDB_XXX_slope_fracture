
import pandas as pd
import geopandas as gpd
import os
import sys
import zipfile
import shutil
import glob
from concurrent.futures import ProcessPoolExecutor, as_completed
import time

# UTF-8 Output
sys.stdout.reconfigure(encoding='utf-8')

# Paths
PROJECT_DIR = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture"
L03_DIR = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\02_Data\raw\MLIT\L03_b_Land_Use"
TEMP_ROOT = os.path.join(PROJECT_DIR, "data", "temp_l03_parallel")
OUTPUT_FILE = os.path.join(PROJECT_DIR, "data", "interim", "habitable_mask.csv")

HABITABLE_CODES = ['0100', '0200', '0500', '0600', '0700', '0901', '0902']

def get_4th_mesh_code(mesh_100m):
    s = str(mesh_100m)
    if len(s) != 10: return None
    base_code = s[:8]
    y = int(s[8])
    x = int(s[9])
    
    if 0 <= y <= 4:
        if 0 <= x <= 4: m = '1'
        else: m = '2'
    else:
        if 0 <= x <= 4: m = '3'
        else: m = '4'
    return base_code + m

def process_single_zip(zip_path):
    pid = os.getpid()
    temp_dir = os.path.join(TEMP_ROOT, f"proc_{pid}")
    os.makedirs(temp_dir, exist_ok=True)
    
    mesh_stats = {}
    
    try:
        # Extract
        try:
            with zipfile.ZipFile(zip_path, 'r') as z:
                z.extractall(temp_dir)
        except Exception as e:
            return {}, f"Error unzip {os.path.basename(zip_path)}: {e}"
            
        # Find SHP
        shp_files = [f for f in os.listdir(temp_dir) if f.endswith('.shp')]
        if not shp_files:
            return {}, f"No SHP in {os.path.basename(zip_path)}"
            
        target_shp = os.path.join(temp_dir, shp_files[0])
        
        # Read
        try:
            df = gpd.read_file(target_shp, ignore_geometry=True, encoding='cp932')
            
            code_col = 'L03b_002'
            mesh_col = 'L03b_001'
            
            if code_col not in df.columns:
                for c in df.columns:
                    if '002' in c: code_col = c
                    if '001' in c: mesh_col = c
            
            if code_col not in df.columns:
                return {}, f"Col missing in {os.path.basename(zip_path)}: {df.columns.tolist()}"
            
            # Process
            # Use dictionary for speed
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
            return {}, f"Error read SHP {os.path.basename(zip_path)}: {e}"
            
    finally:
        # Clean specific temp
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except:
            pass
            
    return mesh_stats, None

def run_parallel():
    print("=== Start Generating Habitable Mask (Parallel) ===")
    start_time = time.time()
    
    if os.path.exists(TEMP_ROOT):
        shutil.rmtree(TEMP_ROOT, ignore_errors=True)
    os.makedirs(TEMP_ROOT, exist_ok=True)
    
    zip_pattern = os.path.join(L03_DIR, "L03-b-21_*.zip")
    zip_files = glob.glob(zip_pattern)
    print(f"Found {len(zip_files)} zip files.")
    
    if not zip_files:
        return

    # Master Accumulator
    final_stats = {}
    
    # Run
    # Adjust max_workers based on CPU
    max_workers = min(os.cpu_count(), 8)
    print(f"Using {max_workers} processes.")
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_single_zip, z): z for z in zip_files}
        
        completed_count = 0
        total = len(zip_files)
        
        for future in as_completed(futures):
            completed_count += 1
            if completed_count % 10 == 0:
                elapsed = time.time() - start_time
                print(f"[{elapsed:.1f}s] Completed {completed_count}/{total}")
                
            res_stats, error = future.result()
            if error:
                print(error)
            
            # Aggregate
            for m4, stats in res_stats.items():
                if m4 not in final_stats:
                    final_stats[m4] = {'total': 0, 'habitable': 0}
                final_stats[m4]['total'] += stats['total']
                final_stats[m4]['habitable'] += stats['habitable']

    # Cleanup Root Temp
    shutil.rmtree(TEMP_ROOT, ignore_errors=True)
    
    # Save
    print("Aggregating and Saving...")
    results = []
    for m4, stats in final_stats.items():
        ratio = stats['habitable'] / stats['total'] if stats['total'] > 0 else 0
        results.append({
            'mesh_code': m4,
            'habitable_ratio': ratio,
            'total_100m_cells': stats['total'],
            'habitable_100m_cells': stats['habitable']
        })
        
    df_result = pd.DataFrame(results)
    df_result.to_csv(OUTPUT_FILE, index=False)
    
    end_time = time.time()
    print(f"Finished in {end_time - start_time:.1f} seconds. Saved to {OUTPUT_FILE}")
    print(f"Rows: {len(df_result)}")

if __name__ == "__main__":
    run_parallel()
