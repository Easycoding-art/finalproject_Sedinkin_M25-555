from valutatrade_hub.core.utils import from_json, to_json, get_rates
import random
import hashlib
from datetime import datetime
from valutatrade_hub.core.exceptions import CurrencyNotFoundError, InsufficientFundsError
from valutatrade_hub.core.currencies import CurrencyMaker
from valutatrade_hub.decorators import log_action
from valutatrade_hub.parser_service.updater import RatesUpdater
from valutatrade_hub.parser_service.config import ParserConfig
from prettytable import PrettyTable

config = ParserConfig()

def register(username, password):
    data = from_json('data/users.json')
    names = [val.get('username') for val in data]
    ids = [val.get('user_id') for val in data]
    if username in names:
        print(f'Имя пользователя {username} уже занято')
        return None
    if len(password) < 4:
        print('Пароль должен быть не короче 4 символов')
        return None
    current_id = ids.max() + 1
    symbols = list('1234567890-=+*%!?><$#@;:qwertyuiopasdfghjklzxcvbnm')
    salt = ''.join(random.choices(symbols, k=random.randint(5, 20)))
    hashed_password = hashlib.sha256(password + salt)
    current_datetime = datetime.now()
    new_user_info = {"user_id": current_id,
                     "username": username,
                     "hashed_password": hashed_password,
                     "salt": salt,
                     "registration_date": current_datetime}
    data.append(new_user_info)
    to_json('data/users.json', data)
    portfolio_info = {"user_id": current_id, "wallets": {}}
    portfolios = from_json('data/portfolios.json')
    portfolios.append(portfolio_info)
    to_json('data\portfolios.json', portfolios)
    return current_id

def login(username, password):
    data = from_json('data/users.json')
    res = [(val.get('salt'),
            val.get('hashed_password'),
            val.get('user_id'))
            for val in data if val.get('username') == username]
    if len(res) == 0:
        print(f'Пользователь {username} не найден')
        return False
    salt, hashed_password, current_id = res[0]
    if hashed_password != hashlib.sha256(password + salt):
        print('Неверный пароль')
        return False
    return current_id

def show_portfolio(logged_in, logged_id, base_currency=config.BASE_CURRENCY):
    if not logged_in:
        print('Сначала выполните login')
        return None
    portfolios = from_json('data/portfolios.json')
    portfolio = [val for val in portfolios if val.get('user_id') == logged_id][0]
    wallets = portfolio.get('wallets')
    if len(wallets.keys()) == 0:
        print('Кошельков нет')
        return None
    if base_currency != config.BASE_CURRENCY:
        print(f'Неизвестная базовая валюта {base_currency}')
        return None
    exchange_rates, _ = get_rates(base_currency)
    result = 0.0
    for key in wallets.keys():
        wallet = wallets.get(key)
        diff = wallet.get('balance') * exchange_rates.get(base_currency)
        result += diff
        print(f'- {base_currency}: {wallet.get('balance')}  → {diff} {base_currency}')
    print(f'ИТОГО: {result} {base_currency}')

@log_action
def buy(logged_id, currency, amount):
    if not logged_id:
        print('Сначала выполните login')
        return None
    if amount < 0:
        print(f'{amount} должен быть положительным числом')
        return None
    exchange_rates, _ = get_rates(config.BASE_CURRENCY)
    if currency not in exchange_rates.keys():
        print(f'Не удалось получить курс для {currency}→{config.BASE_CURRENCY}')
        return None
    portfolios = from_json('data\portfolios.json')
    portfolio_index = [i for i in range(len(portfolios)) if portfolios[i].get('user_id') == logged_id][0]
    portfolio = portfolios[portfolio_index]
    wallets = portfolio.get('wallets')
    if currency not in wallets.keys():
        wallets.update({currency: {"balance": 0.0}})
    before = wallets[currency]["balance"]
    wallets[currency]["balance"] += amount
    cost = amount * exchange_rates.get(currency)
    print(f'- {currency}: было {before} → стало {wallets[currency]["balance"]}')
    print(f'Оценочная стоимость покупки: {cost} {config.BASE_CURRENCY}')
    portfolio['wallets'].update(wallets)
    portfolios[portfolio_index] = portfolio
    to_json('data\portfolios.json', portfolios)

