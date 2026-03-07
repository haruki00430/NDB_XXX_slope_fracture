# -*- coding: utf-8 -*-
"""
北海道の43メッシュから、北海道以外のメッシュを特定
"""

import pandas as pd
import sys

# UTF-8出力を強制
sys.stdout.reconfigure(encoding='utf-8')

# データ読み込み
mapping_df = pd.read_csv(r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture\03_Analysis\data\interim\mesh_prefecture_mapping_final_v2.csv")

# 北海道を含むメッシュを抽出
hokkaido_meshes = mapping_df[mapping_df['prefectures'].str.contains('北海道', na=False)]

print("=== 北海道を含む全43メッシュ ===")
print(f"総数: {len(hokkaido_meshes)}メッシュ\n")

# ユーザー確認の情報
# - 北海道の正しいメッシュ数: 40
# - 青森県との重複: 6240, 6241 (2メッシュ)
# - 離島を含むメッシュ: 6339, 6545, 6546, 6645, 6646, 6647, 6740, 6741, 6747, 6748, 6840, 6841, 6847, 6848 (14メッシュ)

correct_hokkaido_overlap = [6240, 6241]  # 青森県との重複
island_meshes = [6339, 6545, 6546, 6645, 6646, 6647, 6740, 6741, 6747, 6748, 6840, 6841, 6847, 6848]

# 全メッシュリスト
all_meshes = hokkaido_meshes['mesh_code'].tolist()

print("メッシュコード | 中心緯度 | 中心経度 | 都道府県 | 分類")
print("-" * 100)

incorrect_meshes = []

for mesh_code in all_meshes:
    row = hokkaido_meshes[hokkaido_meshes['mesh_code'] == mesh_code].iloc[0]
    
    # 分類
    if mesh_code in correct_hokkaido_overlap:
        category = "青森県と重複（正）"
    elif mesh_code in island_meshes:
        category = "離島を含む（正）"
    else:
        # 青森県との重複でも離島でもない
        prefs = row['prefectures']
        if '青森県' in prefs:
            category = "青森県と重複（要確認）"
            incorrect_meshes.append(mesh_code)
        else:
            category = "北海道単独（正）"
    
    print(f"{mesh_code} | {row['center_lat']:.2f}°N | {row['center_lon']:.2f}°E | {row['prefectures']} | {category}")

print()
print(f"=== 分析結果 ===")
print(f"総メッシュ数: {len(all_meshes)}")
print(f"青森県との重複（ユーザー確認）: {len(correct_hokkaido_overlap)}メッシュ → {correct_hokkaido_overlap}")
print(f"離島を含むメッシュ（ユーザー確認）: {len(island_meshes)}メッシュ")
print(f"青森県と重複（要確認）: {len(incorrect_meshes)}メッシュ → {incorrect_meshes}")
print()
print(f"北海道の正しいメッシュ数（ユーザー確認）: 40メッシュ")
print(f"誤って含まれているメッシュ数: {len(all_meshes) - 40} = {43 - 40}メッシュ")
print()
print("=== 誤って含まれている可能性のあるメッシュ ===")
print("青森県との重複メッシュのうち、6240, 6241以外:")
for mesh_code in incorrect_meshes:
    if mesh_code not in correct_hokkaido_overlap:
        row = hokkaido_meshes[hokkaido_meshes['mesh_code'] == mesh_code].iloc[0]
        print(f"  {mesh_code} | {row['center_lat']:.2f}°N, {row['center_lon']:.2f}°E | {row['prefectures']}")
