from loguru import logger
import sys

def setup_logging():
    logger.remove()
    logger.add(
        sys.stdout,
        format="<green>{time}</green> | <level>{level}</level> | <cyan>{message}</cyan>",
        level="INFO"
    )
