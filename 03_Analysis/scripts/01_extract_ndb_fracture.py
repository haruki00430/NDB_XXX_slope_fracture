"""
Phase 1: NDB骨折手術データと歩行速度データの抽出

入力:
    - NDB手術データ（K046骨折観血的手術）
    - NDB特定健診質問票16（歩行速度）

出力:
    - data/interim/fracture_surgery.csv（都道府県別骨折手術算定回数）
    - data/interim/walking_speed_q16.csv（都道府県別歩行速度「速い」回答率）
"""

import pandas as pd
import numpy as np
from pathlib import Path
import yaml
import logging
import sys

# プロジェクトルート
project_root = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(project_root / "src"))

# ロギング設定
log_dir = Path(__file__).parent.parent / "analysis" / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / "01_extract_ndb_fracture.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def load_config():
    """config.yamlを読み込む"""
    # スクリプトから見て: scripts -> 03_Analysis -> NDB_XXX_slope_fracture -> config
    config_path = Path(__file__).parent.parent.parent / "config" / "config.yaml"
    with open(config_path, encoding="utf-8") as f:
        config = yaml.safe_load(f)
    logger.info(f"設定ファイル読み込み: {config_path}")
    return config


def extract_fracture_surgery():
    """
    K046骨折観血的手術のデータを都道府県別に抽出

    Returns:
        DataFrame: 都道府県別骨折手術算定回数
    """
    logger.info("=" * 80)
    logger.info("K046骨折手術データの抽出")
    logger.info("=" * 80)

    # ファイルパス
    surgery_path = project_root / "02_Data/raw/NDB_OpenData/No.10/01_医科診療行為（算定回数）/01_公費レセプトを含まないデータ/K_手術/款別都道府県別算定回数.xlsx"

    if not surgery_path.exists():
        logger.error(f"ファイル未発見: {surgery_path}")
        return None

    logger.info(f"ファイル: {surgery_path.name}")

    # MultiIndexヘッダーで読み込み
    logger.info("MultiIndex読み込み (header=[0, 1])...")
    df = pd.read_excel(surgery_path, sheet_name=0, header=[0, 1])

    logger.info(f"データサイズ: {df.shape[0]}行 x {df.shape[1]}列")
    logger.info(f"カラム例（最初の5列）: {list(df.columns[:5])}")

    # K046を含む行を検索
    logger.info("\nK046骨折関連行を検索...")

    # 最初の列を確認（診療コード列）
    # インデックスをリセットして、列を確認
    df_reset = df.reset_index(drop=True)

    # 診療コード列を特定（通常は列1または列2）
    code_col_idx = None
    for i in range(min(5, len(df.columns))):
        col_values = df.iloc[:, i].astype(str)
        if col_values.str.contains('K046', na=False).any():
            code_col_idx = i
            logger.info(f"診療コード列を発見: 列{i}")
            break

    if code_col_idx is None:
        logger.error("K046を含む列が見つかりません")
        return None

    # K046を含む行を抽出
    k046_mask = df.iloc[:, code_col_idx].astype(str).str.contains('K046', na=False)
    df_k046 = df[k046_mask]

    logger.info(f"K046行数: {len(df_k046)}")
    logger.info(f"K046行の内容:\n{df_k046.iloc[:, :5]}")

    # 都道府県データの抽出
    # ヘッダーを確認して、都道府県列を特定
    logger.info("\n都道府県別データの抽出...")

    # ヘッダー行から都道府県列を検索
    pref_col_idx = None
    for i in range(min(10, len(df.columns))):
        col_name = str(df.columns[i])
        if '北海道' in col_name or '都道府県' in col_name:
            pref_col_idx = i
            logger.info(f"都道府県列を発見: 列{i} ({col_name})")
            break

    if pref_col_idx is None:
        logger.warning("都道府県列が見つかりません。列名を確認します...")
        logger.info(f"全列名（最初の15列）:")
        for i, col in enumerate(df.columns[:15]):
            logger.info(f"  {i}: {col}")

    # K046の行データを都道府県別に整形
    # （ここでは、まず行161のK046全般データを抽出）
    if len(df_k046) > 0:
        # 最初のK046行を使用
        k046_row = df_k046.iloc[0, :]

        # 都道府県カラムを抽出（列7以降が都道府県と推定）
        pref_data = k046_row.iloc[7:]  # 仮定: 列7以降が都道府県データ

        logger.info(f"\nK046データサンプル（最初の10都道府県）:")
        logger.info(pref_data.head(10))

        # DataFrameとして整形
        result_df = pd.DataFrame({
            'prefecture': pref_data.index,
            'fracture_surgery_count': pref_data.values
        })

        # 数値クリーニング（'-'をNaNに変換）
        result_df['fracture_surgery_count'] = pd.to_numeric(
            result_df['fracture_surgery_count'].replace('-', np.nan),
            errors='coerce'
        )

        logger.info(f"\n抽出結果:")
        logger.info(f"  行数: {len(result_df)}")
        logger.info(f"  欠損値: {result_df['fracture_surgery_count'].isna().sum()}")
        logger.info(f"\nサンプルデータ:")
        logger.info(result_df.head(10))

        return result_df

    return None


