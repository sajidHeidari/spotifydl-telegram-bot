import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Read API keys from environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# A check to ensure all keys are loaded
if not all([TELEGRAM_TOKEN, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET]):
    # This error will be caught on startup if keys are missing
    raise ValueError("One or more essential API keys are missing from the environment.")
