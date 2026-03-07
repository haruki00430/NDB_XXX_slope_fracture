"""
K046骨折手術コードの所在を特定するスクリプト
"""

import pandas as pd
import sys
from pathlib import Path

# プロジェクトルート
project_root = Path(__file__).resolve().parents[4]

def search_k046_in_surgery_data():
    """手術データからK046を検索"""
    print("=" * 80)
    print("K046（骨折手術）コードの検索")
    print("=" * 80)

    surgery_path = project_root / "02_Data/raw/NDB_OpenData/No.10/01_医科診療行為（算定回数）/01_公費レセプトを含まないデータ/K_手術/款別都道府県別算定回数.xlsx"

    if not surgery_path.exists():
        print(f"[ERROR] ファイル未発見: {surgery_path}")
        return

    print(f"[OK] ファイル: {surgery_path.name}\n")

    # 最初のシート（全般）を読み込み
    print("[1] 最初のシート（全般）の読み込み...")
    xl = pd.ExcelFile(surgery_path)

    # ヘッダー行を確認
    df_header = pd.read_excel(surgery_path, sheet_name=0, nrows=10)
    print("\n[ヘッダー部分（最初の10行）]:")
    print(df_header.iloc[:, :5])  # 最初の5列のみ表示
    print()

    # K046を含む行を検索
    print("[2] K046を含む行を検索...")
    df_full = pd.read_excel(surgery_path, sheet_name=0, header=None)

    k046_rows = []
    for idx, row in df_full.iterrows():
        row_str = ' '.join(row.astype(str).tolist())
        if 'K046' in row_str or '骨折' in row_str:
            k046_rows.append((idx, row.tolist()[:10]))  # 最初の10列のみ
            if len(k046_rows) <= 5:  # 最初の5件を表示
                print(f"  行{idx}: {row.tolist()[:5]}")

    print(f"\n[結果] K046を含む行: {len(k046_rows)}件\n")

    # 最も関連性の高い行を特定
    if k046_rows:
        print("[3] 大腿骨骨折（K0461）・上腕骨骨折（K0421）を検索...")
        for idx, row_data in k046_rows[:20]:  # 最初の20件を確認
            row_str = ' '.join(map(str, row_data))
            if 'K0461' in row_str or '大腿骨近位部' in row_str:
                print(f"  [大腿骨] 行{idx}: {row_data}")
            if 'K0421' in row_str or '上腕骨' in row_str:
                print(f"  [上腕骨] 行{idx}: {row_data}")

def main():
    search_k046_in_surgery_data()
    print("=" * 80)
    print("[完了]")
    print("=" * 80)

if __name__ == "__main__":
    main()
