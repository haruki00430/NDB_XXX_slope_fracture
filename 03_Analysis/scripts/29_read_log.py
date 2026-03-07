
import os
import sys

# UTF-8 Encoding for Windows Console
sys.stdout.reconfigure(encoding='utf-8')

LOG_FILE = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture\03_Analysis\scripts\28_error.log"

def read_log():
    if not os.path.exists(LOG_FILE):
        print(f"Log file not found: {LOG_FILE}")
        return

    try:
        # Try UTF-8 (Python default for reconfigure)
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            print("--- LOG CONTENT (UTF-8) ---")
            print(f.read())
    except Exception as e:
        print(f"Failed with UTF-8: {e}")
        try:
            # Try UTF-16
            with open(LOG_FILE, 'r', encoding='utf-16') as f:
                print("--- LOG CONTENT (UTF-16) ---")
                print(f.read())
        except Exception as e2:
             print(f"Failed with UTF-16: {e2}")

if __name__ == "__main__":
    read_log()
