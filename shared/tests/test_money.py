from decimal import Decimal

import pytest

from shared.entities.money import EURO, USD, CurrencySymbol, ExchangeNotDefinedException


def test_create_usd():
    usd = USD(5)
    assert usd.amount == Decimal(5)
    assert usd.symbol == CurrencySymbol.USD


def test_create_euro():
    euro = EURO(7)
    assert euro.amount == Decimal(7)
    assert euro.symbol == CurrencySymbol.EURO


def test_convert_euro_to_usd():
    euro = EURO(7)
    converted = euro.to(USD)
    assert converted
    # TODO: convert to EURO here manually and check if it works. mock converter before that


def test_nested_conversion():
    usd = USD(5)
    converted = usd.to(EURO).to(USD)
    assert converted.amount == pytest.approx(Decimal(5), Decimal(0.001))
    assert converted.symbol == CurrencySymbol.USD


def test_invalid_conversion():
    with pytest.raises(ExchangeNotDefinedException):
        usd = USD(5)
        usd.to(int)
