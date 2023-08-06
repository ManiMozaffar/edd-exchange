from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    GROUP_NAME: str
    redis_host: str = "localhost"
    redis_port: int = 6382
    redis_db: int = 0


setting = Setting()
