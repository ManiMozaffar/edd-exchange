from enum import auto

from shared.entities.order import StartedOrder
from shared.enums import StrEnum


class ABAN_TOPICS_TYPE(StrEnum):
    PROCESS_ORDER = auto()


ABAN_TOPICS = {
    ABAN_TOPICS_TYPE.PROCESS_ORDER: StartedOrder,
}
