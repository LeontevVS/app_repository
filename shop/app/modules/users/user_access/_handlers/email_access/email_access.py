from typing import Annotated

from fastapi import APIRouter, Response, Depends

from modules.users.auth.services.token_service.consts import DEFAULT_EXP_REFRESH_SECONDS
from .models import EmailSignInViewModel, AccessTokenOutViewModel, EmailLogInViewModel
from modules.users.user_access.services.email_access import EmailUserAccessServiceP, get_email_user_access_service

email_router = APIRouter(prefix="/email")


@email_router.post("/signin")
async def email_sign_in(
    response: Response,
    email_access_service: Annotated[EmailUserAccessServiceP, Depends(get_email_user_access_service)],
    sign_in_data: EmailSignInViewModel,
) -> AccessTokenOutViewModel:
    tokens = await email_access_service.signin_with_password(
        email=sign_in_data.email,
        password=sign_in_data.password.encode(),
        role=sign_in_data.role,
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        max_age=DEFAULT_EXP_REFRESH_SECONDS,
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
    )
    return AccessTokenOutViewModel(token=tokens.access_token)
