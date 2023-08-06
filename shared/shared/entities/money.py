from abc import ABC, abstractmethod
from decimal import Decimal
from enum import auto

from shared.enums import StrEnum
from shared.exceptions import SharedBaseException


class ExchangeNotDefinedException(SharedBaseException):
    ...


class CurrencySymbol(StrEnum):
    USD = auto()
    EURO = auto()


def get_rates() -> dict[tuple[CurrencySymbol, CurrencySymbol], Decimal]:
    return {
        (CurrencySymbol.USD, CurrencySymbol.EURO): Decimal("0.85"),
        (CurrencySymbol.EURO, CurrencySymbol.USD): 1 / Decimal("0.85"),
    }


class Currency(ABC):
    @property
    @abstractmethod
    def symbol(self) -> CurrencySymbol:
        ...

    @property
    @abstractmethod
    def amount(self) -> Decimal:
        ...

    def __init__(self, amount: float or str or Decimal):
        ...

    @abstractmethod
    def to(self, target_currency) -> "Currency":
        ...

    def __str__(self):
        return f"{self.amount} {self.symbol.value}"

    def __repr__(self):
        return f"{type(self).__name__}({self.amount})"


class BaseCurrency(Currency):
    def __init__(self, amount: float or str or Decimal):
        self._amount = Decimal(amount)

    @property
    def amount(self):
        return self._amount

    def to(self, target_currency: Currency) -> Currency:
        if Currency in target_currency.__mro__:
            rate = get_rates().get((self.symbol, target_currency.symbol))
            if rate is not None:
                return target_currency(self.amount * rate)

        raise ExchangeNotDefinedException(
            f"Conversion from {str(self)} to {str(target_currency)} not supported."
        )


class USD(BaseCurrency):
    symbol = CurrencySymbol.USD


class EURO(BaseCurrency):
    symbol = CurrencySymbol.EURO
