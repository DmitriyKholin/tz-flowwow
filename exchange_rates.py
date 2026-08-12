import json
import logging
import os
import sys
from datetime import datetime

import pandas as pd
import requests

API_URL = "https://open.er-api.com/v6/latest/USD"
OUTPUT_DIR = "output"
REQUEST_TIMEOUT = 15  # секунд

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(message)s",
    handlers=[
        logging.FileHandler("exchange_rates.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger(__name__)


def fetch_rates(url: str) -> dict:   
    log.info("Запрос курсов валют: %s", url)
    response = requests.get(url, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()  # выбросит исключение при HTTP 4xx/5xx
    data = response.json()

    # У этого API признак успеха — поле "result": "success"
    if data.get("result") != "success":
        raise ValueError(f"API вернул ошибку: {data.get('error-type', 'unknown')}")

    log.info("Получено %d валют (база: %s)",
             len(data.get("rates", {})), data.get("base_code"))
    return data


def backup_json(data: dict, out_dir: str) -> str:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(out_dir, f"backup_{ts}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    log.info("JSON-бэкап сохранён: %s", path)
    return path


def to_dataframe(data: dict) -> pd.DataFrame:
    rates = data["rates"]
    df = pd.DataFrame(list(rates.items()), columns=["Currency", "Rate_to_USD"])
    df = df.sort_values("Currency").reset_index(drop=True)
    return df


def save_outputs(df: pd.DataFrame, out_dir: str) -> None:
    csv_path = os.path.join(out_dir, "exchange_rates.csv")
    xlsx_path = os.path.join(out_dir, "exchange_rates.xlsx")
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    df.to_excel(xlsx_path, index=False)
    log.info("Сохранено: %s", csv_path)
    log.info("Сохранено: %s", xlsx_path)


def main() -> int:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    try:
        data = fetch_rates(API_URL)
        backup_json(data, OUTPUT_DIR)
        df = to_dataframe(data)
        save_outputs(df, OUTPUT_DIR)
        log.info("Готово. Обработано %d строк.", len(df))
        return 0
    except requests.exceptions.RequestException as e:
        log.error("Ошибка сети/HTTP при обращении к API: %s", e)
    except (ValueError, KeyError) as e:
        log.error("Ошибка обработки данных: %s", e)
    except Exception as e:  # на всякий случай ловим всё остальное
        log.exception("Непредвиденная ошибка: %s", e)
    return 1


if __name__ == "__main__":
    sys.exit(main())
