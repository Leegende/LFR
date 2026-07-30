import re
import sys
from pathlib import Path

# Fester Standardpfad für das Hearts of Iron IV Error-Log
DEFAULT_LOG_PATH = Path(
    r"C:\Users\Leegende\Documents\Paradox Interactive\Hearts of Iron IV\logs\error.log"
)


def extract_no_pixel_provinces(log_file_path: Path) -> list[int]:
  """Parst das Clausewitz-Engine-Logfile zur Identifikation von Provinzen,

  die keine Pixelzuweisung in der provinces.bmp besitzen.

  Warum: Direkte Regex-Filterung vermeidet manuelle Analysefehler bei
  großen Log-Dateien und stellt die Vollständigkeit der IDs sicher.
  """
  if not log_file_path.is_file():
    raise FileNotFoundError(f"Log-Datei nicht gefunden: {log_file_path}")

  # Regulärer Ausdruck exakt angepasst an das Clausewitz-Logformat
  pattern = re.compile(
      r"Province\s+(\d+)\s+has\s+no\s+pixels\s+in\s+provinces\.bmp",
      re.IGNORECASE,
  )
  province_ids = set()

  # Einlesen mit Fehlerbehandlung für Encoding-Inkompatibilitäten
  with log_file_path.open("r", encoding="utf-8", errors="ignore") as file:
    for line in file:
      match = pattern.search(line)
      if match:
        province_ids.add(int(match.group(1)))

  return sorted(list(province_ids))


if __name__ == "__main__":
  try:
    provinces = extract_no_pixel_provinces(DEFAULT_LOG_PATH)
    print(f"Total Unique Provinces: {len(provinces)}")
    print(", ".join(map(str, provinces)))
  except Exception as e:
    print(f"Fehler bei der Log-Verarbeitung: {e}", file=sys.stderr)
    sys.exit(1)