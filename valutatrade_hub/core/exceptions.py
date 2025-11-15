class CurrencyNotFoundError(Exception):
    """
    Исключение, возникающее при попытке получить неизвестную валюту.
    Выбрасывается в currencies.get_currency() и при валидации входа в get-rate
    """
    def __init__(self, code: str):
        self.code = code
        super().__init__(f"Неизвестная валюта '{code}")

class InsufficientFundsError(Exception):
    """
    Недостаточно средств.
    Выбрасывается в Wallet.withdraw() и/или в usecases.sell()
    """
    def __init__(self, code, available, required):
        self.code = code
        super().__init__(f"Недостаточно средств: доступно {available} {code}, требуется {required} {code}")

class ApiRequestError(Exception):
    """
    Сбой внешнего API.
    Выбрасывается в слое получения курсов (заглушка/Parser Service).
    """
    def __init__(self, reason: str):
        self.code = reason
        super().__init__(f"Ошибка при обращении к внешнему API: {reason}")