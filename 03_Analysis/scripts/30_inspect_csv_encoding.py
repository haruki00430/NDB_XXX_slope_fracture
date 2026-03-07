
import os
import sys

# UTF-8 Encoding per user rules
sys.stdout.reconfigure(encoding='utf-8')

FILE_PATH = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture\03_Analysis\data\interim\mesh_prefecture_mapping_final_verified.csv"

def inspect_file():
    if not os.path.exists(FILE_PATH):
        print(f"File not found: {FILE_PATH}")
        return

    print(f"Inspecting: {os.path.basename(FILE_PATH)}")
    
    # Read as bytes
    with open(FILE_PATH, 'rb') as f:
        head = f.read(1000)
        
    print(f"First 100 bytes (hex): {head[:100].hex()}")
    
    try:
        decoded = head.decode('utf-8')
        print(f"Decoded as UTF-8:\n{decoded[:200]}")
    except Exception as e:
        print(f"Failed via UTF-8: {e}")
        
    try:
        decoded = head.decode('cp932') # Shift-JIS
        print(f"Decoded as CP932:\n{decoded[:200]}")
    except Exception as e:
        print(f"Failed via CP932: {e}")

if __name__ == "__main__":
    inspect_file()
