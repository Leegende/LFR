
import os
import numpy as np
from PIL import Image





INPUT_FOLDER = r"C:\Users\Leegende\Downloads\ordner"
EXPORT_FOLDER = r"C:\Users\Leegende\Downloads\ordner"


INPUT_FILE_NAME = "input.png"
OUTPUT_FILE_NAME = "farbregister_3x3.png"


INPUT_IMAGE_PATH = os.path.join(INPUT_FOLDER, INPUT_FILE_NAME)
OUTPUT_IMAGE_PATH = os.path.join(EXPORT_FOLDER, OUTPUT_FILE_NAME)

BLOCK_SIZE = 3


def process_image_to_color_register(input_path, output_path, block_size=3):
    """
    Extrahiert alle eindeutigen Farben aus dem Eingabebild unter Ausschluss 
    transparenter Pixel und speichert sie als linear angereihtes 3x3-Pixel-Register.
    """
    
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Die Datei {input_path} wurde nicht gefunden.")
        
    
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    
    img = Image.open(input_path).convert("RGBA")
    img_array = np.array(img)

    
    pixels = img_array.reshape(-1, 4)

    
    
    opaque_pixels = pixels[pixels[:, 3] > 0]

    
    rgb_pixels = opaque_pixels[:, :3]
    unique_colors = np.unique(rgb_pixels, axis=0)

    num_colors = len(unique_colors)
    if num_colors == 0:
        raise ValueError("Das Eingabebild enthält keine verwertbaren Pixeldaten.")

    
    base_register = unique_colors.reshape(1, num_colors, 3)

    
    scaled_register = np.repeat(base_register, block_size, axis=0)  
    scaled_register = np.repeat(scaled_register, block_size, axis=1) 

    
    result_img = Image.fromarray(scaled_register.astype(np.uint8), "RGB")
    result_img.save(output_path)

if __name__ == "__main__":
    process_image_to_color_register(INPUT_IMAGE_PATH, OUTPUT_IMAGE_PATH, BLOCK_SIZE)