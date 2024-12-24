from collections.abc import Callable, Coroutine
from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from modules.users.auth.services.token_service import TokenServiceP, get_token_service, TokenUserInfoDTO
from modules.users.consts import PrivateUserRoles


_SECURITY = HTTPBearer()


def authorize(
    roles: list[PrivateUserRoles] | None = None,
) -> Callable[
    [
        Annotated[TokenServiceP, Depends(get_token_service)],
        Annotated[HTTPAuthorizationCredentials, Depends(_SECURITY)],
    ], Coroutine[None, None, TokenUserInfoDTO]
]:
    async def wrapper(
        token_service: Annotated[TokenServiceP, Depends(get_token_service)],
        token: Annotated[HTTPAuthorizationCredentials, Depends(_SECURITY)],
    ):
        if not token or not token.scheme == "Bearer":
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Unauthorized")

        try:
            user_info = await token_service.get_access_token_user_info(access_token=token.credentials)
        except Exception:
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Unauthorized")

        if roles and user_info.role not in roles:
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Permission denied")

        return user_info

    return wrapper
