
import json
import os
from config import STATE_FILE

def get_bakim_modu():
    if not os.path.exists(STATE_FILE):
        return False
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("bakim_modu", False)

def set_bakim_modu(durum: bool):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump({"bakim_modu": durum}, f, ensure_ascii=False, indent=2)
