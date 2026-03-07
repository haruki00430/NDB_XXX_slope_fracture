import os
import glob
import re

target_dir = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\02_Data\raw\MLIT\L03_b_Land_Use"

def get_approx_region(mesh_code_str):
    try:
        lat_code = int(mesh_code_str[:2])
        if 30 <= lat_code <= 35: return "Kyushu/Okinawa"
        if 36 <= lat_code <= 39: return "Kyushu/Shikoku"
        if 40 <= lat_code <= 47: return "Chugoku/Kansai"
        if 48 <= lat_code <= 52: return "Chubu/Kanto"
        if 53 <= lat_code <= 57: return "Tohoku"
        if 58 <= lat_code <= 68: return "Hokkaido"
        return "Unknown"
    except:
        return "Invalid"

zip_files = glob.glob(os.path.join(target_dir, "*.zip"))
print(f"Total L03-b files: {len(zip_files)}")

coverage = {}
years = {}

for f in zip_files:
    basename = os.path.basename(f)
    # Expected format: L03-b-YY_MMMM-jgd2011_GML.zip
    # YY: Year code (21=R3, 26=H26?, 06=H18?)
    # MMMM: Mesh code
    
    # Regex match
    match = re.search(r"L03-b-(\d+)_(\d+)", basename)
    if match:
        year_code = match.group(1)
        mesh_code = match.group(2)
        
        region = get_approx_region(mesh_code)
        if region not in coverage: coverage[region] = 0
        coverage[region] += 1
        
        if year_code not in years: years[year_code] = 0
        years[year_code] += 1
        
print("\n--- Coverage by Region ---")
for r, c in coverage.items():
    print(f"{r}: {c} files")

print("\n--- Coverage by Year Code ---")
for y, c in years.items():
    print(f"Year {y}: {c} files")

# Check gaps?
# Primary mesh codes range from ~30 to ~68.
# We can check which primary meshes are missing.
present_primary = set()
for f in zip_files:
    match = re.search(r"_(\d{4})", os.path.basename(f))
    if match:
        mesh = match.group(1)
        present_primary.add(mesh[:2])

print(f"\nPresent Primary Meshes: {sorted(list(present_primary))}")
all_primary = set([str(i) for i in range(30, 69)])
missing = sorted(list(all_primary - present_primary))
print(f"Missing Primary Meshes (Approx): {missing}")
