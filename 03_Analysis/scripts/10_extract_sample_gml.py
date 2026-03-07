# -*- coding: utf-8 -*-
"""
サンプルGMLファイルを展開して構造を確認
"""

import os
import zipfile
import sys

# UTF-8出力を強制
sys.stdout.reconfigure(encoding='utf-8')

# パス設定
zip_path = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\02_Data\raw\MLIT\G04_c_Elevation\G04-c-11_5030-jgd_GML.zip"
extract_dir = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture\03_Analysis\data\interim\sample_gml"

# 既存ディレクトリを削除
if os.path.exists(extract_dir):
    import shutil
    shutil.rmtree(extract_dir)

# ZIPファイルを展開
os.makedirs(extract_dir, exist_ok=True)
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_dir)

# 展開されたファイルを確認
print(f"展開先: {extract_dir}\n")
print("展開されたファイル:")
for root, dirs, files in os.walk(extract_dir):
    for file in files:
        file_path = os.path.join(root, file)
        file_size = os.path.getsize(file_path)
        print(f"  {file} ({file_size:,} bytes)")
        
        # GMLファイルの場合、最初の100行を表示
        if file.endswith('.xml') or file.endswith('.gml'):
            print(f"\n  === {file} の最初の100行 ===")
            
            # エンコーディングを試行
            encodings = ['utf-8', 'shift-jis', 'cp932', 'euc-jp']
            content_read = False
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        for i, line in enumerate(f):
                            if i >= 100:
                                break
                            print(f"  {i+1:3d}: {line.rstrip()}")
                    print(f"  (エンコーディング: {encoding})")
                    content_read = True
                    break
                except UnicodeDecodeError:
                    continue
            
            if not content_read:
                print(f"  エラー: ファイルを読み込めませんでした")
            print()

