import os
from typing import Dict
from pydantic import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = os.getenv("DEBUG", True)
    APP_VERSION: str = "0.0.1"
    PROJECT_NAME: str = 'Appointment Manager'
    PROJECT_DESCRIP: str = 'Application to manage professional appointments'
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    MAIN_HELP_URL: str = '/docs'
    APP_CONTACT: Dict[str, str] = {
        "name": "Lucas Lucyk",
        "email": "lucaslucyk@gmail.com"
    }
    APP_LICENSE: Dict[str, str] = {"name": "MIT"}

    SQLALCHEMY_DATABASE_URI: str = "postgresql+psycopg2://root:root@localhost:54320/appointment_mgr"
    ASYNC_SQLALCHEMY_DATABASE_URI: str = "postgresql+asyncpg://root:root@localhost:54320/appointment_mgr"

settings = Settings()