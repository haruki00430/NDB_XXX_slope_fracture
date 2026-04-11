import os

base_dir = r"C:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\02_Data\raw\NDB_OpenData\No.10"

print(f"Listing: {base_dir}")
try:
    for item in os.listdir(base_dir):
        print(f" - {item}")
        if "質問票" in item:
            sub_dir = os.path.join(base_dir, item)
            print(f"   Listing subdirectory: {sub_dir}")
            try:
                for sub_item in os.listdir(sub_dir):
                    print(f"     - {sub_item}")
            except Exception as e:
                print(f"     Error listing subdir: {e}")
except Exception as e:
    print(f"Error listing base dir: {e}")
