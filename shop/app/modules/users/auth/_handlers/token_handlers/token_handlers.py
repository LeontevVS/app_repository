from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Response, Depends, Cookie, HTTPException

from .models import AccessTokenOutViewModel
from modules.users.auth.services.token_service import TokenServiceP, get_token_service, RefreshTokenExpiredError
from modules.users.auth.services.token_service.consts import DEFAULT_EXP_REFRESH_SECONDS

token_router = APIRouter(prefix="/auth")


@token_router.post("/access")
async def access(
    response: Response,
    token_service: Annotated[TokenServiceP, Depends(get_token_service)],
    refresh_token: Annotated[str, Cookie()] = None,
) -> AccessTokenOutViewModel:
    if not refresh_token:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Unauthorised")
    try:
        access_token = await token_service.generate_access_token_from_refresh(refresh_token=refresh_token)
    except RefreshTokenExpiredError:
        response.status_code = HTTPStatus.UNAUTHORIZED
        response.set_cookie(
            key="refresh_token",
            value="",
            max_age=DEFAULT_EXP_REFRESH_SECONDS,
            httponly=True,
        )
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Unauthorised")
    return AccessTokenOutViewModel(token=access_token)


@token_router.post("/refresh")
async def refresh(
    response: Response,
    token_service: Annotated[TokenServiceP, Depends(get_token_service)],
    refresh_token: Annotated[str, Cookie()] = None,
) -> AccessTokenOutViewModel:
    if not refresh_token:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Unauthorised")
    try:
        couple_tokens = await token_service.reissue_tokens(refresh_token=refresh_token)
    except RefreshTokenExpiredError:
        response.status_code = HTTPStatus.UNAUTHORIZED
        response.set_cookie(
            key="refresh_token",
            value="",
            max_age=DEFAULT_EXP_REFRESH_SECONDS,
            httponly=True,
        )
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Unauthorised")
    response.set_cookie(
        key="refresh_token",
        value=couple_tokens.refresh_token,
        max_age=DEFAULT_EXP_REFRESH_SECONDS,
        httponly=True,
    )
    return AccessTokenOutViewModel(token=couple_tokens.access_token)
