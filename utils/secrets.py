from dotenv import load_dotenv
from pathlib import Path
import os

# Caminho ajustado para o .env dentro da pasta app
env_path = Path(__file__).resolve().parent.parent / "app" / ".env"
load_dotenv(dotenv_path=env_path)

API_CREDENTIALS = {
    "username": os.getenv("API_USER"),
    "password": os.getenv("API_PASSWORD"),
}

SCRAPER_CREDENTIALS = {
    "username": os.getenv("SCRAPER_USER"),
    "password": os.getenv("SCRAPER_PASSWORD"),
}
