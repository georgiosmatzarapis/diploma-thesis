""" Module which implements loggging. """
from backend.helpers.main_config import CONFIGURATION
from backend.helpers.lib import file_path
import logging


class Logger:
    def get_logger(self, module_name):
        """ Set up logging and return logger name. """
        
        logger = logging.getLogger(f'app:{module_name}') # specify name logger
        logger.setLevel(CONFIGURATION.level)

        output_format = logging.Formatter(CONFIGURATION.format)

        # save in file
        file_handler = logging.FileHandler(file_path(CONFIGURATION.folder, CONFIGURATION.file))
        file_handler.setFormatter(output_format)

        # to print in console
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(output_format)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

        # keep this line if i want to check only for this type logs
        # file_handler.setLevel(logging.DEBUG)

        return logger