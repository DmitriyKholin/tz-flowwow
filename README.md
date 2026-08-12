# Exchange Rates Fetcher

Простой Python-скрипт (без ООП, только функции), который:

1. Получает список валют и их курсы к доллару США с открытого API
   [ExchangeRate-API](https://www.exchangerate-api.com/)
   (эндпоинт без ключа: `https://open.er-api.com/v6/latest/USD`).
2. Делает бэкап сырого ответа в формате JSON (`output/backup_<timestamp>.json`).
3. Парсит данные в `pandas.DataFrame` с колонками:
   - `Currency` — код валюты (ISO 4217, напр. EUR, GBP, JPY)
   - `Rate_to_USD` — курс валюты к 1 USD
4. Сохраняет результат в `output/exchange_rates.csv` и `output/exchange_rates.xlsx`.
5. Ведёт логирование в консоль и в файл `exchange_rates.log`.

## Стек
- Python 3.11+
- requests
- pandas
- openpyxl (движок записи xlsx)

## Установка и запуск (локально)

```bash
# 1. Клонировать репозиторий
git clone https://github.com/<username>/exchange-rates-fetcher.git
cd exchange-rates-fetcher

# 2. (Рекомендуется) создать виртуальное окружение
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Запустить скрипт
python exchange_rates.py
