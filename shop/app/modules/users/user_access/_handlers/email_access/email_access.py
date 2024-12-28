from typing import Annotated

from fastapi import APIRouter, Response, Depends

from modules.users.auth.services.token_service.consts import DEFAULT_EXP_REFRESH_SECONDS
from modules.notifications.users_notifications.services.confirmation_email_sender import (
    get_confirmation_email_service,
    ConfirmationEmailSenderP,
)
from .models import EmailSignInViewModel, AccessTokenOutViewModel, EmailLogInViewModel, EmailConfirmationViewModel
from modules.users.user_access.services.email_access import EmailUserAccessServiceP, get_email_user_access_service

email_router = APIRouter(prefix="/email")


@email_router.post("/signin")
async def email_sign_in(
    email_access_service: Annotated[EmailUserAccessServiceP, Depends(get_email_user_access_service)],
    confirmation_email_noty_service: Annotated[ConfirmationEmailSenderP, Depends(get_confirmation_email_service)],
    sign_in_data: EmailSignInViewModel,
) -> None:
    code = await email_access_service.signin_with_password(
        email=sign_in_data.email,
        password=sign_in_data.password,
        role=sign_in_data.role,
    )
    await confirmation_email_noty_service.send_confirmation_email(
        to=sign_in_data.email,
        code=code,
    )


@email_router.post("/confirmation")
async def email_confirmation(
    response: Response,
    email_access_service: Annotated[EmailUserAccessServiceP, Depends(get_email_user_access_service)],
    confirmation_data: EmailConfirmationViewModel,
) -> AccessTokenOutViewModel:
    tokens = await email_access_service.confirm_email(
        email=confirmation_data.email,
        code=confirmation_data.code,
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        max_age=DEFAULT_EXP_REFRESH_SECONDS,
        httponly=True,
    )
    return AccessTokenOutViewModel(token=tokens.access_token)


@email_router.post("/login")
async def email_log_in(
    response: Response,
    email_access_service: Annotated[EmailUserAccessServiceP, Depends(get_email_user_access_service)],
    log_in_data: EmailLogInViewModel,
) -> AccessTokenOutViewModel:
    tokens = await email_access_service.login_with_password(
        email=log_in_data.email,
        password=log_in_data.password,
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        max_age=DEFAULT_EXP_REFRESH_SECONDS,
        httponly=True,
    )
    return AccessTokenOutViewModel(token=tokens.access_token)
