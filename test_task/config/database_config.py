from dataclasses import dataclass
import os

@dataclass
class DatabaseConfig:
    user: str = os.getenv("DB_USER")
    password: str = os.getenv("DB_PASSWORD")
    host: str = os.getenv("DB_HOST")
    port: str = os.getenv("DB_PORT")
    name: str = os.getenv("DB_NAME")

    def __post_init__(self):
        self.connect: str = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"