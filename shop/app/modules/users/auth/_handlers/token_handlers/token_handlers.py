from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Response, Depends, Cookie

from .models import AccessTokenOutViewModel
from modules.users.auth.services.token_service import TokenServiceP, get_token_service, RefreshTokenExpiredError

token_router = APIRouter(tags=["auth"], prefix="/auth")


@token_router.post("/access")
async def access(
    refresh_token: Cookie(),
    response: Response,
    token_service: Annotated[TokenServiceP, Depends(get_token_service)],
) -> AccessTokenOutViewModel | str:
    if not refresh_token:
        return "Unauthorised"
    try:
        access_token = await token_service.generate_access_token_from_refresh(refresh_token=refresh_token)
    except RefreshTokenExpiredError:
        response.status_code = HTTPStatus.UNAUTHORIZED
        response.set_cookie(
            key="refresh_token",
            value="",
        )
        return "Unauthorised"
    return AccessTokenOutViewModel(token=access_token)


@token_router.post("/refresh")
async def refresh(
    refresh_token: Cookie(),
    response: Response,
    token_service: Annotated[TokenServiceP, Depends(get_token_service)],
) -> AccessTokenOutViewModel | str:
    if not refresh_token:
        return "Unauthorised"
    try:
        couple_tokens = await token_service.reissue_tokens(refresh_token=refresh_token)
    except RefreshTokenExpiredError:
        response.status_code = HTTPStatus.UNAUTHORIZED
        response.set_cookie(
            key="refresh_token",
            value="",
        )
        return "Unauthorised"
    response.set_cookie(
        key="refresh_token",
        value=couple_tokens.refresh_token,
    )
    return AccessTokenOutViewModel(token=couple_tokens.access_token)
