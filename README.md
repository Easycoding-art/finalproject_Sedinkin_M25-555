# My database

Консольная СУБД, осень 2025 года

---

## Содержание

- [Описание](#-описание)
- [Установка и запуск](#-установка-и-запуск)
- [Управление](#-управление)

---

## Описание

Этот проект завершает курс по Python.

---

## Установка и запуск

Проект использует [Poetry](https://python-poetry.org/) для управления зависимостями и виртуальным окружением.

### Требования
- Python ≥ 3.12
- Poetry ≥ 2.2

### Шаги

1. **Клонируйте репозиторий**
   ```bash
   git clone https://github.com/Easycoding-art/finalproject_Sedinkin_M25-555.git
   ```

2. **Задать ключ доступа к бирже**
   
   В файле корневой папки с названием ```.env``` необходимо создать переменную EXCHANGERATE_API_KEY которая содержит в себе персональный API-ключ. Ключ можно получить бесплатно, пройдя регистрацию на сайте https://www.exchangerate-api.com/.

   Содержимое файла:
   ```text
   EXCHANGERATE_API_KEY=key_example
   ```

3. **Активируйте виртуальное окружение и запустите**
   ```bash
   make install
   make package-install
   make build
   make project
   ```

---

## Управление
Список команд:
   1) Регистрация пользователя: register --username <str> --password <str>
   2) Авторизация пользователя: login --username <str> --password <str>
   3) Показать портфолио пользователя в базовой валюте: show-portfolio
   4) Показать портфолио пользователя в кастомной валюте: show-portfolio --base <str>
   5) Купить валюту: buy --currency <str> --amount <float>
   6) Продать валюту: sell --currency <str> --amount <float>
   7) Получить текущий курс: get-rate --from <str> --to <str>
   8) Получить актуальные курсы валют: update-rates
   9) Показать список актуальных курсов: show-rates
   10) Показать N самых дорогих валют: show-rates --top <int>
   11) Показать курс конкретной валюты: show-rates --currency <str>

Пример работы
   ```
   make project  
   poetry run project 
   Регистрация пользователя: register --username <str> --password <str>
   Авторизация пользователя: login --username <str> --password <str>
   Показать портфолио пользователя в базовой валюте: show-portfolio
   Показать портфолио пользователя в кастомной валюте: show-portfolio --base <str>
   Купить валюту: buy --currency <str> --amount <float>
   Продать валюту: sell --currency <str> --amount <float>
   Получить текущий курс: get-rate --from <str> --to <str>
   Получить актуальные курсы валют: update-rates
   Показать список актуальных курсов: show-rates
   Показать N самых дорогих валют: show-rates --top <int>
   Показать курс конкретной валюты: show-rates --currency <str>
   Введите команду: register --username Mikhail --password qwerty
   Пользователь Mikhail зарегистрирован (id=1). Войдите: login --username Mikhail --password ******
   Введите команду: show-portfolio
   Сначала выполните login
   Введите команду: login --username Mikhail --password qwerty
   Вы вошли как Mikhail
   Введите команду: show-portfolio
   Кошельков нет
   Введите команду: buy --currency BTC --amount 100
   - BTC: было 0.0 → стало 100.0
   Оценочная стоимость покупки: 9362000.0 USD
   INFO 2025-11-17 00:10:22.941276 BUY {} result=OK
   Введите команду: show-portfolio
   - BTC: 100.0  → 9362000.0 USD
   ИТОГО: 9362000.0 USD
   Введите команду: sell --currency BTC --amount 50.5
   Продажа выполнена: 50.5 BTC по курсу 93620 USD/BTC
   Изменения в портфеле:
   - BTC: было 100.0 → стало 49.5
   Оценочная выручка: 4727810.0 USD
   INFO 2025-11-17 00:11:25.807815 SELL {} result=OK
   Введите команду: show-portfolio
   - BTC: 49.5  → 4634190.0 USD
   - USD: 4727810.0  → 4727810.0 USD
   ИТОГО: 9362000.0 USD
   Введите команду: get-rate --from BTC --to USD
   Курс BTC→USD: 93620 (обновлено: 2025-11-17 00:10:22)
   Обратный курс USD→BTC: 1.0681478316599017e-05
   Введите команду: show-rates
   Rates from cache (updated at 2025-11-17T00:10:22):
   +---------+-------------+
   |   Pair  |     Rate    |
   +---------+-------------+
   | BTC_USD | 93620.00000 |
   | ETH_USD |  3072.84000 |
   | EUR_USD |   1.16212   |
   | GBP_USD |   1.31648   |
   | RUB_USD |   0.01237   |
   | SOL_USD |  136.10000  |
   +---------+-------------+
   Введите команду: update-rates
   Update successful. Total rates updated: 6. Last refresh: 2025-11-17 00:12:59.620359
   Введите команду: show-rates
   Rates from cache (updated at 2025-11-17T00:12:59):
   +---------+-------------+
   |   Pair  |     Rate    |
   +---------+-------------+
   | BTC_USD | 93719.00000 |
   | ETH_USD |  3072.82000 |
   | EUR_USD |   1.16212   |
   | GBP_USD |   1.31648   |
   | RUB_USD |   0.01237   |
   | SOL_USD |  136.07000  |
   +---------+-------------+
   Введите команду: exit
   ```