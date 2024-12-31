import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv("../.env")

apikey = os.getenv("ALPHAVANTAGE_API_KEY")
symbol = 'VXX'

url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={apikey}'
r = requests.get(url)
data = r.json()

print(data)


# Features to be used in the model ()
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
] # Additional features coming from API Requests
#   SPY EMA   (Exponential Moving Average)
#   SPY SMA   (Simple Moving Average)
#   SPY RSI   (Relative Strength Index)
#   SPY ADX   (Average Directional Index)
#   day of the week
#   month of the year

