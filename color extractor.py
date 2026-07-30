
import os
import numpy as np
from PIL import Image

# ==============================================================================
# PFAD- UND ORDNER-DEFINITIONEN (HIER ANPASSEN)
# ==============================================================================
# Definition der absoluten oder relativen Ordnerpfade
INPUT_FOLDER = r"C:\Users\Leegende\Downloads\ordner"
EXPORT_FOLDER = r"C:\Users\Leegende\Downloads\ordner"

# Definition der Dateinamen
INPUT_FILE_NAME = "input.png"
OUTPUT_FILE_NAME = "farbregister_3x3.png"

# Vollständige Pfad-Zusammensetzung
INPUT_IMAGE_PATH = os.path.join(INPUT_FOLDER, INPUT_FILE_NAME)
OUTPUT_IMAGE_PATH = os.path.join(EXPORT_FOLDER, OUTPUT_FILE_NAME)

BLOCK_SIZE = 3
# ==============================================================================

def process_image_to_color_register(input_path, output_path, block_size=3):
    """
    Extrahiert alle eindeutigen Farben aus dem Eingabebild unter Ausschluss 
    transparenter Pixel und speichert sie als linear angereihtes 3x3-Pixel-Register.
    """
    # Validierung der Existenz des Eingabeordners/der Eingabedatei
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Die Datei {input_path} wurde nicht gefunden.")
        
    # Automatische Erstellung des Export-Ordners, falls dieser nicht existiert
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # Bild laden und in das RGBA-Format zwingen zur konsistenten Alpha-Kanal-Prüfung
    img = Image.open(input_path).convert("RGBA")
    img_array = np.array(img)

    # Dimensionen flachdrücken auf eine zweidimensionale Matrix (Pixel, Kanäle)
    pixels = img_array.reshape(-1, 4)

    # Filterung: Ausschluss volltransparenter Pixel (Alpha-Wert == 0)
    # Verhindert, dass der transparente Hintergrund als valide Provinzfarbe gezählt wird
    opaque_pixels = pixels[pixels[:, 3] > 0]

    # Reduktion auf RGB-Kanäle zur Ermittlung der eindeutigen Farbwerte
    rgb_pixels = opaque_pixels[:, :3]
    unique_colors = np.unique(rgb_pixels, axis=0)

    num_colors = len(unique_colors)
    if num_colors == 0:
        raise ValueError("Das Eingabebild enthält keine verwertbaren Pixeldaten.")

    # Transformation der Farbliste in eine 1-Pixel-hohe Zeilenstruktur (1, Anzahl_Farben, RGB)
    base_register = unique_colors.reshape(1, num_colors, 3)

    # Skalierung der Pixelblöcke ohne Interpolationsartefakte via Nearest-Neighbor-Duplikation
    scaled_register = np.repeat(base_register, block_size, axis=0)  # Höhe skalieren
    scaled_register = np.repeat(scaled_register, block_size, axis=1) # Breite skalieren

    # Generierung und persistente Speicherung des Zielbildes im RGB-Modus
    result_img = Image.fromarray(scaled_register.astype(np.uint8), "RGB")
    result_img.save(output_path)

if __name__ == "__main__":
    process_image_to_color_register(INPUT_IMAGE_PATH, OUTPUT_IMAGE_PATH, BLOCK_SIZE)