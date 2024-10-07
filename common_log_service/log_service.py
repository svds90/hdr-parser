import logging
import requests


class CommonLogger:

    """A common logger class for logging messages to a specified file."""

    def __init__(self, logger_config: dict):
        self.logger_name = logger_config["logger_name"]
        self.common_log_level = logger_config["log_level"]["common"].upper()
        self.file_handler_log_level = logger_config["log_level"]["file_handler"].upper()
        self.console_handler_log_level = logger_config["log_level"]["console_handler"].upper()
        self.log_dir = logger_config["log_dir"]
        self.log_filename = logger_config["log_filename"]
        self.log_filemode = logger_config["log_filemode"]
        self.logger = self.setup_logger()

    def setup_logger(self):
        """Set up the main logger and its handlers."""

        logger = logging.getLogger(self.logger_name)
        logger.setLevel(getattr(logging, self.common_log_level))

        self.setup_file_handler(logger)
        self.setup_console_handler(logger)

        return logger

    def setup_file_handler(self, logger):
        """Configure the file handler for logging to a file."""

        file_handler = logging.FileHandler(f"{self.log_dir}/{self.log_filename}", self.log_filemode)
        file_handler.setLevel(getattr(logging, self.file_handler_log_level))
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)-7s - %(message)s - [%(filename)s]')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    def setup_console_handler(self, logger):
        """Configure the console handler for logging to the console."""

        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, self.console_handler_log_level))
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)-7s - %(message)s - [%(filename)s]')
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)


settings = {
    "logger_name": "link_collector",
    "log_dir": "/var/log/hdr_parser",
    "log_filename": "link_collector.log",
    "log_filemode": "a",
    "log_level": {
        "common": "info",
        "file_handler": "info",
        "console_handler": "info"
    }
}

r = requests.get("https://www.google.com")

mylogger = CommonLogger(settings)

mylogger.logger.info('some info')

try:
    a = 10 / 0
except Exception as e:
    mylogger.logger.error('%s', e, exc_info=e)
