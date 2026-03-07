import pandas as pd
import sys
import os

# ---------------------------------------------------------
# 設定: UTF-8出力の強制 (Windows環境での文字化け防止)
# ---------------------------------------------------------
sys.stdout.reconfigure(encoding='utf-8')

def extract_fracture_data():
    """
    NDBオープンデータから、特定の骨折手術および人工関節手術の算定回数を抽出する。
    対象シート: '入院'
    対象コード: 大腿骨、上腕骨、前腕骨の骨折観血的手術および人工骨頭・関節置換術
    """
    print("処理を開始します...")

    # ---------------------------------------------------------
    # 1. ファイルパスと出力設定
    # ---------------------------------------------------------
    input_file = r"C:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\02_Data\raw\NDB_OpenData\No.10\01_医科診療行為（算定回数）\01_公費レセプトを含まないデータ\K_手術\款別都道府県別算定回数.xlsx"
    output_dir = r"C:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture\03_Analysis\data\interim"
    output_file = os.path.join(output_dir, "fracture_surgery_site.csv")
    
    # 出力ディレクトリの作成
    os.makedirs(output_dir, exist_ok=True)

    # ---------------------------------------------------------
    # 2. 抽出対象コードの定義
    # ---------------------------------------------------------
    # キー: 診療行為コード, 値: {名称, 部位, カテゴリ}
    # キー: 診療行為コード, 値: {名称, 部位, カテゴリ}
    target_codes = {
        # 大腿骨 (Femur/Hip)
        150016710: {'name_short': '骨折非観血的(大腿)',   'site': 'femur', 'category': 'K044_ClosedReduction'},
        150018310: {'name_short': '経皮的鋼線(大腿)',     'site': 'femur', 'category': 'K045_Percutaneous'},
        150019210: {'name_short': '骨折観血的手術(大腿)', 'site': 'femur', 'category': 'K046_ORIF'},
        150049510: {'name_short': '人工骨頭挿入術(股)',   'site': 'femur', 'category': 'K081_Hemiarthroplasty'},
        150050410: {'name_short': '人工関節置換術(股)',   'site': 'femur', 'category': 'K082_THA'},
        
        # 上腕骨 (Humerus)
        150016610: {'name_short': '骨折非観血的(上腕)',   'site': 'humerus', 'category': 'K044_ClosedReduction'},
        150018210: {'name_short': '経皮的鋼線(上腕)',     'site': 'humerus', 'category': 'K045_Percutaneous'},
        150019110: {'name_short': '骨折観血的手術(上腕)', 'site': 'humerus', 'category': 'K046_ORIF'},
        150049410: {'name_short': '人工骨頭挿入術(肩)',   'site': 'humerus', 'category': 'K081_Hemiarthroplasty'},
        150050310: {'name_short': '人工関節置換術(肩)',   'site': 'humerus', 'category': 'K082_TSA'},

        # 前腕骨 (Forearm)
        150016810: {'name_short': '骨折非観血的(前腕)',   'site': 'forearm', 'category': 'K044_ClosedReduction'},
        150018410: {'name_short': '経皮的鋼線(前腕)',     'site': 'forearm', 'category': 'K045_Percutaneous'},
        150019310: {'name_short': '骨折観血的手術(前腕)', 'site': 'forearm', 'category': 'K046_ORIF'}
    }

    print(f"読み込み中: {input_file}")
    print("対象シート: '入院' (主要な手術は入院で算定されるため)")

    try:
        # ---------------------------------------------------------
        # 3. データ読み込み
        # ---------------------------------------------------------
        # シート名指定で読み込む
        # ヘッダーは通常3行目(index 2)あたりにあることが多いが、列名探索を行う
        # まずはヘッダーなしで読み込み、'都道府県'が含まれる行を探す戦略も有効だが、
        # ここでは固定的にヘッダー行を指定せず、データフレームとして探索する
        
        df = pd.read_excel(input_file, sheet_name='入院', header=None)
        
        print("ファイル読み込み完了。データ構造を解析します。")

        # ---------------------------------------------------------
        # 4. ヘッダー行の特定と列名の整理
        # ---------------------------------------------------------
        # '都道府県' という文字列が含まれる行をヘッダーとみなす
        header_row_idx = None
        for i, row in df.iterrows():
            row_str = row.astype(str).values
            if '都道府県' in row_str or '北海道' in row_str:
                # '都道府県'があればそれがヘッダー候補、なければ'北海道'がある行の1つ上がヘッダーの可能性が高い
                # NDBのフォーマットでは、左側にコード・名称があり、右側に都道府県が並ぶ
                # ここでは単純に、列5 (Index 4) 以降に数値が入る構造を前提に、
                # 列1 (Index 0)〜列4 (Index 3) にコード情報があると仮定する
                pass
        
        # 診療行為コードが含まれる列を探す ('150'から始まる9桁の数字)
        # 列E (Index 4) が '診療行為コード' であることが多い
        # 列F (Index 5) が '診療行為' (名称)
        
        # データフレームの列名を仮定
        # Excelの構造を目視確認した結果 (inspect scriptの出力より):
        # 0: ?, 1: ?, 2: ?, 3: 款コード?, 4: 診療行為コード, 5: 診療行為, 6: 点数?, 7: 総計... 8~: 北海道...
        
        # 実際にデータが入っている行を特定するために、ターゲットコードが含まれる行を抽出する
        # コード列は column 3 (ExcelのD列)
        code_col_idx = 3
        name_col_idx = 4
        
        # 数値型に変換可能な行のみ処理対象とする
        df_extracted = pd.DataFrame()

        results = []

        for idx, row in df.iterrows():
            cell_value = row[code_col_idx]
            
            try:
                # コードがターゲットに含まれているか確認
                code_int = int(cell_value)
                if code_int in target_codes:
                    meta = target_codes[code_int]
                    print(f"発見: {code_int} - {meta['name_short']}")
                    
                    # 都道府県データの抽出
                    # 検査結果より、Column 7 が北海道 (01) であることを確認
                    start_col = 7
                    
                    # 47都道府県分のデータを取得
                    # row[7] = 北海道 ... row[53] = 沖縄
                    prefecture_counts = row[start_col:start_col+47].values
                    
                    # データ格納
                    row_data = {
                        'code': code_int,
                        'name': meta['name_short'],
                        'site': meta['site'],
                        'category': meta['category'],
                        # ここに都道府県データを追加
                    }
                    
                    # 都道府県名のリスト（JIS順 01-47）
                    pref_names = [
                        "01_Hokkaido", "02_Aomori", "03_Iwate", "04_Miyagi", "05_Akita", "06_Yamagata", "07_Fukushima",
                        "08_Ibaraki", "09_Tochigi", "10_Gunma", "11_Saitama", "12_Chiba", "13_Tokyo", "14_Kanagawa",
                        "15_Niigata", "16_Toyama", "17_Ishikawa", "18_Fukui", "19_Yamanashi", "20_Nagano",
                        "21_Gifu", "22_Shizuoka", "23_Aichi", "24_Mie", "25_Shiga", "26_Kyoto", "27_Osaka", "28_Hyogo", "29_Nara", "30_Wakayama",
                        "31_Tottori", "32_Shimane", "33_Okayama", "34_Hiroshima", "35_Yamaguchi",
                        "36_Tokushima", "37_Kagawa", "38_Ehime", "39_Kochi",
                        "40_Fukuoka", "41_Saga", "42_Nagasaki", "43_Kumamoto", "44_Oita", "45_Miyazaki", "46_Kagoshima", "47_Okinawa"
                    ]
                    
                    for i, pref in enumerate(pref_names):
                        # "-" は 0 に置換
                        val = prefecture_counts[i]
                        if val == '-' or pd.isna(val):
                            val = 0
                        row_data[pref] = int(val)
                    
                    results.append(row_data)

            except (ValueError, TypeError):
                continue
        
        # ---------------------------------------------------------
        # 5. 結果の保存
        # ---------------------------------------------------------
        if results:
            df_result = pd.DataFrame(results)
            df_result.to_csv(output_file, index=False, encoding='utf-8-sig') # Excelで開くためBOM付きUTF-8
            print(f"抽出完了: {len(df_result)} 件のデータを保存しました。")
            print(f"保存先: {output_file}")
            print("\n--- 抽出データプレビュー ---")
            print(df_result[['code', 'name', 'site', '01_Hokkaido', '13_Tokyo', '47_Okinawa']].to_string(index=False))
        else:
            print("警告: 対象コードのデータが見つかりませんでした。列の位置やシート名を確認してください。")

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    extract_fracture_data()
