import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r"C:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\02_Data\raw\NDB_OpenData\No.10\01_医科診療行為（算定回数）\01_公費レセプトを含まないデータ\K_手術\款別都道府県別算定回数.xlsx"

def inspect_exact_codes():
    print(f"Reading: {file_path}")
    df = pd.read_excel(file_path, sheet_name='入院', header=None)
    
    # Column indices
    code_col_idx = 3
    name_col_idx = 4
    
    keywords = ['K044', 'K045', '骨折非観血的', '骨折経皮的']
    target_sites = ['大腿', '上腕', '前腕']
    
    print(f"Searching for {keywords} with sites {target_sites}...")
    
    found_items = []
    
    for idx, row in df.iterrows():
        name = str(row[name_col_idx]) if pd.notna(row[name_col_idx]) else ""
        code = str(row[code_col_idx]) if pd.notna(row[code_col_idx]) else ""
        
        # Check if row matches K044/K045 keywords
        if any(k in name or k in code for k in keywords):
            # Check for site
            for site in target_sites:
                if site in name:
                    found_items.append({
                        'category': 'K044/K045',
                        'site': site,
                        'code': code,
                        'name': name,
                        'row_idx': idx
                    })
    
    # Also check K046 just to be sure about the ones we already have
    keywords_k046 = ['K046', '骨折観血的']
    for idx, row in df.iterrows():
        name = str(row[name_col_idx]) if pd.notna(row[name_col_idx]) else ""
        code = str(row[code_col_idx]) if pd.notna(row[code_col_idx]) else ""
        
        if any(k in name or k in code for k in keywords_k046):
             for site in target_sites:
                if site in name:
                    found_items.append({
                        'category': 'K046',
                        'site': site,
                        'code': code,
                        'name': name,
                        'row_idx': idx
                    })

    # Artificial Joint / Head (K081, K082)
    keywords_art = ['人工骨頭', '人工関節', 'K081', 'K082']
    for idx, row in df.iterrows():
        name = str(row[name_col_idx]) if pd.notna(row[name_col_idx]) else ""
        code = str(row[code_col_idx]) if pd.notna(row[code_col_idx]) else ""
        
        if any(k in name or k in code for k in keywords_art):
             for site in ['股', '肩', '膝']: # Hip, Shoulder, Knee
                if site in name:
                    found_items.append({
                        'category': 'Artificial',
                        'site': site,
                        'code': code,
                        'name': name,
                        'row_idx': idx
                    })

    df_res = pd.DataFrame(found_items)
    output_path = r"C:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture\03_Analysis\scripts\02_verify_output.txt"
    with open(output_path, 'w', encoding='utf-8') as f:
        if not df_res.empty:
            # Deduplicate
            df_res = df_res.drop_duplicates(subset=['code', 'name'])
            f.write(df_res.sort_values(by=['category', 'site', 'code']).to_string())
        else:
            f.write("No matches found.")
    print(f"Output written to {output_path}")

if __name__ == "__main__":
    inspect_exact_codes()
