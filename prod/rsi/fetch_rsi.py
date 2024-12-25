import ccxt
import pandas as pd
import configparser

config = configparser.ConfigParser()
config.read("../config.ini")

api_key = config["bybit_keys"]["api_key"]
api_secret = config["bybit_keys"]["api_secret"]

exchange = ccxt.bybit({
    "apiKey": api_key,
    "secret": api_secret
})

#Получение данных по свечам с биржи
def fetch_candles(symbol, timeframe, limit):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df

def calculate_rsi(df, period):
    delta = df["close"].diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    df["rsi"] = rsi
    return df