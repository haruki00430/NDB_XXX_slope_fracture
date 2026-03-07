import zipfile
import glob
import os
import xml.etree.ElementTree as ET

# Find one zip from each year
target_dir = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\02_Data\raw\MLIT\L03_b_Land_Use"
zips = glob.glob(os.path.join(target_dir, "*.zip"))

samples = {}
for z in zips:
    year = os.path.basename(z).split('_')[0].split('-')[2] # L03-b-21... -> 21
    if year not in samples:
        samples[year] = z
        
print(f"Sample Years found: {list(samples.keys())}")

def inspect_xml_content(zip_path):
    print(f"\nScanning: {os.path.basename(zip_path)}")
    with zipfile.ZipFile(zip_path, 'r') as zf:
        xmls = [n for n in zf.namelist() if n.endswith('.xml') and 'META' not in n]
        if not xmls:
            print("No data XML found.")
            return
            
        with zf.open(xmls[0]) as f:
            # Read first few bytes to guess structure
            head = f.read(2000).decode('utf-8', errors='ignore')
            print(head)

for y, p in samples.items():
    inspect_xml_content(p)
