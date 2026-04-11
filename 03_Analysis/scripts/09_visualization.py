import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os
import matplotlib.font_manager as fm

# Windows console encoding fix
sys.stdout.reconfigure(encoding='utf-8')

# Font settings for Japanese
# Use any available Japanese font to display prefecture names correctly
jp_font = None
try:
    font_paths = fm.findSystemFonts()
    for font_path in font_paths:
        if "Meiryo" in font_path or "Yu Gothic" in font_path or "MS Gothic" in font_path:
            jp_font = fm.FontProperties(fname=font_path)
            print(f"Using font: {font_path}")
            break
except:
    pass

# Matplotlib configuration
if jp_font:
    plt.rcParams['font.family'] = jp_font.get_name()
else:
    # Fallback
    plt.rcParams['font.sans-serif'] = ['Meiryo', 'Yu Gothic', 'Hiragino Maru Gothic Pro', 'SimHei', 'Arial']

def create_visualizations():
    print("可視化を開始します...")
    
    # Paths
    base_dir = r"C:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture"
    input_file = os.path.join(base_dir, "03_Analysis", "data", "processed", "analysis_dataset_v1.csv")
    output_dir = os.path.join(base_dir, "03_Analysis", "results", "figures")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Load Data
    if not os.path.exists(input_file):
        print(f"エラー: 入力ファイルが見つかりません: {input_file}")
        return
        
    df = pd.read_csv(input_file)
    print(f"データ読み込み完了: {len(df)} 行")
    
    # 1. Scatter Plot: Slope vs Femur Fracture Rate
    print("散布図を作成中: 傾斜度 vs 大腿骨骨折率...")
    plt.figure(figsize=(12, 8))
    
    x_col = 'habitable_slope_weighted'
    y_col = 'femur_rate'
    
    if x_col in df.columns and y_col in df.columns:
        sns.regplot(x=x_col, y=y_col, data=df, scatter_kws={'alpha':0.6}, line_kws={'color':'red'})
        
        # Add labels
        for i, row in df.iterrows():
            plt.text(row[x_col]+0.1, row[y_col], row['prefecture'], fontsize=9, alpha=0.7)
            
        plt.title('Relationship between Habitable Slope and Femur Fracture Rate')
        plt.xlabel('Habitable Slope (Weighted)')
        plt.ylabel('Femur Fracture Rate (per 100k)')
        plt.grid(True, linestyle='--', alpha=0.6)
        
        output_path = os.path.join(output_dir, "scatter_slope_fracture.png")
        plt.savefig(output_path, dpi=300)
        print(f"保存完了: {output_path}")
        plt.close()
    else:
        print(f"スキップ: 必要な列が見つかりません ({x_col}, {y_col})")

    # 2. Scatter Plot Matrix
    print("散布図行列を作成中...")
    cols = ['habitable_slope_weighted', 'fracture_rate', 'aging_rate', 'fast_walking_rate']
    cols = [c for c in cols if c in df.columns]
    
    if len(cols) > 1:
        sns.pairplot(df[cols])
        output_path = os.path.join(output_dir, "scatter_matrix.png")
        plt.savefig(output_path, dpi=300)
        print(f"保存完了: {output_path}")
        plt.close()

    # 3. Map (Simple visualization using scatter plot with pseudo-coordinates if available, otherwise skip)
    # Ideally use a map library, but for now scatter plot is sufficient.
    
    print("可視化完了。")

if __name__ == "__main__":
    create_visualizations()
