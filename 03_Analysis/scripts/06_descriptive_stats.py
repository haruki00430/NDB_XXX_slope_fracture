import pandas as pd
import sys
import os

# Windows console encoding fix
sys.stdout.reconfigure(encoding='utf-8')

def calculate_descriptive_stats():
    print("記述統計量の計算を開始します...")
    
    # Paths
    base_dir = r"C:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture"
    input_file = os.path.join(base_dir, "03_Analysis", "data", "processed", "analysis_dataset_v1.csv")
    output_dir = os.path.join(base_dir, "03_Analysis", "results")
    output_file = os.path.join(output_dir, "table1_descriptive.csv")
    output_md = os.path.join(output_dir, "table1_descriptive.md")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Load Data
    if not os.path.exists(input_file):
        print(f"エラー: 入力ファイルが見つかりません: {input_file}")
        return
        
    df = pd.read_csv(input_file)
    print(f"データ読み込み完了: {len(df)} 行")
    
    # Variables of Interest
    # 骨折率, 傾斜度, 高齢化率, 歩行速度, 人口密度
    cols = {
        'fracture_rate': 'Total Fracture Rate (per 100k)',
        'femur_rate': 'Femur Fracture Rate',
        'humerus_rate': 'Humerus Fracture Rate',
        'forearm_rate': 'Forearm Fracture Rate',
        'habitable_slope_weighted': 'Habitable Slope (Weighted)',
        'avg_slope_simple': 'Average Slope (Simple)',
        'aging_rate': 'Aging Rate (%)',
        'fast_walking_rate': 'Fast Walking Rate (%)',
        'pop_density': 'Population Density'
    }
    
    stats_list = []
    
    for col, name in cols.items():
        if col in df.columns:
            s = df[col]
            stats = {
                'Variable': name,
                'N': s.count(),
                'Mean': s.mean(),
                'SD': s.std(),
                'Min': s.min(),
                'Median': s.median(),
                'Max': s.max()
            }
            stats_list.append(stats)
        else:
            print(f"警告: カラム {col} が見つかりません")
            
    # Create DataFrame
    df_stats = pd.DataFrame(stats_list)
    
    # Rounding
    numeric_cols = ['Mean', 'SD', 'Min', 'Median', 'Max']
    df_stats[numeric_cols] = df_stats[numeric_cols].round(2)
    
    # Save CSV
    df_stats.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"CSV保存完了: {output_file}")
    
    # Save Markdown
    with open(output_md, 'w', encoding='utf-8') as f:
        f.write("# Table 1: Descriptive Statistics\n\n")
        f.write(df_stats.to_markdown(index=False))
    print(f"Markdown保存完了: {output_md}")
    
    print("\n--- Table 1 ---")
    print(df_stats.to_string(index=False))

if __name__ == "__main__":
    calculate_descriptive_stats()
