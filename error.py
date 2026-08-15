import os
from pathlib import Path
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

def convert_to_true_dxt5(target_dir):
    target_path = Path(target_dir)
    print(f"Konvertiere alle DDS in echtes DXT5 (Legacy) in: {target_path.resolve()}\n")

    for file_path in target_path.rglob("*.dds"):
        try:
            with Image.open(file_path) as img:
                w, h = img.size
                
                # Auf Vielfaches von 4 korrigieren, um den Grafiktreiber-Crash zu verhindern
                new_w = (w + 3) & ~3
                new_h = (h + 3) & ~3
                
                if new_w != w or new_h != h:
                    img = img.resize((new_w, new_h), Image.Resampling.BICUBIC)
                
                # Transparenz-Check: RGBA erzwingen für DXT5, RGB für DXT1
                if img.mode != "RGBA":
                    img = img.convert("RGBA")
                
                # Pillow-Spezifikation für unkomprimiertes/Legacy DXT5 ohne DX10-Header
                img.save(file_path, format="DDS", compression="dxt5")
                print(f"[OPTIMIERT] {file_path.name} -> DXT5 (Legacy) [{new_w}x{new_h}]")
                
        except Exception as e:
            print(f"[FEHLER] {file_path.name}: {e}")

if __name__ == "__main__":
    mod_folder = r"C:\Users\Leegende\Documents\Paradox Interactive\Hearts of Iron IV\mod\LFR"
    convert_to_true_dxt5(mod_folder)