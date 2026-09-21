import json
import os
from datetime import datetime
from src.config import HISTORY_DIR

def save_history_to_file(messages: list) -> str:
    if not os.path.exists(HISTORY_DIR):
        os.makedirs(HISTORY_DIR)
        
    filename = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = os.path.join(HISTORY_DIR, filename)
    
    chat_only = [msg for msg in messages if msg["role"] != "system"]
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(chat_only, f, indent=4)
        
    return filepath