@log_action
def sell(logged_id, currency, amount):
    if not logged_id:
        print('Сначала выполните login')
        return None
    portfolios = from_json('data\portfolios.json')
    portfolio_index = [i for i in range(len(portfolios)) if portfolios[i].get('user_id') == logged_id][0]
    portfolio = portfolios[portfolio_index]
    wallets = portfolio.get('wallets')
    if currency not in wallets.keys():
        print(f'У вас нет кошелька {currency}. Добавьте валюту: она создаётся автоматически при первой покупке.')
        return None
    before = wallets[currency]["balance"]
    try:
        if before < amount:
            raise InsufficientFundsError(currency, before, amount)
    except InsufficientFundsError as e:
        print(e)
        return None
    exchange_rates, _ = get_rates(config.BASE_CURRENCY)
    cost = amount * exchange_rates.get(currency)
    wallets[config.BASE_CURRENCY]["balance"] += cost
    wallets[currency]["balance"] -= cost
    print(f'Продажа выполнена: {amount} {currency} по курсу {exchange_rates.get(currency)} {config.BASE_CURRENCY}/{currency}')
    print('Изменения в портфеле:')
    print(f'- {currency}: было {before} → стало {wallets[currency]["balance"]}')
    print(f'Оценочная выручка: {cost} {config.BASE_CURRENCY}')
    portfolio['wallets'].update(wallets)
    portfolios[portfolio_index] = portfolio
    to_json('data\portfolios.json', portfolios)

def get_rate(curr_from, curr_to):
    cm = CurrencyMaker()
    try:
        a = cm.get_currency(curr_from)
        b = cm.get_currency(curr_to)
    except CurrencyNotFoundError as e:
        print(e)
        currs = ', '.join(cm.get_currency_list())
        print(f'Список доступных валют: {currs}')
        return None
    exchange_rates, update_dates = get_rates(curr_to)
    exchange_rates_2, _ = get_rates(curr_from)
    if len(exchange_rates.keys()) == 0:
        print(f'Курс {curr_from}→{curr_to} недоступен. Повторите попытку позже.')
        return None
    date = update_dates[exchange_rates.keys().index(curr_from)]
    print(f'Курс {curr_from}→{curr_to}: {exchange_rates.get(curr_from)} (обновлено: {date})')
    print(f'Обратный курс {curr_to}→{curr_from}: {exchange_rates_2.get(curr_to)}')

def update_rates(source):
    sources = [source] if source else None
    try:
        updater = RatesUpdater(config)
        count = updater.run_update(sources)
        last_refresh = datetime.now()
        if count > 0:
            print(
                f"Update successful. Total rates updated: {count}. Last refresh: {last_refresh}"
            )
        else:
            print("Update completed with errors. Check logs/parser.log for details.")
    except Exception as e:
        print(f"Update failed. Error: {e}. Check logs/parser.log for details.")

def show_rates(currency, top, base):
    base = config.BASE_CURRENCY if base == None else base
    rates_data = from_json("data/rates.json")
    if (
        isinstance(rates_data, list)
        or not rates_data
        or "pairs" not in rates_data
        or not rates_data["pairs"]
    ):
        raise FileNotFoundError("Кеш пуст")
    pairs = rates_data["pairs"]
    last_update = rates_data.get("last_refresh", "unknown")
    print(f"Rates from cache (updated at {last_update}):")
    table = PrettyTable(["Pair", "Rate"])
    base_usd_pair = f"{base}_USD"
    base_usd_rate = pairs.get(
        base_usd_pair, {}
    ).get("rate", 1.0) if base != "USD" else 1.0

    if currency:
        cur_pair = f"{currency.upper()}_{base}"
        cur_usd_pair = f"{currency.upper()}_USD"
        cur_usd_rate = pairs.get(cur_usd_pair, {}).get("rate", 0)
        cur_base_rate = (
            cur_usd_rate / base_usd_rate
            if base != "USD" else cur_usd_rate
        )
        if cur_usd_rate == 0:
            print(f"Курс для '{currency}' не найден в кеше.")
        else:
            table.add_row([cur_pair, f"{cur_base_rate:.5f}"])
            print(table)

    if top:
        top_n = int(top)
        crypto_usd = {
            k: v for k, v in pairs.items()
            if k.split("_")[0] in config.CRYPTO_CURRENCIES
        }
        sorted_crypto = sorted(
            crypto_usd.items(),
            key=lambda x: x[1]["rate"] / base_usd_rate,
            reverse=True,
        )[:top_n]
        for pair_usd, p in sorted_crypto:
            code = pair_usd.split("_")[0]
            rate_base = (
                p["rate"] / base_usd_rate
                if base != "USD" else p["rate"]
            )
            table.add_row([f"{code}_{base}", f"{rate_base:.2f}"])
        print(table)

    for pair_usd, p in sorted(pairs.items()):
        code = pair_usd.split("_")[0]
        rate_usd = p["rate"]
        rate_base = (
            rate_usd / base_usd_rate
            if base != "USD" else rate_usd
        )
        pair_base = f"{code}_{base}"
        table.add_row([pair_base, f"{rate_base:.5f}"])
    print(table)
    