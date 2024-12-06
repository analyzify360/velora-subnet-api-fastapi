from typing import Literal, Any
import datetime
import logging


def iso_timestamp_now() -> str:
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    iso_now = now.isoformat()
    return iso_now


def log(
    msg: str,
    *values: object,
    sep: str | None = " ",
    end: str | None = "\n",
    file: Any | None = None,
    flush: Literal[False] = False,
):
    print(
        f"[{iso_timestamp_now()}] {msg}",
        *values,
        sep=sep,
        end=end,
        file=file,
        flush=flush,
    )
class Logger:
    def __init__(self, name: str, level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.handler = logging.StreamHandler()
        self.formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)
        self.logger.propagate = False
    
    def log_info(self, msg: str, *values: object):
        self.logger.info(msg, *values)
    
    def log_warning(self, msg: str, *values: object):
        self.logger.warning(msg, *values)
    
    def log_error(self, msg: str, *values: object):
        self.logger.error(msg, *values)
    
    def log_debug(self, msg: str, *values: object):
        self.logger.debug(msg, *values)
    
    def log_critical(self, msg: str, *values: object):
        self.logger.critical(msg, *values)
    
    def log_exception(self, msg: str, *values: object):
        self.logger.exception(msg, *values)

    