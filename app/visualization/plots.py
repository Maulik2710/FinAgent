import matplotlib.pyplot as plt
import pandas as pd


def plot_closing_price(df: pd.DataFrame):

    plt.figure(figsize=(15,6))
    plt.plot(df.index, df["Close"])
    plt.title("Closing Price")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid(True)
    plt.show()


def plot_volume(df: pd.DataFrame):

    plt.figure(figsize=(15,5))
    plt.plot(df.index, df["Volume"])
    plt.title("Trading Volume")
    plt.xlabel("Date")
    plt.ylabel("Volume")
    plt.grid(True)
    plt.show()


def plot_histogram(df: pd.DataFrame):

    plt.figure(figsize=(8,5))
    plt.hist(df["Close"], bins=30)
    plt.title("Closing Price Distribution")
    plt.xlabel("Price")
    plt.ylabel("Frequency")
    plt.show()


def plot_boxplot(df: pd.DataFrame):

    plt.figure(figsize=(6,5))
    plt.boxplot(df["Close"])
    plt.title("Closing Price Boxplot")
    plt.show()


def plot_daily_returns(df: pd.DataFrame):

    plt.figure(figsize=(15,5))
    plt.plot(df.index, df["Daily_Return"])
    plt.title("Daily Returns")
    plt.grid(True)
    plt.show()


def plot_moving_average(df: pd.DataFrame,
                        window: int = 20):

    column = f"SMA_{window}"

    plt.figure(figsize=(15,6))
    plt.plot(df.index, df["Close"], label="Close")
    plt.plot(df.index,
             df[column],
             label=column)
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_rolling_volatility(df: pd.DataFrame):

    plt.figure(figsize=(15,5))
    plt.plot(df.index,
             df["Rolling_Volatility"])
    plt.title("Rolling Volatility")
    plt.grid(True)
    plt.show()