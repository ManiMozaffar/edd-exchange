from enum import auto
from typing import Type

from shared.enums import StrEnum

from .aban import AbanCrypto
from .abc import AbstractCrypto
from .tether import TetherCrypto


class ECurrenciesType(StrEnum):
    TETHER = auto()
    ABAN = auto()


CRYPTO_MAPPER: dict[ECurrenciesType, Type[AbstractCrypto]] = {
    ECurrenciesType.TETHER: AbanCrypto,
    ECurrenciesType.TETHER: TetherCrypto,
}
