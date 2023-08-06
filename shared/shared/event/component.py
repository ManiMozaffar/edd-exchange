from abc import ABC, abstractmethod
from typing import Type

from pydantic import BaseModel
from redis import exceptions
from shared.database.redis.abc import RedisAbstract

from .topics import ABAN_TOPICS, ABAN_TOPICS_TYPE


class AbanProducer:
    @staticmethod
    def produce_message(
        redis: RedisAbstract, topic: ABAN_TOPICS_TYPE, message: BaseModel
    ) -> str:
        return redis.xadd(str(topic), message.model_dump_json())


class AbanConsumer(ABC):
    def __init__(
        self,
        redis: RedisAbstract,
        group_name: str,
        consumer_name: str,
    ):
        self.redis = redis
        self.group_name = group_name
        self.consumer_name = consumer_name

    def register_consumer_group(self, topic: ABAN_TOPICS_TYPE):
        stream_name = str(topic)
        if not self.redis.exists(stream_name):
            self.redis.xadd(stream_name, {"dummy": "dummy"})

        try:
            self.redis.xgroup_create(
                stream_name, self.group_name, id="0", mkstream=True
            )
        except exceptions.ResponseError:
            # Handle the case where the group name already exists
            ...

    def consume_message(self, topic: ABAN_TOPICS_TYPE):
        """Fetch message from Redis using consumer group"""
        while True:
            messages = self.redis.xreadgroup(
                self.group_name, self.consumer_name, {str(topic): ">"}, count=1
            )
            for _, message_list in messages:
                for message_id, message_data in message_list:
                    try:
                        data_model: Type[BaseModel] = ABAN_TOPICS.get(
                            topic
                        ).model_validate_json(
                            message_data,
                        )
                        self.process_message(data_model)
                        # Acknowledge the message after processing
                        self.message_acknowledgment(topic, message_id)
                    except Exception as e:
                        print(f"Error while processing message: {e}")
                        # Decide to retry, log or notify about the failed message

    @abstractmethod
    def process_message(self, message_data):
        """
        Subclasses should implement this method to provide their own logic for processing the
        message.
        """
        pass

    def message_acknowledgment(self, topic: ABAN_TOPICS_TYPE, message_id):
        self.redis.xack(str(topic), self.group_name, message_id)
