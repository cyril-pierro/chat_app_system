"""Log tool

This module is used for logging errors, exceptions an critical
"""
import logging
import os
from typing import Dict

from config import settings

app_settings = settings.Settings()


class Log:
    """
    Log class for Managing logs in Project
    """

    # Log Level Storage
    __level_category: Dict = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL,
    }

    def __init__(
        self, name, level: str = "info", filename: str = app_settings.log_file_name
    ):
        """
        Constructor for log class
        @param name: str
        @param level: str
        @filename: str
        :return: None
        """

        self.__format = logging.Formatter(
            "%(levelname)s: %(name)s: %(message)s: %(asctime)s", "%Y-%m-%d %H:%M:%S"
        )
        self.__logger = logging.getLogger(name)
        self.__logger.setLevel(self.__level_category.get(level.lower()))
        self.__file_handler = logging.FileHandler(filename)
        self.__file_handler.setFormatter(self.__format)
        self.__logger.addHandler(self.__file_handler)

    def error(self, message):
        """
        Error method logs error messages to log file
        @param message: str
        :return: None
        """
        self.__logger.error(message)

    def info(self, message):
        """
        Info method logs info messages to log file
        @param message: str
        :return: None
        """
        self.__logger.info(message)

    def critical(self, message):
        """
        Critical method logs critical messages to log file
        @param message: str
        :return: None
        """
        self.__logger.critical(message)

    def exception(self, message):
        """
        Exception method logs exception messages to log file
        @param message: str
        :return: None
        """
        self.__logger.exception(message)
