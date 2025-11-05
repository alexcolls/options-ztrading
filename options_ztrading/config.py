"""Configuration management using environment variables."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = Path(os.getenv("OUTPUT_DIR", PROJECT_ROOT / "data"))

# Polygon API
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
if not POLYGON_API_KEY:
    raise ValueError(
        "POLYGON_API_KEY not found in environment. "
        "Please set it in your .env file or environment variables."
    )

# Default parameters
DEFAULT_CONTRACT = os.getenv("DEFAULT_CONTRACT", "put")
DEFAULT_EXPIRATION = os.getenv("DEFAULT_EXPIRATION", "2024-01-19")
DEFAULT_LIMIT = int(os.getenv("DEFAULT_LIMIT", "250"))
MAX_WORKERS = int(os.getenv("MAX_WORKERS", "8"))

# API settings
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))
API_RETRY_COUNT = int(os.getenv("API_RETRY_COUNT", "3"))
API_RETRY_DELAY = float(os.getenv("API_RETRY_DELAY", "1"))

# Ensure data directory exists
DATA_DIR.mkdir(parents=True, exist_ok=True)
