#JSON-formatted logger module to be imported in all pipelines built in the future

from __future__ import annotations # for function signature with type annotations.
import json,logging,time
from pathlib import Path


'''
This defines a custom JsonFormatter class that inherits from Python's logging.Formatter. 
It overrides the format() method to convert each LogRecord into a JSON-formatted string. 
The method receives a LogRecord object containing details about a specific log event, 
such as the log level, logger name, and message. Whenever a log event occurs, 
format() is called, and the current timestamp is captured using time.time() 
before the record is converted into a JSON string.
'''
class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        return json.dumps({
            "ts": round(time.time(),3),
            "level": record.levelname,
            "msg": record.getMessage(),
            "logger": record.name
        })
    

"""
Creates and returns a configured logger.

The function initializes a named logger with INFO level logging,
creates the log directory if required, attaches a FileHandler that
writes JSON-formatted log records, and prevents duplicate handlers
when the logger is initialized multiple times.
"""

def get_logger(
        name: str = "pipeline",
        log_path: str | Path = "logs/pipeline.log") ->logging.Logger:
    "Return a configured logger that writes JSON lines to a file."
    log = logging.getLogger(name)
    log.setLevel(logging.INFO)
    if log.handlers:
        return log 
    #avoids double attachment of of handlers if already invoked. 
    #Else every log message will be written more than once.
    
    Path(log_path).parent.mkdir(parents=True, exist_ok=True)
    fh = logging.FileHandler(log_path)
    fh.setFormatter(JsonFormatter())
    log.addHandler(fh)
    return log
    

