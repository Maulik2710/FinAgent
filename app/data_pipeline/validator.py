import pandas as pd

from .config import MIN_ROWS

REQUIRED_COLUMNS = [
    "Open",
    "High",
    "Low",
    "Close",
    "Volume"
]

PRICE_COLUMNS = ["Open", "High", "Low", "Close"]


def check_empty(df: pd.DataFrame) -> bool:
    """Return True if the dataframe has no rows or no columns."""
    return df is None or df.empty


def check_column(df: pd.DataFrame) -> bool:
    """Return True if all required columns are present."""
    return all(column in df.columns for column in REQUIRED_COLUMNS)


def validate_dataframe(df: pd.DataFrame, strict: bool = False) -> bool:
    """
    Validate a stock dataframe.

    strict=False : structure checks only (use on freshly downloaded data,
                   which may still contain NaNs / duplicates).
    strict=True  : also verify the data is clean (use after cleaning).
    """

    # 1. Empty check FIRST, so an empty download gives a clear message
    if check_empty(df):
        raise ValueError("Downloaded dataframe is empty.")

    # 2. Columns
    if not check_column(df):
        missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
        raise ValueError(f"Required columns are missing: {missing}")

    # 3. Enough history for the model
    if len(df) < MIN_ROWS:
        raise ValueError(
            f"Not enough rows: {len(df)} (minimum required: {MIN_ROWS})."
        )

    if strict:
        if df[REQUIRED_COLUMNS].isnull().any().any():
            raise ValueError("Data still contains missing values.")

        if (df[PRICE_COLUMNS] <= 0).any().any():
            raise ValueError("Data contains zero or negative prices.")

        if df.index.duplicated().any():
            raise ValueError("Data contains duplicate dates.")

        if not df.index.is_monotonic_increasing:
            raise ValueError("Data is not sorted by date.")

    return True