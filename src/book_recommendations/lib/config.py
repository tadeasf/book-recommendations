import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
API_HOST = os.environ.get("HOST", "0.0.0.0")
API_PORT = int(os.environ.get("PORT", 6969))
API_KEY = os.environ.get("X_API_KEY")

# Database Configuration 
DB_USER = os.environ.get("POSTGRES_USER")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DB_NAME = os.environ.get("POSTGRES_DB")
DB_URL = os.environ.get("POSTGRES_URL")

# OpenAI Configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# PgAdmin Configuration
PGADMIN_EMAIL = os.environ.get("PGADMIN_EMAIL")
PGADMIN_PASSWORD = os.environ.get("PGADMIN_PASSWORD")
