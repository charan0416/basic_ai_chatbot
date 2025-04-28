# File: chatbot/config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file located in the parent directory
# Adjust path if your structure is different or .env is elsewhere
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

class Config:
    """Application configuration."""
    # Get the Bank API base URL from environment variable or use a default
    BANK_API_URL = os.getenv('BANK_API_BASE_URL', 'http://localhost:8888/api/simulated') # Fallback default

APP_CONFIG = Config()