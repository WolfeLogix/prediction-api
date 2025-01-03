from os import getenv

import requests
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine

# Load environment variables from .env file
load_dotenv("../.env")
apikey = getenv("ALPHAVANTAGE_API_KEY")


def get_data(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={
        symbol}&apikey={apikey}'
    r = requests.get(url, timeout=99999)
    return r.json()


def process_data(symbol, time_series_daily_data):
    """Transform the data from the API into a DataFrame"""

    # Convert the Time Series (Daily) dictionary to a DataFrame
    df = pd.DataFrame.from_dict(
        time_series_daily_data["Time Series (Daily)"],
        orient="index"
    )
    df.index.name = "date"
    df.reset_index(inplace=True)

    # Rename columns
    df.columns = ["date", "open", "high", "low", "close", "volume"]

    # Convert date column to datetime
    df["date"] = pd.to_datetime(df["date"])

    # Sort by date descending (newest to oldest)
    df = df.sort_values(by="date", ascending=False)

    # Add symbol column
    df["symbol"] = symbol

    # Create 'prev_*' columns by shifting -1
    # because the data is now sorted newest to oldest
    df["prev_open"] = df["open"].shift(-1)
    df["prev_close"] = df["close"].shift(-1)
    df["prev_high"] = df["high"].shift(-1)
    df["prev_low"] = df["low"].shift(-1)
    df["prev_volume"] = df["volume"].shift(-1)

    # Drop the last row because it has no "previous" row
    df = df.iloc[:-1]

    # Reorder columns
    df = df[
        [
            "date",
            "symbol",
            "open",
            "close",
            "high",
            "low",
            "volume",
            "prev_open",
            "prev_close",
            "prev_high",
            "prev_low",
            "prev_volume"
        ]
    ]

    return df


def get_database():
    """Get the database connection string from environment variables."""
    user = getenv("DB_USER")
    password = getenv("DB_PASSWORD")
    host = getenv("DB_HOST")
    port = getenv("DB_PORT")
    db = getenv("DB_NAME")
    conn = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    return conn


def dataframe_to_database(df, db_url):
    """
    - Renames the 'date' column to 'time' to match the DDL schema.
    - Appends the dataframe to the raw_daily_price table without dropping it.
    """
    engine = create_engine(db_url)

    df = df.rename(columns={"date": "time"})

    # Append (do not drop/replace) data
    df.to_sql("raw_daily_price", engine, if_exists="append", index=False)


# Features to be used in the model
symbols = [
    'VXX',  # Volatility
    'SPY',  # S&P 500
    'DJI',  # Dow Jones
    'QQQ',  # Nasdaq
    'RUT',  # Russell 2000
    'GLD',  # Gold
    'TIP',  # Inflation
    'TLT',  # Long-term bonds
    'VTI',  # Total stock market
    'VNQ',  # Real estate
    'UUP',  # US dollar
    'DBC',  # Commodities
    'VEA',  # Developed markets
    'VWO',  # Emerging markets
]  # Additional features coming from API Requests
#   SPY EMA   (Exponential Moving Average)
#   SPY SMA   (Simple Moving Average)
#   SPY RSI   (Relative Strength Index)
#   SPY ADX   (Average Directional Index)
#   day of the week
#   month of the year


# Load data to the database
for symbol in symbols:
    data = get_data(symbol)
    dataframe = process_data('SPY', data)
    dataframe_to_database(dataframe, get_database())
    print(f"Data for {symbol} has been loaded to the database.")
