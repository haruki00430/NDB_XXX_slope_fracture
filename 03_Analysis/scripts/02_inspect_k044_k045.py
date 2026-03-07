import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r"C:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\02_Data\raw\NDB_OpenData\No.10\01_医科診療行為（算定回数）\01_公費レセプトを含まないデータ\K_手術\款別都道府県別算定回数.xlsx"

def inspect_k044_k045():
    print(f"Reading: {file_path}")
    # Read Inpatient sheet
    df = pd.read_excel(file_path, sheet_name='入院', header=None)
    
    # Column indices based on previous finding
    code_col_idx = 3
    name_col_idx = 4
    total_count_col_idx = 7 # Column 7 is usually '総計' (Total) or first prefecture? 
    # Actually, based on previous `00_temp_inspect_output.txt`:
    # Col 5 is '総計(算定回数)' (Index 6) ?
    # Let's check the header in row 2 (Index 2) from previous output:
    # 2: ... 4:診療行為コード 5:診療行為 6:点数 7:総計(算定回数) 8:01(Hokkaido)...
    # So Total Count is Index 7.
    
    keywords = ['K044', 'K045', '骨折非観血的', '骨折経皮的']
    target_sites = ['大腿', '上腕', '前腕']
    
    print(f"Searching for {keywords} with sites {target_sites}...")
    
    results = []
    
    for idx, row in df.iterrows():
        name = str(row[name_col_idx]) if pd.notna(row[name_col_idx]) else ""
        code = str(row[code_col_idx]) if pd.notna(row[code_col_idx]) else ""
        
        # Check if row matches K044/K045 keywords
        is_target_proc = any(k in name or k in code for k in keywords)
        
        if is_target_proc:
            # Check for site
            site_match = next((site for site in target_sites if site in name), None)
            
            if site_match:
                count = row[7] # Total count
                results.append({
                    'code': code,
                    'name': name,
                    'site': site_match,
                    'total_count': count
                })

    # Convert to DataFrame
    df_res = pd.DataFrame(results)
    
    if not df_res.empty:
        print("\n--- Identified K044/K045 Records ---")
        # Clean count (remove non-numeric)
        df_res['total_count'] = pd.to_numeric(df_res['total_count'], errors='coerce').fillna(0)
        
        print(df_res.sort_values(by='total_count', ascending=False).to_string())
        
        # Summary by type and site
        print("\n--- Summary by Site ---")
        print(df_res.groupby('site')['total_count'].sum())
    else:
        print("No matching K044/K045 records found for target sites.")

if __name__ == "__main__":
    inspect_k044_k045()
