# -*- coding: utf-8 -*-
"""
離島を持つ都道府県のメッシュを分析
"""

import pandas as pd
import sys

# UTF-8出力を強制
sys.stdout.reconfigure(encoding='utf-8')

# データ読み込み
mesh_df = pd.read_csv(r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture\03_Analysis\data\interim\mesh_coordinates.csv")
mapping_df = pd.read_csv(r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture\03_Analysis\data\interim\mesh_prefecture_mapping_final_v2.csv")

# 離島を持つ可能性のある都道府県
island_prefs = ['北海道', '東京都', '長崎県', '鹿児島県', '沖縄県', '島根県', '新潟県', '石川県']

results = {}

for pref in island_prefs:
    # 該当都道府県を含むメッシュを抽出
    pref_meshes = mapping_df[mapping_df['prefectures'].str.contains(pref, na=False)]
    
    # 座標情報と結合
    pref_with_coords = pd.merge(
        pref_meshes,
        mesh_df[['mesh_code', 'south_lat', 'north_lat', 'west_lon', 'east_lon']],
        on='mesh_code'
    )
    
    # 緯度・経度でソート
    pref_with_coords = pref_with_coords.sort_values(['center_lat', 'center_lon'])
    
    results[pref] = {
        'total': len(pref_meshes),
        'lat_range': (pref_with_coords['south_lat'].min(), pref_with_coords['north_lat'].max()),
        'lon_range': (pref_with_coords['west_lon'].min(), pref_with_coords['east_lon'].max()),
        'meshes': pref_with_coords
    }

# 結果を出力
output_lines = []
output_lines.append("=== 離島を持つ都道府県のメッシュ分析 ===\n\n")

for pref, data in results.items():
    output_lines.append(f"【{pref}】\n")
    output_lines.append(f"総メッシュ数: {data['total']}\n")
    output_lines.append(f"緯度範囲: {data['lat_range'][0]:.2f}°N - {data['lat_range'][1]:.2f}°N\n")
    output_lines.append(f"経度範囲: {data['lon_range'][0]:.2f}°E - {data['lon_range'][1]:.2f}°E\n")
    output_lines.append("\nメッシュ一覧:\n")
    
    for _, row in data['meshes'].iterrows():
        output_lines.append(
            f"  {row['mesh_code']} | {row['center_lat']:.2f}°N, {row['center_lon']:.2f}°E | "
            f"緯度{row['south_lat']:.2f}-{row['north_lat']:.2f}°N, "
            f"経度{row['west_lon']:.2f}-{row['east_lon']:.2f}°E\n"
        )
    
    output_lines.append("\n" + "="*80 + "\n\n")

# ファイルに保存
output_file = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture\03_Analysis\data\interim\island_prefecture_analysis.txt"
with open(output_file, 'w', encoding='utf-8') as f:
    f.writelines(output_lines)

print(f"分析結果を保存: {output_file}")
print()
print(''.join(output_lines[:50]))  # 最初の50行のみ表示
