import glob
import os

l03_dir = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\02_Data\raw\MLIT\L03_b_Land_Use"
files = glob.glob(os.path.join(l03_dir, "*.xml"))
if not files:
    # Try recursive or zip
    files = glob.glob(os.path.join(l03_dir, "**", "*.xml"), recursive=True)

print(f"Found {len(files)} XML files in L03_b.")

if files:
    print(f"Inspecting structure of: {files[0]}")
    with open(files[0], 'r', encoding='utf-8', errors='ignore') as f:
        print(f.read(1000))
else:
    print("No XML found. Checking for Zips.")
    zips = glob.glob(os.path.join(l03_dir, "*.zip"))
    print(f"Found {len(zips)} Zip files.")
