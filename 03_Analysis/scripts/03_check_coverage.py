import os
import glob

# Simplified mesh code to prefecture mapping logic
# (Very rough approximation based on first 2 digits of 2nd/3rd mesh)
# 1st digit: Latitude (x 1.5), 2nd digit: Longitude (x 1 + 100)
# e.g., 5339 -> Lat 35.33 (Saitama/Tokyo), Lon 139.00
# 36xx -> Lat ~24N (Okinawa)
# 68xx -> Lat ~45N (Hokkaido)

def get_approx_region(mesh_code_str):
    try:
        lat_code = int(mesh_code_str[:2])
        if 36 <= lat_code <= 40: return "Okinawa/Kyushu South"
        if 40 <= lat_code <= 48: return "Kyushu/Shikoku"
        if 48 <= lat_code <= 52: return "Kansai/Chubu"
        if 52 <= lat_code <= 54: return "Kanto/Chubu"
        if 54 <= lat_code <= 60: return "Tohoku"
        if 60 <= lat_code <= 68: return "Hokkaido"
        return "Unknown"
    except:
        return "Invalid"

files = glob.glob(r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\02_Data\raw\MLIT\G04_c_Elevation\*.zip")
regions_covered = set()

for f in files:
    try:
        # G04-c-11_5339...
        mesh = os.path.basename(f).split('_')[1].split('-')[0]
        region = get_approx_region(mesh)
        regions_covered.add(region)
    except:
        pass

print("Covered Regions (Approx):", sorted(list(regions_covered)))
