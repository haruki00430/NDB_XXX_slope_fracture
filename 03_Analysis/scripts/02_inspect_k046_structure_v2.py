import pandas as pd
import sys
import os

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

file_path = r"C:\\Users\\user\\SharedWorkspace\\projects\\NDB_Research_Hub\\02_Data\\raw\\NDB_OpenData\\No.10\\01_医科診療行為（算定回数）\\01_公費レセプトを含まないデータ\\K_手術\\款別都道府県別算定回数.xlsx"
output_path = r"C:\\Users\\user\\SharedWorkspace\\projects\\NDB_Research_Hub\\projects\\NDB_XXX_slope_fracture\\03_Analysis\\results\\k046_inspection.txt"

# Ensure results directory exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(f"Reading file: {file_path}\n\n")

    try:
        # Get sheet names
        xl = pd.ExcelFile(file_path)
        f.write(f"Sheet names: {xl.sheet_names}\n\n")

        # Target '入院' (Inpatient) sheet - usually where major surgeries are
        # If '入院' is not found, try index 2 (as per screenshot order: Outpatient, Outpatient+, Inpatient, Inpatient+)
        if '入院' in xl.sheet_names:
            target_sheet = '入院'
        elif len(xl.sheet_names) > 2:
            target_sheet = xl.sheet_names[2]
        else:
            target_sheet = 0 # Fallback
            
        f.write(f"--- Inspecting Sheet: {target_sheet} ---\n")
        
        # Read the header first to find the '診療行為' column (Column E, usually index 4)
        df_head = pd.read_excel(file_path, sheet_name=target_sheet, header=None, nrows=20)
        f.write("--- Header Inspection (First 20 rows) ---\n")
        f.write(df_head.to_string())
        f.write("\n\n")

        df_all = pd.read_excel(file_path, sheet_name=target_sheet, header=None)
        
        # Keywords for Hip/Femur Fracture
        # K046-1 (骨折観血的手術), K081 (人工骨頭), K082 (人工関節), 大腿 (Femur), 頚部 (Neck), 転子 (Trochanter)
        keywords = ['大腿', '骨折', '人工骨頭', '人工関節', 'K046', 'K081', 'K082']
        f.write(f"--- Searching for keywords in ALL columns: {keywords} ---\n")
        
        # Search in all columns
        mask = df_all.astype(str).apply(lambda x: x.str.contains('|'.join(keywords), na=False)).any(axis=1)
        found_rows = df_all[mask]
        
        f.write(f"Found {len(found_rows)} rows containing keywords in '{target_sheet}' sheet\n")
        
        if not found_rows.empty:
             f.write(found_rows.to_string())

        print(f"Inspection complete. Results saved to {output_path}")

    except Exception as e:
        f.write(f"\nError: {e}\n")
        print(f"Error: {e}")
