import os
import re
import sys

# ==============================================================================
# KONFIGURATION
# ==============================================================================
DEFINITION_PATH = r"C:\Users\Leegende\Documents\Paradox Interactive\Hearts of Iron IV\mod\LFR\map\definition.csv"
STATES_DIR = r"C:\Users\Leegende\Documents\Paradox Interactive\Hearts of Iron IV\mod\LFR\history\states"

PROVINCES_TO_DELETE = [
16210, 16810, 18031, 18403]

def execution_pipeline():
    # 1. Validierung der Dateisystempfade
    if not os.path.exists(DEFINITION_PATH):
        sys.exit(f"[ERROR] definition.csv nicht auffindbar: {DEFINITION_PATH}")
    if not os.path.exists(STATES_DIR):
        sys.exit(f"[ERROR] States-Verzeichnis nicht auffindbar: {STATES_DIR}")

    # 2. Bereinigtes Einlesen der CSV
    # splitlines() + strip() eliminiert trailing \n, die den Index off-by-one shiften
    with open(DEFINITION_PATH, 'r', encoding='utf-8', errors='ignore') as f:
        csv_lines = [line for line in f.read().splitlines() if line.strip()]

    # 3. State-Dateien iterieren und syntaktische Struktur auflösen
    # State Data Structure: Pfad -> {prefix, suffix, provinces (List[int]), modified}
    state_data = {}
    pattern = re.compile(r"(provinces\s*=\s*\{)([^}]*)(\})", re.IGNORECASE)

    for root, _, files in os.walk(STATES_DIR):
        for file in files:
            if file.endswith('.txt'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                match = pattern.search(content)
                if match:
                    # Extraktion des Inhalts aus 'provinces = { ... }'
                    prov_str = match.group(2)
                    # Casting zu Integers für robustere Array-Operationen (ignoriert Whitespaces)
                    prov_list = [int(p) for p in prov_str.split() if p.strip().isdigit()]
                    
                    state_data[path] = {
                        'prefix': content[:match.start(2)],
                        'suffix': content[match.end(2):],
                        'provinces': prov_list,
                        'modified': False
                    }
                else:
                    # Datei beinhaltet keine Provinzen
                    state_data[path] = None

    # 4. Sequenzieller Reverse-Durchlauf
    # Absteigende Sortierung schützt die Index-Korrelation, wenn das Array iterativ schrumpft.
    sorted_targets = sorted(list(set(PROVINCES_TO_DELETE)), reverse=True)

    for target in sorted_targets:
        last_id = len(csv_lines) - 1

        if target > last_id:
            continue
            
        if target == last_id:
            # Fall A: Provinz ist bereits das End-Element. Keine Neu-Verteilung notwendig.
            csv_lines.pop()
            
            # Aus allen betroffenen States extrahieren
            for data in state_data.values():
                if data and target in data['provinces']:
                    data['provinces'].remove(target)
                    data['modified'] = True
        else:
            # Fall B: Swap-and-Pop Mechanik
            last_line_data = csv_lines[last_id].split(';')
            # Überschreibe ID-Attribut der End-Provinz
            last_line_data[0] = str(target)
            
            # Repliziere modifizierte End-Provinz an die Position der gelöschten Ziel-Provinz
            csv_lines[target] = ';'.join(last_line_data)
            # Zerstöre redundanten End-Datensatz
            csv_lines.pop()

            # State-Synchronisation
            for data in state_data.values():
                if data:
                    provs = data['provinces']
                    # 1. Ziel-Provinz aus States tilgen
                    if target in provs:
                        provs.remove(target)
                        data['modified'] = True
                    # 2. Die End-Provinz (last_id) übernimmt die ID der Ziel-Provinz
                    if last_id in provs:
                        provs.remove(last_id)
                        provs.append(target)
                        data['modified'] = True

    # 5. Disk I/O Write
    with open(DEFINITION_PATH, 'w', encoding='utf-8') as f:
        # Neu-Konstruktion inklusive sicherem EOF-Newline für die Clausewitz-Engine
        f.write('\n'.join(csv_lines) + '\n')

    for path, data in state_data.items():
        if data and data['modified']:
            # Syntaktische Formatierung des Blocks: "\n\t\t[IDs]\n\t"
            formatted_provs = "\n\t\t" + " ".join(str(p) for p in data['provinces']) + "\n\t"
            new_content = data['prefix'] + formatted_provs + data['suffix']
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)

if __name__ == "__main__":
    execution_pipeline()