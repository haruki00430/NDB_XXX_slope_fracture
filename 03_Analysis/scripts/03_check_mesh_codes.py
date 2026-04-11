import os
import glob

dem_dir = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\02_Data\raw\MLIT\G04_c_Elevation"
zip_files = glob.glob(os.path.join(dem_dir, "*.zip"))

print(f"Total files: {len(zip_files)}")

# Extract unique prefixes (e.g., "11" from "G04-c-11_...")
# Actually, the format is G04-c-YY_MMMM... where YY is year? No, 11 is likely not year 2011?
# Let's check the filename format definition.
# G04-c-11_5339... 
# If 11 is "Year 2011" (Heisei 23), then it might be national data released in 2011.
# But inside the zip, the XML has <ksj:tertiaryMeshCode>53390000</ksj:tertiaryMeshCode>
# 5339 is standard mesh code (Saitama/Tokyo area).

# Let's see the unique mesh codes (first 4 digits of the numeric part).
mesh_codes = set()
for f in zip_files:
    basename = os.path.basename(f)
    # G04-c-11_5339-jgd_GML.zip
    try:
        parts = basename.split('_')
        # parts[0] = G04-c-11
        # parts[1] = 5339-jgd
        mesh_part = parts[1].split('-')[0] # 5339
        mesh_codes.add(mesh_part)
    except:
        pass

print(f"Unique Mesh Codes (First 4 digits): {sorted(list(mesh_codes))}")
