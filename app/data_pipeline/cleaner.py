import pandas as pd


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates()

def sort_by_date(df: pd.DataFrame) -> pd.DataFrame:
    return df.sort_index()

def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    df = df.ffill()
    df = df.bfill()
    return df

def convert_datatypes(df: pd.DataFrame) -> pd.DataFrame:
    numeric_columns = [
        "Open",
        "High",
        "Low",
        "Close",
        "Volume"
    ]
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column])
    
    return df


def clean_stock_data(df: pd.DataFrame):
    df = sort_by_date(df)
    df = convert_datatypes(df)
    df = handle_missing_values(df)
    df = remove_duplicates(df)

    return df

