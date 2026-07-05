from pathlib import Path

# ----------------------------
# Project Directories
# ----------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"

RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
NEWS_DATA_DIR = DATA_DIR / "news"

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
NEWS_DATA_DIR.mkdir(parents=True, exist_ok=True)

# ----------------------------
# Stocks
# ----------------------------

STOCKS = [
    "AAPL",
    "MSFT",
    "NVDA",
    "GOOGL",
    "AMZN",
    "META",
    "TSLA",
    "AMD",
    "NFLX",
    "JPM"
]

# ----------------------------
# Download Settings
# ----------------------------

START_DATE = "2019-01-01"

END_DATE = None

INTERVAL = "1d"

AUTO_ADJUST = True