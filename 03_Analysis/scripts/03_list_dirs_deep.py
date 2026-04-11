import os

target_dir = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\02_Data\raw\MLIT"

print(f"Listing directories in: {target_dir}")

try:
    for root, dirs, files in os.walk(target_dir):
        for d in dirs:
            print(os.path.join(root, d))
except Exception as e:
    print(f"Error: {e}")
