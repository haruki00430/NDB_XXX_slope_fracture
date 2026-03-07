import os
import glob
import zipfile
import pandas as pd
import xml.etree.ElementTree as ET
import numpy as np

# ---------------------------------------------------------
# 設定
# ---------------------------------------------------------
# プロジェクトルート
PROJECT_DIR = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture"
# 共通データルート (Hub直下)
HUB_DIR = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub"

DEM_DIR = os.path.join(HUB_DIR, "02_Data", "raw", "MLIT", "G04_c_Elevation")
OUTPUT_FILE = os.path.join(PROJECT_DIR, "03_Analysis", "data", "interim", "slope_by_prefecture.csv")

# 都道府県コードマッピング (簡易)
PREF_MAP = {
    1: "Hokkaido", 2: "Aomori", 3: "Iwate", 4: "Miyagi", 5: "Akita", 6: "Yamagata", 7: "Fukushima",
    8: "Ibaraki", 9: "Tochigi", 10: "Gunma", 11: "Saitama", 12: "Chiba", 13: "Tokyo", 14: "Kanagawa",
    15: "Niigata", 16: "Toyama", 17: "Ishikawa", 18: "Fukui", 19: "Yamanashi", 20: "Nagano",
    21: "Gifu", 22: "Shizuoka", 23: "Aichi", 24: "Mie", 25: "Shiga", 26: "Kyoto", 27: "Osaka",
    28: "Hyogo", 29: "Nara", 30: "Wakayama", 31: "Tottori", 32: "Shimane", 33: "Okayama", 34: "Hiroshima",
    35: "Yamaguchi", 36: "Tokushima", 37: "Kagawa", 38: "Ehime", 39: "Kochi", 40: "Fukuoka",
    41: "Saga", 42: "Nagasaki", 43: "Kumamoto", 44: "Oita", 45: "Miyazaki", 46: "Kagoshima", 47: "Okinawa"
}

def parse_gml_zip(zip_path):
    """
    Zip内のXML(GML)をパースして、平均傾斜(avg_slope)のリストを返す
    """
    slopes = []
    
    with zipfile.ZipFile(zip_path, 'r') as z:
        # XMLファイルを探す (.xml)
        for filename in z.namelist():
            if filename.endswith('.xml') and 'KS-META' not in filename: # メタデータはスキップ
                with z.open(filename) as f:
                    try:
                        # XMLをパース
                        tree = ET.parse(f)
                        root = tree.getroot()
                        
                        # ネームスペース処理
                        ns = {'gml': 'http://www.opengis.net/gml/3.2'}
                        
                        # tupleListを探す
                        # gml:DataBlock -> gml:tupleList
                        for tuple_list in root.findall('.//gml:tupleList', ns):
                            text = tuple_list.text
                            if text:
                                lines = text.strip().split('\n')
                                for line in lines:
                                    parts = line.strip().split(',')
                                    if len(parts) >= 10:
                                        # 533900001,563.0,...,5.9
                                        # Index 9 is Avg Slope (according to schema)
                                        try:
                                            slope = float(parts[9])
                                            slopes.append(slope)
                                        except ValueError:
                                            pass
                    except ET.ParseError:
                        print(f"XML Parse Error: {filename}")
                        
    return slopes

def aggregate_slopes():
    print("DEMデータの集計を開始します...")
    
# import jismesh.utils as ju

def get_pref_code_from_mesh(mesh_code):
    """
    メッシュコード(3次/4次)から都道府県コードを推定する
    (簡易実装: jismeshを使用しない版)
    """
    try:
        # jismeshがないため、一旦メッシュコードの上2桁(1次メッシュ)をそのまま返す
        # 下流処理でこれをマッピングする
        return mesh_code[:4] 
    except:
        return "Unknown"

def aggregate_slopes():
    print("DEMデータの集計を開始します(全国版)...")
    
    zip_files = glob.glob(os.path.join(DEM_DIR, "*.zip"))
    print(f"対象ファイル数: {len(zip_files)}")
    
    mesh_slopes = []
    
    for i, zip_file in enumerate(zip_files):
        if i % 10 == 0: print(f"Processing {i}/{len(zip_files)}...")
        
        # ファイル名からメッシュコード取得 (G04-c-11_5339...)
        # 5339 は 2次メッシュコード
        basename = os.path.basename(zip_file)
        try:
            mesh2 = basename.split('_')[1].split('-')[0]
        except:
            mesh2 = "Unknown"
        
        slopes = parse_gml_zip(zip_file)
        if slopes:
            avg = np.mean(slopes)
            count = len(slopes)
            mesh_slopes.append({
                "mesh2": mesh2,
                "avg_slope": avg,
                "count": count
            })
            
    df = pd.DataFrame(mesh_slopes)
    
    # 2次メッシュ -> 都道府県 のマッピング
    # (外部データが必要だが、一旦簡易的に実装)
    
    print("\n--- メッシュ別集計結果(Top 5) ---")
    print(df.head())
    
    # 保存 (一旦メッシュ単位で保存)
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\n保存完了: {OUTPUT_FILE}")


if __name__ == "__main__":
    aggregate_slopes()
