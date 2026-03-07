# -*- coding: utf-8 -*-
"""
メッシュ座標から都道府県を特定（修正版：東京都を本州と離島に分離）
"""

import pandas as pd
import sys

# UTF-8出力を強制
sys.stdout.reconfigure(encoding='utf-8')

# メッシュ座標データを読み込み
mesh_df = pd.read_csv(r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture\03_Analysis\data\interim\mesh_coordinates.csv")

# 都道府県の緯度経度範囲（修正版：東京都を本州と離島に分離）
pref_ranges = {
    '北海道': {'lat': (41.0, 46.0), 'lon': (139.0, 149.0)},
    '青森県': {'lat': (40.0, 41.6), 'lon': (139.5, 141.5)},
    '岩手県': {'lat': (38.7, 40.5), 'lon': (140.5, 142.0)},
    '宮城県': {'lat': (37.7, 39.0), 'lon': (140.3, 141.7)},
    '秋田県': {'lat': (38.8, 40.6), 'lon': (139.5, 141.0)},
    '山形県': {'lat': (37.7, 39.3), 'lon': (139.5, 140.7)},
    '福島県': {'lat': (36.8, 38.0), 'lon': (139.0, 141.0)},
    '茨城県': {'lat': (35.7, 36.9), 'lon': (139.7, 140.9)},
    '栃木県': {'lat': (36.2, 37.2), 'lon': (139.3, 140.3)},
    '群馬県': {'lat': (36.0, 37.2), 'lon': (138.4, 139.7)},
    '埼玉県': {'lat': (35.7, 36.3), 'lon': (138.7, 140.0)},
    '千葉県': {'lat': (34.9, 36.1), 'lon': (139.7, 140.9)},
    # 東京都は本州部分と離島部分を分けて定義
    '東京都（本州）': {'lat': (35.5, 36.0), 'lon': (138.9, 140.0)},
    '東京都（離島）': {'lat': (20.0, 35.0), 'lon': (136.0, 154.0)},
    '神奈川県': {'lat': (35.1, 35.6), 'lon': (138.9, 140.0)},
    '新潟県': {'lat': (36.7, 38.6), 'lon': (137.6, 139.9)},
    '富山県': {'lat': (36.3, 37.0), 'lon': (136.8, 137.8)},
    '石川県': {'lat': (36.0, 37.9), 'lon': (136.2, 137.4)},
    '福井県': {'lat': (35.3, 36.4), 'lon': (135.4, 136.9)},
    '山梨県': {'lat': (35.1, 36.0), 'lon': (138.2, 139.2)},
    '長野県': {'lat': (35.1, 37.1), 'lon': (137.3, 138.9)},
    '岐阜県': {'lat': (35.2, 36.4), 'lon': (136.4, 137.9)},
    '静岡県': {'lat': (34.6, 35.7), 'lon': (137.5, 139.2)},
    '愛知県': {'lat': (34.4, 35.4), 'lon': (136.7, 137.8)},
    '三重県': {'lat': (33.7, 35.2), 'lon': (135.8, 136.9)},
    '滋賀県': {'lat': (34.8, 35.7), 'lon': (135.8, 136.5)},
    '京都府': {'lat': (34.7, 35.8), 'lon': (134.9, 136.0)},
    '大阪府': {'lat': (34.3, 35.0), 'lon': (135.1, 135.7)},
    '兵庫県': {'lat': (34.2, 35.7), 'lon': (134.2, 135.5)},
    '奈良県': {'lat': (33.9, 34.8), 'lon': (135.6, 136.2)},
    '和歌山県': {'lat': (33.4, 34.4), 'lon': (135.1, 136.0)},
    '鳥取県': {'lat': (35.1, 35.6), 'lon': (133.2, 134.4)},
    '島根県': {'lat': (34.2, 36.0), 'lon': (131.7, 133.5)},
    '岡山県': {'lat': (34.2, 35.4), 'lon': (133.2, 134.4)},
    '広島県': {'lat': (34.0, 35.0), 'lon': (132.0, 133.5)},
    '山口県': {'lat': (33.7, 34.6), 'lon': (130.8, 132.3)},
    '徳島県': {'lat': (33.6, 34.3), 'lon': (133.5, 134.8)},
    '香川県': {'lat': (34.1, 34.5), 'lon': (133.5, 134.5)},
    '愛媛県': {'lat': (32.9, 34.4), 'lon': (132.3, 133.5)},
    '高知県': {'lat': (32.7, 33.9), 'lon': (132.4, 134.3)},
    '福岡県': {'lat': (33.0, 34.0), 'lon': (129.7, 131.2)},
    '佐賀県': {'lat': (33.0, 33.6), 'lon': (129.7, 130.5)},
    '長崎県': {'lat': (32.5, 34.0), 'lon': (128.8, 130.5)},
    '熊本県': {'lat': (32.0, 33.3), 'lon': (130.2, 131.3)},
    '大分県': {'lat': (32.8, 33.6), 'lon': (130.8, 132.0)},
    '宮崎県': {'lat': (31.3, 32.8), 'lon': (130.7, 131.9)},
    '鹿児島県': {'lat': (24.0, 32.2), 'lon': (128.0, 131.5)},
    '沖縄県': {'lat': (24.0, 28.0), 'lon': (122.0, 132.0)},
}

def check_overlap(mesh_s_lat, mesh_n_lat, mesh_w_lon, mesh_e_lon, pref_lat, pref_lon):
    """メッシュの範囲と都道府県の範囲が重なっているかチェック"""
    pref_s_lat, pref_n_lat = pref_lat
    pref_w_lon, pref_e_lon = pref_lon
    
    # 緯度の重なりをチェック
    lat_overlap = not (mesh_n_lat < pref_s_lat or mesh_s_lat > pref_n_lat)
    # 経度の重なりをチェック
    lon_overlap = not (mesh_e_lon < pref_w_lon or mesh_w_lon > pref_e_lon)
    
    return lat_overlap and lon_overlap

# 各メッシュに対して都道府県を判定
results = []
for _, row in mesh_df.iterrows():
    mesh_code = row['mesh_code']
    s_lat, n_lat = row['south_lat'], row['north_lat']
    w_lon, e_lon = row['west_lon'], row['east_lon']
    c_lat, c_lon = row['center_lat'], row['center_lon']
    
    # 該当する都道府県を探す（メッシュ範囲全体で判定）
    matched_prefs = []
    for pref, ranges in pref_ranges.items():
        if check_overlap(s_lat, n_lat, w_lon, e_lon, ranges['lat'], ranges['lon']):
            # 東京都（本州）と東京都（離島）は「東京都」として統合
            if pref.startswith('東京都'):
                if '東京都' not in matched_prefs:
                    matched_prefs.append('東京都')
            else:
                matched_prefs.append(pref)
    
    results.append({
        'mesh_code': mesh_code,
        'center_lat': c_lat,
        'center_lon': c_lon,
        'prefectures': ', '.join(matched_prefs) if matched_prefs else '不明',
        'pref_count': len(matched_prefs)
    })

# DataFrameに変換
result_df = pd.DataFrame(results)

# 都道府県ごとのメッシュ数を集計
pref_mesh_counts = {}
for prefs_str in result_df['prefectures']:
    if prefs_str != '不明':
        for pref in prefs_str.split(', '):
            pref_mesh_counts[pref] = pref_mesh_counts.get(pref, 0) + 1

# 結果を保存
output_file = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture\03_Analysis\data\interim\mesh_prefecture_mapping_corrected.csv"
result_df.to_csv(output_file, index=False, encoding='utf-8')

# レポート作成
report_lines = []
report_lines.append("=== G04-c メッシュの都道府県カバレッジ（修正版：東京都を本州と離島に分離） ===\n")
report_lines.append(f"総メッシュ数: {len(result_df)}\n\n")

report_lines.append("=== 都道府県別メッシュ数 ===\n")
sorted_prefs = sorted(pref_mesh_counts.items(), key=lambda x: x[1], reverse=True)
for pref, count in sorted_prefs:
    report_lines.append(f"{pref}: {count}メッシュ\n")

report_lines.append(f"\n=== サマリー ===\n")
report_lines.append(f"カバーされている都道府県数: {len(pref_mesh_counts)}\n")

# レポートを保存
report_file = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture\03_Analysis\data\interim\prefecture_coverage_report_corrected.txt"
with open(report_file, 'w', encoding='utf-8') as f:
    f.writelines(report_lines)

print(''.join(report_lines))
print(f"\nマッピングファイル: {output_file}")
print(f"レポートファイル: {report_file}")
