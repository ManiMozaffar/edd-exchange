from enum import auto

from shared.enums import StrEnum

from .binance import BinanceAPI
from .proto import GatewayProtocol


class IntegrationType(StrEnum):
    BinanceAPI = auto()
    SomeOtherAPI = auto()


INTEGRATION_MAPPER: dict[IntegrationType, GatewayProtocol] = {
    IntegrationType.BinanceAPI: BinanceAPI,
}
