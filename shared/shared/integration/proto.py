"""
We are using protocol here, because an implementation of API may not support buy or sell,
We may use an API protocol that supports only buy action or sell action.
"""

from typing import Protocol, Type

from shared.crypto import AbstractCrypto
from shared.entities.money import USD, Currency


class GatewayProtocol(Protocol):
    @staticmethod
    def get_minimum_currency() -> USD:
        ...

    @staticmethod
    def buy_crypto(
        money_amount: Currency,
        crypto: AbstractCrypto,
    ) -> AbstractCrypto:
        ...

    @staticmethod
    def sell_crypto(
        currency_type: Type[Currency],
        crypto: AbstractCrypto,
    ) -> Currency:
        ...
