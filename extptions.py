class BaseError(Exception):
    message = 'error'


class AmountNotIntError(BaseError):
    message = "Некорректная команда"
