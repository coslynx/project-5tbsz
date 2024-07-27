import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_TYPE = os.getenv("DATABASE_TYPE")
DATABASE_NAME = os.getenv("DATABASE_NAME", None)
DATABASE_USER = os.getenv("DATABASE_USER", None)
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", None)
DATABASE_HOST = os.getenv("DATABASE_HOST", None)
DATABASE_PORT = int(os.getenv("DATABASE_PORT", 5432))