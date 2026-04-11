import zipfile
import glob
import os

target_dir = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\02_Data\raw\MLIT\L03_b_Land_Use"
zips = glob.glob(os.path.join(target_dir, "*.zip"))
target_zip = zips[0]

print(f"Reading head of: {target_zip}")

with zipfile.ZipFile(target_zip, 'r') as zf:
    xmls = [n for n in zf.namelist() if n.endswith('.xml') and 'META' not in n]
    with zf.open(xmls[0]) as f:
        # Read 2000 bytes
        head = f.read(2000).decode('utf-8', errors='ignore')
        print(head)
