import pandas as pd
import sys

# Windows console encoding fix
sys.stdout.reconfigure(encoding='utf-8')

file_path = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture\03_Analysis\data\processed\analysis_dataset_v1.csv"

try:
    print(f"Reading {file_path}...")
    df = pd.read_csv(file_path)
    
    print(f"Rows: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    
    # Check for NaNs
    print("\nMissing Values:")
    print(df.isna().sum()[df.isna().sum() > 0])
    
    # Check Correlations
    print("\nCorrelation Matrix (Selected Columns):")
    cols = ['fracture_rate', 'femur_rate', 'humerus_rate', 'forearm_rate', 
            'aging_rate', 'pop_density', 'fast_walking_rate', 'habitable_slope_weighted', 'avg_slope_simple']
    
    # Ensure cols exist
    existing_cols = [c for c in cols if c in df.columns]
    
    if existing_cols:
        corr_matrix = df[existing_cols].corr()
        print(corr_matrix)
    else:
        print("Required columns for correlation missing.")

except Exception as e:
    print(f"Error: {e}")
