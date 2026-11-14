import numpy as np
import pandas as pd

# EMA / MACD need time to "warm up" (they start from the first price), so the
# first rows are unreliable. These rows are dropped after all indicators are built.
WARMUP_ROWS = 50

REQUIRED_COLUMNS = ["Close", "Volume"]


def _require(df: pd.DataFrame, columns: list) -> None:
    missing = [c for c in columns if c not in df.columns]
    if missing:
        raise ValueError(f"Missing column(s): {missing}")


def add_daily_return(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add Daily Percentage Return.
    """
    _require(df, ["Close"])
    df = df.copy()
    df["Daily_Return"] = df["Close"].pct_change(fill_method=None)
    return df


def add_sma(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    """
    Add Simple Moving Average.
    """
    _require(df, ["Close"])
    df = df.copy()
    df[f"SMA_{window}"] = df["Close"].rolling(window).mean()
    return df


def add_ema(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    """
    Add Exponential Moving Average.
    """
    _require(df, ["Close"])
    df = df.copy()
    df[f"EMA_{window}"] = df["Close"].ewm(span=window, adjust=False).mean()
    return df


def add_rsi(df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
    """
    Add Relative Strength Index (Wilder's smoothing, the standard definition).

    RSI > 70 -> potentially overbought, RSI < 30 -> potentially oversold.
    """
    _require(df, ["Close"])
    df = df.copy()

    delta = df["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(alpha=1 / window, min_periods=window, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / window, min_periods=window, adjust=False).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    # Edge cases: no losses at all -> 100, no movement at all -> 50
    rsi = rsi.where(avg_loss != 0, 100.0)
    rsi = rsi.where(~((avg_gain == 0) & (avg_loss == 0)), 50.0)

    df[f"RSI_{window}"] = rsi
    return df


def add_macd(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add MACD, its signal line, and price-normalized versions of both
    (dividing by Close makes them comparable across years and stocks).
    """
    _require(df, ["Close"])
    df = df.copy()

    ema12 = df["Close"].ewm(span=12, adjust=False).mean()
    ema26 = df["Close"].ewm(span=26, adjust=False).mean()

    df["MACD"] = ema12 - ema26
    df["MACD_Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()

    df["MACD_Norm"] = df["MACD"] / df["Close"]
    df["MACD_Signal_Norm"] = df["MACD_Signal"] / df["Close"]

    return df


def add_rolling_volatility(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    """
    Add rolling volatility (std of daily returns).
    """
    if "Daily_Return" not in df.columns:
        df = add_daily_return(df)

    df = df.copy()
    df["Rolling_Volatility"] = df["Daily_Return"].rolling(window).std()
    return df


def add_price_ratios(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add Close relative to its moving averages (stationary versions of
    SMA_20 / EMA_20: they stay in a similar range even when the price trends).
    """
    _require(df, ["Close", "SMA_20", "EMA_20"])
    df = df.copy()
    df["Close_SMA_Ratio"] = df["Close"] / df["SMA_20"] - 1
    df["Close_EMA_Ratio"] = df["Close"] / df["EMA_20"] - 1
    return df


def add_volume_change(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add day-over-day log change in volume (raw volume is not stationary).
    """
    _require(df, ["Volume"])
    df = df.copy()
    volume = df["Volume"].replace(0, np.nan)
    df["Volume_Change"] = np.log(volume).diff()
    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add all technical indicators.

    The data must be sorted oldest -> newest. Every indicator only uses
    past/current rows, so there is no look-ahead leakage.
    """
    _require(df, REQUIRED_COLUMNS)

    if df.empty:
        raise ValueError("Cannot engineer features on an empty dataframe.")

    df = add_daily_return(df)
    df = add_sma(df)
    df = add_ema(df)
    df = add_rsi(df)
    df = add_macd(df)
    df = add_rolling_volatility(df)
    df = add_price_ratios(df)
    df = add_volume_change(df)

    df = df.replace([np.inf, -np.inf], np.nan)

    # Drop the unreliable warm-up period, then any remaining NaN rows
    df = df.iloc[WARMUP_ROWS:]
    df = df.dropna().reset_index(drop=True)

    if df.empty:
        raise ValueError(
            "No rows left after feature engineering "
            f"(need more than {WARMUP_ROWS + 20} rows of input)."
        )

    return df