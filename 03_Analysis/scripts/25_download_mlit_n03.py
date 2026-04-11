# -*- coding: utf-8 -*-
"""
国土数値情報（行政区域データ）をダウンロードして解凍
"""

import os
import urllib.request
import zipfile
import sys

# UTF-8出力を強制
sys.stdout.reconfigure(encoding='utf-8')

# ダウンロード先のディレクトリ
download_dir = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture\data\raw\MLIT_N03"
os.makedirs(download_dir, exist_ok=True)

# ダウンロードURL（2024年1月1日時点のデータ）
# URLパターン: https://nlftp.mlit.go.jp/ksj/gml/data/N03/N03-2024/N03-20240101_GML.zip
url = "https://nlftp.mlit.go.jp/ksj/gml/data/N03/N03-2024/N03-20240101_GML.zip"
zip_path = os.path.join(download_dir, "N03-20240101_GML.zip")

print(f"ダウンロード開始: {url}")
try:
    urllib.request.urlretrieve(url, zip_path)
    print("ダウンロード完了")
except Exception as e:
    print(f"ダウンロード失敗: {e}")
    # 2023年版を試行
    url = "https://nlftp.mlit.go.jp/ksj/gml/data/N03/N03-2023/N03-20230101_GML.zip"
    zip_path = os.path.join(download_dir, "N03-20230101_GML.zip")
    print(f"2023年版を試行: {url}")
    try:
        urllib.request.urlretrieve(url, zip_path)
        print("ダウンロード完了")
    except Exception as e:
        print(f"ダウンロード失敗: {e}")
        sys.exit(1)

# 解凍
print("解凍中...")
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(download_dir)
print("解凍完了")

# シェープファイルを確認
files = os.listdir(download_dir)
shp_files = [f for f in files if f.endswith('.shp') or f.endswith('.geojson')]
print(f"取得したファイル: {shp_files}")
