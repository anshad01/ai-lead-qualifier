from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    GROQ_API_KEY: str
    GOOGLE_SHEET_NAME: str = "AI Lead Qualifier"
    GOOGLE_CREDENTIALS_PATH: str = "credentials.json"
    MODEL_NAME: str = "llama-3.1-70b-versatile"

    class Config:
        env_file = ".env"


settings = Settings()