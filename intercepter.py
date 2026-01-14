from loguru import logger #noqa
import logging


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            # Get corresponding Loguru level if it exists
            level = logger.level(record.levelname).name

        except ValueError:
            # No corresponding Loguru level, use numeric level
            level = record.levelno
        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        
        
        while frame.f_code.co_filename == logging.__file__:
             
            frame = frame.f_back
            depth += 1
        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )
