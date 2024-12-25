import ccxt
import pandas as pd
import numpy as np

# Создание экземпляра ByBit API через CCXT
exchange = ccxt.bybit({
    "apiKey": "q7KB41OFuQriCb5c58",
    "secret": "ifLF49bc4ZR1o7UmtSrT18LHLqY1oonWE0uY"
})

# Параметры
symbol = "ETHUSDT"  # Инструмент
timeframe = "15m"     # Таймфрейм (например, 1 час)
limit = 200          # Количество свечей для анализа
rsi_period = 14      # Период RSI

# Получение исторических данных
def fetch_candles(symbol, timeframe, limit):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df

# Вычисление RSI
def calculate_rsi(df, period):
    delta = df["close"].diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    df["rsi"] = rsi
    return df

# Получение и расчет RSI
df = fetch_candles(symbol, timeframe, limit)
df = calculate_rsi(df, rsi_period)

# Вывод последних значений RSI
last_values = df[["timestamp", "close", "rsi"]].tail()
result_rsi = last_values.to_dict()
print(result_rsi)