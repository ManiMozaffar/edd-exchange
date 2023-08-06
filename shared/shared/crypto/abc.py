from abc import ABC, abstractmethod, abstractproperty
from decimal import Decimal
from typing import Type

from shared.entities.money import Currency


class AbstractCrypto(ABC):
    @abstractmethod
    def get_price_from_units(self, currency: Type[Currency]) -> Currency:
        """Call an API to get price for a unit of e-currency."""
        ...

    @abstractmethod
    def get_units_from_price(self, currency: Currency) -> "AbstractCrypto":
        """Call an API to get the purchasable units for a currency."""
        ...

    @abstractmethod
    def get_rate_from_usd(self) -> Decimal:
        ...

    @abstractproperty
    def amount(self) -> Decimal:
        ...
