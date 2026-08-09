import os

# ==============================================================================
# KONFIGURATION & TARGET-IDs
# ==============================================================================
TARGET_PROVINCES = {
    "53", "166", "457", "618", "644", "916", "1042", "1131", "1198", "1344", 
    "1808", "1998", "2102", "2173", "2249", "2355", "2398", "2540", "2611", "2639", 
    "2705", "2718", "3086", "3424", "3553", "3557", "3599", "3607", "3811", "4114", 
    "4185", "4458", "4562", "4582", "4662", "4792", "4827", "4905", "4976", "5225", 
    "5240", "5407", "5432", "5483", "6047", "6273", "6371", "6410", "6465", "6566", 
    "7198", "7361", "7383", "7387", "7430", "7486", "7678", "7726", "7741", "7994", 
    "8040", "8255", "8365", "8469", "8827", "9020", "9137", "9148", "9234", "9264", 
    "9375", "9405", "9449", "9643", "9659", "9697", "9753", "9899", "9953", "9969", 
    "10034", "10207", "10666", "10709", "10883", "11030", "11128", "11380", "11631", "11780", 
    "12012", "12445", "12709", "13210", "13595", "13690", "14244", "14683", "14909", "14940", 
    "15139", "15367", "15846", "15858", "15961", "16071", "16467", "16712", "16832", "16904", 
    "17330", "17555", "18789", "18797", "18968", "19362"
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