from typing import Any


class CurrencyError(Exception):
    pass

CACHE = []
"""
The class represents currency exchange rates based for the abstract unit: CHF
"""
class CurrencyExchange:
    rates = {
        "usd": 0.9,
        "chf": 1,
        "uah": 0.03,
        "eur": 0.85,
        "gbp": 1.1
    }

    @classmethod
    def convert(cls, value: float, from_: str, to_: str) -> float:
        try:
            from_rate = cls.rates[from_]
            to_rate = cls.rates[to_]
            result = from_rate / to_rate
            return result * value
        except Exception as error:
            raise CurrencyError() from error

def auth(func):
    user_list = {
        "ann": "qwer1234",
        "admin": "admin"
    }
    def user_auth():
        global CACHE
        while (len(CACHE)==0):
            try:
                username = input("User Name: ")
                password = input("Password: ")
                if user_list[username]==password:
                    CACHE.append(username)
            except Exception:
                pass

    def wrapper(*args, **kwargs):
        user_auth()
        func(*args, **kwargs)
    return wrapper

class Price:
    @auth
    def __init__(self, value: float, currency: str):
        self.value: float = value
        self.currency: str = currency

    def __str__(self) -> str:
        return f"Price: {self.value} {self.currency}"

    def adjust(self, other: "Price") -> "Price":
        return Price(value=CurrencyExchange.convert(value=other.value, from_=other.currency,to_=self.currency), currency=self.currency)

    def __add__(self, other: Any) -> "Price":
        if not isinstance(other, Price):
            raise ValueError("Can perform operation only with Pirces objects")
        else:
            if self.currency != other.currency:
                other = self.adjust(other)
            return Price(value=self.value + other.value, currency=self.currency)

    def __sub__(self, other: Any) -> "Price":
        if not isinstance(other, Price):
            raise ValueError("Can perform operation only with Pirces objects")
        else:
            if self.currency != other.currency:
                other = self.adjust(other)
            return Price(value=self.value - other.value, currency=self.currency)

phone = Price(value=200, currency="usd")
tablet = Price(value=400, currency="uah")
tv = Price(value=300, currency="eur")

print(f"Phone and Tablet: {phone + tablet}")
print(f"TV and Tablet: {tv + tablet}")
print(f"Diff between TV and Phone: {tv - phone}")