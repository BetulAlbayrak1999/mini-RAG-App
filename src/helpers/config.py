from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):

    APP_NAME: str
    APP_VERSION: str
    OPENAI_API_KEY: str

    class Config:
        env_file= os.path.join(os.path.dirname(__file__), ".env")


def get_settings():
    return Settings()