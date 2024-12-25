import loader_rsi as lr
symbols = ["ETHUSDT", "BTCUSDT"]
symbol = "ETHUSDT"  # Инструмент
timeframe = "15m"     # Таймфрейм (например, 1 час)
limit = 200          # Количество свечей для анализа
rsi_period = 14      # Период RSI

run_data = []


def main(symb):
    global run_data
    for pair in symb:
        data = lr.get_data_rsi(pair, timeframe, limit, rsi_period)
        data = lr.show_data(data)
        
        run_data = data
        print(run_data)
    return data 


if __name__ == "__main__":
    main(symbols)