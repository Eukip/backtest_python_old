import os
import pytz
from pydantic import BaseSettings


class Settings(BaseSettings):
    host: str = '0.0.0.0'
    port: int = 5000

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 5
    authjwt_secret_key: str = 'secretkey'
    SECRET_KEY = "abd6e3e21d6c99696c91b9c1a08783e4c77de4e3901d58ece33a2ad992abfaa7"
    ALGORITHM = "HS256"
    # ACCESS_TOKEN_EXPIRE_MINUTES = 511200
    CLICKHOUSE_HOST: str = os.getenv("CLICKHOUSE_HOST")
    CLICKHOUSE_PORT: str = os.getenv("CLICKHOUSE_PORT")
    CLICKHOUSE_USER: str = os.getenv("CLICKHOUSE_USER")
    CLICKHOUSE_PASSWORD: str = os.getenv("CLICKHOUSE_PASSWORD")
    CLICKHOUSE_DATABASE: str = os.getenv("CLICKHOUSE_DATABASE")
    REDIS_PORT: int = os.getenv("REDIS_PORT")
    REDIS_DB: int = os.getenv("REDIS_DB")
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD")
    REDIS_HOST: str = os.getenv("REDIS_HOST")
    DATABASE_URL = "postgres://{}:{}@{}/{}".format(os.getenv("DB_USER"),
                                                   os.getenv("DB_PASS"),
                                                   os.getenv("DB_HOST"),
                                                   os.getenv("DB_NAME"))
    API_V1_STR: str = "/api/v1"
    BASE_DIR: str = "/app/"
    USER_PASSWORD_LENGTH: int = 6
    MOSCOW_TZ = pytz.timezone('Europe/Moscow')

    APPS_MODELS = [
        "aerich.models",
        "models.user",
        "models.pair",
        "models.order",
        "models.strategy",
        "models.timeinterval",
        "models.deal",
        "models.master_timeinterval",
        "models.formula",
        "models.coinapi"
    ]

    class Config:
        case_sensitive = True


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8'
)

