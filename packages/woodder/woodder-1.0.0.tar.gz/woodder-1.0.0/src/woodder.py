import logging
import os
from datetime import datetime


class Woodder(object):
    DEFAULT_LOG_DIR = "logs"

    @staticmethod
    def configure_logging(project_name, log_dir=DEFAULT_LOG_DIR):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(filename)s - %(levelname)s - %(message)s'
        )

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        timestamp = datetime.now().strftime("%Y-%M-%d-%H-%M-%S")

        os.makedirs(log_dir, exist_ok=True)
        file_name = f"{project_name}-{timestamp}.log"
        file_path = f"{log_dir}/{file_name}"
        fh = logging.FileHandler(file_path)

        ch.setFormatter(formatter)
        fh.setFormatter(formatter)

        logger.addHandler(ch)
        logger.addHandler(fh)