def extract_walking_speed():
    """
    質問項目16（歩行速度）のデータを都道府県別に抽出

    Returns:
        DataFrame: 都道府県別歩行速度「速い」回答率
    """
    logger.info("\n" + "=" * 80)
    logger.info("質問項目16（歩行速度）データの抽出")
    logger.info("=" * 80)

    # ファイルパス
    q16_path = project_root / "02_Data/raw/NDB_OpenData/No.10/07_特定健診 質問票/01_公費レセプトを含まないデータ/標準的な質問票（質問項目１６） 都道府県別性年齢階級別分布.xlsx"

    if not q16_path.exists():
        logger.error(f"ファイル未発見: {q16_path}")
        return None

    logger.info(f"ファイル: {q16_path.name}")

    # MultiIndexヘッダーで読み込み (header=[2, 3])
    logger.info("MultiIndex読み込み (header=[2, 3])...")
    df = pd.read_excel(q16_path, sheet_name=0, header=[2, 3])

    logger.info(f"データサイズ: {df.shape[0]}行 x {df.shape[1]}列")

    # 列名を簡素化
    df.columns = [f'{col[0]}_{col[1]}' if 'Unnamed' not in col[0]
                  else col[1] for col in df.columns]

    # 最初の2列をリネーム
    df.rename(columns={df.columns[0]: '都道府県', df.columns[1]: '回答'}, inplace=True)

    logger.info(f"列名（最初の10列）: {list(df.columns[:10])}")
    logger.info(f"\nデータサンプル:")
    logger.info(df.head())

    # ヘッダー行を除外
    df = df[df['回答'].notna()].reset_index(drop=True)

    # 都道府県名をffill
    df['都道府県'] = df['都道府県'].ffill()

    # 数値列
    numeric_cols = [col for col in df.columns if col not in ['都道府県', '回答']]

    # 都道府県別に「はい」回答率を計算
    results = []
    for pref in df['都道府県'].unique():
        df_pref = df[df['都道府県'] == pref]

        # 「はい」と「いいえ」の行を抽出
        df_yes = df_pref[df_pref['回答'] == 'はい']
        df_no = df_pref[df_pref['回答'] == 'いいえ']

        if len(df_yes) == 0 or len(df_no) == 0:
            logger.warning(f"{pref}: 回答データ不完全")
            continue

        # 数値データの合計（'-'をNaNに変換）
        yes_total = df_yes[numeric_cols].replace('-', np.nan).astype(float).sum().sum()
        no_total = df_no[numeric_cols].replace('-', np.nan).astype(float).sum().sum()

        total = yes_total + no_total
        if total == 0:
            logger.warning(f"{pref}: 回答数が0")
            continue

        response_rate = (yes_total / total) * 100

        results.append({
            "prefecture": pref,
            "yes_count": yes_total,
            "total_count": total,
            "walking_speed_fast_rate": response_rate
        })

    result_df = pd.DataFrame(results)

    logger.info(f"\n抽出結果:")
    logger.info(f"  都道府県数: {len(result_df)}")
    logger.info(f"\nサンプルデータ:")
    logger.info(result_df.head(10))

    return result_df


def main():
    """メイン処理"""
    logger.info("\n" + "="*80)
    logger.info("Phase 1: NDBデータ抽出開始")
    logger.info("="*80)

    # config読み込み
    config = load_config()

    # 出力ディレクトリ作成
    output_dir = Path(__file__).parent.parent / "data" / "interim"
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. 骨折手術データ抽出
    df_fracture = extract_fracture_surgery()
    if df_fracture is not None:
        output_path = output_dir / "fracture_surgery.csv"
        df_fracture.to_csv(output_path, index=False, encoding="utf-8-sig")
        logger.info(f"\n[保存] {output_path}")

    # 2. 歩行速度データ抽出
    df_walking = extract_walking_speed()
    if df_walking is not None:
        output_path = output_dir / "walking_speed_q16.csv"
        df_walking.to_csv(output_path, index=False, encoding="utf-8-sig")
        logger.info(f"\n[保存] {output_path}")

    logger.info("\n" + "="*80)
    logger.info("Phase 1: 完了")
    logger.info("="*80)


if __name__ == "__main__":
    main()
