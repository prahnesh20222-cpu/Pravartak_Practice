import logging
import json
from datetime import datetime


class CustomJsonFormatter(logging.Formatter):
    def format(self, record):
        log_rec= {
        "timestamp": datetime.fromtimestamp(record.created).strftime('%Y-%m-%dT%H:%M:%S'),
        "level": record.levelname,
        "message": record.getMessage()
        }
        return json.dumps(log_rec)


def setup_logger(name = "Mylogger", level = logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setFormatter(CustomJsonFormatter())
    logger.addHandler(handler)
    return logger