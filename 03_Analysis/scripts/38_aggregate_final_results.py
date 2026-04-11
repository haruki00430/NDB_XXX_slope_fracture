import pandas as pd
import os
import sys

# UTF-8 Output
sys.stdout.reconfigure(encoding='utf-8')

# Paths
PROJECT_DIR = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture"
INPUT_FILE = os.path.join(PROJECT_DIR, "data", "interim", "slope_by_mesh_final.csv")
OUTPUT_FILE = os.path.join(PROJECT_DIR, "results", "statistics", "prefecture_habitable_slope.csv")
REPORT_FILE = os.path.join(PROJECT_DIR, "results", "statistics", "slope_comparison_report.md")

def main():
    print("=== Start Aggregating Final Slope Statistics ===")
    
    if not os.path.exists(INPUT_FILE):
        print(f"Error: Input file not found: {INPUT_FILE}")
        return

    print("Loading master dataset...")
    df = pd.read_csv(INPUT_FILE)
    print(f"Loaded {len(df)} rows.")
    
    # Filter valid data
    # Must have Slope, Prefecture
    df_valid = df.dropna(subset=['avg_slope', 'prefecture'])
    print(f"Valid rows (with slope & prefecture): {len(df_valid)}")
    
    # Fill habitable_ratio NaN with 0
    df_valid['habitable_ratio'] = df_valid['habitable_ratio'].fillna(0)
    
    # Calculate Weighted Slope components
    df_valid['weighted_sum'] = df_valid['avg_slope'] * df_valid['habitable_ratio']
    
    # Aggregation
    print("Aggregating by Prefecture...")
    stats = df_valid.groupby('prefecture').agg(
        mesh_count=('mesh_code', 'count'),
        avg_slope_simple=('avg_slope', 'mean'),
        total_weighted_slope=('weighted_sum', 'sum'),
        total_habitable_ratio=('habitable_ratio', 'sum'),
        max_slope=('avg_slope', 'max'),
        min_slope=('avg_slope', 'min')
    ).reset_index()
    
    # Calculate Final Weighted Average
    # If total_habitable_ratio is 0, it means no habitable land in that prefecture's meshes (unlikely but possible for small islands if L03 misses them)
    # In that case, fallback to simple average or 0? 
    # Fallback to simple average is safer.
    
    def calc_weighted(row):
        if row['total_habitable_ratio'] > 0:
            return row['total_weighted_slope'] / row['total_habitable_ratio']
        else:
            return row['avg_slope_simple'] # Fallback
            
    stats['habitable_slope_weighted'] = stats.apply(calc_weighted, axis=1)
    
    # Sort by Habitable Slope
    stats = stats.sort_values('habitable_slope_weighted', ascending=False)
    
    # Save
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    stats.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')
    print(f"Saved statistics to {OUTPUT_FILE}")
    
    # Generate Report
    print("Generating comparison report...")
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write("# 都道府県別傾斜度分析レポート（可住地加重 vs 単純平均）\n\n")
        f.write(f"**データソース**: 国土数値情報 G04-c (標高・傾斜度) & L03-b (土地利用)\n")
        f.write(f"**集計メッシュ数**: {len(df_valid)}\n\n")
        
        f.write("## 傾斜度上位10都道府県（可住地加重）\n")
        f.write("| 順位 | 都道府県 | 可住地傾斜度 (度) | 単純平均傾斜度 (度) | 差分 (単純 - 可住地) |\n")
        f.write("|---|---|---|---|---|\n")
        
        for i, (_, row) in enumerate(stats.head(10).iterrows()):
            diff = row['avg_slope_simple'] - row['habitable_slope_weighted']
            f.write(f"| {i+1} | {row['prefecture']} | {row['habitable_slope_weighted']:.2f} | {row['avg_slope_simple']:.2f} | {diff:.2f} |\n")
            
        f.write("\n## 傾斜度下位10都道府県（可住地加重）\n")
        f.write("| 順位 | 都道府県 | 可住地傾斜度 (度) | 単純平均傾斜度 (度) | 差分 (単純 - 可住地) |\n")
        f.write("|---|---|---|---|---|\n")
        
        for i, (_, row) in enumerate(stats.tail(10).iterrows()):
            diff = row['avg_slope_simple'] - row['habitable_slope_weighted']
            # tail is bottom, but i want rank from 47 down.
            # stats is sorted desc. tail(10) is 38-47.
            # actually tail(10) gives 47, 46... in that order if sorted desc? No, tail gives last rows.
            pass 
            
        # Re-iterate for bottom
        tail_df = stats.tail(10).iloc[::-1] # Reverse to show 47, 46...
        rank_start = len(stats)
        for i, (_, row) in enumerate(tail_df.iterrows()):
            diff = row['avg_slope_simple'] - row['habitable_slope_weighted']
            f.write(f"| {rank_start - i} | {row['prefecture']} | {row['habitable_slope_weighted']:.2f} | {row['avg_slope_simple']:.2f} | {diff:.2f} |\n")
            
    print(f"Saved report to {REPORT_FILE}")
    
    # Print preview
    print("\n--- Top 5 Prefectures ---")
    print(stats[['prefecture', 'habitable_slope_weighted', 'avg_slope_simple']].head(5))

if __name__ == "__main__":
    main()
