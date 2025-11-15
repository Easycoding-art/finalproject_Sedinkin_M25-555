import json
from datetime import datetime
from valutatrade_hub.core.exceptions import ApiRequestError
from valutatrade_hub.parser_service.updater import RatesUpdater

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
    while True:
        try:
            with open('data/rates.json', 'r') as file:
                data = json.load(file)
            valid_keys = [key for key in data.keys() if f'_{to_currency}' in key]
            valid_courses = {key.replace(f'_{to_currency}', '') : data[key].get('rate') for key in valid_keys}
            update_dates = [data[key].get('updated_at') for key in valid_keys]
            d1 = datetime.now()
            to_date = lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
            minutes = lambda x: (x - d1).total_seconds() / 60
            conditions = [minutes(to_date(date)) > 5 for date in update_dates]
            if any(conditions):
                global config
                updater = RatesUpdater(config)
                updater.run_update()
            else:
                break
        except FileNotFoundError:
            return {}, []
    return valid_courses, update_dates