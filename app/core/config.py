from typing import Optional
from pydantic_settings  import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30
    OPENAI_API_KEY: str

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
