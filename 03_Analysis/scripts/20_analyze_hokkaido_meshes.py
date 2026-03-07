# -*- coding: utf-8 -*-
"""
北海道のメッシュを確認し、本州部分と離島部分を特定
"""

import pandas as pd
import sys

# UTF-8出力を強制
sys.stdout.reconfigure(encoding='utf-8')

# データ読み込み
mesh_df = pd.read_csv(r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture\03_Analysis\data\interim\mesh_coordinates.csv")
mapping_df = pd.read_csv(r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture\03_Analysis\data\interim\mesh_prefecture_mapping_final_v2.csv")

# 北海道を含むメッシュを抽出
hokkaido_meshes = mapping_df[mapping_df['prefectures'].str.contains('北海道', na=False)]

print("=== 北海道を含むメッシュ一覧 ===")
print(f"総数: {len(hokkaido_meshes)}メッシュ")
print()

# 座標情報と結合
hokkaido_with_coords = pd.merge(
    hokkaido_meshes,
    mesh_df[['mesh_code', 'south_lat', 'north_lat', 'west_lon', 'east_lon']],
    on='mesh_code'
)

# 緯度・経度でソート
hokkaido_with_coords = hokkaido_with_coords.sort_values(['center_lat', 'center_lon'])

print("メッシュコード | 中心緯度 | 中心経度 | 緯度範囲 | 経度範囲 | 都道府県")
print("-" * 100)
for _, row in hokkaido_with_coords.iterrows():
    print(f"{row['mesh_code']} | {row['center_lat']:.2f}°N | {row['center_lon']:.2f}°E | "
          f"{row['south_lat']:.2f}-{row['north_lat']:.2f}°N | "
          f"{row['west_lon']:.2f}-{row['east_lon']:.2f}°E | {row['prefectures']}")

# 緯度・経度の分布を確認
print()
print("=== 北海道メッシュの緯度・経度分布 ===")
print(f"緯度範囲: {hokkaido_with_coords['south_lat'].min():.2f}°N - {hokkaido_with_coords['north_lat'].max():.2f}°N")
print(f"経度範囲: {hokkaido_with_coords['west_lon'].min():.2f}°E - {hokkaido_with_coords['east_lon'].max():.2f}°E")

# 北海道本島の範囲（おおよそ）
# 緯度: 41.5°N - 45.5°N
# 経度: 139.5°E - 145.5°E
print()
print("=== 北海道本島の推定範囲 ===")
print("緯度: 41.5°N - 45.5°N")
print("経度: 139.5°E - 145.5°E")

# 本島外のメッシュを特定
mainland_meshes = hokkaido_with_coords[
    (hokkaido_with_coords['south_lat'] >= 41.5) &
    (hokkaido_with_coords['north_lat'] <= 45.5) &
    (hokkaido_with_coords['west_lon'] >= 139.5) &
    (hokkaido_with_coords['east_lon'] <= 145.5)
]

island_meshes = hokkaido_with_coords[
    ~hokkaido_with_coords['mesh_code'].isin(mainland_meshes['mesh_code'])
]

print()
print(f"=== 分類結果 ===")
print(f"本島メッシュ: {len(mainland_meshes)}メッシュ")
print(f"離島メッシュ: {len(island_meshes)}メッシュ")

if len(island_meshes) > 0:
    print()
    print("=== 離島メッシュの詳細 ===")
    for _, row in island_meshes.iterrows():
        print(f"{row['mesh_code']} | {row['center_lat']:.2f}°N, {row['center_lon']:.2f}°E | {row['prefectures']}")

# 結果をCSVに保存
output_file = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture\03_Analysis\data\interim\hokkaido_mesh_analysis.csv"
hokkaido_with_coords.to_csv(output_file, index=False, encoding='utf-8')
print()
print(f"分析結果を保存: {output_file}")
