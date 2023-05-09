from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    MONGO_USERNAME: str
    MONGO_PASSWORD: str
    MONGO_URL: str
    DB_NAME: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
