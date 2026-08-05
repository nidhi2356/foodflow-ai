from loguru import logger

import sys

logger.remove()

logger.add(
    sys.stdout,  #Print logs to the terminal.
    level = "INFO",
    format = "{time: YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)