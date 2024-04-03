from fastapi_utils.api_settings import BaseSettings
from loguru import logger

logger.add('logs/logs.json', format='{level} {time}, {message}', level='DEBUG',
           rotation='100 MB', compression='zip')


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    DEV: str
    LOG_LEVEL: str


settings = Settings(_env_file='.env')
