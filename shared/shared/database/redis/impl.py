from redis.client import Redis


def get_redis(host: str, port: int, db: int):
    return Redis(host=host, port=port, db=db)
