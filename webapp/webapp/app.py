"""Consider designing this application if the code was scaling.
As of now, this is only a PROTO-TYPE
"""

from typing import Type

from fastapi import Depends, FastAPI
from shared.database.redis.impl import Redis, get_redis
from shared.entities.order import CryptoOrder, RejectedOrder, StartedOrder
from shared.event.component import AbanProducer
from shared.event.topics import ABAN_TOPICS_TYPE

_redis = get_redis(host="localhost", port=6382, db=0)


def redis():
    return _redis


def producer():
    return AbanProducer


async def start_order(order: CryptoOrder) -> StartedOrder | RejectedOrder:
    # PERFORM VALIDATION HERE
    # IF VALIDATION FAILS, GIVE BACK THE MONEY TO USER WALLET
    ...


app = FastAPI()


@app.post("/event")
async def register_event(
    data: CryptoOrder = Depends(),
    redis: Redis = Depends(redis),
    producer: Type[AbanProducer] = Depends(producer),
) -> None:
    result = await start_order(data)
    if isinstance(result, StartedOrder):
        # REDUCE MONEY
        producer.produce_message(
            redis=redis,
            topic=ABAN_TOPICS_TYPE.PROCESS_ORDER,
            message=data,
        )
    else:
        ...
        # ORDER WAS REJECTED!
