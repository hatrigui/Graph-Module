# config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    mongodb_url: str = "mongodb://localhost:27017/graphdb"

    class Config:
        env_file = ".env"

settings = Settings()
