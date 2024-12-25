import fetch_rsi as fr

# Параметры
symbol = "ETHUSDT"  # Инструмент
timeframe = "15m"     # Таймфрейм (например, 1 час)
limit = 200          # Количество свечей для анализа
rsi_period = 14      # Период RSI


def get_data_rsi(symbol, timeframe, limit, period):
    df = fr.fetch_candles(symbol, timeframe, limit)
    df = fr.calculate_rsi(df, period)

    last_values = df[["timestamp", "close", "rsi"]].tail()
    result_rsi = last_values.to_dict()

    return result_rsi

def show_data(rsi):
    rsi_info = {
    key: [rsi['timestamp'][key], rsi['close'][key], rsi['rsi'][key]]
    for key in rsi['timestamp']
    }

    return rsi_info

#data = get_data_rsi(symbol, timeframe, limit, rsi_period)
#c = show_data(data)
#print(c)