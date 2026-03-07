import zipfile
import glob
import os
import xml.etree.ElementTree as ET

target_dir = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\02_Data\raw\MLIT\L03_b_Land_Use"
zips = glob.glob(os.path.join(target_dir, "*.zip"))

# Pick one file (e.g. 2021)
target_zip = [z for z in zips if '21_' in z][0]
print(f"Target: {target_zip}")

with zipfile.ZipFile(target_zip, 'r') as zf:
    xmls = [n for n in zf.namelist() if n.endswith('.xml') and 'META' not in n]
    if xmls:
        with zf.open(xmls[0]) as f:
            # Parse limited lines
            head = [f.readline().decode('utf-8') for _ in range(50)]
            print("".join(head))
