# My database

Консольная СУБД, осень 2025 года

---

## Содержание

- [Описание](#-описание)
- [Установка и запуск](#-установка-и-запуск)
- [Управление таблицами](#-управление-таблицами)

---

## Описание

Этот проект демонстрирует владение ООП в Python.

---

## Установка и запуск

Проект использует [Poetry](https://python-poetry.org/) для управления зависимостями и виртуальным окружением.

### Требования
- Python ≥ 3.12
- Poetry ≥ 2.2

### Шаги

1. **Клонируйте репозиторий**
   ```bash
   git clone https://github.com/Easycoding-art/project-2_Sedinkin_M25-555.git
   ```

2. **Установите зависимости**
   ```bash
   poetry install
   ```

3. **Активируйте виртуальное окружение и запустите игру**
   ```bash
   make install
   make package-install
   make build
   make project
   ```

---

## Управление таблицами
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
   
   ```