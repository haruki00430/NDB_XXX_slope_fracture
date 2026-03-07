import os
import glob
import re
from collections import defaultdict

target_dir = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\02_Data\raw\MLIT\G04_c_Elevation"

# 全ファイルを取得
zip_files = glob.glob(os.path.join(target_dir, "*.zip"))
print(f"Total files: {len(zip_files)}")

# メッシュコードを抽出して都道府県を推定
# より詳細なマッピング辞書を作成

# 1次メッシュコード(上2桁)から都道府県を推定
# 参考: https://www.gsi.go.jp/KOKUJYOHO/MENCHO/backnumber/mesh_map.html

def estimate_prefecture_from_mesh(mesh_code_str):
    """
    メッシュコードから都道府県を推定する(詳細版)
    1次メッシュコード(4桁)の上2桁から推定
    """
    try:
        first_two = int(mesh_code_str[:2])
        
        # より詳細なマッピング
        # 緯度ベース(北緯20度〜46度)
        if 30 <= first_two <= 31:
            return "沖縄県"
        elif 32 <= first_two <= 33:
            return "鹿児島県"
        elif 34 <= first_two <= 35:
            return "宮崎県"
        elif 36 <= first_two <= 37:
            return "熊本県"
        elif 38 <= first_two <= 39:
            return "大分県"
        elif 40 <= first_two <= 41:
            return "福岡県/佐賀県/長崎県"
        elif 42 <= first_two <= 43:
            return "山口県/広島県"
        elif 44 <= first_two <= 45:
            return "島根県/鳥取県"
        elif 46 <= first_two <= 47:
            return "岡山県/兵庫県"
        elif 48 <= first_two <= 49:
            return "香川県/徳島県/愛媛県/高知県"
        elif 50 <= first_two <= 51:
            return "大阪府/京都府/奈良県/和歌山県"
        elif 52 <= first_two <= 53:
            return "滋賀県/三重県/愛知県/岐阜県"
        elif 54 <= first_two <= 55:
            return "静岡県/山梨県/長野県/神奈川県/東京都"
        elif 56 <= first_two <= 57:
            return "埼玉県/千葉県/茨城県/栃木県/群馬県"
        elif 58 <= first_two <= 59:
            return "新潟県/福島県/山形県"
        elif 60 <= first_two <= 61:
            return "秋田県/岩手県/宮城県"
        elif 62 <= first_two <= 63:
            return "青森県"
        elif 64 <= first_two <= 68:
            return "北海道"
        else:
            return "不明"
    except:
        return "エラー"

# メッシュコード別にカウント
mesh_distribution = defaultdict(int)
region_distribution = defaultdict(int)

for f in zip_files:
    basename = os.path.basename(f)
    # G04-c-11_MMMM-jgd_GML.zip
    match = re.search(r'_(\d{4})', basename)
    if match:
        mesh_code = match.group(1)
        mesh_distribution[mesh_code[:2]] += 1
        region = estimate_prefecture_from_mesh(mesh_code)
        region_distribution[region] += 1

print("\n=== 1次メッシュコード(上2桁)別ファイル数 ===")
for mesh, count in sorted(mesh_distribution.items()):
    region = estimate_prefecture_from_mesh(mesh + "00")
    print(f"{mesh}xx: {count:3d}ファイル → {region}")

print("\n=== 推定地域別ファイル数 ===")
for region, count in sorted(region_distribution.items(), key=lambda x: x[1], reverse=True):
    print(f"{region}: {count}ファイル")

# 全メッシュコードをリスト化
all_meshes = []
for f in zip_files:
    basename = os.path.basename(f)
    match = re.search(r'_(\d{4})', basename)
    if match:
        all_meshes.append(match.group(1))

print(f"\n=== メッシュコード範囲 ===")
print(f"最小: {min(all_meshes)}")
print(f"最大: {max(all_meshes)}")
print(f"ユニーク数: {len(set(all_meshes))}")
