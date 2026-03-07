import pandas as pd
import sys
import os

# ---------------------------------------------------------
# 設定: UTF-8出力の強制
# ---------------------------------------------------------
sys.stdout.reconfigure(encoding='utf-8')

def extract_walking_speed():
    """
    特定健診データから「歩行速度」の回答データを抽出する。
    対象ファイル: 標準的な質問票（質問項目１２）...
    対象年齢: 65-74歳 (特定健診の対象範囲かつ高齢者)
    """
    print("歩行速度データ(Q12)の抽出を開始します...")

    input_file = r"C:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\02_Data\raw\NDB_OpenData\No.10\07_特定健診 質問票\01_公費レセプトを含まないデータ\標準的な質問票（質問項目１２） 都道府県別性年齢階級別分布.xlsx"
    output_dir = r"C:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture\03_Analysis\data\interim"
    output_file = os.path.join(output_dir, "walking_speed_q12.csv")

    os.makedirs(output_dir, exist_ok=True)

    print(f"読み込み中: {input_file}")

    try:
        # ヘッダーは行4 (Index 3) が年齢区分、行5 (Index 4) が「人数」など
        # 都道府県データは行6 (Index 5) から開始
        # Col 0: 都道府県, Col 1: 回答
        # Col 7: 男65-69, Col 8: 男70-74
        # Col 15: 女65-69, Col 16: 女70-74
        
        # header=Noneで読み込み、行列番号でアクセスする
        df = pd.read_excel(input_file, header=None)
        
        results = []
        
        # 都道府県リスト（順序保持のため）
        current_pref = None
        
        # データ行（Index 5から）を走査
        # 都道府県名は結合セルになっている可能性が高い（"北海道"の次はNaN）
        
        # 一時保存用
        yes_count = 0
        no_count = 0
        
        # 都道府県行の開始
        start_row = 5
        
        # イテレーション
        # NDBの表は "都道府県 -> はい行 -> いいえ行" の順序で並んでいると想定
        # インスペクション結果:
        # Index 5: 北海道, はい
        # Index 6: NaN, いいえ
        # Index 7: 青森県, はい
        # Index 8: NaN, いいえ
        
        cols_indices = [7, 8, 15, 16] # 65-69M, 70-74M, 65-69F, 70-74F
        
        for idx in range(start_row, len(df)):
            row = df.iloc[idx]
            
            pref_val = row[0]
            answer_val = row[1]
            
            # 都道府県名の更新
            if pd.notna(pref_val):
                current_pref = str(pref_val).strip()
                # 新しい都道府県の開始時にカウントリセットは不要（行ごとに処理して最後にまとめるか、都度処理するか）
                # ここでは「はい」と「いいえ」の行をペアで処理するロジックより、
                # 辞書に貯めていく方が安全
            
            if not current_pref:
                continue
                
            if pd.isna(answer_val):
                continue
                
            answer = str(answer_val).strip()
            
            # 数値データの取得（ハイフンなどは0にする）
            count_sum = 0
            for col_idx in cols_indices:
                val = row[col_idx]
                if pd.isna(val) or str(val) == '-':
                    val = 0
                try:
                    count_sum += int(val)
                except:
                    pass
            
            # 結果リストに追加（後でpivotする）
            results.append({
                'prefecture': current_pref,
                'answer': answer,
                'count_65_74': count_sum
            })

        # データフレーム化
        df_res = pd.DataFrame(results)
        
        print(f"抽出行数: {len(df_res)}")
        
        # ピボットテーブル作成 (都道府県 x 回答)
        df_pivot = df_res.pivot_table(index='prefecture', columns='answer', values='count_65_74', aggfunc='sum').reset_index()
        
        # カラム名整理 ('はい', 'いいえ' があるはず)
        # 答えには 'はい', 'いいえ' 以外に '回答しない' などがあるかも？ インスペクションでは 'はい', 'いいえ' のみ見えた
        
        if 'はい' in df_pivot.columns and 'いいえ' in df_pivot.columns:
            df_pivot['total'] = df_pivot['はい'] + df_pivot['いいえ']
            df_pivot['fast_walking_rate'] = (df_pivot['はい'] / df_pivot['total']) * 100
        else:
            print("警告: 'はい' または 'いいえ' の列が見つかりません。")
            print(df_pivot.columns)
            
        # 都道府県コードの割り当て（ソート用）
        # NDBの都道府県順はJISコード順（01北海道...47沖縄）であると仮定
        # マッピング辞書を作成
        pref_order = [
            "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県",
            "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県",
            "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県",
            "岐阜県", "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県", "奈良県", "和歌山県",
            "鳥取県", "島根県", "岡山県", "広島県", "山口県",
            "徳島県", "香川県", "愛媛県", "高知県",
            "福岡県", "佐賀県", "長崎県", "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"
        ]
        
        # 順序付け
        df_pivot['pref_id'] = df_pivot['prefecture'].apply(lambda x: pref_order.index(x) + 1 if x in pref_order else 99)
        df_pivot = df_pivot.sort_values('pref_id')
        
        # 保存
        df_pivot.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"保存完了: {output_file}")
        print(df_pivot.head())

    except Exception as e:
        print(f"エラー: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    extract_walking_speed()
