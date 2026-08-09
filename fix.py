import re

def clean_positions(file_path, max_x, max_z):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Regex zum Finden von Provinz-Blöcken in positions.txt
    pattern = re.compile(r'(\d+)\s*=\s*\{([^}]*?x\s*=\s*([-\d.]+)[^}]*?z\s*=\s*([-\d.]+)[^}]*?)\}', re.DOTALL)
    
    def evaluate_block(match):
        prov_id = match.group(1)
        block = match.group(0)
        x = float(match.group(3))
        z = float(match.group(4))

        # Prüfung auf Grenzwertüberschreitung
        if x < 0 or x > max_x or z < 0 or z > max_z:
            # Fallback: Auf 0,0 setzen oder Block modifizieren
            print(f"Korrigiere Provinz {prov_id}: X={x}, Z={z} außerhalb der Grenzen.")
            # Ersetzen der Koordinaten durch Standardwerte (0)
            cleaned_block = re.sub(r'x\s*=\s*[-\d.]+', 'x = 0.000', block)
            cleaned_block = re.sub(r'z\s*=\s*[-\d.]+', 'z = 0.000', cleaned_block)
            return cleaned_block
        return block

    new_content = pattern.sub(evaluate_block, content)

    with open(file_path + '_fixed.txt', 'w', encoding='utf-8') as file:
        file.write(new_content)

# Beispielaufruf (Maximalwerte der Map-Dimensionen eintragen, z. B. 8192 x 4096)
# clean_positions('positions.txt', 8192.0, 4096.0)