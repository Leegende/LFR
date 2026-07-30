import os

# ==============================================================================
# KONFIGURATION & TARGET-IDs
# ==============================================================================
TARGET_PROVINCES = {
    "4114", "3718", "4114", "4185", "4706", "5240", "8365", "19362", "19767"
}

# Dynamische Ermittlung des Skript-Verzeichnisses (C:\...\mod\LFR)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Automatische Pfad-Kaskade für Hearts of Iron IV Mod-Strukturen
HOI4_MAP_PATH = os.path.join(BASE_DIR, "map", "definition.csv")
ROOT_PATH = os.path.join(BASE_DIR, "definition.csv")

if os.path.exists(HOI4_MAP_PATH):
    FILE_PATH = HOI4_MAP_PATH
elif os.path.exists(ROOT_PATH):
    FILE_PATH = ROOT_PATH
else:
    raise FileNotFoundError(
        f"definition.csv weder in {HOI4_MAP_PATH} noch in {ROOT_PATH} gefunden. "
        f"Prüfen Sie, ob die Datei existiert."
    )
# ==============================================================================

def fix_coastal_provinces_inplace(file_path, target_ids):
    # Da Verschlüsselungen in Paradox-Dateien variieren, wird standardmäßig cp1252/latin-1 
    # oder utf-8 vorausgesetzt. errors="ignore" verhindert Byte-Konflikte bei Sonderzeichen.
    encoding = "utf-8"
    
    with open(file_path, "r", encoding=encoding, errors="ignore") as f:
        lines = f.readlines()
    
    updated_lines = []
    for line in lines:
        stripped_line = line.rstrip("\n\r")
        parts = stripped_line.split(";")
        
        if parts and parts[0] in target_ids:
            if len(parts) > 5 and parts[5].lower() == "true":
                parts[5] = "false"
                line = ";".join(parts) + "\n"
        
        updated_lines.append(line)
        
    with open(file_path, "w", encoding=encoding) as f:
        f.writelines(updated_lines)
    
    print(f"Erfolgreich verarbeitet. Datei modifiziert: {file_path}")

if __name__ == "__main__":
    fix_coastal_provinces_inplace(FILE_PATH, TARGET_PROVINCES)