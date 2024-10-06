import logging
import os


class CommonLogger:

    """A common logger class for logging messages to a specified file."""

    def __init__(self, logger_config: dict):
        self.logger_name = logger_config["logger_name"]
        self.log_level = logger_config["log_level"].upper()
        self.log_filename = logger_config["log_filename"]
        self.log_filemode = logger_config["log_filemode"]

        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(getattr(logging, self.log_level))

        file_handler = logging.FileHandler(self.log_filename, self.log_filemode)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)-7s - %(message)s - [%(filename)s]')
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)


settings = {"logger_name": "link_collecor", "log_level": "info",
            "log_filename": "test.log", "log_filemode": "a"}
mylogger = CommonLogger(settings)

mylogger.logger.info('some info')

try:
    10 / 0
except Exception as e:
    mylogger.logger.error('%s', e, exc_info=e)

project_root = os.path.basename(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

print(project_root)
