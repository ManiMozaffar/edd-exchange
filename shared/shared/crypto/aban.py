from typing import Type

from shared.entities.money import USD, Currency

from .abc import AbstractCrypto


class AbanCrypto(AbstractCrypto):
    def __init__(self, amount):
        self._amount = amount

    def get_rate_from_usd(self):
        return USD(amount=4)

    def get_price_from_units(self, currency: Type[Currency] = USD) -> Currency:
        """Call an API to get the amount converted to a price"""
        usd_obj = USD(self.amount * self.get_rate_from_usd().amount)
        return usd_obj.to(currency)

    def get_units_from_price(self, currency: Currency) -> "AbanCrypto":
        usd_obj = USD(currency)
        self.amount = usd_obj.amount / self.get_rate_from_usd().amount
        return self

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, amount):
        self._amount = amount
