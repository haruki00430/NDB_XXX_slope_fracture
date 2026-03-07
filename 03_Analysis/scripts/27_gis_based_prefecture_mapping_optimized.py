# -*- coding: utf-8 -*-
"""
国土数値情報（行政区域データ）を使用してメッシュの都道府県を正確に判定（高速化版）
"""

import geopandas as gpd
import pandas as pd
from shapely.geometry import box
import os
import sys

# UTF-8出力を強制
sys.stdout.reconfigure(encoding='utf-8')

# パス設定
base_dir = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture"
data_dir = os.path.join(base_dir, "data", "raw", "MLIT_N03")
mesh_file = os.path.join(base_dir, "03_Analysis", "data", "interim", "mesh_coordinates.csv")
output_file = os.path.join(base_dir, "03_Analysis", "data", "interim", "mesh_prefecture_mapping_gis.csv")
report_file = os.path.join(base_dir, "03_Analysis", "data", "interim", "prefecture_coverage_report_gis.txt")

# シェープファイルを検索
shp_files = [f for f in os.listdir(data_dir) if f.endswith('.shp') and 'N03' in f]
if not shp_files:
    print(f"エラー: シェープファイルが見つかりません: {data_dir}")
    sys.exit(1)
shp_path = os.path.join(data_dir, shp_files[0])
print(f"行政区域データ読み込み中: {shp_path}")

# 行政区域データの読み込み
# 必要なカラム: N03_001 (都道府県名), geometry
# N03-2024はUTF-8の可能性が高いので、まずはUTF-8で試行
try:
    print("UTF-8で読み込みを試行...")
    gdf_pref = gpd.read_file(shp_path, encoding='utf-8')
except Exception as e:
    print(f"UTF-8での読み込みに失敗 ({e})。CP932で試行...")
    gdf_pref = gpd.read_file(shp_path, encoding='cp932')

print("行政区域データ読み込み完了")
print(f"総ポリゴン数: {len(gdf_pref)}")

# 高速化のため、Dissolve（統合）をスキップし、そのまま空間結合を行う
# 空間インデックスが効くため、多数のポリゴンでも高速に判定可能

# メッシュデータの読み込み
print("メッシュデータ読み込み中...")
df_mesh = pd.read_csv(mesh_file)
print(f"メッシュ数: {len(df_mesh)}")

# メッシュのジオメトリ作成
geoms = [box(row['west_lon'], row['south_lat'], row['east_lon'], row['north_lat']) for _, row in df_mesh.iterrows()]
gdf_mesh = gpd.GeoDataFrame(df_mesh, geometry=geoms, crs=gdf_pref.crs)

# 空間結合（Spatial Join）
# 各メッシュがどのポリゴン（行政区域）と交差するか判定
print("空間結合（交差判定）実行中...")
# predicate='intersects' で交差するものを抽出
join_result = gpd.sjoin(gdf_mesh, gdf_pref[['N03_001', 'geometry']], how='left', predicate='intersects')

# 結果の集計
print("結果集計中...")
mesh_pref_map = {}

# メッシュごとに都道府県をリスト化（重複排除）
for mesh_code, group in join_result.groupby('mesh_code'):
    prefs = group['N03_001'].dropna().unique().tolist()
    # ソートして文字列化
    prefs.sort()
    mesh_pref_map[mesh_code] = prefs

# 結果をDataFrameに格納
results = []
for _, row in df_mesh.iterrows():
    mesh_code = row['mesh_code']
    prefs = mesh_pref_map.get(mesh_code, [])
    
    results.append({
        'mesh_code': mesh_code,
        'center_lat': row['center_lat'],
        'center_lon': row['center_lon'],
        'prefectures': ', '.join(prefs) if prefs else '海域/国外',
        'pref_count': len(prefs)
    })

result_df = pd.DataFrame(results)

# 保存
result_df.to_csv(output_file, index=False, encoding='utf-8')
print(f"マッピング保存完了: {output_file}")

# レポート作成
pref_counts = {}
for prefs in result_df['prefectures']:
    if prefs != '海域/国外':
        for p in prefs.split(', '):
            pref_counts[p] = pref_counts.get(p, 0) + 1

with open(report_file, 'w', encoding='utf-8') as f:
    f.write("=== GISデータに基づく正確な都道府県カバレッジ（高速版） ===\n\n")
    f.write(f"使用データ: {shp_path}\n")
    f.write(f"総メッシュ数: {len(result_df)}\n\n")
    
    f.write("=== 都道府県別メッシュ数 ===\n")
    sorted_counts = sorted(pref_counts.items(), key=lambda x: x[1], reverse=True)
    for p, c in sorted_counts:
        f.write(f"{p}: {c}\n")
    
    f.write("\n=== 複数都道府県にまたがるメッシュ ===\n")
    multi_pref = result_df[result_df['pref_count'] > 1]
    for _, row in multi_pref.iterrows():
        f.write(f"{row['mesh_code']} ({row['prefectures']})\n")

print("レポート作成完了")
print(open(report_file, 'r', encoding='utf-8').read())
