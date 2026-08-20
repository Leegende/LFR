from pathlib import Path


def fix_province_counts(input_path: str, output_path: str) -> None:
  """Korrigiert die angegebene Anzahl von Provinzen (2. Spalte)

  basierend auf der tatsächlichen Anzahl der folgenden Provinz-IDs.
  """
  input_file = Path(input_path)
  output_file = Path(output_path)

  corrected_lines = []

  with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
      stripped = line.strip()
      if not stripped:
        corrected_lines.append(line)
        continue

      parts = stripped.split()
      if len(parts) < 2:
        corrected_lines.append(line)
        continue

      # Formatannahme: [Präfix/ID] [Deklarierte Anzahl] [Provinz-ID_1] ...
      declared_count = int(parts[1])
      province_ids = parts[2:]
      actual_count = len(province_ids)

      if declared_count != actual_count:
        # Korrektur: Aktualisierung des Zählwerts auf die tatsächliche ID-Anzahl
        parts[1] = str(actual_count)
        corrected_lines.append(" ".join(parts) + "\n")
      else:
        corrected_lines.append(line)

  with open(output_file, "w", encoding="utf-8") as f:
    f.writelines(corrected_lines)


if __name__ == "__main__":
  fix_province_counts("map/railways.txt", "map/railways.txt")