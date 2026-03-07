
import zipfile
import os
import sys

# UTF-8 Output
sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture"
DEM_DIR = r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\02_Data\raw\MLIT\G04_c_Elevation"
TEMP_DIR = os.path.join(PROJECT_DIR, "data", "temp_g04")

TARGET_ZIP = os.path.join(DEM_DIR, "G04-c-11_5339-jgd_GML.zip")

def inspect_xml():
    print(f"Inspecting {TARGET_ZIP}")
    os.makedirs(TEMP_DIR, exist_ok=True)
    
    with zipfile.ZipFile(TARGET_ZIP, 'r') as z:
        xml_files = [f for f in z.namelist() if f.endswith('.xml') and 'META' not in f]
        if not xml_files:
            print("No data XML found.")
            return
            
        target_xml = xml_files[0]
        print(f"Extracting {target_xml}")
        z.extract(target_xml, TEMP_DIR)
        
        xml_path = os.path.join(TEMP_DIR, target_xml)
        
        print("\n--- XML Content (First 200 lines) ---")
        output_lines = []
        with open(xml_path, 'r', encoding='utf-8') as f:
            for i in range(200):
                line = f.readline()
                if not line: break
                print(line.strip())
                output_lines.append(line)
                
        with open("xml_head.txt", "w", encoding="utf-8") as out_f:
            out_f.writelines(output_lines)

        print("\n--- End of Snippet ---")
        
        # Clean up
        os.remove(xml_path)

if __name__ == "__main__":
    inspect_xml()
