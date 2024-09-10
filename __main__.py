from app import app
import config
from loguru import logger


if __name__ == "__main__":
    logger.debug("starting server")

    app.run(
        host=config.app_config.host,
        port=config.app_config.port,
    )