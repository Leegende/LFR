import re
import os

# CONFIGURATION - EDIT THESE PATHS IF NEEDED
#-----------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
VP_FILE = "victory_points.txt"
PROVINCE_FILE = "province_definitions.txt"
OUTPUT_FILE = "modified_province_definitions.txt"
#-----------------------------------------------------

def load_victory_points():
    vp_data = {}
    try:
        vp_path = os.path.join(SCRIPT_DIR, VP_FILE)
        with open(vp_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Updated regex pattern for multi-line victory points
        pattern = re.compile(
            r'victory_points\s*=\s*\{\n\s*(\d+)\n\s*(\d+)\n\s*\}',
            re.MULTILINE
        )
        
        for match in pattern.finditer(content):
            prov_id = int(match.group(1))
            value = int(match.group(2))
            vp_data[prov_id] = value
            
        return vp_data
            
    except Exception as e:
        print(f"Error reading victory points: {str(e)}")
        input("Press Enter to exit...")
        exit()

def modify_provinces(vp_data):
    modified = []
    try:
        prov_path = os.path.join(SCRIPT_DIR, PROVINCE_FILE)
        with open(prov_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    modified.append(line)
                    continue
                
                parts = line.split(';')
                if len(parts) < 8:
                    modified.append(line)
                    continue
                
                try:
                    prov_id = int(parts[0])
                    if prov_id in vp_data:
                        value = vp_data[prov_id]
                        if value >= 40:
                            parts[6] = "dense_urban"
                        elif value >= 11:
                            parts[6] = "urban"
                        else:
                            parts[6] = "town"
                    modified.append(';'.join(parts))
                except ValueError:
                    modified.append(line)
                    
        return modified
        
    except Exception as e:
        print(f"Error processing provinces: {str(e)}")
        input("Press Enter to exit...")
        exit()

def main():
    print("HOI4 Province Terrain Updater")
    print("Loading victory points...")
    vp_data = load_victory_points()
    
    print(f"Found {len(vp_data)} victory points")
    print("Processing province definitions...")
    modified = modify_provinces(vp_data)
    
    output_path = os.path.join(SCRIPT_DIR, OUTPUT_FILE)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(modified))
    
    print(f"Success! Saved modified provinces to:\n{output_path}")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()