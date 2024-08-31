import os

from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("DB_PATH")

def get_database_path() -> str:
    return DB_PATH