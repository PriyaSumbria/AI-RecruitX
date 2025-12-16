import pandas as pd
import json
import os
import zipfile
import io

def convert_esco_to_json(zip_path, output_json):
    print(f"Opening ZIP file: {zip_path}")
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            # The specific file we need inside the ZIP
            target_file = 'skills_en.csv'
            
            if target_file not in z.namelist():
                print(f"Error: {target_file} not found in the ZIP. Available files: {z.namelist()[:3]}...")
                return

            # Open the specific CSV file from the ZIP
            with z.open(target_file) as f:
                df = pd.read_csv(f)
                print(f"Successfully loaded {target_file}")

        library = {
            "technical": [],
            "soft": [],
            "mapping": {
                "reactjs": "react",
                "nodejs": "node.js",
                "ml": "machine learning"
            }
        }

        # ESCO Columns: 'preferredLabel' (Skill Name) and 'skillType' (Category)
        for _, row in df.iterrows():
            skill_name = str(row['preferredLabel']).lower().strip()
            skill_type = str(row['skillType']).lower()

            # ESCO categorizes Hard Skills as 'knowledge' and Soft as 'skill/competence'
            if 'knowledge' in skill_type:
                library["technical"].append(skill_name)
            else:
                library["soft"].append(skill_name)

        # Cleanup: Remove duplicates
        library["technical"] = sorted(list(set(library["technical"])))
        library["soft"] = sorted(list(set(library["soft"])))

        # Save the structured library
        os.makedirs(os.path.dirname(output_json), exist_ok=True)
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(library, f, indent=4)
        
        print(f"✅ Success! Generated library with {len(library['technical'])} hard and {len(library['soft'])} soft skills.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Use the absolute path to your ZIP file on the desktop
    # Example: r"C:\Users\YourName\Desktop\v1.1.1.zip"
    input_zip = r"C:\Users\Priya Sumbria\Downloads\ESCO dataset - v1.2.1 - classification - en - csv.zip"
    output_path = "backend/app/data/skills_library.json"
    
    convert_esco_to_json(input_zip, output_path)