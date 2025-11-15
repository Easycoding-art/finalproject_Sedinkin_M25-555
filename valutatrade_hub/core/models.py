import hashlib


class User():
    '''
    Пример хранения в JSON (users.json):
    [
    {
    "user_id": 1,
    "username": "alice",
    "hashed_password": "3e2a19...",
    "salt": "x5T9!",
    "registration_date": "2025-10-09T12:00:00"
    }
    ]
    '''  
    def __init__(self, user_id, username, password, salt, date):
        self.__user_id = user_id
        self.__username = username
        self.__hashed_password = password
        self.__salt = salt
        self.__registration_date = date
    
    @property
    def username(self):
        return self.__username
    
    @property.setter
    def set_username(self, name):
        if name != '':
            self.__username = name
    
    @property
    def user_id(self):
        return self.__user_id
    
    @property.setter
    def set_user_id(self, id):
        self.__user_id = id
    
    @property
    def registration_date(self):
        return self.__registration_date
       
    def get_user_info(self):
        '''
        выводит информацию о пользователе (без пароля).
        '''
        print(f'Name: {self.__username}')
        print(f'ID: {self.__user_id}')
        print(f'Registration date: {self.__registration_date}')
    
    def change_password(self, new_password: str):
        '''
        изменяет пароль пользователя, с хешированием нового пароля
        '''
        if len(new_password) >= 4:
            self.__hashed_password = hashlib.sha256(new_password + self.__salt)
    
    def verify_password(self, password: str):
        '''
        проверяет введённый пароль на совпадение.
        '''
        return self.__hashed_password == hashlib.sha256(password + self.__salt)
    
class Wallet():
    '''
    Пример хранения в JSON (в составе портфеля):
    {
    "BTC": {"currency_code": "BTC", "balance": 0.05},
    "USD": {"currency_code": "USD", "balance": 1200.0}
    }  
    '''
    def __init__(self, currency_code):
        self.currency_code = currency_code
        self.__balance = 0.0
    
    @property
    def balance(self):
        return self.__balance
    
    @property.setter
    def get_balance(self, value):
        if isinstance(float, value) and value >= 0:
            self.__balance = value

    def deposit(self, amount: float):
        '''
        пополнение баланса.
        '''
        self.__balance += amount
    
    def withdraw(self, amount: float):
        '''
        снятие средств (если баланс позволяет).
        '''
        if self.__balance >= amount:
            self.__balance -= amount
    
    def get_balance_info(self):
        '''
        вывод информации о текущем балансе.
        '''
        print(f'Баланс: {self.__balance} {self.currency_code}')

class Portfolio():
    '''
    При покупке валюты сумма списывается с USD-кошелька.
    При продаже — сумма начисляется на USD-кошелёк.
    Пример хранения в JSON (portfolios.json):

    [
    {
    "user_id": 1,
    "wallets": {
    "USD": {"balance": 1500.0},
    "BTC": {"balance": 0.05},
    "EUR": {"balance": 200.0}
    }
    }
    ] 
    '''
    def __init__(self, user_id, wallets):
        self.__user_id = user_id
        self.__wallets = wallets
    
    def add_currency(self, currency_code: str):
        '''
        добавляет новый кошелёк в портфель (если его ещё нет)
        '''
        if currency_code not in self.__wallets.keys():
            self.__wallets[currency_code] =  Wallet(currency_code)

    def get_total_value(self, base_currency='USD'):
        '''
        возвращает общую стоимость всех валют пользователя в указанной базовой валюте (по курсам, полученным из API или фиктивным данным)
        '''
        exchange_rates = {'RUB' : 70.0, 'EU' : 1.5}
        result = 0.0
        for key in self.__wallets.keys():
            wallet = self.__wallets.get(key)
            result += wallet.balance * exchange_rates.get(base_currency)
        return result

    def get_wallet(self, currency_code):
        '''
        возвращает объект Wallet по коду валюты.
        '''
        return self.__wallets.get(currency_code)

    @property
    def user(self):
        return User(self.__user_id)
    
    @property
    def wallets(self):
        return self.__wallets.copy()
    