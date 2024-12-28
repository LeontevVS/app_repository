from typing import Protocol

from .models import UnconfirmedEmailSignIn


class EmailAccessCacheP(Protocol):
    async def add_unconfirmed_email_signin(self, data: UnconfirmedEmailSignIn) -> None:
        pass

    async def get_unconfirmed_email_signin(self, email: str) -> UnconfirmedEmailSignIn | None:
        pass
