import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"C:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\02_Data\raw\NDB_OpenData\No.10"
output_file = r"C:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture\03_Analysis\scripts\03_dir_list.txt"

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(f"Listing: {base_dir}\n")
    try:
        for item in os.listdir(base_dir):
            f.write(f" - {item}\n")
            if "質問" in item:
                sub_dir = os.path.join(base_dir, item)
                f.write(f"   Listing subdirectory: {sub_dir}\n")
                try:
                    for sub_item in os.listdir(sub_dir):
                        f.write(f"     - {sub_item}\n")
                except Exception as e:
                    f.write(f"     Error listing subdir: {e}\n")
    except Exception as e:
        f.write(f"Error listing base dir: {e}\n")

print(f"Directory listing saved to {output_file}")
