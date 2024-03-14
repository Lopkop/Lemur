from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=('.env', '.env.prod'), env_file_encoding='utf-8')

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str


settings = Settings()
