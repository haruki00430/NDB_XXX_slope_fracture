
import zipfile
import os
import sys

# UTF-8 Output
sys.stdout.reconfigure(encoding='utf-8')

# Paths
L03_DIR = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\02_Data\raw\MLIT\L03_b_Land_Use"
TEMP_DIR = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture\data\temp"

# Ensure temp dir exists
os.makedirs(TEMP_DIR, exist_ok=True)

# Find first zip
zip_files = [f for f in os.listdir(L03_DIR) if f.endswith('.zip')]
if not zip_files:
    print("No zip files found!")
    sys.exit(1)

target_zip = os.path.join(L03_DIR, "L03-b-21_5339-jgd2011_GML.zip")
print(f"Extracting: {target_zip}")

with zipfile.ZipFile(target_zip, 'r') as z:
    z.extractall(TEMP_DIR)
    
print(f"Extracted to: {TEMP_DIR}")
print("Contents:")
for f in os.listdir(TEMP_DIR):
    print(f)
