import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import os
import matplotlib

# Windows console encoding fix
sys.stdout.reconfigure(encoding='utf-8')

# Font settings for Japanese (try to use standard fonts)
# matplotlib.rcParams['font.family'] = 'Meiryo' 

def analyze_correlation():
    print("相関分析を開始します...")
    
    # Paths
    base_dir = r"C:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture"
    input_file = os.path.join(base_dir, "03_Analysis", "data", "processed", "analysis_dataset_v1.csv")
    output_dir = os.path.join(base_dir, "03_Analysis", "results")
    fig_dir = os.path.join(output_dir, "figures")
    output_csv = os.path.join(output_dir, "correlation_matrix.csv")
    output_img = os.path.join(fig_dir, "heatmap_correlation.png")
    
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(fig_dir, exist_ok=True)
    
    # Load Data
    if not os.path.exists(input_file):
        print(f"エラー: 入力ファイルが見つかりません: {input_file}")
        return
        
    df = pd.read_csv(input_file)
    
    # Variables (English labels for plot)
    cols_map = {
        'fracture_rate': 'Total Fracture',
        'femur_rate': 'Femur',
        'humerus_rate': 'Humerus',
        'forearm_rate': 'Forearm',
        'habitable_slope_weighted': 'Slope',
        'aging_rate': 'Aging Rate',
        'fast_walking_rate': 'Fast Walk',
        'pop_density': 'Pop Density'
    }
    
    # Filter and Rename
    target_cols = [c for c in cols_map.keys() if c in df.columns]
    df_corr = df[target_cols].rename(columns=cols_map)
    
    # Calculate Correlation
    corr = df_corr.corr()
    
    # Save CSV
    corr.to_csv(output_csv, encoding='utf-8-sig')
    print(f"相関行列保存完了: {output_csv}")
    print(corr)
    
    # Plot Heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", vmin=-1, vmax=1)
    plt.title('Correlation Matrix of Fracture Risk and Environmental Factors')
    plt.tight_layout()
    
    plt.savefig(output_img)
    print(f"ヒートマップ保存完了: {output_img}")

if __name__ == "__main__":
    analyze_correlation()
