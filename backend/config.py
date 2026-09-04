import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Server config
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
DEBUG = os.getenv("DEBUG", "true").lower() == "true"

# TTS config
DEFAULT_VOICE = os.getenv("DEFAULT_VOICE", "en-US-AriaNeural")
DEFAULT_RATE = os.getenv("DEFAULT_RATE", "+0%")
DEFAULT_PITCH = os.getenv("DEFAULT_PITCH", "+0Hz")
DEFAULT_VOLUME = os.getenv("DEFAULT_VOLUME", "+0%")

# Chunking config
MAX_CHUNK_SIZE = int(os.getenv("MAX_CHUNK_SIZE", 5000))  # characters per chunk
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 100))

# CORS
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
