import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r"C:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\02_Data\raw\NDB_OpenData\No.10\07_特定健診 質問票\01_公費レセプトを含まないデータ\標準的な質問票（質問項目１２） 都道府県別性年齢階級別分布.xlsx"

print(f"Reading: {file_path}")

# Read first few rows as header to understand the structure
try:
    # Read without header first to see raw layout
    df = pd.read_excel(file_path, sheet_name=0, header=None, nrows=20)
    
    with open(r"C:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture\03_Analysis\scripts\02_inspect_q16_output.txt", "w", encoding="utf-8") as f:
        f.write("--- Raw Data (First 20 rows) ---\n")
        f.write(df.to_string())
    print("Output written to 02_inspect_q16_output.txt")

    # Try to identify multi-index header
    # Usually row 0-2 or similar are headers
    
except Exception as e:
    print(f"Error reading file: {e}")
