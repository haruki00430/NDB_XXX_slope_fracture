# -*- coding: utf-8 -*-
"""
G04_c_Elevation ディレクトリ内の176ファイルから都道府県カバレッジを正確に検証
"""

import os
import re
import sys
from collections import defaultdict

# UTF-8出力を強制
sys.stdout.reconfigure(encoding='utf-8')

# メッシュコードから都道府県を推定するための辞書
# 1次メッシュコード(最初の2桁)から都道府県を特定
MESH_TO_PREF = {
    # 北海道・東北
    '30': ['北海道'],
    '36': ['北海道'],
    '37': ['青森県'],
    '38': ['青森県', '秋田県'],
    '39': ['秋田県', '岩手県'],
    '40': ['岩手県', '宮城県'],
    '41': ['宮城県', '山形県'],
    '42': ['山形県', '福島県'],
    '43': ['福島県'],
    '44': ['福島県', '新潟県'],
    
    # 関東
    '45': ['新潟県', '群馬県'],
    '46': ['群馬県', '栃木県', '茨城県'],
    '47': ['栃木県', '茨城県', '千葉県'],
    '48': ['千葉県', '東京都', '神奈川県'],
    '49': ['東京都', '神奈川県', '山梨県'],
    '50': ['山梨県', '静岡県'],
    '51': ['静岡県', '長野県'],
    '52': ['長野県', '岐阜県'],
    '53': ['岐阜県', '愛知県'],
    '54': ['愛知県', '三重県'],
    '55': ['三重県', '滋賀県'],
    '56': ['滋賀県', '京都府'],
    '57': ['京都府', '大阪府'],
    '58': ['大阪府', '兵庫県'],
    '59': ['兵庫県', '鳥取県'],
    '60': ['鳥取県', '島根県'],
    '61': ['島根県', '広島県'],
    '62': ['広島県', '岡山県'],
    '63': ['岡山県', '香川県'],
    '64': ['香川県', '徳島県'],
    '65': ['徳島県', '愛媛県'],
    '66': ['愛媛県', '高知県'],
    '67': ['高知県', '福岡県'],
}

def extract_mesh_code(filename):
    """ファイル名からメッシュコードを抽出"""
    # G04-c-11_5039-jgd_GML.zip -> 5039
    match = re.search(r'_(\d{4})-jgd', filename)
    if match:
        return match.group(1)
    return None

def get_prefectures_from_mesh(mesh_code):
    """メッシュコードから都道府県を推定"""
    if not mesh_code or len(mesh_code) < 2:
        return []
    
    first_two = mesh_code[:2]
    return MESH_TO_PREF.get(first_two, [])

def main():
    # データディレクトリ
    data_dir = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\02_Data\raw\MLIT\G04_c_Elevation"
    
    # 出力ファイル
    output_file = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture\03_Analysis\data\interim\prefecture_coverage_report.txt"
    
    # ファイル一覧を取得
    files = [f for f in os.listdir(data_dir) if f.endswith('.zip')]
    
    # 結果を格納するリスト
    lines = []
    
    lines.append(f"=== G04_c_Elevation 都道府県カバレッジ検証 ===\n")
    lines.append(f"総ファイル数: {len(files)}\n")
    
    # メッシュコードごとに集計
    mesh_counts = defaultdict(int)
    pref_to_meshes = defaultdict(set)
    
    for filename in files:
        mesh_code = extract_mesh_code(filename)
        if mesh_code:
            mesh_counts[mesh_code] += 1
            prefs = get_prefectures_from_mesh(mesh_code)
            for pref in prefs:
                pref_to_meshes[pref].add(mesh_code)
    
    # 結果を表示
    lines.append(f"\n検出されたユニークメッシュコード数: {len(mesh_counts)}\n")
    
    lines.append("\n=== メッシュコード分布 (上位20) ===\n")
    sorted_meshes = sorted(mesh_counts.items(), key=lambda x: x[1], reverse=True)
    for mesh, count in sorted_meshes[:20]:
        prefs = get_prefectures_from_mesh(mesh)
        pref_str = ', '.join(prefs) if prefs else '不明'
        lines.append(f"{mesh}: {count}ファイル ({pref_str})\n")
    
    lines.append(f"\n=== 都道府県別カバレッジ ===\n")
    sorted_prefs = sorted(pref_to_meshes.items(), key=lambda x: len(x[1]), reverse=True)
    
    for pref, meshes in sorted_prefs:
        lines.append(f"{pref}: {len(meshes)}メッシュ\n")
    
    lines.append(f"\n=== サマリー ===\n")
    lines.append(f"カバーされている都道府県数: {len(pref_to_meshes)}\n")
    lines.append(f"カバーされている都道府県:\n")
    for pref in sorted([p for p in pref_to_meshes.keys()]):
        lines.append(f"  - {pref}\n")
    
    # 全47都道府県のリスト
    all_prefs = [
        '北海道', '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県',
        '茨城県', '栃木県', '群馬県', '埼玉県', '千葉県', '東京都', '神奈川県',
        '新潟県', '富山県', '石川県', '福井県', '山梨県', '長野県',
        '岐阜県', '静岡県', '愛知県', '三重県',
        '滋賀県', '京都府', '大阪府', '兵庫県', '奈良県', '和歌山県',
        '鳥取県', '島根県', '岡山県', '広島県', '山口県',
        '徳島県', '香川県', '愛媛県', '高知県',
        '福岡県', '佐賀県', '長崎県', '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県'
    ]
    
    missing_prefs = set(all_prefs) - set(pref_to_meshes.keys())
    lines.append(f"\nカバーされていない都道府県数: {len(missing_prefs)}\n")
    if missing_prefs:
        lines.append(f"カバーされていない都道府県:\n")
        for pref in sorted(missing_prefs):
            lines.append(f"  - {pref}\n")
    
    # ファイルに保存
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"レポートを保存しました: {output_file}")

if __name__ == "__main__":
    main()

