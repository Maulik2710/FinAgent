import pandas as pd

REQUIRED_COLUMNS = [
    "Open",
    "High",
    "Low",
    "Close",
    "Volume"
]
def check_empty(df: pd.DataFrame) -> bool:
    return df.empty

def check_column(df: pd.DataFrame) -> bool:
    return all(column in df.columns for column in REQUIRED_COLUMNS)

def validate_dataframe(df: pd.DataFrame):

    if check_empty(df):
        raise ValueError("Downloaded dataframe is empty.")

    if not check_column(df):
        raise ValueError("Required columns are missing.")

    return True
