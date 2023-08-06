from shared.crypto import CRYPTO_MAPPER
from shared.database.redis.impl import get_redis
from shared.entities.money import USD
from shared.entities.order import OrderActionType, ShippedOrder, StartedOrder
from shared.event.component import AbanConsumer
from shared.event.topics import ABAN_TOPICS_TYPE
from shared.integration import INTEGRATION_MAPPER

from .settings import setting


def finish_order(order: StartedOrder) -> ShippedOrder:
    # if it was sale, then ADD earned_usd TO USER BALANCE IN WEBSITE
    api_integration = INTEGRATION_MAPPER.get(order.gateway)
    user_balance = USD(order.user_balance)
    crypto_cls_impl = CRYPTO_MAPPER.get(order.crypto_type)
    crypto = crypto_cls_impl(amount=order.crypto_amount)
    if order.action == OrderActionType.BUY_CRYPTO:
        earned_crypto = api_integration.buy_crypto(
            money_amount=user_balance,
            crypto=crypto,
        )
        crypto_amount = order.crypto_amount + earned_crypto.amount
        return ShippedOrder(
            **order.model_dump(exclude=["crypto_amount"]),
            crypto_amount=crypto_amount,
        )

    elif order.action == OrderActionType.SELL_CRYPTO:
        earned_usd = api_integration.sell_crypto(
            currency_type=USD,
            crypto=crypto,
        )
        user_balance = order.user_balance + earned_usd.amount
        return ShippedOrder(
            **order.model_dump(exclude=["user_balance"]),
            user_balance=user_balance,
        )


class ExchangeConsumer(AbanConsumer):
    def process_message(self, message_data: StartedOrder):
        """
        Implement logic to process an order
        """
        result = finish_order(order=message_data)
        # NOW save the result into database


consumer = ExchangeConsumer(
    redis=get_redis(
        host=setting.redis_host,
        port=setting.redis_port,
        db=setting.redis_db,
    ),
    group_name=setting.GROUP_NAME,
)
consumer.consume_message(topic=ABAN_TOPICS_TYPE.PROCESS_ORDER)
