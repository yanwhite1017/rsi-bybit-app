import ccxt
import pandas as pd
import configparser

# Чтение конфигурации
config = configparser.ConfigParser()
config.read("../config.ini")

api_key = config["bybit_keys"]["api_key"]
api_secret = config["bybit_keys"]["api_secret"]

# Подключение к бирже
exchange = ccxt.bybit({
    "apiKey": api_key,
    "secret": api_secret
})

# Получение данных по свечам с биржи
def fetch_candles(symbol, timeframe, limit):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df

# Расчет RSI вручную
def calculate_rsi(df, period):
    delta = df["close"].diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()

    # Используем метод Wilder для сглаживания
    for i in range(period, len(avg_gain)):
        avg_gain.iat[i] = (avg_gain.iat[i - 1] * (period - 1) + gain.iat[i]) / period
        avg_loss.iat[i] = (avg_loss.iat[i - 1] * (period - 1) + loss.iat[i]) / period

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    df["rsi"] = rsi
    return df