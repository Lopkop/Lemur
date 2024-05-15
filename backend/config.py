import logging

from fastapi_utils.api_settings import BaseSettings

logging.basicConfig(
    format="%(levelname)s: %(asctime)s: %(message)s",
    filename="logs/logs.txt",
    level=logging.INFO,
)

logging.getLogger("uvicorn.access").disabled = True

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.getLevelName(logging.DEBUG))


class Settings(BaseSettings):
    DATABASE_URL: str
    FRONTEND_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    DEV: str
    LOG_LEVEL: str
    ENCRYPTION_KEY: str


settings = Settings(_env_file=".env")
