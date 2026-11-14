from pathlib import Path

# ---------------- dataset ----------------
SEQUENCE_LENGTH = 60
TRAIN_SPLIT = 0.8

# Stationary features only (no raw price levels), so the model is not
# confused by the stock trending to new highs.
FEATURE_COLUMNS = [
    "Daily_Return",
    "Close_SMA_Ratio",
    "Close_EMA_Ratio",
    "RSI_14",
    "MACD_Norm",
    "MACD_Signal_Norm",
    "Rolling_Volatility",
    "Volume_Change",
]

# Raw columns that must exist in the processed CSV
REQUIRED_RAW_COLUMNS = [
    "Close", "Volume", "Daily_Return", "SMA_20", "EMA_20",
    "RSI_14", "MACD", "MACD_Signal", "Rolling_Volatility",
]

# ---------------- model ----------------
LSTM_UNITS = 64
DROPOUT_RATE = 0.2
LEARNING_RATE = 0.001

# ---------------- training ----------------
EPOCHS = 100
BATCH_SIZE = 32
VALIDATION_SPLIT = 0.2
EARLY_STOP_PATIENCE = 10
RANDOM_SEED = 42

# ---------------- saving (one model + scaler PER symbol) ----------------
MODEL_NAME = "lstm.keras"
SCALER_NAME = "scaler.pkl"
MODEL_DIR = Path("models")


def get_paths(symbol: str):
    """Return (model_path, scaler_path) for a symbol, creating the folder."""
    folder = MODEL_DIR / symbol.upper()
    folder.mkdir(parents=True, exist_ok=True)
    return folder / MODEL_NAME, folder / SCALER_NAME
