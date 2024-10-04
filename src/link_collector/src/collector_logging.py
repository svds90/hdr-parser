import logging


class LinkCollectorLogger:
    def __init__(self, logging_config: dict):
        self.log_level = logging_config["log_level"].upper()
        self.log_filename = logging_config["log_filename"]
        self.log_filemode = logging_config["log_filemode"]

        logging.basicConfig(
            level=getattr(logging, self.log_level.upper()),
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            filename=self.log_filename,
            filemode=self.log_filemode
        )

        self.logger = logging.getLogger(__name__)


settings = {"log_level": "info", "log_filename": "test.log", "log_filemode": "a"}
mylogger = LinkCollectorLogger(settings)

mylogger.logger.error
