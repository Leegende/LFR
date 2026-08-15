import os
from pathlib import Path
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

def fix_textures(target_dirs):
    target_widths = {984, 510}
    
    for directory in target_dirs:
        target_path = Path(directory)
        if not target_path.exists():
            print(f"Pfad nicht gefunden: {target_path}")
            continue
            
        print(f"Scanne: {target_path}")
        for file_path in target_path.rglob("*"):
            if file_path.suffix.lower() in {".dds", ".tga"}:
                try:
                    with Image.open(file_path) as img:
                        w, h = img.size
                        # Wenn Breite passt oder Höhe beschädigt (0) ist
                        if w in target_widths or h == 0:
                            print(f"[GEFUNDEN] {file_path}")
                            # Hier nur Info, keine automatische Korrektur im Vanilla-Ordner!
                except Exception:
                    pass

if __name__ == "__main__":
    # Liste beider Verzeichnisse
    dirs_to_scan = [
        r"C:\Users\Leegende\Documents\Paradox Interactive\Hearts of Iron IV\mod\LFR",
        r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV"
    ]
    fix_textures(dirs_to_scan)