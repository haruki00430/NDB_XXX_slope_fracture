import pandas as pd
import sys
import os

# Windows console encoding fix
sys.stdout.reconfigure(encoding='utf-8')

def integrate_datasets():
    print("データ統合プロセスを開始します...")

    # Paths
    base_dir = r"C:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture"
    interim_dir = os.path.join(base_dir, "03_Analysis", "data", "interim")
    processed_dir = os.path.join(base_dir, "03_Analysis", "data", "processed")
    stats_dir = os.path.join(base_dir, "results", "statistics")
    
    os.makedirs(processed_dir, exist_ok=True)

    # Inputs
    path_fracture = os.path.join(interim_dir, "fracture_surgery_site.csv")
    path_walking = os.path.join(interim_dir, "walking_speed_q12.csv")
    path_census = os.path.join(interim_dir, "statistics_2020.csv")
    path_slope = os.path.join(stats_dir, "prefecture_habitable_slope.csv")

    # 1. Load Data
    print(f"Loading fracture data: {path_fracture}")
    df_fracture = pd.read_csv(path_fracture)
    
    print(f"Loading walking data: {path_walking}")
    df_walking = pd.read_csv(path_walking)
    
    print(f"Loading census data: {path_census}")
    df_census = pd.read_csv(path_census)
    
    print(f"Loading slope data: {path_slope}")
    df_slope = pd.read_csv(path_slope)

    # 2. Process Fracture Data (Aggregate by Prefecture)
    # df_fracture has 13 rows (codes) and columns for prefectures (01_Hokkaido, etc.)
    # We need to transpose or melt it.
    
    # Melt
    df_fracture_melt = df_fracture.melt(
        id_vars=['code', 'name', 'site', 'category'], 
        var_name='prefecture_code_name', 
        value_name='count'
    )
    
    # Extract prefecture name from '01_Hokkaido' -> 'Hokkaido' or '01'
    # Actually, other datasets use Japanese names (e.g., "北海道").
    # We need a mapping from '01_Hokkaido' to '北海道'.
    
    pref_map = {
        "01_Hokkaido": "北海道", "02_Aomori": "青森県", "03_Iwate": "岩手県", "04_Miyagi": "宮城県", 
        "05_Akita": "秋田県", "06_Yamagata": "山形県", "07_Fukushima": "福島県", "08_Ibaraki": "茨城県", 
        "09_Tochigi": "栃木県", "10_Gunma": "群馬県", "11_Saitama": "埼玉県", "12_Chiba": "千葉県", 
        "13_Tokyo": "東京都", "14_Kanagawa": "神奈川県", "15_Niigata": "新潟県", "16_Toyama": "富山県", 
        "17_Ishikawa": "石川県", "18_Fukui": "福井県", "19_Yamanashi": "山梨県", "20_Nagano": "長野県", 
        "21_Gifu": "岐阜県", "22_Shizuoka": "静岡県", "23_Aichi": "愛知県", "24_Mie": "三重県", 
        "25_Shiga": "滋賀県", "26_Kyoto": "京都府", "27_Osaka": "大阪府", "28_Hyogo": "兵庫県", 
        "29_Nara": "奈良県", "30_Wakayama": "和歌山県", "31_Tottori": "鳥取県", "32_Shimane": "島根県", 
        "33_Okayama": "岡山県", "34_Hiroshima": "広島県", "35_Yamaguchi": "山口県", "36_Tokushima": "徳島県", 
        "37_Kagawa": "香川県", "38_Ehime": "愛媛県", "39_Kochi": "高知県", "40_Fukuoka": "福岡県", 
        "41_Saga": "佐賀県", "42_Nagasaki": "長崎県", "43_Kumamoto": "熊本県", "44_Oita": "大分県", 
        "45_Miyazaki": "宮崎県", "46_Kagoshima": "鹿児島県", "47_Okinawa": "沖縄県"
    }
    
    df_fracture_melt['prefecture'] = df_fracture_melt['prefecture_code_name'].map(pref_map)
    
    # Aggregate Total Fracture Count per Prefecture
    df_fracture_agg = df_fracture_melt.groupby('prefecture')['count'].sum().reset_index()
    df_fracture_agg.rename(columns={'count': 'total_fracture_count'}, inplace=True)
    
    # Also aggregate by Site (Femur, Humerus, Forearm)
    df_site = df_fracture_melt.pivot_table(index='prefecture', columns='site', values='count', aggfunc='sum').reset_index()
    df_site.columns = ['prefecture', 'femur_count', 'forearm_count', 'humerus_count'] # verification needed for order
    
    # Merge aggregations
    df_fracture_final = pd.merge(df_fracture_agg, df_site, on='prefecture')
    
    print("Fracture data processed.")
    print(df_fracture_final.head())

    # 3. Merge All
    # Base: Census (47 prefs)
    df_merged = pd.merge(df_census, df_fracture_final, on='prefecture', how='left')
    df_merged = pd.merge(df_merged, df_walking[['prefecture', 'fast_walking_rate']], on='prefecture', how='left')
    df_merged = pd.merge(df_merged, df_slope[['prefecture', 'habitable_slope_weighted', 'avg_slope_simple']], on='prefecture', how='left')

    # 4. Calculate Rates (per 100,000)
    df_merged['fracture_rate'] = (df_merged['total_fracture_count'] / df_merged['total_pop']) * 100000
    df_merged['femur_rate'] = (df_merged['femur_count'] / df_merged['total_pop']) * 100000
    df_merged['humerus_rate'] = (df_merged['humerus_count'] / df_merged['total_pop']) * 100000
    df_merged['forearm_rate'] = (df_merged['forearm_count'] / df_merged['total_pop']) * 100000

    # 5. Save
    output_path = os.path.join(processed_dir, "analysis_dataset_v1.csv")
    df_merged.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"Data verification:")
    print(f"Rows: {len(df_merged)}")
    print(df_merged[['prefecture', 'fracture_rate', 'habitable_slope_weighted', 'aging_rate']].head())
    
    # Correlation Matrix
    print("\nCorrelation Matrix:")
    cols = ['fracture_rate', 'femur_rate', 'humerus_rate', 'forearm_rate', 
            'aging_rate', 'pop_density', 'fast_walking_rate', 'habitable_slope_weighted']
    print(df_merged[cols].corr())

    print(f"\nFinal dataset saved to: {output_path}")

if __name__ == "__main__":
    integrate_datasets()
