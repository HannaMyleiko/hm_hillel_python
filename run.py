from typing import Any


class CurrencyError(Exception):
    pass

CACHE = []
"""
The class represents currency exchange rates based for the abstract unit: CHF
"""
class CurrencyExchange:
    rates = {
        "usd": {
            "usd": 1,
            "uah": 40,
            "eur": 0.95,
            "chf": 0.85,
            "gbp": 0.9
        },
        "chf": {
            "usd": 1.3,
            "uah": 50,
            "eur": 1.2,
            "chf": 1,
            "gbp": 1.05
        },
        "uah": {
            "usd": 0.02,
            "uah": 1,
            "eur": 0.015,
            "chf": 0.013,
            "gbp": 0.014
        },
        "eur": {
            "usd": 1.1,
            "uah": 45,
            "eur": 1,
            "chf": 0.95,
            "gbp": 0.97
        },
        "gbp": {
            "usd": 1.2,
            "uah": 47,
            "eur": 1.15,
            "chf": 0.95,
            "gbp": 1
        }
    }

    CONVERTER_BASE = "chf"

    @classmethod
    def convert(cls, value: float, from_: str, to_: str) -> "Price":
        try:
            coef = cls.rates[from_.lower()][to_.lower()]
            result = Price(value = value * coef, currency=to_.lower())
            return result
        except Exception as error:
            raise CurrencyError() from error

class Price:

    def __init__(self, value: float, currency: str):
        self.value: float = value
        self.currency: str = currency.lower()

    def __str__(self) -> str:
        return f"Price: {self.value} {self.currency}"

    def __add__(self, other: Any) -> "Price":
        if not isinstance(other, Price):
            raise ValueError("Can perform operation only with Prices objects")
        else:
            if self.currency != other.currency:
                other = self.adjust(other)
            return Price(value=self.value + other.value, currency=self.currency)

    def __sub__(self, other: Any) -> "Price":
        if not isinstance(other, Price):
            raise ValueError("Can perform operation only with Prices objects")
        else:
            if self.currency != other.currency:
                other = self.adjust(other)
            return Price(value=self.value - other.value, currency=self.currency)

    """
    Converts Price to the specified currency directly
    """
    def convert(self, to_: str) -> "Price":
        result = CurrencyExchange.convert(value=self.value, from_=self.currency, to_=to_)
        return result

    """
    Adjusts the specified Price to the current Price's currency using a middle currency (specified in CurrencyExchange.CONVERTER_BASE)
    """
    def adjust(self, other: "Price") -> "Price":
        result = other.convert(CurrencyExchange.CONVERTER_BASE).convert(self.currency)
        return result

# Test run
phone = Price(value=200, currency="usd")
tablet = Price(value=400, currency="uah")
tv = Price(value=300, currency="eur")

print(f"Phone and Tablet: {phone + tablet}")
print(f"TV and Tablet: {tv + tablet}")
print(f"Diff between TV and Phone: {tv - phone}")