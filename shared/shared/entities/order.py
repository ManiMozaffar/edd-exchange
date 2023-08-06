from decimal import Decimal
from enum import auto

from pydantic import BaseModel, validator
from shared.crypto import CRYPTO_MAPPER, ECurrenciesType
from shared.enums import StrEnum
from shared.integration import INTEGRATION_MAPPER, IntegrationType

from .exceptions import CurrencyNotFound, ImplementationNotFound


class OrderActionType(StrEnum):
    BUY_CRYPTO = auto()
    SELL_CRYPTO = auto()


class OrderStatusType(StrEnum):
    PENDING = auto()
    REJECTED = auto()
    REVOKED = auto()
    STARTED = auto()
    SHIPPED = auto()


class CryptoOrder(BaseModel):
    user_id: str
    wanted_amount: Decimal
    user_balance: Decimal
    crypto_amount: Decimal
    crypto_type: ECurrenciesType
    gateway: IntegrationType
    action: OrderActionType
    status: OrderStatusType

    @validator("gateway", always=True)
    def check_gateway(cls, gateway):
        if INTEGRATION_MAPPER.get(gateway) is None:
            raise ImplementationNotFound
        return gateway

    @validator("crypto_type", always=True)
    def check_currency(cls, crypto_type):
        if CRYPTO_MAPPER.get(crypto_type) is None:
            raise CurrencyNotFound
        return crypto_type

    class Config:
        arbitrary_types_allowed = True


class StartedOrder(CryptoOrder):
    status: OrderStatusType = OrderStatusType.STARTED


class RejectedOrder(CryptoOrder):
    status: OrderStatusType = OrderStatusType.REJECTED


class ShippedOrder(CryptoOrder):
    status: OrderStatusType = OrderStatusType.SHIPPED
