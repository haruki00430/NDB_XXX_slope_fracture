import pandas as pd
import sys

# Windows console encoding fix
sys.stdout.reconfigure(encoding='utf-8')

file_path = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\02_Data\raw\Statistics_Bureau\Census_2020\tblT001141H01.txt"

try:
    print(f"Reading {file_path}...")
    # Read first 10 rows
    df = pd.read_csv(file_path, encoding='cp932', nrows=10, dtype=str)
    
    print("\nColumns:")
    for i, col in enumerate(df.columns):
        print(f"{i}: {col}")
        
    print("\nFirst 5 rows:")
    print(df.head())
    
except Exception as e:
    print(f"Error: {e}")
