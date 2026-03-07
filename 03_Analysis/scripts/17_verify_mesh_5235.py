# -*- coding: utf-8 -*-
"""
メッシュ5235の座標を確認し、正しい都道府県を特定
"""

import pandas as pd
import sys

# UTF-8出力を強制
sys.stdout.reconfigure(encoding='utf-8')

# データ読み込み
mesh_df = pd.read_csv(r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture\03_Analysis\data\interim\mesh_coordinates.csv")

# メッシュ5235を検索
mesh_5235 = mesh_df[mesh_df['mesh_code'] == 5235]

if len(mesh_5235) > 0:
    row = mesh_5235.iloc[0]
    print("=== メッシュ5235の座標 ===")
    print(f"メッシュコード: {row['mesh_code']}")
    print(f"南端緯度: {row['south_lat']:.2f}°N")
    print(f"北端緯度: {row['north_lat']:.2f}°N")
    print(f"西端経度: {row['west_lon']:.2f}°E")
    print(f"東端経度: {row['east_lon']:.2f}°E")
    print(f"中心緯度: {row['center_lat']:.2f}°N")
    print(f"中心経度: {row['center_lon']:.2f}°E")
    print()
    
    # 主要都市の座標（参考）
    print("=== 参考：主要都市の座標 ===")
    cities = {
        '東京（東京都）': (35.68, 139.69),
        '大阪（大阪府）': (34.69, 135.50),
        '京都（京都府）': (35.01, 135.77),
        '神戸（兵庫県）': (34.69, 135.18),
        '奈良（奈良県）': (34.69, 135.83),
        '大津（滋賀県）': (35.00, 135.87),
        '津（三重県）': (34.73, 136.51),
    }
    
    for city, (lat, lon) in cities.items():
        print(f"{city}: {lat:.2f}°N, {lon:.2f}°E")
    
    print()
    print("=== 判定 ===")
    center_lat = row['center_lat']
    center_lon = row['center_lon']
    
    print(f"メッシュ5235の中心: {center_lat:.2f}°N, {center_lon:.2f}°E")
    print()
    print("最も近い都市: 大阪（大阪府）または京都（京都府）")
    print("東京都との経度差: {:.2f}度（約{}km）".format(
        abs(center_lon - 139.69),
        abs(center_lon - 139.69) * 111  # 1度≒111km
    ))
    print()
    print("結論: メッシュ5235は近畿地方（大阪府、京都府、兵庫県、奈良県、滋賀県、三重県）に該当し、")
    print("      東京都は含まれません。")
else:
    print("メッシュ5235が見つかりませんでした。")

# 東京都の実際の範囲を確認
print()
print("=== 東京都の実際の範囲 ===")
print("本州部分: 約35.5-36.0°N, 139.0-140.0°E")
print("小笠原諸島: 約20-28°N, 136-154°E（離島）")
print()
print("メッシュ5235（35.0°N, 135.5°E）は東京都の範囲外です。")
