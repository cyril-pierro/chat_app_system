"""Exception handlers

This module demonstrates how to handle any
Exception that occurs within the application

Attributes:
    logger (object): A log utility for logging
"""
import fastapi
from fastapi_jwt_auth import exceptions as exc

from error import exceptions
from tools.log import Log

logger = Log(__file__)


class AppExceptionHandler:
    """Application Exception Handler"""

    @staticmethod
    def operations(
        request: fastapi.Request,
        exec: exceptions.UserOperationsError,  # type: ignore
    ):
        """Operations exception handler

        This method is responsible for handling
        any operation exceptions raised

        Args:
            request (object): request from the client
            exec (object): Exception raised

        Returns:
            object: Fastapi Json response
        """
        logger.error(exec.msg)
        return fastapi.responses.JSONResponse(
            # type: ignore
            content={"error": exec.msg},
            status_code=exec.status_code,
        )

    @staticmethod
    def server_operation(
        request: fastapi.Request,
        exec: exceptions.ServerError,  # type: ignore
    ):
        """Server operation Handler

        This method is responsible for handling
        any server operation exception raised

        Args:
            request (object): request from the client
            exec (object): Exception raised

        Returns:
            object: Fastapi Json response
        """

        logger.critical(exec.msg)
        return fastapi.responses.JSONResponse(
            content={"error": exec.msg}, status_code=500
        )

    @staticmethod
    def authjwt_exception_handler(
        request: fastapi.Request,
        exec: exc.AuthJWTException,  # type: ignore
    ):
        """Auth jwt Exceptions Handler

        This method is responsible for handling
        any jwt exception raised
        Args:
            request (object): request from the client
            exec (object): Exception raised

        Returns:
            object: Fastapi Json response
        """
        logger.exception(exec.message)
        return fastapi.responses.JSONResponse(
            status_code=exec.status_code, content={"error": exec.message}
        )
