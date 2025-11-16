import json
from datetime import datetime

from valutatrade_hub.parser_service.config import ParserConfig
from valutatrade_hub.parser_service.updater import RatesUpdater

config = ParserConfig()

def from_json(filepath):
    '''
    Загружает данные из JSON-файла.
    Если файл не найден, возвращает пустой словарь {}.
    Используйте try...except FileNotFoundError.
    '''
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return {}

def to_json(filepath, data):
    '''
    Сохраняет переданные данные в JSON-файл.
    '''
    with open(filepath, 'w') as file:
        json.dump(data, file)

def get_rates(to_currency):
    '''
    Загружает курсы валют из JSON-файла.
    Если файл не найден, возвращает пустой словарь {}.
    Используйте try...except FileNotFoundError.
    '''
    try:
        with open('data/rates.json', 'r') as file:
            loaded = json.load(file)
        data = loaded.get('pairs')
        last_date = loaded.get("last_refresh")
        d1 = datetime.now()
        last_date = datetime.strptime(last_date, '%Y-%m-%dT%H:%M:%S')
        minutes = (d1 - last_date).total_seconds() / 60
        if minutes > 5:
            global config
            updater = RatesUpdater(config)
            updater.run_update(None)
            with open('data/rates.json', 'r') as file:
                loaded = json.load(file)
            data = loaded.get('pairs')
            last_date = loaded.get("last_refresh")
        valid_keys = [key for key in data.keys() if f'_{to_currency}' in key]
        valid_courses = {key.replace(f'_{to_currency}', '') : data[key].get('rate') for key in valid_keys}
        update_dates = [str(last_date)] * len(valid_keys)
        return valid_courses, update_dates
    except FileNotFoundError:
        return {}, []