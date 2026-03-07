import pandas as pd
import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
# from ndb_library.viz import set_japanese_font # Library not found
import matplotlib.font_manager as fm

# Try to set Japanese font for Windows
try:
    plt.rcParams['font.family'] = 'MS Gothic'
except:
    pass

# ---------------------------------------------------------
# 設定: UTF-8出力
# ---------------------------------------------------------
sys.stdout.reconfigure(encoding='utf-8')

def integrate_and_analyze():
    print("データの統合と予備解析を開始します...")
    
    base_dir = r"C:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture\03_Analysis\data\interim"
    fracture_file = os.path.join(base_dir, "fracture_surgery_site.csv")
    walking_file = os.path.join(base_dir, "walking_speed_q12.csv")
    output_combined = os.path.join(base_dir, "interim_combined_phase1.csv")
    output_fig = os.path.join(r"C:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture\03_Analysis\results\figures", "preliminary_scatter.png")
    
    os.makedirs(os.path.dirname(output_fig), exist_ok=True)
    
    # 1. 読み込み
    try:
        df_frac = pd.read_csv(fracture_file)
        df_walk = pd.read_csv(walking_file)
        
        print(f"骨折データ(Wide): {len(df_frac)}行")
        print(f"歩行速度データ: {len(df_walk)}行")
        
        # 2. 骨折データの整形 (Wide -> Long -> Aggregate)
        # site='femur' のみを抽出して合計する
        df_femur = df_frac[df_frac['site'] == 'femur'].copy()
        
        # 都道府県カラムの特定 (01_Hokkaido ... 47_Okinawa)
        # columns 4以降が都道府県と仮定 (code, name, site, category の4つがメタデータ)
        pref_cols = [c for c in df_frac.columns if c not in ['code', 'name', 'site', 'category']]
        
        print(f"都道府県カラム数: {len(pref_cols)}")
        
        # 転置して集計
        # index: 都道府県, columns: 各手術
        # sum(axis=0) で各都道府県の大腿骨手術総数を出す
        femur_counts = df_femur[pref_cols].sum(axis=0)
        
        # DataFrame化
        df_frac_agg = pd.DataFrame({'pref_en_code': femur_counts.index, 'count_femur': femur_counts.values})
        
        # pref_en_code (e.g. "01_Hokkaido") から ID (1) を抽出して紐付ける
        def extract_id(s):
            try:
                return int(s.split('_')[0])
            except:
                return 99
                
        df_frac_agg['pref_id'] = df_frac_agg['pref_en_code'].apply(extract_id)
        
        # 3. 結合
        # walking_speed_q12.csv には 'pref_id' がある
        df_merged = pd.merge(df_frac_agg, df_walk, on="pref_id", how="inner")
        
        print(f"結合後データ: {len(df_merged)}行")
        
        # 4. 予備解析指標の作成
        if 'count_femur' in df_merged.columns:
            # 簡易骨折率（対 受診者数）
            # walking_speed_q12.csv の 'total' は 65-74歳の回答者総数
            # これを分母にするのは近似的だが、相関を見るには一旦ヨシ
            df_merged['temp_femur_rate'] = df_merged['count_femur'] / df_merged['total']
            
            # 相関
            corr = df_merged[['temp_femur_rate', 'fast_walking_rate', 'count_femur', 'total']].corr()
            print("\n相関行列 (予備):")
            print(corr)
            
            # 5. 可視化
            plt.figure(figsize=(10, 6))
            try:
                plt.rcParams['font.family'] = 'MS Gothic'
            except:
                pass
                
            sns.scatterplot(data=df_merged, x='fast_walking_rate', y='temp_femur_rate')
            sns.regplot(data=df_merged, x='fast_walking_rate', y='temp_femur_rate', scatter=False, color='red')
            
            # 相関係数をタイトルに
            r_val = corr.loc['fast_walking_rate', 'temp_femur_rate']
            
            plt.title(f"【予備解析】歩行速度(速い%) vs 大腿骨骨折率 (r={r_val:.3f})")
            plt.xlabel("歩行速度が速い割合 (%)")
            plt.ylabel("大腿骨骨折数 / 特定健診受診者数 (65-74)")
            
            plt.tight_layout()
            plt.savefig(output_fig)
            print(f"散布図保存: {output_fig}")
            
        # 保存
        df_merged.to_csv(output_combined, index=False, encoding='utf-8-sig')
        print(f"統合データ保存: {output_combined}")
        
    except Exception as e:
        print(f"エラー: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    integrate_and_analyze()
