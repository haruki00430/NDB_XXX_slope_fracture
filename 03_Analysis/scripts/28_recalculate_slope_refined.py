import pandas as pd
import os
import sys

# UTF-8 Encoding for Windows
sys.stdout.reconfigure(encoding='utf-8')

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------
PROJECT_DIR = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture"

# Inputs
MAPPING_FILE = os.path.join(PROJECT_DIR, "03_Analysis", "data", "interim", "mesh_prefecture_mapping_final_verified.csv")
MESH_SLOPE_FILE = os.path.join(PROJECT_DIR, "03_Analysis", "data", "interim", "slope_by_prefecture.csv")

# Output
OUTPUT_FILE = os.path.join(PROJECT_DIR, "03_Analysis", "data", "interim", "slope_by_prefecture_verified.csv")
REPORT_FILE = os.path.join(PROJECT_DIR, "03_Analysis", "data", "interim", "slope_verification_report.txt")
DEBUG_LOG = os.path.join(PROJECT_DIR, "03_Analysis", "scripts", "slope_recalc_debug.log")

def log(msg):
    print(msg)
    with open(DEBUG_LOG, 'a', encoding='utf-8') as f:
        f.write(str(msg) + "\n")

def recalculate_slope():
    # Clear log
    with open(DEBUG_LOG, 'w', encoding='utf-8') as f:
        f.write("=== Debug Log ===\n")

    log("=== Start Recalculating Slope by Prefecture (Verified Mapping) ===")
    
    # 1. Load Data
    log(f"Loading mapping from: {os.path.basename(MAPPING_FILE)}")
    try:
        df_map = pd.read_csv(MAPPING_FILE, encoding='utf-8')
        log(f"Mapping Columns: {list(df_map.columns)}")
        log(f"Mapping Head:\n{df_map.head().to_string()}")
    except Exception as e:
        log(f"Failed to load mapping: {e}")
        return

    log(f"Loading slope data from: {os.path.basename(MESH_SLOPE_FILE)}")
    try:
        df_slope = pd.read_csv(MESH_SLOPE_FILE, encoding='utf-8')
        log(f"Slope Columns: {list(df_slope.columns)}")
        log(f"Slope Head:\n{df_slope.head().to_string()}")
    except Exception as e:
        log(f"Failed to load slope data: {e}")
        return
    
    df_map['mesh_code'] = df_map['mesh_code'].astype(str)
    df_slope['mesh_code'] = df_slope['mesh2'].astype(str)
    
    # 2. Merge
    merged = pd.merge(df_map, df_slope, on='mesh_code', how='inner')
    log(f"Merged data: {len(merged)} meshes")
    if  len(merged) == 0:
        log("MERGE FAILED. No common mesh codes!")
        log(f"Map Mesh Types: {df_map['mesh_code'].dtype}")
        log(f"Slope Mesh Types: {df_slope['mesh_code'].dtype}")
        log(f"Sample Map Meshes: {df_map['mesh_code'].head().tolist()}")
        log(f"Sample Slope Meshes: {df_slope['mesh_code'].head().tolist()}")
        return

    # 3. Explode
    expanded_rows = []
    for _, row in merged.iterrows():
        pref_str = row['prefectures']
        if pd.isna(pref_str): continue
        # Handle mixed separators if any, but verify content
        prefs = [p.strip() for p in str(pref_str).replace('、', ',').split(',')]
        for pref in prefs:
            if not pref: continue
            new_row = row.to_dict()
            new_row['target_prefecture'] = pref
            expanded_rows.append(new_row)
            
    df_expanded = pd.DataFrame(expanded_rows)
    log(f"Expanded to {len(df_expanded)} rows")
    
    if len(df_expanded) > 0:
        unique_prefs = df_expanded['target_prefecture'].unique()
        log(f"Unique Prefectures ({len(unique_prefs)}): {unique_prefs}")
        
        # Check Hokkaido specifically
        hokkaido = df_expanded[df_expanded['target_prefecture'].str.contains('北海道')]
        log(f"Hokkaido rows: {len(hokkaido)}")
    else:
        log("df_expanded is empty!")
        return
    
    # 4. Aggregate
    df_expanded['weighted_slope'] = df_expanded['avg_slope'] * df_expanded['count']
    
    agg_funcs = {
        'weighted_slope': 'sum',
        'count': 'sum',
        'avg_slope': 'mean',
        'mesh_code': 'count'
    }
    
    df_result = df_expanded.groupby('target_prefecture').agg(agg_funcs).reset_index()
    df_result['final_avg_slope'] = df_result['weighted_slope'] / df_result['count']
    
    df_result = df_result.rename(columns={
        'target_prefecture': 'prefecture',
        'mesh_code': 'mesh_count',
        'count': 'total_cells'
    })
    
    final_cols = ['prefecture', 'final_avg_slope', 'mesh_count', 'total_cells']
    df_final = df_result[final_cols].sort_values('final_avg_slope', ascending=False)
    
    # 5. Output
    log("\n--- Top 5 Steepest ---")
    log(df_final.head(5).to_string(index=False))
    
    df_final.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')
    log(f"\nSaved verified slope data to: {OUTPUT_FILE}")
    
    # Report
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write("=== 都道府県別平均傾斜度検証レポート ===\n")
        f.write(f"Source Mapping: {os.path.basename(MAPPING_FILE)}\n")
        f.write(f"Source Slope: {os.path.basename(MESH_SLOPE_FILE)}\n\n")
        f.write("計算方法: メッシュ単位の平均傾斜度を、セル数（有効データ数）で加重平均。\n")
        f.write("境界処理: 境界にあるメッシュは、接する全ての都道府県の集計対象としてカウント。\n\n")
        
        f.write("--- ランキング (急勾配順) ---\n")
        f.write(df_final.to_string(index=False))
        f.write("\n\n")
        f.write("--- メッシュ数確認 ---\n")
        
        # Safe access
        hokkaido_row = df_final[df_final['prefecture']=='北海道']
        if not hokkaido_row.empty:
             val = hokkaido_row['mesh_count'].values[0]
             f.write(f"北海道: {val} (Should be 40)\n")
        else:
             f.write("北海道: Not Found!\n")
             
    log(f"Saved report to: {REPORT_FILE}")

if __name__ == "__main__":
    recalculate_slope()
