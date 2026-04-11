import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import sys
import os

# Windows console encoding fix
sys.stdout.reconfigure(encoding='utf-8')

def run_regression_analysis():
    print("回帰分析を開始します...")
    
    # Paths
    base_dir = r"C:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture"
    input_file = os.path.join(base_dir, "03_Analysis", "data", "processed", "analysis_dataset_v1.csv")
    output_dir = os.path.join(base_dir, "03_Analysis", "results")
    output_txt = os.path.join(output_dir, "regression_results.txt")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Load Data
    if not os.path.exists(input_file):
        print(f"エラー: 入力ファイルが見つかりません: {input_file}")
        return
        
    df = pd.read_csv(input_file)
    print(f"データ読み込み完了: {len(df)} 行")
    
    # Scale variables for better interpretation (optional, but good for reporting)
    # Slope is in degrees. Aging rate in %. Fracture rate per 100k.
    # No scaling needed for standard interpretation.
    
    results_buffer = []
    
    def add_result(text):
        print(text)
        results_buffer.append(text + "\n")

    add_result("==================================================")
    add_result("Regression Analysis Results")
    add_result("==================================================")
    
    # Target Variables
    targets = {
        'fracture_rate': 'Total Fracture Rate',
        'femur_rate': 'Femur Fracture Rate',
        'humerus_rate': 'Humerus Fracture Rate',
        'forearm_rate': 'Forearm Rate'
    }
    
    # Models
    # Model 1: Single Regression (Y ~ Slope)
    # Model 2: Multiple Regression (Y ~ Slope + Aging + Walking + PopDensity)
    
    for target_col, target_name in targets.items():
        if target_col not in df.columns:
            continue
            
        add_result(f"\nTarget: {target_name} ({target_col})")
        add_result("-" * 50)
        
        # Model 1
        formula1 = f"{target_col} ~ habitable_slope_weighted"
        model1 = smf.ols(formula1, data=df).fit()
        add_result(f"Model 1: {formula1}")
        add_result(f"R-squared: {model1.rsquared:.4f}")
        add_result(f"Slope Coeff: {model1.params['habitable_slope_weighted']:.4f} (p={model1.pvalues['habitable_slope_weighted']:.4f})")
        
        # Model 2
        formula2 = f"{target_col} ~ habitable_slope_weighted + aging_rate + fast_walking_rate + pop_density"
        # Check if columns exist
        available_cols = [c for c in ['aging_rate', 'fast_walking_rate', 'pop_density'] if c in df.columns]
        if available_cols:
            formula2 = f"{target_col} ~ habitable_slope_weighted + {' + '.join(available_cols)}"
            model2 = smf.ols(formula2, data=df).fit()
            add_result(f"\nModel 2: {formula2}")
            add_result(model2.summary().as_text())
        else:
            add_result("\nModel 2 skipped (missing covariates)")
            
    # Save Results
    with open(output_txt, "w", encoding="utf-8") as f:
        f.writelines(results_buffer)
        
    print(f"結果保存完了: {output_txt}")

if __name__ == "__main__":
    run_regression_analysis()
