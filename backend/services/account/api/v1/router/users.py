from fastapi import APIRouter, Depends, responses
from sqlalchemy.orm import Session

from controller import auth as authorized
from controller.account import AccountOperations
from controller.users import UserOperations
from schemas import error, users
from utils import session

router = APIRouter()


@router.post(
    "/register",
    response_model=users.User,
    responses={
        401: {"model": error.UserNotFound},
    },
)
async def register_user(
    login: users.RegisterUser, db: Session = Depends(session.create)
):
    """
    This API is used to register
    a new user into the system

    It takes the following:
     - username: str
     - password: str
    """
    user_operation = UserOperations(db)
    account_operation = AccountOperations(db)
    user = user_operation.register_user(login)
    account_operation.create_account(user.id)
    return user


@router.post(
    "/change/email",
    response_model=users.ChangeOut,
    responses={
        401: {"model": error.UserNotFound},
        404: {"model": error.UnAuthorizedError},
    },
)
async def change_email(
    data: users.ChangeEmail,
    _: str = Depends(authorized.bearerschema),
    authorize: authorized.Auth = Depends(),
    db: Session = Depends(session.create),
):
    """
    This API is used to change
    the email of an
    authenticated user
    It takes the following:
     - email: str
    """
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    user_operation = UserOperations(db)
    user_operation.reset_user_email(user_id, data.email)
    return responses.JSONResponse(
        content={"message": "email changed successfully"}, status_code=200
    )


@router.post(
    "/change/username",
    response_model=users.ChangeOut,
    responses={
        401: {"model": error.UserNotFound},
        404: {"model": error.UnAuthorizedError},
    },
)
async def change_username(
    data: users.ChangeUsername,
    _: str = Depends(authorized.bearerschema),
    authorize: authorized.Auth = Depends(),
    db: Session = Depends(session.create),
):
    """
    This API is used to change the
    username of an authenticated user
    It takes the following data:
      - username: str

    """
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    user_operation = UserOperations(db)
    user_operation.reset_user_username(user_id, data.username)
    return responses.JSONResponse(
        content={"message": "username changed successfully"}, status_code=200
    )


@router.post(
    "/change/password",
    response_model=users.ChangeOut,
    responses={
        401: {"model": error.UserNotFound},
        404: {"model": error.UnAuthorizedError},
    },
)
async def change_password(
    _: str = Depends(authorized.bearerschema),
    authorize: authorized.Auth = Depends(),
):
    """
    This API is used to generate a token
    to change the password of an
    authenticated user
    """
    authorize.jwt_required()
    access_token = authorize.create_access_token(
        subject=authorize.get_jwt_subject(), fresh=True  # type: ignore
    )
    return responses.JSONResponse(
        content={"access_token": access_token}, status_code=200
    )


@router.post(
    "/change/password/confirm",
    response_model=users.ChangeOut,
    responses={
        401: {"model": error.UserNotFound},
        404: {"model": error.UnAuthorizedError},
    },
)
async def confirm_password_change(
    data: users.ChangePassword,
    _: str = Depends(authorized.bearerschema),
    authorize: authorized.Auth = Depends(),
    db: Session = Depends(session.create),
):
    """
    This API is used to change
    the password of an
    authenticated user
    The payload takes:
      - password: str
    """
    authorize.fresh_jwt_required()
    user_id = authorize.get_jwt_subject()
    user_operation = UserOperations(db)
    user_operation.reset_user_password(user_id, data.password)
    return responses.JSONResponse(
        content={"message": "changed password successfully"}, status_code=200
    )


@router.get(
    "/username",
    response_model=users.ChangeOut,
    responses={
        401: {"model": error.UserNotFound},
        404: {"model": error.UnAuthorizedError},
    },
)
async def get_username(
    _: str = Depends(authorized.bearerschema),
    authorize: authorized.Auth = Depends(),
    db: Session = Depends(session.create),
):
    """
    This API is used to get
    a username of an
    authenticated user
    """
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    user_operation = UserOperations(db)
    username = user_operation.get_username(user_id)
    return responses.JSONResponse(
        content={"message": username}, status_code=200  # type: ignore
    )
