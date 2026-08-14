import re
from pathlib import Path

def parse_error_log(log_path: Path):
    errors = {}
    pattern = re.compile(r"prov\s+(\d+)\s+stack\s+(\d+)")
    if not log_path.exists():
        print(f"[Error] Log file not found: {log_path}")
        return errors
    
    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            match = pattern.search(line)
            if match:
                prov_id = int(match.group(1))
                stack_idx = int(match.group(2))
                errors.setdefault(prov_id, set()).add(stack_idx)
                
    return errors

def fix_unitstacks(unitstacks_path: Path, errors: dict):
    if not unitstacks_path.exists():
        print(f"[Error] {unitstacks_path} not found.")
        return

    with open(unitstacks_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    province_templates = {}
    existing_entries = set()
    parsed_lines = []

    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith('
            parsed_lines.append((None, line))
            continue
        
        parts = stripped.split(';')
        if len(parts) >= 7:
            try:
                p_id = int(parts[0])
                s_idx = int(parts[1])
                existing_entries.add((p_id, s_idx))
                if p_id not in province_templates:
                    province_templates[p_id] = parts[2:]  
                parsed_lines.append(('entry', line))
            except ValueError:
                parsed_lines.append((None, line))
        else:
            parsed_lines.append((None, line))

    new_lines = [item[1] for item in parsed_lines]
    added_count = 0

    for prov_id, missing_indices in errors.items():
        template = province_templates.get(prov_id, ["0.00", "9.70", "0.00", "0.00", "0.20"])
        for idx in sorted(missing_indices):
            if (prov_id, idx) not in existing_entries:
                new_line = f"{prov_id};{idx};" + ";".join(template) + "\n"
                new_lines.append(new_line)
                existing_entries.add((prov_id, idx))
                added_count += 1

    with open(unitstacks_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print(f"[Success] Added {added_count} missing stack entries in CSV semicolon format to unitstacks.txt.")

if __name__ == "__main__":
    error_log_path = Path(r"C:\Users\Leegende\Documents\Paradox Interactive\Hearts of Iron IV\logs\error.log")
    unitstacks_path = Path("map/unitstacks.txt")
    
    error_map = parse_error_log(error_log_path)
    fix_unitstacks(unitstacks_path, error_map)