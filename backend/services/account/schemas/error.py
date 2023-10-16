"""Errors Schema

This module contains the schemas for errors
"""
import pydantic


class NotFound(pydantic.BaseModel):
    """Not Found Schema
    Attributes:
        error (str): error for the payload
    """

    error: str


class InvalidPayload(pydantic.BaseModel):
    """Invalid payload used in schema
    Attributes:
        error (str): error for the payload
    """

    error: str


class UnAuthorizedError(pydantic.BaseModel):
    """Unauthorized error Schema
    Attributes:
        error (str): error for the payload
    """

    error: str


class InvalidRefreshToken(pydantic.BaseModel):
    """Invalid Refresh Token Schema
    Attributes:
        error (str): error for the payload
    """

    error: str


class InternalServerError(pydantic.BaseModel):
    """Internal error Schema
    Attributes:
        error (str): error for the payload
    """

    error: str
