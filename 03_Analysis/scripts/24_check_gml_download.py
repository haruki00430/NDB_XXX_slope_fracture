# -*- coding: utf-8 -*-
"""
サンプルGMLファイルをダウンロードして都道府県情報を確認
"""

import urllib.request
import os
import sys

# UTF-8出力を強制
sys.stdout.reconfigure(encoding='utf-8')

# サンプルメッシュコード（北海道の6139を使用）
mesh_code = "6139"

# ダウンロードURL（国土地理院のG04-c DEM）
# URL形式: https://cyberjapandata.gsi.go.jp/xyz/dem5a_png/{mesh_code}.txt
# 実際のGMLファイルのURL形式を確認する必要がある

# まず、国土地理院のデータカタログページを確認
print("=== G04-c DEMデータのダウンロード方法を確認 ===")
print()
print("国土地理院のG04-c（数値標高モデル）データは以下の方法で入手可能:")
print()
print("1. 基盤地図情報ダウンロードサービス")
print("   https://fgd.gsi.go.jp/download/menu.php")
print()
print("2. 地理院タイル（標高タイル）")
print("   https://maps.gsi.go.jp/development/ichiran.html")
print()
print("注: G04-cデータは基盤地図情報として提供されており、")
print("    メッシュ単位でのダウンロードにはユーザー登録が必要です。")
print()
print("代替案:")
print("1. 地理院地図でメッシュコードを検索し、含まれる都道府県を目視確認")
print("2. 都道府県境界のGISデータ（Shapefile）を使用して自動判定")
print()

# 出力ディレクトリを作成
output_dir = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture\data\raw"
os.makedirs(output_dir, exist_ok=True)

print(f"出力ディレクトリ: {output_dir}")
