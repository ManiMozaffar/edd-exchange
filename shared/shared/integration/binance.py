from typing import Type

from shared.crypto import AbstractCrypto
from shared.entities.money import USD, Currency


class BinanceAPI:
    def get_minimum_currency(self) -> USD:
        return USD(10)

    def buy_crypto(
        money_amount: Currency,
        crypto: AbstractCrypto,
    ) -> AbstractCrypto:
        """Implement the logic here, call binance API to actually buy the currency"""
        return crypto.get_units_from_price(money_amount)

    def sell_crypto(
        currency_type: Type[Currency],
        crypto: AbstractCrypto,
    ) -> Currency:
        """Implement the logic here, call binance API to actually sell the currency"""
        return crypto.get_price_from_units(currency_type)
