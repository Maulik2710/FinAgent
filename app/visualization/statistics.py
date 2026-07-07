import pandas as pd


def get_dataset_info(df: pd.DataFrame) -> dict:
    """
    Returns basic information about the dataset.
    """
    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "column_names": list(df.columns),
        "dtypes": df.dtypes.to_dict()
    }


def get_missing_values(df: pd.DataFrame) -> pd.Series:
    """
    Returns the number of missing values in each column.
    """
    return df.isnull().sum()


def get_duplicate_count(df: pd.DataFrame) -> int:
    """
    Returns the total number of duplicate rows.
    """
    return int(df.duplicated().sum())


def get_statistical_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns descriptive statistics.
    """
    return df.describe()


def get_date_range(df: pd.DataFrame) -> tuple:
    """
    Returns the start and end date.
    """
    return df.index.min(), df.index.max()


def calculate_daily_returns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds Daily_Return column.
    """
    df = df.copy()
    df["Daily_Return"] = df["Close"].pct_change()
    return df


def calculate_moving_average(df: pd.DataFrame,
                             window: int = 20) -> pd.DataFrame:
    """
    Adds Simple Moving Average.
    """
    df = df.copy()
    df[f"SMA_{window}"] = df["Close"].rolling(window).mean()
    return df


def calculate_rolling_volatility(df: pd.DataFrame,
                                 window: int = 20) -> pd.DataFrame:
    """
    Adds Rolling Volatility.
    """
    df = calculate_daily_returns(df)

    df["Rolling_Volatility"] = (
        df["Daily_Return"]
        .rolling(window)
        .std()
    )

    return df