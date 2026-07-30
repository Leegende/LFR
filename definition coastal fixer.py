import os

# ==============================================================================
# KONFIGURATION & TARGET-IDs
# ==============================================================================
TARGET_PROVINCES = {
    "45", "405", "870", "939", "1296", "1307", "1485", "1864", "2182", "2393",
    "2813", "3003", "3069", "3826", "3848", "3920", "4044", "4073", "4451", "4603",
    "4833", "4899", "5070", "5130", "5264", "5283", "6641", "7201", "7634", "8211",
    "8869", "8881", "8907", "8953", "9228", "9255", "9783", "9787", "9804", "9825",
    "9854", "9862", "9871", "9949", "9964", "9970", "16244", "16285", "16312", "16443",
    "16452", "16676", "16748", "16763", "16891", "16934", "17009", "17113", "17325", "17400",
    "17512", "17535", "17730", "17757", "17908", "18142", "18244", "18487", "18515", "18517",
    "18887"
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