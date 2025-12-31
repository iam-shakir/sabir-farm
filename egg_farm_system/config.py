"""
Configuration file for Egg Farm Management System
"""
import os
from pathlib import Path

# Application metadata
APP_NAME = "Egg Farm Management System"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Farm Management Team"

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "egg_farm.db"
LOGS_DIR = BASE_DIR / "logs"

# Create necessary directories
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Database
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Currency settings
BASE_CURRENCY = "AFG"
SECONDARY_CURRENCY = "USD"
DEFAULT_EXCHANGE_RATE = 78.0  # Default AFG to USD rate

# Farm settings
MAX_FARMS = 4

# UI Settings
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
SIDEBAR_WIDTH = 250

# Expense categories
EXPENSE_CATEGORIES = [
    "Labor",
    "Medicine",
    "Electricity",
    "Water",
    "Transport",
    "Miscellaneous"
]

# Feed types
FEED_TYPES = ["Starter", "Grower", "Layer"]

# Egg grades
EGG_GRADES = ["Small", "Medium", "Large", "Broken"]

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
