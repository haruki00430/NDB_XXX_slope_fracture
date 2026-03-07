"""
手術データの詳細分析：K046骨折関連データの抽出可能性を検証
"""

import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parents[4]

def analyze_surgery_detail():
    """手術データの詳細分析"""
    print("=" * 80)
    print("手術データの詳細分析")
    print("=" * 80)

    surgery_path = project_root / "02_Data/raw/NDB_OpenData/No.10/01_医科診療行為（算定回数）/01_公費レセプトを含まないデータ/K_手術/款別都道府県別算定回数.xlsx"

    if not surgery_path.exists():
        print(f"[ERROR] ファイル未発見")
        return

    # 全シートのデータを確認
    xl = pd.ExcelFile(surgery_path)
    print(f"\n[シート一覧]:")
    for i, sheet in enumerate(xl.sheet_names):
        print(f"  {i}. {sheet}")

    # 最初のシート（全般）を読み込み
    print("\n" + "=" * 80)
    print("[シート0（全般）の分析]")
    print("=" * 80)

    # ヘッダーなしで全体を読み込み
    df_full = pd.read_excel(surgery_path, sheet_name=0, header=None)
    print(f"\n[データサイズ]: {df_full.shape[0]}行 x {df_full.shape[1]}列\n")

    # 最初の20行を確認（ヘッダー構造を理解）
    print("[最初の20行（ヘッダー部分）]:")
    for idx in range(min(20, len(df_full))):
        row_preview = df_full.iloc[idx, :5].tolist()
        print(f"  行{idx}: {row_preview}")

    # K046を含む行を詳細に検索
    print("\n" + "=" * 80)
    print("[K046骨折関連の行を検索]")
    print("=" * 80)

    k046_rows = []
    for idx, row in df_full.iterrows():
        row_str = ' '.join([str(x) for x in row.tolist() if pd.notna(x)])
        if 'K046' in row_str:
            k046_rows.append((idx, row.tolist()))

    print(f"\n[発見]: K046を含む行が {len(k046_rows)} 件\n")

    # 最初の10件を詳細表示
    for i, (idx, row_data) in enumerate(k046_rows[:10]):
        print(f"\n--- 行{idx} ---")
        print(f"  列0: {row_data[0]}")
        print(f"  列1: {row_data[1]}")
        print(f"  列2: {row_data[2]}")
        print(f"  列3: {row_data[3]}")
        print(f"  列4: {row_data[4]}")
        if len(row_data) > 5:
            print(f"  列5-10: {row_data[5:11]}")

    # データ行の開始位置を特定
    print("\n" + "=" * 80)
    print("[データ行の開始位置を特定]")
    print("=" * 80)

    # 都道府県名が出現する行を探す
    prefecture_keywords = ['北海道', '青森', '秋田', '東京', '大阪', '福岡', '沖縄']
    data_start_row = None

    for idx, row in df_full.iterrows():
        row_str = ' '.join([str(x) for x in row.tolist() if pd.notna(x)])
        for keyword in prefecture_keywords:
            if keyword in row_str:
                print(f"\n[都道府県発見] 行{idx}: {keyword}")
                if data_start_row is None:
                    data_start_row = idx
                if idx < 50:  # 最初の50行のみ表示
                    print(f"  行内容: {row.tolist()[:10]}")
                break

    if data_start_row:
        print(f"\n[推定] データ開始行: {data_start_row}")

    # MultiIndexとして読み込みを試みる（header行を推定）
    if data_start_row and data_start_row > 3:
        print("\n" + "=" * 80)
        print(f"[MultiIndex読み込みテスト] header=[0, 1]")
        print("=" * 80)
        try:
            df_multi = pd.read_excel(surgery_path, sheet_name=0, header=[0, 1])
            print(f"\n[成功] 行数: {len(df_multi)}, 列数: {len(df_multi.columns)}")
            print(f"\n[カラム例（最初の15列）]:")
            for i, col in enumerate(df_multi.columns[:15]):
                print(f"  {i+1}. {col}")

            # データの一部を表示
            print(f"\n[データサンプル（最初の5行×5列）]:")
            print(df_multi.iloc[:5, :5])

        except Exception as e:
            print(f"[ERROR] MultiIndex読み込み失敗: {e}")

def main():
    analyze_surgery_detail()
    print("\n" + "=" * 80)
    print("[完了]")
    print("=" * 80)

if __name__ == "__main__":
    main()
