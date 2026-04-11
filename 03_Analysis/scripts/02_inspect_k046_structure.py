import pandas as pd
import sys

# Ensure UTF-8 output for Japanese characters
sys.stdout.reconfigure(encoding='utf-8')

file_path = r"C:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\02_Data\raw\NDB_OpenData\No.10\01_医科診療行為（算定回数）\01_公費レセプトを含まないデータ\K_手術\款別都道府県別算定回数.xlsx"

print(f"Reading file: {file_path}")

try:
    # Read the first 20 rows to visually identify the header
    print("\n--- First 20 rows (Header Inspection) ---")
    df_head = pd.read_excel(file_path, sheet_name=0, header=None, nrows=20)
    print(df_head.to_string())

    # Search for 'K046' to find the relevant data block
    print("\n--- Searching for 'K046' ---")
    # Read the whole sheet without header to use numerical indexing
    df_all = pd.read_excel(file_path, sheet_name=0, header=None)
    
    # Assuming code is in column B (index 1) or C (index 2)
    # Let's search in all columns for safety
    mask = df_all.astype(str).apply(lambda x: x.str.contains('K046', na=False)).any(axis=1)
    k046_rows = df_all[mask]
    
    print(f"Found {len(k046_rows)} rows containing 'K046'")
    
    if not k046_rows.empty:
        # Get the first occurrence
        first_idx = k046_rows.index[0]
        
        # Display rows around the first K046 occurrence to understand the hierarchy
        start_row = max(0, first_idx - 5)
        end_row = min(len(df_all), first_idx + 25) # Show enough rows to see the breakdown
        
        print(f"\n--- Rows around K046 (Row {start_row} to {end_row}) ---")
        # Display columns A to M (0 to 12) to see metadata and some prefectures
        print(df_all.iloc[start_row:end_row, :15].to_string())

except Exception as e:
    print(f"Error: {e}")
