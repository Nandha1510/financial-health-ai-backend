import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./financial_ai.db"
)

SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_ME_IN_PROD")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

OPENAI_MODEL = "gpt-4o"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-test-key-set-env-var")

ENCRYPTION_KEY = os.getenv(
    "ENCRYPTION_KEY",
    "this_should_be_32_bytes_long!!"
)
