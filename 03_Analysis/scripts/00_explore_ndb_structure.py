"""
NDBデータ構造の探索スクリプト
手術データと質問票データの構造を確認する
"""

import pandas as pd
import sys
from pathlib import Path

# プロジェクトルートへのパス設定
# スクリプトから見て: scripts -> 03_Analysis -> NDB_XXX_slope_fracture -> projects -> NDB_Research_Hub
project_root = Path(__file__).resolve().parents[4]
sys.path.append(str(project_root))

print(f"[INFO] プロジェクトルート: {project_root}\n")

def explore_surgery_data():
    """手術データの構造を探索"""
    print("=" * 80)
    print("手術データの探索")
    print("=" * 80)

    # 手術データパス
    surgery_path = project_root / "02_Data/raw/NDB_OpenData/No.10/01_医科診療行為（算定回数）/01_公費レセプトを含まないデータ/K_手術/款別都道府県別算定回数.xlsx"

    if not surgery_path.exists():
        print(f"[ERROR] ファイルが見つかりません: {surgery_path}")
        return

    print(f"[OK] ファイル発見: {surgery_path.name}\n")

    # シート名を確認
    print("[シート名]:")
    xl = pd.ExcelFile(surgery_path)
    for i, sheet in enumerate(xl.sheet_names, 1):
        print(f"  {i}. {sheet}")
    print()

    # 最初のシートを読み込み（ヘッダー確認）
    print("[最初のシートの先頭5行（ヘッダー構造確認）]:")
    df_raw = pd.read_excel(surgery_path, sheet_name=0, nrows=5)
    print(df_raw)
    print()

    # MultiIndexヘッダーとして読み込み
    print("[MultiIndexとして読み込み（header=[0, 1]）]:")
    df_multi = pd.read_excel(surgery_path, sheet_name=0, header=[0, 1], nrows=3)
    print(f"カラム数: {len(df_multi.columns)}")
    print(f"カラムの例（最初の10列）:")
    for i, col in enumerate(df_multi.columns[:10], 1):
        print(f"  {i}. {col}")
    print()

    # K046（骨折）を検索
    print("[K046（骨折手術）コードを検索]:")
    for sheet_name in xl.sheet_names:
        if 'K046' in sheet_name or '骨折' in sheet_name:
            print(f"  [OK] 発見: {sheet_name}")
    print()

def explore_questionnaire_data():
    """質問票データの構造を探索"""
    print("=" * 80)
    print("質問票データの探索（質問項目16：歩行速度）")
    print("=" * 80)

    # 質問票16（歩行速度）のパス
    q16_path = project_root / "02_Data/raw/NDB_OpenData/No.10/07_特定健診 質問票/01_公費レセプトを含まないデータ/標準的な質問票（質問項目１６） 都道府県別性年齢階級別分布.xlsx"

    if not q16_path.exists():
        print(f"[ERROR] ファイルが見つかりません: {q16_path}")
        return

    print(f"[OK] ファイル発見: {q16_path.name}\n")

    # シート名を確認
    print("[シート名]:")
    xl = pd.ExcelFile(q16_path)
    for i, sheet in enumerate(xl.sheet_names, 1):
        print(f"  {i}. {sheet}")
    print()

    # 最初のシートを読み込み（ヘッダー確認）
    print("[最初のシートの先頭5行（ヘッダー構造確認）]:")
    df_raw = pd.read_excel(q16_path, sheet_name=0, nrows=5)
    print(df_raw)
    print()

    # MultiIndexヘッダーとして読み込み（header=[2, 3]）
    print("[MultiIndexとして読み込み（header=[2, 3]）]:")
    try:
        df_multi = pd.read_excel(q16_path, sheet_name=0, header=[2, 3], nrows=3)
        print(f"カラム数: {len(df_multi.columns)}")
        print(f"カラムの例（最初の15列）:")
        for i, col in enumerate(df_multi.columns[:15], 1):
            print(f"  {i}. {col}")
        print()

        # データ本体
        print("[データ本体（都道府県行）]:")
        print(df_multi.head(3))
    except Exception as e:
        print(f"[ERROR] エラー: {e}")
    print()

def main():
    """メイン処理"""
    print("\n[NDB_XXX_slope_fracture プロジェクト]")
    print("Phase 1: NDBデータ構造探索\n")

    # 手術データ探索
    explore_surgery_data()

    # 質問票データ探索
    explore_questionnaire_data()

    print("=" * 80)
    print("[完了] 探索完了")
    print("=" * 80)

if __name__ == "__main__":
    main()
