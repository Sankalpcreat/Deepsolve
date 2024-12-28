from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from dotenv import load_dotenv


load_dotenv(dotenv_path=".env")

class Settings(BaseSettings):
    
    DB_HOST: str = "localhost"
    DB_PORT: int = 2500
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "instagram_db"
    SECRET_KEY: str = "change_this_secret"

    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    def __init__(self, **data):
        super().__init__(**data)
        
        if not self.SECRET_KEY or self.SECRET_KEY == "change_this_secret":
            print("WARNING: Use a strong, unique SECRET_KEY in production")

settings = Settings()
