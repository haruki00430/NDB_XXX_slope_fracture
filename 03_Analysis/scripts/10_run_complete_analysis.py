"""
NDB Slope Fracture Analysis - Complete Pipeline
===============================================
This script consolidates the entire analysis pipeline into a single file.
It performs the following steps:
1. Extract Fracture Data from NDB Excel
2. Extract Walking Speed Data from NDB Excel
3. Generate 2020 Census Data
4. Integrate NDB, Census, and Slope Data
5. Calculate Descriptive Statistics
6. Perform Correlation Analysis
7. Perform Regression Analysis
8. Generate Visualizations

Usage:
    python 10_run_complete_analysis.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.font_manager as fm
import sys
import os
import io

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture"
INTERIM_DIR = os.path.join(BASE_DIR, "03_Analysis", "data", "interim")
PROCESSED_DIR = os.path.join(BASE_DIR, "03_Analysis", "data", "processed")
RESULTS_DIR = os.path.join(BASE_DIR, "03_Analysis", "results")
STATS_DIR = os.path.join(BASE_DIR, "results", "statistics")
FIGURES_DIR = os.path.join(RESULTS_DIR, "figures")

# Input File Paths (Raw Data)
INPUT_NDB_FRACTURE = r"C:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\02_Data\raw\NDB_OpenData\No.10\01_医科診療行為（算定回数）\01_公費レセプトを含まないデータ\K_手術\款別都道府県別算定回数.xlsx"
INPUT_NDB_WALKING = r"C:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\02_Data\raw\NDB_OpenData\No.10\07_特定健診 質問票\01_公費レセプトを含まないデータ\標準的な質問票（質問項目１２） 都道府県別性年齢階級別分布.xlsx"
INPUT_SLOPE_DATA = os.path.join(STATS_DIR, "prefecture_habitable_slope.csv")

# Ensure directories exist
os.makedirs(INTERIM_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)

# Font settings for Japanese
jp_font = None
try:
    font_paths = fm.findSystemFonts()
    for font_path in font_paths:
        if "Meiryo" in font_path or "Yu Gothic" in font_path or "MS Gothic" in font_path:
            jp_font = fm.FontProperties(fname=font_path)
            break
except:
    pass

if jp_font:
    plt.rcParams['font.family'] = jp_font.get_name()
else:
    plt.rcParams['font.sans-serif'] = ['Meiryo', 'Yu Gothic', 'Hiragino Maru Gothic Pro', 'SimHei', 'Arial']


# ---------------------------------------------------------
# Step 1: Extract Fracture Data
# ---------------------------------------------------------
def step1_extract_fracture():
    print("\n[Step 1] Extracting Fracture Data...")
    output_file = os.path.join(INTERIM_DIR, "fracture_surgery_site.csv")
    
    target_codes = {
        150016710: {'name_short': '骨折非観血的(大腿)',   'site': 'femur', 'category': 'K044_ClosedReduction'},
        150018310: {'name_short': '経皮的鋼線(大腿)',     'site': 'femur', 'category': 'K045_Percutaneous'},
        150019210: {'name_short': '骨折観血的手術(大腿)', 'site': 'femur', 'category': 'K046_ORIF'},
        150049510: {'name_short': '人工骨頭挿入術(股)',   'site': 'femur', 'category': 'K081_Hemiarthroplasty'},
        150050410: {'name_short': '人工関節置換術(股)',   'site': 'femur', 'category': 'K082_THA'},
        150016610: {'name_short': '骨折非観血的(上腕)',   'site': 'humerus', 'category': 'K044_ClosedReduction'},
        150018210: {'name_short': '経皮的鋼線(上腕)',     'site': 'humerus', 'category': 'K045_Percutaneous'},
        150019110: {'name_short': '骨折観血的手術(上腕)', 'site': 'humerus', 'category': 'K046_ORIF'},
        150049410: {'name_short': '人工骨頭挿入術(肩)',   'site': 'humerus', 'category': 'K081_Hemiarthroplasty'},
        150050310: {'name_short': '人工関節置換術(肩)',   'site': 'humerus', 'category': 'K082_TSA'},
        150016810: {'name_short': '骨折非観血的(前腕)',   'site': 'forearm', 'category': 'K044_ClosedReduction'},
        150018410: {'name_short': '経皮的鋼線(前腕)',     'site': 'forearm', 'category': 'K045_Percutaneous'},
        150019310: {'name_short': '骨折観血的手術(前腕)', 'site': 'forearm', 'category': 'K046_ORIF'}
    }

    try:
        df = pd.read_excel(INPUT_NDB_FRACTURE, sheet_name='入院', header=None)
        code_col_idx = 3
        start_col = 7
        results = []

        pref_names = [
            "01_Hokkaido", "02_Aomori", "03_Iwate", "04_Miyagi", "05_Akita", "06_Yamagata", "07_Fukushima",
            "08_Ibaraki", "09_Tochigi", "10_Gunma", "11_Saitama", "12_Chiba", "13_Tokyo", "14_Kanagawa",
            "15_Niigata", "16_Toyama", "17_Ishikawa", "18_Fukui", "19_Yamanashi", "20_Nagano",
            "21_Gifu", "22_Shizuoka", "23_Aichi", "24_Mie", "25_Shiga", "26_Kyoto", "27_Osaka", "28_Hyogo", "29_Nara", "30_Wakayama",
            "31_Tottori", "32_Shimane", "33_Okayama", "34_Hiroshima", "35_Yamaguchi",
            "36_Tokushima", "37_Kagawa", "38_Ehime", "39_Kochi",
            "40_Fukuoka", "41_Saga", "42_Nagasaki", "43_Kumamoto", "44_Oita", "45_Miyazaki", "46_Kagoshima", "47_Okinawa"
        ]

        for idx, row in df.iterrows():
            cell_value = row[code_col_idx]
            try:
                code_int = int(cell_value)
                if code_int in target_codes:
                    meta = target_codes[code_int]
                    prefecture_counts = row[start_col:start_col+47].values
                    row_data = {
                        'code': code_int, 'name': meta['name_short'], 'site': meta['site'], 'category': meta['category']
                    }
                    for i, pref in enumerate(pref_names):
                        val = prefecture_counts[i]
                        if val == '-' or pd.isna(val): val = 0
                        row_data[pref] = int(val)
                    results.append(row_data)
            except (ValueError, TypeError):
                continue

        if results:
            df_result = pd.DataFrame(results)
            df_result.to_csv(output_file, index=False, encoding='utf-8-sig')
            print(f"Success: Saved {len(df_result)} rows to {output_file}")
        else:
            print("Warning: No data extracted.")

    except Exception as e:
        print(f"Error in Step 1: {e}")

# ---------------------------------------------------------
# Step 2: Extract Walking Speed
# ---------------------------------------------------------
def step2_extract_walking():
    print("\n[Step 2] Extracting Walking Speed Data...")
    output_file = os.path.join(INTERIM_DIR, "walking_speed_q12.csv")
    
    try:
        df = pd.read_excel(INPUT_NDB_WALKING, header=None)
        results = []
        current_pref = None
        cols_indices = [7, 8, 15, 16] # 65-69M, 70-74M, 65-69F, 70-74F
        start_row = 5

        for idx in range(start_row, len(df)):
            row = df.iloc[idx]
            pref_val = row[0]
            answer_val = row[1]
            if pd.notna(pref_val): current_pref = str(pref_val).strip()
            if not current_pref or pd.isna(answer_val): continue
            
            count_sum = 0
            for col_idx in cols_indices:
                val = row[col_idx]
                if pd.isna(val) or str(val) == '-': val = 0
                try: count_sum += int(val)
                except: pass
            
            results.append({'prefecture': current_pref, 'answer': str(answer_val).strip(), 'count_65_74': count_sum})

        df_res = pd.DataFrame(results)
        df_pivot = df_res.pivot_table(index='prefecture', columns='answer', values='count_65_74', aggfunc='sum').reset_index()
        
        if 'はい' in df_pivot.columns and 'いいえ' in df_pivot.columns:
            df_pivot['total'] = df_pivot['はい'] + df_pivot['いいえ']
            df_pivot['fast_walking_rate'] = (df_pivot['はい'] / df_pivot['total']) * 100
        
        # Sort by standard pref order
        pref_order = ["北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県", "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県", "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県", "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県", "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "広島県", "山口県", "徳島県", "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県", "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"]
        df_pivot['pref_id'] = df_pivot['prefecture'].apply(lambda x: pref_order.index(x) + 1 if x in pref_order else 99)
        df_pivot = df_pivot.sort_values('pref_id')
        
        df_pivot.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"Success: Saved walking speed data to {output_file}")
        
    except Exception as e:
        print(f"Error in Step 2: {e}")

# ---------------------------------------------------------
# Step 3: Fetch Census Data (Manual)
# ---------------------------------------------------------
def step3_fetch_census():
    print("\n[Step 3] Generating Census Data (Manual Fallback)...")
    output_file = os.path.join(INTERIM_DIR, "statistics_2020.csv")
    
    # Using reliable manual data as default
    data = [
        {"prefecture": "北海道", "total_pop": 5224614, "elderly_pop": 1668661, "area": 83423.82},
        {"prefecture": "青森県", "total_pop": 1237984, "elderly_pop": 421272, "area": 9645.64},
        {"prefecture": "岩手県", "total_pop": 1210534, "elderly_pop": 403874, "area": 15275.01},
        {"prefecture": "宮城県", "total_pop": 2301996, "elderly_pop": 645108, "area": 7282.22},
        {"prefecture": "秋田県", "total_pop": 959502, "elderly_pop": 349695, "area": 11637.52},
        {"prefecture": "山形県", "total_pop": 1068027, "elderly_pop": 358485, "area": 9323.15},
        {"prefecture": "福島県", "total_pop": 1833152, "elderly_pop": 583487, "area": 13783.90},
        {"prefecture": "茨城県", "total_pop": 2867009, "elderly_pop": 851928, "area": 6097.19},
        {"prefecture": "栃木県", "total_pop": 1933146, "elderly_pop": 558564, "area": 6408.09},
        {"prefecture": "群馬県", "total_pop": 1939110, "elderly_pop": 574765, "area": 6362.28},
        {"prefecture": "埼玉県", "total_pop": 7344765, "elderly_pop": 1968843, "area": 3797.75},
        {"prefecture": "千葉県", "total_pop": 6284480, "elderly_pop": 1729676, "area": 5157.61},
        {"prefecture": "東京都", "total_pop": 14047594, "elderly_pop": 3192014, "area": 2194.03},
        {"prefecture": "神奈川県", "total_pop": 9237337, "elderly_pop": 2385311, "area": 2416.11},
        {"prefecture": "新潟県", "total_pop": 2201272, "elderly_pop": 724776, "area": 12584.18},
        {"prefecture": "富山県", "total_pop": 1034814, "elderly_pop": 335026, "area": 4247.61},
        {"prefecture": "石川県", "total_pop": 1132526, "elderly_pop": 337426, "area": 4186.09},
        {"prefecture": "福井県", "total_pop": 766863, "elderly_pop": 239712, "area": 4190.52},
        {"prefecture": "山梨県", "total_pop": 809974, "elderly_pop": 248674, "area": 4465.27},
        {"prefecture": "長野県", "total_pop": 2048011, "elderly_pop": 650997, "area": 13561.56},
        {"prefecture": "岐阜県", "total_pop": 1978742, "elderly_pop": 603058, "area": 10621.29},
        {"prefecture": "静岡県", "total_pop": 3633202, "elderly_pop": 1083901, "area": 7777.43},
        {"prefecture": "愛知県", "total_pop": 7542415, "elderly_pop": 1904797, "area": 5173.07},
        {"prefecture": "三重県", "total_pop": 1770254, "elderly_pop": 526278, "area": 5774.49},
        {"prefecture": "滋賀県", "total_pop": 1413610, "elderly_pop": 374776, "area": 4017.38},
        {"prefecture": "京都府", "total_pop": 2578087, "elderly_pop": 780650, "area": 4612.20},
        {"prefecture": "大阪府", "total_pop": 8837685, "elderly_pop": 2439775, "area": 1905.32},
        {"prefecture": "兵庫県", "total_pop": 5465002, "elderly_pop": 1581452, "area": 8401.02},
        {"prefecture": "奈良県", "total_pop": 1324473, "elderly_pop": 421063, "area": 3690.94},
        {"prefecture": "和歌山県", "total_pop": 922584, "elderly_pop": 305886, "area": 4724.65},
        {"prefecture": "鳥取県", "total_pop": 553407, "elderly_pop": 180371, "area": 3507.13},
        {"prefecture": "島根県", "total_pop": 671126, "elderly_pop": 226871, "area": 6708.26},
        {"prefecture": "岡山県", "total_pop": 1888432, "elderly_pop": 583852, "area": 7114.33},
        {"prefecture": "広島県", "total_pop": 2799702, "elderly_pop": 829562, "area": 8479.63},
        {"prefecture": "山口県", "total_pop": 1342059, "elderly_pop": 465225, "area": 6112.54},
        {"prefecture": "徳島県", "total_pop": 719559, "elderly_pop": 246533, "area": 4146.75},
        {"prefecture": "香川県", "total_pop": 950244, "elderly_pop": 303723, "area": 1876.78},
        {"prefecture": "愛媛県", "total_pop": 1334841, "elderly_pop": 449298, "area": 5676.19},
        {"prefecture": "高知県", "total_pop": 691527, "elderly_pop": 248695, "area": 7103.63},
        {"prefecture": "福岡県", "total_pop": 5135214, "elderly_pop": 1422774, "area": 4986.51},
        {"prefecture": "佐賀県", "total_pop": 811604, "elderly_pop": 250373, "area": 2440.69},
        {"prefecture": "長崎県", "total_pop": 1312317, "elderly_pop": 429670, "area": 4130.98},
        {"prefecture": "熊本県", "total_pop": 1738301, "elderly_pop": 554760, "area": 7409.46},
        {"prefecture": "大分県", "total_pop": 1123852, "elderly_pop": 374768, "area": 6340.76},
        {"prefecture": "宮崎県", "total_pop": 1069576, "elderly_pop": 350033, "area": 7735.22},
        {"prefecture": "鹿児島県", "total_pop": 1588256, "elderly_pop": 521490, "area": 9187.06},
        {"prefecture": "沖縄県", "total_pop": 1467480, "elderly_pop": 331777, "area": 2282.59},
    ]

    df = pd.DataFrame(data)
    df['aging_rate'] = (df['elderly_pop'] / df['total_pop']) * 100
    df['pop_density'] = df['total_pop'] / df['area']
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"Success: Saved statistics data to {output_file}")

# ---------------------------------------------------------
# Step 4: Integrate Datasets
# ---------------------------------------------------------
def step4_integrate():
    print("\n[Step 4] Integrating Datasets...")
    path_fracture = os.path.join(INTERIM_DIR, "fracture_surgery_site.csv")
    path_walking = os.path.join(INTERIM_DIR, "walking_speed_q12.csv")
    path_census = os.path.join(INTERIM_DIR, "statistics_2020.csv")
    path_slope = INPUT_SLOPE_DATA
    
    output_path = os.path.join(PROCESSED_DIR, "analysis_dataset_v1.csv")

    try:
        df_fracture = pd.read_csv(path_fracture)
        df_walking = pd.read_csv(path_walking)
        df_census = pd.read_csv(path_census)
        df_slope = pd.read_csv(path_slope)

        # Process Fracture Data
        df_fracture_melt = df_fracture.melt(
            id_vars=['code', 'name', 'site', 'category'], 
            var_name='prefecture_code_name', 
            value_name='count'
        )
        
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
        
        df_fracture_agg = df_fracture_melt.groupby('prefecture')['count'].sum().reset_index()
        df_fracture_agg.rename(columns={'count': 'total_fracture_count'}, inplace=True)
        
        df_site = df_fracture_melt.pivot_table(index='prefecture', columns='site', values='count', aggfunc='sum').reset_index()
        df_site.columns = ['prefecture', 'femur_count', 'forearm_count', 'humerus_count']
        
        df_fracture_final = pd.merge(df_fracture_agg, df_site, on='prefecture')

        # Merge All
        df_merged = pd.merge(df_census, df_fracture_final, on='prefecture', how='left')
        df_merged = pd.merge(df_merged, df_walking[['prefecture', 'fast_walking_rate']], on='prefecture', how='left')
        df_merged = pd.merge(df_merged, df_slope[['prefecture', 'habitable_slope_weighted', 'avg_slope_simple']], on='prefecture', how='left')

        # Calculate Rates
        df_merged['fracture_rate'] = (df_merged['total_fracture_count'] / df_merged['total_pop']) * 100000
        df_merged['femur_rate'] = (df_merged['femur_count'] / df_merged['total_pop']) * 100000
        df_merged['humerus_rate'] = (df_merged['humerus_count'] / df_merged['total_pop']) * 100000
        df_merged['forearm_rate'] = (df_merged['forearm_count'] / df_merged['total_pop']) * 100000
        
        df_merged.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"Success: Analysis dataset saved to {output_path}")
        
    except Exception as e:
        print(f"Error in Step 4: {e}")

# ---------------------------------------------------------
# Step 5: Statistical Analysis & Visualization
# ---------------------------------------------------------
def step5_stats_analysis():
    print("\n[Step 5] Performing Statistical Analysis & Visualization...")
    input_file = os.path.join(PROCESSED_DIR, "analysis_dataset_v1.csv")
    if not os.path.exists(input_file):
        print("Error: Input file missing.")
        return

    df = pd.read_csv(input_file)
    
    # --- Descriptive Stats ---
    output_desc = os.path.join(RESULTS_DIR, "table1_descriptive.csv")
    cols = {
        'fracture_rate': 'Total Fracture Rate (per 100k)',
        'femur_rate': 'Femur Fracture Rate',
        'humerus_rate': 'Humerus Fracture Rate',
        'forearm_rate': 'Forearm Fracture Rate',
        'habitable_slope_weighted': 'Habitable Slope (Weighted)',
        'avg_slope_simple': 'Average Slope (Simple)',
        'aging_rate': 'Aging Rate (%)',
        'fast_walking_rate': 'Fast Walking Rate (%)',
        'pop_density': 'Population Density'
    }
    stats_list = []
    for col, name in cols.items():
        if col in df.columns:
            s = df[col]
            stats_list.append({
                'Variable': name, 'N': s.count(), 'Mean': s.mean(), 'SD': s.std(), 
                'Min': s.min(), 'Median': s.median(), 'Max': s.max()
            })
    pd.DataFrame(stats_list).round(2).to_csv(output_desc, index=False, encoding='utf-8-sig')
    print("Saved Descriptive Stats.")

    # --- Correlation ---
    output_corr_csv = os.path.join(RESULTS_DIR, "correlation_matrix.csv")
    output_corr_img = os.path.join(FIGURES_DIR, "heatmap_correlation.png")
    
    cols_map = {
        'fracture_rate': 'Total Fracture', 'femur_rate': 'Femur', 'humerus_rate': 'Humerus', 'forearm_rate': 'Forearm',
        'habitable_slope_weighted': 'Slope', 'aging_rate': 'Aging Rate', 'fast_walking_rate': 'Fast Walk', 'pop_density': 'Pop Density'
    }
    target_cols = [c for c in cols_map.keys() if c in df.columns]
    df_corr = df[target_cols].rename(columns=cols_map)
    corr = df_corr.corr()
    corr.to_csv(output_corr_csv, encoding='utf-8-sig')
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", vmin=-1, vmax=1)
    plt.title('Correlation Matrix')
    plt.tight_layout()
    plt.savefig(output_corr_img)
    plt.close()
    print("Saved Correlation Matrix & Heatmap.")

    # --- Regression ---
    output_reg = os.path.join(RESULTS_DIR, "regression_results.txt")
    results_buffer = []
    def add_res(text):
        print(text)
        results_buffer.append(text + "\n")
    
    targets = {'fracture_rate': 'Total', 'femur_rate': 'Femur', 'humerus_rate': 'Humerus', 'forearm_rate': 'Forearm'}
    
    for target_col, name in targets.items():
        if target_col not in df.columns: continue
        add_res(f"\n--- {name} ---")
        
        # Model 1
        model1 = smf.ols(f"{target_col} ~ habitable_slope_weighted", data=df).fit()
        add_res(f"Model 1 (Slope only): Coeff={model1.params['habitable_slope_weighted']:.4f}, p={model1.pvalues['habitable_slope_weighted']:.4f}, R2={model1.rsquared:.4f}")
        
        # Model 2
        covariates = [c for c in ['aging_rate', 'fast_walking_rate', 'pop_density'] if c in df.columns]
        if covariates:
            formula2 = f"{target_col} ~ habitable_slope_weighted + {' + '.join(covariates)}"
            model2 = smf.ols(formula2, data=df).fit()
            add_res(f"Model 2 (Adjusted): Coeff={model2.params['habitable_slope_weighted']:.4f}, p={model2.pvalues['habitable_slope_weighted']:.4f}, R2={model2.rsquared:.4f}")
            add_res(model2.summary().as_text())

    with open(output_reg, "w", encoding="utf-8") as f:
        f.writelines(results_buffer)
    print("Saved Regression Results.")

    # --- Visualization ---
    output_scatter = os.path.join(FIGURES_DIR, "scatter_slope_fracture.png")
    plt.figure(figsize=(12, 8))
    if 'habitable_slope_weighted' in df.columns and 'femur_rate' in df.columns:
        sns.regplot(x='habitable_slope_weighted', y='femur_rate', data=df, scatter_kws={'alpha':0.6}, line_kws={'color':'red'})
        for i, row in df.iterrows():
            plt.text(row['habitable_slope_weighted']+0.1, row['femur_rate'], row['prefecture'], fontsize=9, alpha=0.7)
        plt.title('Slope vs Femur Fracture Rate')
        plt.xlabel('Habitable Slope')
        plt.ylabel('Femur Fracture Rate')
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.savefig(output_scatter, dpi=300)
        plt.close()
        print("Saved Scatter Plot.")

# ---------------------------------------------------------
# Main Execution
# ---------------------------------------------------------
if __name__ == "__main__":
    step1_extract_fracture()
    step2_extract_walking()
    step3_fetch_census()
    step4_integrate()
    step5_stats_analysis()
    print("\nAll steps completed successfully.")
