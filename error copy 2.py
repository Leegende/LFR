import os
from pathlib import Path

def find_matching_files(mod_dir, file_list):
    mod_path = Path(mod_dir)
    # Dateinamen aus der Liste extrahieren (nur den Dateinamen ohne den Steam-Pfad)
    target_filenames = {Path(p).name.lower() for p in file_list}
    
    print(f"Suche in Mod-Ordner: {mod_path.resolve()}\n")
    print(f"{'DATEINAME':<40} | {'STATUS / MOD-PFAD'}")
    print("-" * 90)

    found_count = 0
    for file_path in mod_path.rglob("*"):
        if file_path.is_file() and file_path.name.lower() in target_filenames:
            print(f"{file_path.name:<40} | {file_path}")
            found_count += 1

    print("-" * 90)
    print(f"Suche beendet. {found_count} von {len(target_filenames)} Dateien im LFR-Mod-Ordner gefunden.")

if __name__ == "__main__":
    mod_folder = r"C:\Users\Leegende\Documents\Paradox Interactive\Hearts of Iron IV\mod\LFR"
    
    # Die von dir aufgelisteten Pfade als Referenzliste
    target_paths = [
        r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV\gfx\interface\division_3d_entry_half_width.dds",
        r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV\gfx\interface\leader_selection_active_entry_bg.dds",
        r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV\gfx\interface\leader_selection_entry_bg.dds",
        r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV\gfx\interface\leader_selection_unavailable_active_entry_bg.dds",
        r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV\gfx\interface\leader_selection_unavailable_entry_bg.dds",
        r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV\gfx\interface\logistics_air_equipment_entry_bg.dds",
        r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV\gfx\interface\logistics_equipment_entry_bg.dds",
        r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV\gfx\interface\logistics_naval_equipment_entry_bg.dds",
        r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV\gfx\interface\marshal_captured_bg.dds",
        r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV\gfx\interface\marshal_selection_active_entry_bg.dds",
        r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV\gfx\interface\marshal_selection_entry_bg.dds",
        r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV\gfx\interface\naval_leader_selection_active_entry_bg.dds",
        r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV\gfx\interface\naval_leader_selection_entry_bg.dds",
        r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV\gfx\interface\decisionview\decision_description_bg.dds",
        r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV\gfx\interface\divisiondesigner\bg_3d_air.dds",
        r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV\gfx\interface\divisiondesigner\bg_3d_land.dds",
        r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV\gfx\interface\divisiondesigner\bg_3d_sea.dds",
        r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV\gfx\interface\occupation\occupation_policy_icon_strip.dds",
        r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV\gfx\interface\factions\ui\faction_intelligence_background.dds",
        r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV\gfx\interface\factions\ui\faction_spymaster_background.dds",
        r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV\gfx\interface\factions\ui\leader_selection_active_entry_bg_faction.dds",
        r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV\gfx\interface\factions\ui\leader_selection_entry_bg_faction.dds"
    ]
    
    find_matching_files(mod_folder, target_paths)