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

# More history = more training samples for the LSTM.
# (2019 gave only ~1,900 rows; 2010 gives ~4,200 for most of these stocks.)
START_DATE = "2010-01-01"

END_DATE = None

INTERVAL = "1d"

AUTO_ADJUST = True

# Retry a failed download this many times before giving up on a symbol
DOWNLOAD_RETRIES = 3
RETRY_DELAY_SECONDS = 3

# ----------------------------
# Validation Settings
# ----------------------------

# Minimum rows needed so that the LSTM can build sequences and a test set
MIN_ROWS = 300