# -*- coding: utf-8 -*-
"""
指定メッシュの座標を確認し、正しい都道府県を特定
"""

import pandas as pd
import sys

# UTF-8出力を強制
sys.stdout.reconfigure(encoding='utf-8')

# データ読み込み
mesh_df = pd.read_csv(r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture\03_Analysis\data\interim\mesh_coordinates.csv")

# 指定されたメッシュコード
target_meshes = ['5035', '5036', '5135', '5136', '5233', '5234', '5235', '5236', 
                 '5238', '5239', '5240', '5333', '5334', '5338', '5339', '5340', 
                 '5438', '5439', '5440']

# メッシュコードを文字列に変換
mesh_df['mesh_code'] = mesh_df['mesh_code'].astype(str)

# フィルタリング
filtered = mesh_df[mesh_df['mesh_code'].isin(target_meshes)]

print("=== 指定されたメッシュコードの座標 ===\n")

# 日本の主要都市の座標（参考）
reference_cities = {
    '埼玉県（さいたま市）': (35.86, 139.65),
    '神奈川県（横浜市）': (35.44, 139.64),
    '奈良県（奈良市）': (34.69, 135.83),
    '鳥取県（鳥取市）': (35.50, 134.23),
}

print("【参考】主要都市の座標:")
for city, (lat, lon) in reference_cities.items():
    print(f"  {city}: {lat:.2f}°N, {lon:.2f}°E")
print()

for _, row in filtered.sort_values('mesh_code').iterrows():
    mesh = row['mesh_code']
    s_lat, w_lon = row['south_lat'], row['west_lon']
    n_lat, e_lon = row['north_lat'], row['east_lon']
    c_lat, c_lon = row['center_lat'], row['center_lon']
    
    print(f"メッシュ {mesh}:")
    print(f"  範囲: {s_lat:.2f}°N-{n_lat:.2f}°N, {w_lon:.2f}°E-{e_lon:.2f}°E")
    print(f"  中心: {c_lat:.2f}°N, {c_lon:.2f}°E")
    
    # 手動で都道府県を判定
    pref = "不明"
    if 35.5 <= c_lat <= 36.3 and 138.7 <= c_lon <= 140.0:
        if c_lon >= 139.3:
            pref = "埼玉県または東京都"
        else:
            pref = "長野県または群馬県"
    elif 35.0 <= c_lat <= 35.7 and 139.0 <= c_lon <= 140.0:
        if c_lat >= 35.4:
            pref = "東京都または埼玉県"
        else:
            pref = "神奈川県または東京都"
    elif 34.3 <= c_lat <= 35.0 and 135.5 <= c_lon <= 136.5:
        pref = "奈良県または大阪府または京都府"
    elif 35.0 <= c_lat <= 35.7 and 133.5 <= c_lon <= 134.5:
        pref = "鳥取県または兵庫県"
    
    print(f"  推定: {pref}")
    print()
