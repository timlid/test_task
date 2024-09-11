import os
from dataclasses import dataclass

from config.database_config import DatabaseConfig

@dataclass
class AppConfig:
    port: int = os.getenv("APP_PORT")
    host: str = os.getenv("APP_HOST")
    mode: str = os.getenv("APP_MODE")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_DATABASE_URI: str = DatabaseConfig().connect
    DEVELOPMENT: bool = False
    SECRET_KEY: str = os.getenv('APP_SECRET_KEY')

    def __post_init__(self):
        match self.mode:
            case "local" | "stage" | "dev":
                self.DEBUG: bool = True
                self.DEVELOPMENT: bool = True

            case "prod":
                self.DEBUG: bool = False

            case _:
                self.DEBUG: bool = False