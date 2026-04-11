import pandas as pd
import sys

file_path = r"C:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\02_Data\raw\NDB_OpenData\No.10\01_医科診療行為（算定回数）\01_公費レセプトを含まないデータ\K_手術\款別都道府県別算定回数.xlsx"
output_path = r"C:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture\03_Analysis\scripts\00_temp_inspect_output.txt"

try:
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"Reading: {file_path}\n")
        df = pd.read_excel(file_path, sheet_name='入院', header=None, nrows=20)
        f.write(df.to_string())
except Exception as e:
    print(e)
