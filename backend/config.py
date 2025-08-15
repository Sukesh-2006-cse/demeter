"""
Configuration constants for the agricultural AI system
"""
import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
LOCAL_MODELS_DIR = MODELS_DIR / "local"
CLOUD_MODELS_DIR = MODELS_DIR / "cloud"

# API Configuration
FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"

# Model paths
MODEL_PATHS = {
    "crop_recommendation": CLOUD_MODELS_DIR / "crop_recommendation.pkl",
    "market_price": CLOUD_MODELS_DIR / "market_price.pkl",
    "yield_model": CLOUD_MODELS_DIR / "yield_model.pkl",
    "pest_model": CLOUD_MODELS_DIR / "pest_model.onnx",
    "weather_risk": CLOUD_MODELS_DIR / "weather_risk.pkl",
    "main_mt5": LOCAL_MODELS_DIR / "main_mt5_model"
}

# API Keys (load from environment)
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
MARKET_DATA_API_KEY = os.getenv("MARKET_DATA_API_KEY")
GOOGLE_TRANSLATE_API_KEY = os.getenv("GOOGLE_TRANSLATE_API_KEY")

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///agricultural_ai.db")

# Cache Configuration
CACHE_TTL = int(os.getenv("CACHE_TTL", 3600))  # 1 hour default
ENABLE_CACHE = os.getenv("ENABLE_CACHE", "True").lower() == "true"

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "app.log")

# Model Configuration
MODEL_CONFIDENCE_THRESHOLD = float(os.getenv("MODEL_CONFIDENCE_THRESHOLD", 0.7))
MAX_IMAGE_SIZE = int(os.getenv("MAX_IMAGE_SIZE", 5 * 1024 * 1024))  # 5MB

# Supported Languages
SUPPORTED_LANGUAGES = [
    "en", "es", "fr", "pt", "hi", "zh", "ar", "sw", "am"
]

# Default language
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "en")

# Agent Configuration
AGENT_TIMEOUT = int(os.getenv("AGENT_TIMEOUT", 30))  # seconds

# Data file paths
DATA_FILES = {
    "crop_dataset": DATA_DIR / "crop_dataset.csv",
    "market_dataset": DATA_DIR / "market_dataset.csv",
    "weather_data": DATA_DIR / "weather_data.csv",
    "pest_images": DATA_DIR / "pest_images"
}

# Training Configuration
TRAINING_CONFIG = {
    "test_size": 0.2,
    "random_state": 42,
    "cross_validation_folds": 5,
    "max_epochs": 100,
    "early_stopping_patience": 10
}

# Feature flags
FEATURES = {
    "offline_mode": os.getenv("OFFLINE_MODE", "False").lower() == "true",
    "multilingual_support": os.getenv("MULTILINGUAL_SUPPORT", "True").lower() == "true",
    "image_processing": os.getenv("IMAGE_PROCESSING", "True").lower() == "true",
    "weather_integration": os.getenv("WEATHER_INTEGRATION", "True").lower() == "true"
}