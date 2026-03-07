
import pandas as pd
import os
import sys

# UTF-8 Output
sys.stdout.reconfigure(encoding='utf-8')

# Paths
PROJECT_DIR = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture"
MAPPING_FILE = os.path.join(PROJECT_DIR, "03_Analysis", "data", "interim", "mesh_prefecture_mapping_final_verified.csv")
MESH_SLOPE_FILE = os.path.join(PROJECT_DIR, "03_Analysis", "data", "interim", "slope_by_prefecture.csv") # Actually mesh level
# MESH_SLOPE_FILE columns: mesh2 (code), avg_slope, count
HABITABLE_MASK_FILE = os.path.join(PROJECT_DIR, "03_Analysis", "data", "interim", "habitable_mask.csv")
# HABITABLE_MASK_FILE columns: mesh_code, habitable_ratio, total_100m_cells, habitable_100m_cells

OUTPUT_FILE = os.path.join(PROJECT_DIR, "03_Analysis", "data", "interim", "slope_by_prefecture_habitable.csv")
REPORT_FILE = os.path.join(PROJECT_DIR, "03_Analysis", "data", "interim", "slope_comparison_report.txt")

def recalculate():
    print("=== Start Recalculating Slope (Habitable Land Only) ===")
    
    # 1. Load Data
    print("Loading datasets...")
    # Mapping
    df_map = pd.read_csv(MAPPING_FILE, dtype={'mesh_code': str})
    print(f"Mapping: {len(df_map)} meshes")
    
    # Slope
    df_slope = pd.read_csv(MESH_SLOPE_FILE, dtype={'mesh2': str})
    df_slope = df_slope.rename(columns={'mesh2': 'mesh_code'})
    print(f"Slope: {len(df_slope)} meshes")
    
    # Habitable Mask
    if not os.path.exists(HABITABLE_MASK_FILE):
        print(f"Error: Habitable mask file not found: {HABITABLE_MASK_FILE}")
        return
        
    df_mask = pd.read_csv(HABITABLE_MASK_FILE, dtype={'mesh_code': str})
    print(f"Habitable Mask: {len(df_mask)} meshes")
    
    # 2. Merge
    # Left join to Mapping to keep all mapped meshes, but we need intersection of all 3
    # Inner join Mapping and Slope first (Phase 2 base)
    merged = pd.merge(df_map, df_slope, on='mesh_code', how='inner')
    print(f"Merged (Map+Slope): {len(merged)}")
    
    # Merge with Mask
    # If mask is missing for a mesh, assume ratio=0? Or ratio=1?
    # Mask covers "Habitable Land Use Survey Area". 
    # If missing, it might be deep mountains (non-habitable) or sea.
    # We'll use left join and fillna(0) for safety.
    final_df = pd.merge(merged, df_mask[['mesh_code', 'habitable_ratio']], on='mesh_code', how='left')
    final_df['habitable_ratio'] = final_df['habitable_ratio'].fillna(0)
    
    print(f"Merged (All): {len(final_df)}")
    
    # 3. Calculate Weighted Data
    # Weight = Count (DEM cells) * Habitable Ratio
    final_df['weight'] = final_df['count'] * final_df['habitable_ratio']
    final_df['weighted_slope'] = final_df['avg_slope'] * final_df['weight']
    
    # 4. Expand Prefectures
    expanded_rows = []
    for _, row in final_df.iterrows():
        pref_str = row['prefectures']
        if pd.isna(pref_str): continue
        prefs = [p.strip() for p in str(pref_str).replace('、', ',').split(',')]
        for pref in prefs:
            if not pref: continue
            new_row = row.to_dict()
            new_row['prefecture'] = pref
            expanded_rows.append(new_row)
            
    df_expanded = pd.DataFrame(expanded_rows)
    print(f"Expanded to {len(df_expanded)} rows")
    
    # 5. Aggregate
    agg_funcs = {
        'weighted_slope': 'sum',
        'weight': 'sum',
        'mesh_code': 'count'
    }
    
    df_result = df_expanded.groupby('prefecture').agg(agg_funcs).reset_index()
    
    # Avoid division by zero
    df_result['habitable_slope'] = df_result.apply(
        lambda r: r['weighted_slope'] / r['weight'] if r['weight'] > 0 else 0, axis=1
    )
    
    df_result = df_result.sort_values('habitable_slope', ascending=False)
    
    # 6. Save
    df_result.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')
    print(f"Saved: {OUTPUT_FILE}")
    
    # 7. Compare with Original (Phase 2)
    compare_result(df_result)

def compare_result(df_new):
    # Load Phase 2 result
    phase2_file = os.path.join(PROJECT_DIR, "03_Analysis", "data", "interim", "slope_by_prefecture_verified.csv")
    if not os.path.exists(phase2_file):
        print("Phase 2 result not found.")
        return
        
    df_old = pd.read_csv(phase2_file)
    
    # Merge
    merged = pd.merge(df_new[['prefecture', 'habitable_slope', 'weight']], 
                      df_old[['prefecture', 'final_avg_slope', 'total_cells']], 
                      on='prefecture', suffixes=('_habitable', '_original'))
                      
    merged['diff'] = merged['habitable_slope'] - merged['final_avg_slope']
    merged = merged.sort_values('habitable_slope', ascending=False)
    
    print("\n=== Comparison: Habitable Slope vs Original Slope ===")
    print(merged[['prefecture', 'habitable_slope', 'final_avg_slope', 'diff', 'weight', 'total_cells']].head(10).to_string(index=False))
    
    # Save Report
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write("=== 可住地傾斜度 vs 全域傾斜度 比較レポート ===\n")
        f.write("Habitable Slope: 土地利用データに基づく可住地（田畑、建物、道路等）のみの傾斜度\n")
        f.write("Original Slope: 都道府県全域の平均傾斜度\n\n")
        f.write(merged.to_string(index=False))
        
    print(f"Saved comparison report: {REPORT_FILE}")

if __name__ == "__main__":
    recalculate()
