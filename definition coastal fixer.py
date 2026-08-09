import os

# ==============================================================================
# FEHLERANALYSE & KORREKTUR:
# 1. parts[0].strip() behebt Whitespace-Probleme beim ID-Abgleich.
# 2. parts[5] muss auf "true" gesetzt werden, da die Provinzen laut Bitmap 
#    an Wasser grenzen (Küste) und die Definition dies bisher fälschlicherweise 
#    auf "false" gesetzt hat ("Bitmap adjacency result will be preferred").
# ==============================================================================

TARGET_PROVINCES = {
    "4114", "4185", "5240", "8365", "18041", "18624", "18638", "18678", 
    "18750", "18794", "18799", "18809", "18911", "19101", "19362", "19370"
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HOI4_MAP_PATH = os.path.join(BASE_DIR, "map", "definition.csv")
ROOT_PATH = os.path.join(BASE_DIR, "definition.csv")

if os.path.exists(HOI4_MAP_PATH):
    FILE_PATH = HOI4_MAP_PATH
elif os.path.exists(ROOT_PATH):
    FILE_PATH = ROOT_PATH
else:
    raise FileNotFoundError(
        f"definition.csv weder in {HOI4_MAP_PATH} noch in {ROOT_PATH} gefunden."
    )

def fix_coastal_provinces_inplace(file_path, target_ids):
    encoding = "utf-8-sig"
    
    with open(file_path, "r", encoding=encoding, errors="ignore") as f:
        lines = f.readlines()
    
    updated_lines = []
    modified_count = 0
    
    for line in lines:
        stripped_line = line.rstrip("\n\r")
        parts = stripped_line.split(";")
        
        if parts:
            province_id = parts[0].strip()
            if province_id in target_ids:
                if len(parts) > 5:
                    # Auf "true" setzen, da die Engine bei Diskrepanzen 
                    # ("Bitmap adjacency result will be preferred") die Küsteneigenschaft 
                    # erzwingt, die Definition aber synchronisiert sein muss.
                    parts[5] = "true"
                    line = ";".join(parts) + "\n"
                    modified_count += 1
        
        updated_lines.append(line)
        
    with open(file_path, "w", encoding=encoding) as f:
        f.writelines(updated_lines)
    
    print(f"Erfolgreich verarbeitet. Modifizierte Provinzen: {modified_count} in {file_path}")

if __name__ == "__main__":
    fix_coastal_provinces_inplace(FILE_PATH, TARGET_PROVINCES)