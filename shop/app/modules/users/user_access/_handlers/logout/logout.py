from typing import Annotated

from fastapi import APIRouter, Depends, Response, Cookie

from modules.users.user_access.services.logout import get_logout_service, LogoutUserServiceP


logout_router = APIRouter()


@logout_router.post("/logout")
async def logout(
    logout_service: Annotated[LogoutUserServiceP, Depends(get_logout_service)],
    response: Response,
    refresh_token: Cookie(),
) -> dict:
    if refresh_token:
        await logout_service.logout(refresh_token=refresh_token)
        response.set_cookie(
            key="refresh_token",
            value="",
        )
    return {"status": "ok"}
