import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Coba gunakan python-dotenv jika tersedia, jika tidak baca file .env secara manual
env_file = BASE_DIR / ".env"
if env_file.exists():
    try:
        from dotenv import load_dotenv
        load_dotenv(env_file)
    except ImportError:
        # Simple manual fallback parser
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
BOT_NAME = os.getenv("BOT_NAME", "EduBot - Media Pembelajaran Informatika")

# Path Berkas Data & Database
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = BASE_DIR / "database" / "edubot_database.sqlite"
MATERIALS_FILE = DATA_DIR / "materials.json"
QUIZ_BANK_FILE = DATA_DIR / "quiz_bank.json"
KNOWLEDGE_BASE_FILE = DATA_DIR / "knowledge_base.json"
ASSETS_DIR = BASE_DIR / "assets"
