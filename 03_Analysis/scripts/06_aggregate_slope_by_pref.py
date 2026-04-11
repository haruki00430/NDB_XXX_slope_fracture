import pandas as pd
import numpy as np
import os
import sys

# UTF-8出力設定
sys.stdout.reconfigure(encoding='utf-8')

# ---------------------------------------------------------
# 設定
# ---------------------------------------------------------
PROJECT_DIR = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture"

# Input
MESH_PREF_FILE = os.path.join(PROJECT_DIR, "03_Analysis", "data", "interim", "mesh_prefecture_mapping.csv")

# Output
OUTPUT_FILE = os.path.join(PROJECT_DIR, "03_Analysis", "data", "interim", "slope_by_prefecture_final.csv")

# 都道府県名マッピング
PREF_MAP = {
    1: "Hokkaido", 2: "Aomori", 3: "Iwate", 4: "Miyagi", 5: "Akita", 6: "Yamagata", 7: "Fukushima",
    8: "Ibaraki", 9: "Tochigi", 10: "Gunma", 11: "Saitama", 12: "Chiba", 13: "Tokyo", 14: "Kanagawa",
    15: "Niigata", 16: "Toyama", 17: "Ishikawa", 18: "Fukui", 19: "Yamanashi", 20: "Nagano",
    21: "Gifu", 22: "Shizuoka", 23: "Aichi", 24: "Mie", 25: "Shiga", 26: "Kyoto", 27: "Osaka",
    28: "Hyogo", 29: "Nara", 30: "Wakayama", 31: "Tottori", 32: "Shimane", 33: "Okayama", 34: "Hiroshima",
    35: "Yamaguchi", 36: "Tokushima", 37: "Kagawa", 38: "Ehime", 39: "Kochi", 40: "Fukuoka",
    41: "Saga", 42: "Nagasaki", 43: "Kumamoto", 44: "Oita", 45: "Miyazaki", 46: "Kagoshima", 47: "Okinawa"
}

def aggregate_slope_by_prefecture():
    """
    メッシュ単位の傾斜度データを都道府県別に集計する。
    """
    
    print("都道府県別傾斜度集計を開始します...")
    
    # データ読み込み
    df = pd.read_csv(MESH_PREF_FILE, encoding='utf-8')
    print(f"Total meshes: {len(df)}")
    print(f"Meshes with prefecture: {len(df[df['pref_code'].notna()])}")
    
    # 欠損値を除外
    df = df[df['pref_code'].notna()].copy()
    
    # 都道府県別に集計
    # 各メッシュの傾斜度を、そのメッシュ内のセル数で重み付けして平均
    df['weighted_slope'] = df['avg_slope'] * df['count']
    
    grouped = df.groupby('pref_code').agg({
        'weighted_slope': 'sum',
        'count': 'sum',
        'avg_slope': ['mean', 'median', 'std', 'min', 'max']
    }).reset_index()
    
    # カラム名を整理
    grouped.columns = ['pref_code', 'weighted_slope_sum', 'total_cells', 
                       'mean_slope', 'median_slope', 'std_slope', 'min_slope', 'max_slope']
    
    # 加重平均傾斜度を計算
    grouped['avg_slope_weighted'] = grouped['weighted_slope_sum'] / grouped['total_cells']
    
    # 都道府県名を追加
    grouped['pref_code'] = grouped['pref_code'].astype(int)
    grouped['prefecture'] = grouped['pref_code'].map(PREF_MAP)
    
    # 列の順序を整理
    result = grouped[['pref_code', 'prefecture', 'avg_slope_weighted', 'mean_slope', 
                      'median_slope', 'std_slope', 'min_slope', 'max_slope', 'total_cells']]
    
    # ソート
    result = result.sort_values('pref_code')
    
    print("\n--- 都道府県別傾斜度集計結果 (Top 10) ---")
    print(result.head(10).to_string(index=False))
    
    print(f"\n--- 傾斜度が高い都道府県 (Top 5) ---")
    top5 = result.nlargest(5, 'avg_slope_weighted')[['prefecture', 'avg_slope_weighted']]
    print(top5.to_string(index=False))
    
    # 保存
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    result.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')
    print(f"\n保存完了: {OUTPUT_FILE}")
    print(f"集計都道府県数: {len(result)}")
    
    return result

if __name__ == "__main__":
    aggregate_slope_by_prefecture()
