import pandas as pd
import os
import sys
import glob

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"C:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\02_Data\raw\NDB_OpenData\No.10\07_特定健診 質問票\01_公費レセプトを含まないデータ"
search_term = "速度"

print(f"Searching for '{search_term}' in headers of files in {base_dir}...")

xlsx_files = glob.glob(os.path.join(base_dir, "*.xlsx"))

found = False
for file_path in xlsx_files:
    filename = os.path.basename(file_path)
    try:
        # Read just the first row to check title
        df = pd.read_excel(file_path, sheet_name=0, header=None, nrows=1)
        title = str(df.iloc[0, 0])
        
        if search_term in title:
            with open(r"C:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture\03_Analysis\scripts\04_find_result.txt", "w", encoding="utf-8") as f:
                f.write(f"FOUND: {filename}\n")
                f.write(f"Title: {title}\n")
                f.write(f"Full Path: {file_path}\n")
            print(f"Result written to 04_find_result.txt")
            found = True
            break
            
    except Exception as e:
        # print(f"Error reading {filename}: {e}")
        pass

if not found:
    print(f"\nNo file found containing '{search_term}'.")

