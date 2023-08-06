from abc import ABC, abstractmethod


class RedisAbstract(ABC):
    @abstractmethod
    def xadd(self, stream_name, message):
        """
        Add a message to the specified stream.
        """
        pass

    @abstractmethod
    def xread(self, streams, count=None, block=None):
        """
        Read messages from one or multiple streams.
        """
        pass

    @abstractmethod
    def xgroup_create(self, stream_name, group_name, id="$", mkstream=False):
        """
        Create a new consumer group associated with the specified stream.
        """
        pass

    @abstractmethod
    def xreadgroup(self, group_name, consumer_name, streams, count=None, block=None):
        """
        Read messages from one or multiple streams as part of a consumer group.
        """
        pass

    @abstractmethod
    def xack(self, stream_name, group_name, message_id):
        """
        Acknowledge the receipt of a message in a consumer group.
        """
        pass

    @abstractmethod
    def exists(self, name) -> int:
        ...
