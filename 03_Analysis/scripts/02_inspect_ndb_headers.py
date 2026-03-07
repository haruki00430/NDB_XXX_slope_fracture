
import pandas as pd
import sys

# Windows console encoding fix
sys.stdout.reconfigure(encoding='utf-8')

def inspect_file(path, name):
    print(f"\n{'='*20} {name} {'='*20}")
    print(f"Path: {path}")
    try:
        # Read first few rows without header to see raw structure
        df = pd.read_excel(path, header=None, nrows=20)
        print("First 20 rows (raw):")
        print(df.head(20))
        
        # Try to detect "K046" in the surgery file
        if "手術" in name:
            # Load more rows to find K046 if possible, or just search in what we have if it's sparse
            # But K046 is likely deep down. Let's read column 1-5 for all rows to find row index
            print("\nSearching for 'K046' in first few columns...")
            df_full = pd.read_excel(path, header=None, usecols=range(5))
            k046_rows = []
            for idx, row in df_full.iterrows():
                row_str = row.astype(str).values
                if any("K046" in x for x in row_str):
                    k046_rows.append(idx)
            
            print(f"Found 'K046' at rows: {k046_rows}")
            
            if k046_rows:
                # Show the first found row
                target_row = k046_rows[0]
                print(f"\nRow {target_row} content:")
                print(pd.read_excel(path, header=None, nrows=1, skiprows=target_row))

    except Exception as e:
        print(f"Error reading file: {e}")

# Paths
surgery_path = r"C:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\02_Data\raw\NDB_OpenData\No.10\01_医科診療行為（算定回数）\01_公費レセプトを含まないデータ\K_手術\款別都道府県別算定回数.xlsx"
q12_path = r"C:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\02_Data\raw\NDB_OpenData\No.10\07_特定健診 質問票\01_公費レセプトを含まないデータ\標準的な質問票（質問項目１２） 都道府県別性年齢階級別分布.xlsx"

inspect_file(surgery_path, "Fracture Surgery (K_Surgery)")
inspect_file(q12_path, "Walking Speed (Q12)")
