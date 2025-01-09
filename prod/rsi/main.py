import time
from flask import Flask, jsonify
from concurrent.futures import ThreadPoolExecutor
import threading
import loader_rsi as lr

app = Flask(__name__)

# Список символов для обработки
symbs = [
    {'symbol': 'ETHUSDT', 'timeframe': '15m', 'limit': 1000, 'rsi_period': 14},
    {'symbol': 'BTCUSDT', 'timeframe': '15m', 'limit': 1000, 'rsi_period': 14}
]

# Локальная переменная для хранения данных
run_data = []
data_lock = threading.Lock()  # Для защиты run_data при доступе из разных потоков

# Флаг для отслеживания, запущено ли периодическое обновление
updating = False
updating_lock = threading.Lock()

def fetch_rsi(symbols):
    """
    Функция для получения и обработки данных RSI для заданных символов.
    Преобразует данные в JSON-сериализуемый формат.
    """
    local_run_data = []
    for pair in symbols:
        data = lr.get_data_rsi(pair['symbol'], pair['timeframe'], pair['limit'], pair['rsi_period'])
        data = lr.show_data(data)

        # Преобразуем данные в сериализуемый формат
        serializable_data = {
            'symbol': pair['symbol'],
            'timeframe': pair['timeframe'],
            'limit': pair['limit'],
            'rsi_period': pair['rsi_period'],
            'data': []
        }

        for key, value in data.items():
            # value is a list: [Timestamp, price, rsi]
            timestamp, price, rsi = value
            serializable_data['data'].append({
                'index': key,
                'timestamp': timestamp.isoformat(),  # Преобразуем Timestamp в строку
                'price': price,
                'rsi': rsi
            })

        local_run_data.append(serializable_data)

    with data_lock:
        global run_data
        run_data = local_run_data
    print(time.ctime(), " Data fetched successfully")

def periodic_fetch():
    """
    Функция, которая будет запускать fetch_rsi каждые 30 секунд.
    """
    while True:
        fetch_rsi(symbs)
        time.sleep(30)

@app.route('/fetch', methods=['GET'])
def fetch_rsi_endpoint():
    """
    Маршрут для запуска периодического обновления данных.
    """
    global updating
    with updating_lock:
        if not updating:
            executor = ThreadPoolExecutor(max_workers=1)
            executor.submit(periodic_fetch)
            updating = True
            return jsonify({"message": "Data fetching started, it will update every 30 seconds."}), 202
        else:
            return jsonify({"message": "Data fetching is already running."}), 200

@app.route('/data', methods=['GET'])
def get_data():
    """
    Маршрут для получения актуальных данных RSI.
    """
    with data_lock:
        if not run_data:
            return jsonify({"message": "No data available, please fetch first."}), 400
        return jsonify(run_data)

if __name__ == "__main__":
    app.run(debug=True)
