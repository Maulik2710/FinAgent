import pandas as pd

PRICE_COLUMNS = ["Open", "High", "Low", "Close"]
NUMERIC_COLUMNS = PRICE_COLUMNS + ["Volume"]


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate DATES (not duplicate values) and keep the last one."""
    return df[~df.index.duplicated(keep="last")]


def sort_by_date(df: pd.DataFrame) -> pd.DataFrame:
    return df.sort_index()


def convert_datatypes(df: pd.DataFrame) -> pd.DataFrame:
    """Convert OHLCV columns to numbers; bad values become NaN."""
    df = df.copy()
    for column in NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce")
    return df


def remove_invalid_prices(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drop rows with missing / zero / negative prices.

    A missing price day is dropped instead of forward-filled, because a
    filled price would create a fake 0% return day for the model.
    """
    valid = df[PRICE_COLUMNS].notna().all(axis=1) & (df[PRICE_COLUMNS] > 0).all(axis=1)
    return df[valid]


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Forward-fill the remaining gaps (e.g. a missing Volume).

    No backward-fill: that would copy FUTURE values into the past
    (look-ahead leakage). Leading rows that cannot be filled are dropped.
    """
    df = df.ffill()
    df = df.dropna()
    return df


def clean_stock_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Make sure the index is a proper DatetimeIndex
    df.index = pd.to_datetime(df.index)

    # Keep only the OHLCV columns
    df = df[NUMERIC_COLUMNS]

    df = remove_duplicates(df)
    df = sort_by_date(df)
    df = convert_datatypes(df)
    df = remove_invalid_prices(df)
    df = handle_missing_values(df)

    # Downstream code (feature engineering, API) expects a "Date" column
    df.index.name = "Date"

    return df