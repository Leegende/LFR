import re
from pathlib import Path

def parse_error_log(log_path: Path):
    """Parses error.log to extract (province_id, stack_index) pairs from provincegraphics errors."""
    errors = set()
    pattern = re.compile(r"prov\s+(\d+)\s+stack\s+(\d+)")
    
    if not log_path.exists():
        print(f"[Error] Log file not found at: {log_path}")
        return errors
    
    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            match = pattern.search(line)
            if match:
                prov_id = int(match.group(1))
                stack_idx = int(match.group(2))
                errors.add((prov_id, stack_idx))
                
    print(f"[Info] Parsed {len(errors)} unique stack error entries from log.")
    return errors

def clean_unitstacks(unitstacks_path: Path, errors: set):
    """Filters out faulty stack lines from unitstacks.txt based on logged errors."""
    if not unitstacks_path.exists():
        print(f"[Error] unitstacks.txt not found at: {unitstacks_path}")
        return

    with open(unitstacks_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    new_lines = []
    removed_count = 0

    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            new_lines.append(line)
            continue
            
        parts = stripped.split(';')
        if len(parts) >= 2:
            try:
                prov_id = int(parts[0])
                stack_idx = int(parts[1])
                if (prov_id, stack_idx) in errors:
                    removed_count += 1
                    continue  # Drop the invalid/out-of-bounds stack line
            except ValueError:
                pass
                
        new_lines.append(line)

    if removed_count > 0:
        with open(unitstacks_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"[Success] Removed {removed_count} faulty stack entries from unitstacks.txt.")
    else:
        print("[Warning] No matching stack entries found to remove in unitstacks.txt.")

if __name__ == "__main__":
    error_log_path = Path(r"C:\Users\Leegende\Documents\Paradox Interactive\Hearts of Iron IV\logs\error.log")
    unitstacks_path = Path("map/unitstacks.txt")
    
    error_pairs = parse_error_log(error_log_path)
    clean_unitstacks(unitstacks_path, error_pairs)