import os
from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    user: str = os.getenv("DB_USER")
    password: str = os.getenv("DB_PASSWORD")
    host: str = os.getenv("DB_HOST")
    port: str = os.getenv("DB_PORT")
    name: str = os.getenv("DB_NAME")

    def __post_init__(self):
        self.connect: str = f"jdbc:postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


database_config = DatabaseConfig()


@dataclass
class AppConfig:
    port: int = os.getenv("APP_PORT")
    host: str = os.getenv("APP_HOST")
    mode: str = os.getenv("APP_MODE")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_DATABASE_URI: str = database_config.connect
    DEVELOPMENT: bool = False
    SECRET_KEY: str = "123123"

    def __post_init__(self):
        match self.mode:
            case "local" | "stage" | "dev":
                self.DEBUG: bool = True
                self.DEVELOPMENT: bool = True

            case "prod":
                self.DEBUG: bool = False

            case _:
                self.DEBUG: bool = False


app_config = AppConfig()