import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r"C:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\02_Data\raw\NDB_OpenData\No.10\01_医科診療行為（算定回数）\01_公費レセプトを含まないデータ\K_手術\款別都道府県別算定回数.xlsx"

def comprehensive_fracture_inspection():
    """
    NDB入院シートから骨折関連の全コードを抽出
    """
    print(f"Reading: {file_path}")
    df = pd.read_excel(file_path, sheet_name='入院', header=None)
    
    # Column indices
    code_col_idx = 3
    name_col_idx = 4
    
    # 骨折関連キーワード（広範囲）
    keywords = [
        '骨折', '人工骨頭', '人工関節', 
        'K044', 'K045', 'K046', 'K081', 'K082',
        '大腿', '上腕', '前腕', '股', '肩'
    ]
    
    print(f"Searching for fracture-related procedures...")
    
    found_items = []
    
    for idx, row in df.iterrows():
        name = str(row[name_col_idx]) if pd.notna(row[name_col_idx]) else ""
        code = str(row[code_col_idx]) if pd.notna(row[code_col_idx]) else ""
        
        # Check if row matches any keyword
        if any(k in name or k in code for k in keywords):
            found_items.append({
                'row_idx': idx,
                'code': code,
                'name': name
            })
    
    df_res = pd.DataFrame(found_items)
    
    output_path = r"C:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture\03_Analysis\scripts\03_comprehensive_fracture_codes.txt"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        if not df_res.empty:
            # Deduplicate
            df_res = df_res.drop_duplicates(subset=['code', 'name'])
            f.write("=" * 80 + "\n")
            f.write("NDB入院シート: 骨折関連コード全件リスト\n")
            f.write("=" * 80 + "\n\n")
            
            # Sort by code
            df_sorted = df_res.sort_values(by='code')
            
            for _, row in df_sorted.iterrows():
                f.write(f"Code: {row['code']}\n")
                f.write(f"Name: {row['name']}\n")
                f.write(f"Row:  {row['row_idx']}\n")
                f.write("-" * 80 + "\n")
            
            f.write(f"\n\n総件数: {len(df_sorted)} 件\n")
            
            # 部位別集計
            f.write("\n" + "=" * 80 + "\n")
            f.write("部位別集計\n")
            f.write("=" * 80 + "\n")
            
            sites = ['大腿', '上腕', '前腕', '股', '肩']
            for site in sites:
                site_codes = df_sorted[df_sorted['name'].str.contains(site, na=False)]
                if not site_codes.empty:
                    f.write(f"\n【{site}】 ({len(site_codes)}件)\n")
                    for _, row in site_codes.iterrows():
                        f.write(f"  {row['code']}: {row['name']}\n")
        else:
            f.write("No matches found.")
    
    print(f"Output written to {output_path}")
    print(f"Total records found: {len(df_res) if not df_res.empty else 0}")

if __name__ == "__main__":
    comprehensive_fracture_inspection()
