from datetime import datetime
from config.settings import MOCK_OUTPUT_FILE

def send_raw(raw_data: str):
    with open(MOCK_OUTPUT_FILE, "w", encoding="ascii") as f:
        f.write("=== MOCK PRINTER OUTPUT ===\n")
        f.write(f"Timestamp: {datetime.now()}\n\n")
        f.write(raw_data)

    print("[MOCK PRINTER] Data written to", MOCK_OUTPUT_FILE)
