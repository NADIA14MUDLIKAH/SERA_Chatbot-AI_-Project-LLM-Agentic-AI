import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "openai/gpt-oss-120b"
HISTORY_DIR = "history"

# ==========================================
# LLM SETTINGS (Sesuai Konsep Prompt Engineering)
# ==========================================
# Disetel rendah (0.2) dan top_p (0.9) untuk Factual Q&A
# agar model memberikan jawaban konsisten, faktual, 
# dan tidak berhalusinasi saat memberikan diagnosa.
TEMPERATURE = 0.2
TOP_P = 0.9

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY tidak ditemukan. Pastikan file .env sudah diatur.")