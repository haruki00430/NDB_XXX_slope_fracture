# -*- coding: utf-8 -*-
"""
元データから都道府県別メッシュ数を正確に再集計（簡易版）
"""

import pandas as pd
import sys

# UTF-8出力を強制
sys.stdout.reconfigure(encoding='utf-8')

# データ読み込み
df = pd.read_csv(r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture\03_Analysis\data\interim\mesh_prefecture_mapping_final.csv")

# 都道府県別メッシュ数を集計
pref_counts = {}

for _, row in df.iterrows():
    prefs_str = row['prefectures']
    if prefs_str != '不明':
        # カンマ区切りで都道府県を分割
        prefs = [p.strip() for p in str(prefs_str).split(',')]
        for pref in prefs:
            pref_counts[pref] = pref_counts.get(pref, 0) + 1

# 結果をCSVに保存
result_df = pd.DataFrame(list(pref_counts.items()), columns=['prefecture', 'mesh_count'])
result_df = result_df.sort_values('mesh_count', ascending=False)
result_df.to_csv(r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture\03_Analysis\data\interim\prefecture_mesh_counts_verified.csv", index=False, encoding='utf-8')

print(f"Saved to prefecture_mesh_counts_verified.csv")
print(f"Total prefectures: {len(result_df)}")
