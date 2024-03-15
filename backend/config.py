from fastapi_utils.api_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    DEV: str
    LOG_LEVEL: str


settings = Settings(_env_file='.env')
