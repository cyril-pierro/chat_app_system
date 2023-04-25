"""Application Builder and App Instance

This module is responsible for creating fastapi
application instances and configurating the 
instance with the neccessary features

Attributes:
    settings (object): Application settings
"""
from typing import Union

import fastapi
from fastapi_jwt_auth import exceptions as exc_jwt

from api.v1.router import account, users
from config import setting
from core import setup as db_setup
from error import exceptions
from handlers.exceptions import AppExceptionHandler
from interfaces import builder

settings = setting.AppSettings()


class AppSingleton:
    """Application Instance creation

    This class instantiate an application
    only once.
    Attributes:
        _app_instance (object, None): Application instance

    """
    _app_instance = None

    @classmethod
    def get_app_instance(cls) -> Union[fastapi.FastAPI, None]:
        """Instantiate a fastapi application 

        This method generates a fastapi application
        instance 

        Returns:
            object: fastapi application instance
        """
        if cls._app_instance is None:
            cls._app_instance = fastapi.FastAPI()
        return cls._app_instance


class AppBuilder(builder.AppBuilderInterface):
    """Application Builder class

    This class builds adds features to a new or
    existing fastapi application instance

    Attributes:
        _app (object): The fastapi application 

    """

    def __init__(self) -> None:
        """Construct a new application
        """
        self._app = AppSingleton.get_app_instance()

    def register_exceptions(self) -> None:
        """Register all exceptions to be used

        This method is used to handle all
        exceptions for the application
        """
        self._app.add_exception_handler(
            exceptions.UserOperationsError, AppExceptionHandler.operations
        )
        self._app.add_exception_handler(
            exceptions.AccountOperationsError, AppExceptionHandler.operations
        )
        self._app.add_exception_handler(
            exceptions.ServerError, AppExceptionHandler.server_operation
        )
        self._app.add_exception_handler(
            exc_jwt.AuthJWTException,
            AppExceptionHandler.authjwt_exception_handler,  # type: ignore
        )

    def register_middlewares(self) -> None:
        """Register all middlewares

        This method is used to handle all
        middlewares for the application
        """

    def register_routes(
        self,
    ) -> Union[None, fastapi.responses.RedirectResponse]:  # type: ignore
        """Register routes to be used

        This method is used to handle all
        routers for the application
        """
        self._app.include_router(
            users.router, prefix=settings.API_PREFIX, tags=["User"]
        )
        self._app.include_router(
            account.router, prefix=settings.API_PREFIX, tags=["Account"]
        )

        @self._app.get("/", include_in_schema=False)
        def index() -> fastapi.responses.RedirectResponse:
            """Redirect visitor to the docs page

            Returns:
                object: redirect response
            """
            return fastapi.responses.RedirectResponse("/docs")

        return index()

    def register_database(self) -> None:
        """Register all databases
        """
        db_setup.Base.metadata.create_all(
            bind=db_setup.database.get_engine  # type : ignore
        )

    def add_app_details(
        self, title: str = None, description: str = None  # type: ignore
    ) -> None:
        """Append features to the fastapi instance

        This method is responsible for including 
        details to the fastapi instance

        Args:
            title (str): Title used for the application
            description (str): Description for the application
        """
        self._app.title = title
        self._app.description = description

    def build_app(self) -> fastapi.FastAPI:
        """Build Application

        This method is used to construct the
        application

        Returns:
            object: fastapi instance 
        """
        self.register_database()
        self.register_exceptions()
        self.add_app_details(
            title=settings.APP_TITLE,
            description=settings.APP_DESCRIPTION,
        )
        self.register_middlewares()
        self.register_routes()
        return self._app