import os

root_dir = r"C:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\02_Data"
keyword = "質問"

print(f"Searching for files containing '{keyword}' in {root_dir}")

found_files = []
for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if keyword in filename and filename.endswith(".xlsx"):
            full_path = os.path.join(dirpath, filename)
            print(f"Found: {full_path}")
            found_files.append(full_path)

if not found_files:
    print("No matching files found.")
