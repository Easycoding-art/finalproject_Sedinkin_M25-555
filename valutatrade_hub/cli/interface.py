import shlex
import prompt
from valutatrade_hub.core.usecases import register, login, show_portfolio, sell, buy, get_rate, update_rates, show_rates

def print_help():
    print('Регистрация пользователя: register --username <str> --password <str>')
    print('Авторизация пользователя: login --username <str> --password <str>')
    print('Показать портфолио пользователя в базовой валюте: show-portfolio')
    print('Показать портфолио пользователя в кастомной валюте: show-portfolio --base <str>')
    print('Купить валюту: buy --currency <str> --amount <float>')
    print('Продать валюту: sell --currency <str> --amount <float>')
    print('Получить текущий курс: get-rate --from <str> --to <str>')
    print('Получить актуальные курсы валют: update-rates')
    print('Показать список актуальных курсов: show-rates')
    print('Показать N самых дорогих валют: show-rates --top <int>')
    print('Показать курс конкретной валюты: show-rates --currency <str>')

logged_in = False
logged_id = None

def run():
    print_help()
    global logged_in
    global logged_id
    while True:
        query = prompt.string('Введите команду: ')
        args = shlex.split(query)
        match args[0]:
            case 'register':
                id = register(args[2], args[4])
                if id is not None:
                    print(f'Пользователь {args[2]} зарегистрирован (id={id}). Войдите: login --username {args[2]} --password {'*' * len(args[4])}')
            case 'login':
                logged_id = login(args[2], args[4])
                if logged_id is not None:
                    logged_in = True
                if logged_in:
                    print(f'Вы вошли как {args[2]}')
            case 'show-portfolio':
                base_currency = args[2] if len(args) == 3 else None
                show_portfolio(logged_in, logged_id, base_currency=base_currency)
            case 'buy':
                buy(logged_id, args[2], args[4])
            case 'sell':
                sell(logged_id, args[2], args[4])
            case 'get-rate':
                get_rate(args[2], args[4])
            case 'update-rates':
                sourse = args[2] if len(args) == 3 else None
                update_rates(sourse)
            case 'show-rates':
                if '--currency' in args and '--top' not in args:
                    currency = args[args.index('--currency') + 1]
                    top = None
                elif '--currency' not in args and '--top' in args:
                    top = args[args.index('--top') + 1]
                    currency = None
                if '--base' in args:
                    currency = args[args.index('--base') + 1]
                else:
                    base = None

                show_rates(currency, top, base)
            case 'exit':
                break
            case 'help':
                print_help()
            case _:
                print(f'Функции {args[0]} нет. Попробуйте снова.')