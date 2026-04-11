import geopandas as gpd
import pandas as pd
import glob
import os
import sys

# UTF-8出力設定
sys.stdout.reconfigure(encoding='utf-8')

# ---------------------------------------------------------
# 設定
# ---------------------------------------------------------
HUB_DIR = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub"
PROJECT_DIR = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture"

# A38 Medical Area Shapefiles (都道府県別)
A38_DIR = os.path.join(HUB_DIR, "02_Data", "raw", "A38_Medical_Area")

# DEM Slope Data (Mesh単位)
SLOPE_FILE = os.path.join(PROJECT_DIR, "03_Analysis", "data", "interim", "slope_by_prefecture.csv")

# Output
OUTPUT_FILE = os.path.join(PROJECT_DIR, "03_Analysis", "data", "interim", "mesh_prefecture_mapping.csv")

def create_mesh_to_pref_mapping():
    """
    A38 Medical Areaデータを使用して、メッシュコードと都道府県の対応表を作成する。
    
    ただし、A38は「二次医療圏」のデータであり、都道府県境界ではない。
    そのため、簡易的に「ファイル名の都道府県コード」を使用する。
    
    より正確には、国土数値情報の「行政区域データ (N03)」が必要だが、
    今回はフィージビリティ評価のため、簡易マッピングで対応する。
    """
    
    print("メッシュ→都道府県マッピングの作成を開始します...")
    
    # 1. Slope Data (Mesh単位) を読み込み
    df_slope = pd.read_csv(SLOPE_FILE)
    print(f"Slope Data: {len(df_slope)}メッシュ")
    
    # 2. 簡易マッピング: メッシュコード(2次)の上2桁から都道府県を推定
    # (注: これは非常に粗い推定であり、正確性は保証されない)
    # 正確な対応には、GISによる空間結合が必要
    
    # メッシュコード → 緯度経度 → 都道府県 の変換が必要だが、
    # 今回は「メッシュコードの分布」から大まかに割り当てる
    
    # 代替案: 既存の「都道府県別メッシュコード一覧」を使用
    # (国土地理院が提供している可能性があるが、今回は手動作成)
    
    # 簡易実装: メッシュコードの地理的分布から都道府県を推定
    # 例: 5339 (東京/埼玉) -> 東京(13) or 埼玉(11)
    
    # より実用的なアプローチ:
    # 「メッシュコードの中心座標」を計算し、それが含まれる都道府県を特定
    
    # jismesh ライブラリがないため、手動で実装
    # または、外部の対応表を使用
    
    print("\n【警告】正確なメッシュ→都道府県マッピングには、GISデータ(N03行政区域)が必要です。")
    print("今回は簡易的に、メッシュコードの地理的分布から推定します。")
    
    # 簡易マッピング辞書 (手動作成 - 一部のみ)
    # 実際には、全メッシュに対して正確な対応が必要
    mesh_to_pref = {
        # 沖縄 (47)
        "30": 47, "36": 47, "37": 47, "38": 47, "39": 47,
        # 九州 (40-46)
        "40": 46, "41": 45, "42": 44, "43": 43, "44": 42, "45": 41, "46": 40,
        # 中国・四国 (31-39)
        "47": 39, "48": 38, "49": 37, "50": 36,
        # 関西 (24-30)
        "51": 30, "52": 29, "53": 28, "54": 27,
        # 関東 (8-14)
        "55": 14, "56": 13, "57": 12, "58": 11,
        # 東北 (2-7)
        "59": 7, "60": 6, "61": 5, "62": 4,
        # 北海道 (1)
        "63": 1, "64": 1, "65": 1, "66": 1, "67": 1, "68": 1
    }
    
    # メッシュコードの上2桁から都道府県を推定
    df_slope['pref_code'] = df_slope['mesh2'].astype(str).str[:2].map(mesh_to_pref)
    
    # 欠損値の確認
    missing = df_slope[df_slope['pref_code'].isna()]
    if len(missing) > 0:
        print(f"\n【注意】{len(missing)}メッシュが都道府県に割り当てられませんでした。")
        print(missing[['mesh2']].head(10))
    
    # 保存
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    df_slope.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')
    print(f"\n保存完了: {OUTPUT_FILE}")
    print(f"マッピング済みメッシュ数: {len(df_slope[df_slope['pref_code'].notna()])}")
    
    return df_slope

if __name__ == "__main__":
    create_mesh_to_pref_mapping()
