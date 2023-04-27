"""Application Build up or setup


This module demonstrates to setup
a celery application that is integrated
with a consumer

Attributes:
    app_settings (object): Application Settings
    app_logger (object): Logger instance
"""

import celery

from config import settings
from plugins import consumer as cm
from tools import log

from . import start

app_settings = settings.Settings()
app_logger = log.Log(__file__)


class AppSingleton:
    """Get a single Celery Instance

    Attributes:
        _app(object): Celery application
    """

    _app = None

    @classmethod
    def get_app(cls) -> celery.Celery:
        """Get the Application instance

        Returns:
            object: Application instance
        """
        if cls._app is None:
            try:
                cls._app = celery.Celery(
                    app_settings.app_name,
                    broker=app_settings.celery_broker_url,
                    backend=app_settings.celery_result_backend,
                )
            except Exception as e:
                app_logger.critical(e.args[0])

        return cls._app


class AppBuilder:
    """Application builder"""

    def __init__(self):
        self._app = AppSingleton.get_app()

    def start_app(self):
        """Start the whole application

        This method registers all tasks that
        the celery uses
        """

        @self._app.task(name="send_email_to_users")
        def send_email():
            cm.NewUsersConsumer.start_process()

        @self._app.task(name="send_metrics_data")
        def send_metrics():
            start.start_metrics()

        send_email.delay()
        send_metrics.delay()
        return self._app
