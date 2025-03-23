from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):

    APP_NAME: str
    APP_VERSION: str
    OPENAI_API_KEY: str

    class Config:
        model_config= SettingsConfigDict(env_file= ".env", extra="ignore")


def get_settings():
    return Settings()