# -*- coding: utf-8 -*-
"""
全176個のG04-cファイルから座標範囲を抽出
"""

import os
import zipfile
import xml.etree.ElementTree as ET
import sys
import re

# UTF-8出力を強制
sys.stdout.reconfigure(encoding='utf-8')

# パス設定
data_dir = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\02_Data\raw\MLIT\G04_c_Elevation"
output_file = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture\03_Analysis\data\interim\mesh_coordinates.csv"

# 結果を格納
results = []

# 全ZIPファイルを処理
zip_files = [f for f in os.listdir(data_dir) if f.endswith('.zip')]
print(f"処理対象ファイル数: {len(zip_files)}")

for i, zip_filename in enumerate(zip_files, 1):
    zip_path = os.path.join(data_dir, zip_filename)
    
    # メッシュコードを抽出
    match = re.search(r'_(\d{4})-jgd', zip_filename)
    if not match:
        print(f"警告: メッシュコードを抽出できません: {zip_filename}")
        continue
    
    mesh_code = match.group(1)
    
    try:
        # ZIPファイルを開く
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # GMLファイルを探す
            gml_files = [f for f in zip_ref.namelist() if f.endswith('.xml') and not f.startswith('KS-META')]
            
            if not gml_files:
                print(f"警告: GMLファイルが見つかりません: {zip_filename}")
                continue
            
            gml_filename = gml_files[0]
            
            # GMLファイルを読み込む
            with zip_ref.open(gml_filename) as gml_file:
                # XMLをパース
                tree = ET.parse(gml_file)
                root = tree.getroot()
                
                # 名前空間を定義
                namespaces = {
                    'gml': 'http://www.opengis.net/gml/3.2',
                    'ksj': 'http://nlftp.mlit.go.jp/ksj/schemas/ksj-app'
                }
                
                # boundedByから座標範囲を取得
                bounded_by = root.find('.//gml:boundedBy', namespaces)
                if bounded_by is not None:
                    lower_corner = bounded_by.find('.//gml:lowerCorner', namespaces)
                    upper_corner = bounded_by.find('.//gml:upperCorner', namespaces)
                    
                    if lower_corner is not None and upper_corner is not None:
                        # 座標を分割
                        lower_coords = lower_corner.text.strip().split()
                        upper_coords = upper_corner.text.strip().split()
                        
                        south_lat = float(lower_coords[0])
                        west_lon = float(lower_coords[1])
                        north_lat = float(upper_coords[0])
                        east_lon = float(upper_coords[1])
                        
                        results.append({
                            'mesh_code': mesh_code,
                            'filename': zip_filename,
                            'south_lat': south_lat,
                            'west_lon': west_lon,
                            'north_lat': north_lat,
                            'east_lon': east_lon,
                            'center_lat': (south_lat + north_lat) / 2,
                            'center_lon': (west_lon + east_lon) / 2
                        })
                        
                        if i % 20 == 0:
                            print(f"処理中... {i}/{len(zip_files)}")
                    else:
                        print(f"警告: 座標情報が見つかりません: {zip_filename}")
                else:
                    print(f"警告: boundedByが見つかりません: {zip_filename}")
    
    except Exception as e:
        print(f"エラー: {zip_filename} - {str(e)}")

# CSVに保存
print(f"\n抽出完了: {len(results)}件")
print(f"保存先: {output_file}")

with open(output_file, 'w', encoding='utf-8') as f:
    f.write("mesh_code,filename,south_lat,west_lon,north_lat,east_lon,center_lat,center_lon\n")
    for r in results:
        f.write(f"{r['mesh_code']},{r['filename']},{r['south_lat']},{r['west_lon']},{r['north_lat']},{r['east_lon']},{r['center_lat']},{r['center_lon']}\n")

print("\n最初の10件:")
for r in results[:10]:
    print(f"  {r['mesh_code']}: ({r['south_lat']:.2f}, {r['west_lon']:.2f}) - ({r['north_lat']:.2f}, {r['east_lon']:.2f})")
