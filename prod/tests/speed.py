import time
import requests

# Актуальный эндпоинт ByBit API для получения времени
url = "https://api.bybit.com/v3/public/time"

# Функция для измерения времени отклика
def measure_latency():
    start_time = time.time()  # Засекаем время перед отправкой запроса
    response = requests.get(url)  # Отправляем GET-запрос
    end_time = time.time()  # Засекаем время после получения ответа

    if response.status_code == 200:
        latency = (end_time - start_time) * 1000  # Время отклика в миллисекундах
        print(f"Время отклика: {latency:.2f} мс")
        print(f"Ответ от сервера: {response.json()}")
    else:
        print("Ошибка соединения:", response.status_code)

# Измеряем скорость
measure_latency()
