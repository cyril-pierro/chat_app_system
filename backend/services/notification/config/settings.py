"""General Configuration Settings

This module demonstrates the necessary configurations
required to run process in this configuration

Attributes:
    load_dotenv (function): Loads all environment variables
    CONFIG_INI (str): name of the ini file
    celery_name (str): name of the celery config directive
    email_name (str): name of the email config directive
    kafka_name (str): name of the kafka config directive
"""

import configparser
import os
from dataclasses import dataclass

from dotenv import load_dotenv

from interfaces import parser

load_dotenv()

celery_name: str = "celery_config"
email_name: str = "email_config"
kafka_name: str = "kafka_config"
application_name: str = "application"
CONFIG_INI = "config.ini"


class Parser(parser.ParserInterface):
    """Converts config ini configuration to
    values
    Attributes:
        _cfg (object): ConfigParser instance
    """

    _cfg = configparser.ConfigParser()

    @classmethod
    def get(cls, directive: str, key: str) -> str:
        """Get the value for the configuration
        Args:
            directive(str): the ini config header
            key (str): the ini config header key

        Returns:
            str : the ini config header key value
        """
        cls._cfg.read(CONFIG_INI)
        return cls._cfg.get(directive, key, vars=os.environ)


@dataclass
class Settings:
    """Application Settings
    This class contains the general configurations
    used in this project
    """

    broker_url: str = Parser.get(kafka_name, "broker_url")
    celery_broker_url = Parser.get(celery_name, "broker_url")
    celery_result_backend = Parser.get(celery_name, "result_backend")
    stmp_server = Parser.get(email_name, "stmp_server")
    email_port = Parser.get(email_name, "mail_port")
    sender_email = Parser.get(email_name, "mail_username")
    email_password = Parser.get(email_name, "mail_password")
    app_name = Parser.get(application_name, "app_name")
    topic_to_listen_on = Parser.get(kafka_name, "topic")
    consumer_group_id = Parser.get(kafka_name, "group_id")
    log_file_name = Parser.get(application_name, "log_file_name")
    auth_service_url = Parser.get(application_name, "account_server_url")
